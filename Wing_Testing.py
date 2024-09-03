import aerosandbox as asb
import aerosandbox.numpy as np
import matplotlib.pyplot as plt
import aerosandbox.tools.pretty_plots as p
import logging

# Configure logging to log everything (DEBUG level and above) and write to a file
logging.basicConfig(filename='Wing_Test_log.txt', filemode='a', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Define airfoils
logging.debug("Defining airfoils")
wing_airfoil = asb.Airfoil("sd7037")
tail_airfoil = asb.Airfoil("naca0010")

# Define the airplane geometry
logging.debug("Defining airplane geometry")
airplane = asb.Airplane(
    name="SAE Aero 2025",
    xyz_ref=[0, 0, 0],  # CG location
    wings=[
        asb.Wing(
            name="Main Wing",
            symmetric=True,
            xsecs=[
                asb.WingXSec(xyz_le=[0, 0, 0], chord=0.9144, twist=0, airfoil=wing_airfoil),
                asb.WingXSec(xyz_le=[0.1524, 3.625, 0.08], chord=0.6096, twist=0, airfoil=wing_airfoil),
                asb.WingXSec(xyz_le=[0.3048, 7.25, 0.16], chord=0.3048, twist=-0, airfoil=wing_airfoil),
            ]                                       # Z values are based on 2 degree of dihedral
        )
    ]
)

# Set up and run VLM analysis
logging.debug("Setting up and running VLM analysis")
vlm = asb.VortexLatticeMethod(
    airplane=airplane,
    op_point=asb.OperatingPoint(velocity=20, alpha=5)
)
aero = vlm.run()
for k, v in aero.items():
    logging.info(f"{k.rjust(4)} : {v}")

# Draw VLM results
logging.debug("Drawing VLM results")
vlm.draw(show_kwargs=dict(jupyter_backend="static"))

# Set up optimization problem to maximize L/D
logging.debug("Setting up optimization problem to maximize L/D")
opti = asb.Opti()
alpha = opti.variable(init_guess=5)
vlm = asb.VortexLatticeMethod(
    airplane=airplane,
    op_point=asb.OperatingPoint(velocity=20, alpha=alpha), #velocity=m/s
    align_trailing_vortices_with_wind=False,
)
aero = vlm.run()
L_over_D = aero["CL"] / aero["CD"]
logging.debug(f"Initial L/D: {L_over_D}")

opti.minimize(-L_over_D)
sol = opti.solve()
best_alpha = sol(alpha)
logging.info(f"Alpha for max L/D: {best_alpha:.3f} deg")

# Set up optimization problem to optimize wing chord distribution
logging.debug("Setting up optimization problem to optimize wing chord distribution")
opti = asb.Opti()
N = 16
section_y = np.sinspace(0, 1, N, reverse_spacing=True)
chords = opti.variable(init_guess=np.ones(N))
wing = asb.Wing(
    symmetric=True,
    xsecs=[
        asb.WingXSec(
            xyz_le=[-0.25 * chords[i], section_y[i], 0],
            chord=chords[i],
        )
        for i in range(N)
    ]
)
airplane = asb.Airplane(wings=[wing])
opti.subject_to(chords > 0)
opti.subject_to(wing.area() == 0.25)
opti.subject_to(np.diff(chords) <= 0)
alpha = opti.variable(init_guess=5, lower_bound=0, upper_bound=30)
op_point = asb.OperatingPoint(velocity=1, alpha=alpha)
vlm = asb.VortexLatticeMethod(
    airplane=airplane,
    op_point=op_point,
    spanwise_resolution=1,
    chordwise_resolution=8,
)
aero = vlm.run()
opti.subject_to(aero["CL"] == 1)
opti.minimize(aero["CD"])
sol = opti.solve()
vlm = sol(vlm)
vlm.draw(show_kwargs=dict(jupyter_backend="static"))

# Plot results
logging.debug("Plotting results")
fig, ax = plt.subplots()
plt.plot(section_y, sol(chords), ".-", label="AeroSandbox VLM Result", zorder=4)
y_plot = np.linspace(0, 1, 500)
plt.plot(y_plot, (1 - y_plot ** 2) ** 0.5 * 4 / np.pi * 0.125, label="Elliptic Distribution")
p.show_plot("AeroSandbox Drag Optimization using VortexLatticeMethod", "Span [m]", "Chord [m]")

# Compare theoretical and computed induced drag
logging.debug("Comparing theoretical and computed induced drag")
AR = 2 ** 2 / 0.25
CL = 1
CDi_theory = CL ** 2 / (np.pi * AR)
CDi_computed = sol(aero["CD"])
logging.info(f"CDi (theory)   : {CDi_theory:.4f}")
logging.info(f"CDi (computed) : {CDi_computed:.4f}")