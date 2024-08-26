# LiftCalculator.py - by Caelan Hadley
# Defines the Lift Object which given an angle of attack, wing area, 
# speed, and coefficients of lift will calculate your wing's ideal lift.



import matplotlib.pyplot as plt
import math
import logging

# Configure logging to log everything (DEBUG level and above) and write to a file
logging.basicConfig(filename='log.txt', filemode='a', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Version of the script
__version__ = "0.05"

logging.info(f"Starting Insert Data to Shop Floor script v{__version__}")

class Lift():
    def __init__(self, velocity, density, wing_area, alpha):
        self.velocity = velocity
        self.density = density # Air rho = 1.225
        self.wing_area = wing_area
        self.alpha = alpha
        self.dynamic_pressure = 0
        
        self.af_data_alpha = [
        -12,-11.75,-11.25,-11,-10.75,-10.5,-10.25,-10,-9.75,-9.5,-9.25,-9,-8.75,-8.5,-8.25,-8,-7.75,-7.5,-7.25,-7,-6.75,-6.5,-6.25,-6,-5.75,-5.5,-5.25,-5,-4.75,-4.5,-4.25,-4,-3.75,-3.5,-3.25,-3,-2.75,-2.5,-2.25,-2,-1.75,-1.5,-1.25,-1,-0.75,-0.5,-0.25,0,0.25,0.5,0.75,1,1.25,1.5,1.75,2,2.25,2.5,2.75,3,3.25,3.5,3.75,4,4.25,4.5,4.75,5,5.25,5.5,5.75,6,6.25,6.5,6.75,7,7.25,7.5,7.75,8,8.25,8.5,8.75,9,9.25,9.5,9.75,10,10.25,10.5,10.75,11,11.25,11.5,11.75,12,12.25,12.5,12.75,13,13.25,13.5,13.75,14,14.25,14.5,14.75,15,15.25,15.5,15.75,16,16.25,16.5,16.75,17,17.25,17.5,17.75,18

        ]
        self.af_data_cl = [
        -0.2925,-0.2904,-0.6446,-0.6274,-0.5983,-0.5693,-0.5463,-0.5198,-0.4987,-0.4739,-0.4551,-0.4386,-0.4169,-0.3945,-0.3724,-0.3499,-0.3273,-0.3037,-0.28,-0.2573,-0.2342,-0.2093,-0.184,-0.1591,-0.1329,-0.1089,-0.0833,-0.0569,-0.0309,-0.005,0.0211,0.0485,0.0749,0.1013,0.1285,0.1546,0.1809,0.2073,0.2343,0.2603,0.2863,0.3138,0.3396,0.3656,0.3925,0.4187,0.4443,0.4709,0.496,0.521,0.5461,0.5714,0.5966,0.6211,0.6458,0.6696,0.6865,0.8497,0.8715,0.892,0.9119,0.9311,0.9492,0.9674,0.9848,1.002,1.0195,1.0366,1.0535,1.0699,1.0859,1.101,1.1162,1.1314,1.1437,1.1531,1.1637,1.1768,1.1883,1.203,1.2147,1.2311,1.2447,1.2591,1.2744,1.2868,1.3037,1.3187,1.3309,1.3476,1.3635,1.3768,1.3896,1.4066,1.42,1.4314,1.4477,1.4587,1.4726,1.4822,1.4904,1.4814,1.4739,1.4495,1.4443,1.4441,1.4435,1.4382,1.4388,1.4371,1.433,1.4271,1.4173,1.4046,1.3966,1.3883,1.3786,1.3672,1.3557,1.3423
        ]

    def calculate_dynamic_pressure(self, velocity, density):
        return (0.5 * density * pow(velocity, 2))

    def generate_dynamic_pressure(self):
        self.dynamic_pressure = (0.5 * self.density * pow(self.velocity, 2))

    def set_dynamic_pressure(self, dynamic_pressureIn):
        self.dynamic_pressure = dynamic_pressureIn
    
    def get_dynamic_pressure(self):
        return self.dynamic_pressure
    
    def set_velocity(self, velocity_in):
        self.velocity = velocity_in
    
    def get_velocity(self):
        return self.velocity
    
    def set_density(self, density_in):
        self.density = density_in
    
    def get_density(self):
        return self.density
    
    def set_wing_area(self, wing_area_in):
        self.wing_area = wing_area_in
    
    def get_wing_area(self):
        return self.wing_area
    
    def set_alpha(self, alpha_in):
        self.alpha = alpha_in
    
    def get_alpha(self):
        return self.alpha

    def find_cl_from_alpha(self):
        iter = 0
        closest_value = self.af_data_alpha[0]
        position = -1
        for i in self.af_data_alpha:
            if (self.alpha - self.af_data_alpha[iter]) >= 0:
                closest_value = self.af_data_alpha[iter]
                position = iter 
            iter += 1
        return self.af_data_cl[position]

    def calculate_lift(self):
        return (self.dynamic_pressure * self.find_cl_from_alpha() * self.wing_area)
    
    def toString(self):
        logging.info(str(self.get_velocity()), " speed (feet per second)")
        logging.info(str(self.get_alpha()), " alpha (degrees)")
        logging.info(str(self.get_wing_area()), " wing area (ft^2)")
        logging.info(str(self.get_dynamic_pressure()), " dynamic pressure (unit)")
        logging.info(str(self.calculate_lift()), " Lift (lbs)")

class Plotter():
    def __init__(self):
        self.x_data = []
        self.y_data = []

        self.x_sub_data = []
        self.y_sub_data = []
    
    def getPlotData(self, liftObj, number_of_points):
        for i in range(0, number_of_points):
            #liftObj.set_wing_area(i)
            alpha_temp = 15 * (i / number_of_points)
            liftObj.set_alpha(alpha_temp)
            liftObj.generate_dynamic_pressure()
            self.add_plot_data(alpha_temp, liftObj.calculate_lift())
            self.add_sub_plot_data(i, alpha_temp)
    
    def add_plot_data(self, x_data_in, y_data_in):
        self.x_data.append(x_data_in)
        self.y_data.append(y_data_in)
    
    def add_sub_plot_data(self, x_data_in, y_data_in):
        self.x_sub_data.append(x_data_in)
        self.y_sub_data.append(y_data_in)

    
    def plot_data(self, liftObj_in):
        plt.figure(1)
        plt.subplot(211)
        plt.plot(self.x_data, self.y_data)
        plt.title(f'Lift/Angle generated at {liftObj_in.velocity} fps')
        plt.ylabel('lift generated (lbs)')
        plt.xlabel('alpha (deg)')
        
        plt.subplot(212)
        plt.plot(self.x_sub_data, self.y_sub_data)
        plt.xlabel('wing area (ft^2)')
        plt.ylabel('alpha (deg)')
        plt.show()
    

# 24in x 6in
# 0.6096 m x 0.1524 m
# 0.09290304 m^2
# mph * 1.467 = fps
# kg/m^3 / 515 = slug/ft^3
# 24 kts = 40.5074 fps

# velocity, density, wing_area, alpha
if __name__ == "__main__":

    logging.info("------ Run 1 ------")
    liftObj = Lift(32, 0.00237, 0.667, 0) # Imperial units (fps, slug/ft^3, ft^2, degrees)
    liftObj.generate_dynamic_pressure()
    liftObj.toString()

    
    
    logging.info("\n------ Run 2 ------")

    liftObj.set_alpha(10)
    liftObj.generate_dynamic_pressure()
    logging.info(liftObj.find_cl_from_alpha())
    liftObj.toString()

    logging.info("\n------ Plot ------")

    pl = Plotter()
    pl.getPlotData(liftObj, 75)
    pl.plot_data(liftObj)