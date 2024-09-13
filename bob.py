# -*- coding: utf-8 -*-
"""
@author: Azadfaraj
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import warnings
warnings.filterwarnings("ignore")

def LLT(b,AR,S,beta_t,beta_r,alpha_i,alpha_L0_tip,alpha_L0_root,N,a_0_root,a_0_tip):
    """
    Implement LLT to allow the user to find aerodynamic properties
    (lift coefficient, induced drag coefficient) of a tapered wing.

    Parameters
    ----------
    b : float
        wing span (m).
    AR : float
        aspect ratio.
    S : float
        wing area (m^2).
    beta_t : float
        twist angle at wing tip (deg).
    beta_r : float
        twist angle at wing root (deg).
    alpha_i : float
        angle of incidence(deg).
    alpha_L0_tip : float
        aerofoil zero lift angle of attack at wing tip.
    alpha_L0_root : float
        aerofoil zero lift angle of attack at wing root.
    N : int
        number of spanwise stations along wingspan.
    a_0_root : float
        lift curve slope at wing root.
    a_0_tip : float
        lift curve slope at wing tip.

    Returns
    -------
    None.

    """
    #print("S=",S, "AR=",AR, "b=",b)

    c_av= (S/AR)**0.5 #mean chord length
    c_r = (2*S)/((1+lamda)*b) #root chord
    c_t=lamda*c_r #tip chord
    MAC=2/3*c_r*(1+lamda+lamda**2)/(1+lamda) #mean aerodynamic chord
    Y_=b/6 *(1+2*lamda)/(1+lamda)   #mean aerodynamic chord distance from root
    #print("c_av=",c_av,"cr=",c_r,"ct=",c_t,"mean aero chord =",MAC)

    #twist angle distribution
    h_tip= c_t*np.sin(beta_t*np.pi/180) #in degrees
    #print("h_tip =",h_tip)

    #Discretization
    pheta=np.linspace(0, np.pi, num=N)

    #Spanwise distribuiton
    y=[]
    for i in range(0,N):
        y.append(-b/2*np.cos(pheta[i]))

    #print("y",y)

    c=[]
    for k in range(0,N):
        c.append( (c_t-c_r)/(b/2)*abs(y[k])+c_r)
    #print("c=",c)

    beta=[]  #twist angle (degrees)
    for k in range(0,int(N)):
        if y[k]<0:
            beta.append(  np.arcsin(-2*y[k]/(b*c[k])*h_tip)*180/np.pi )
        else:
            beta.append(  np.arcsin(2*y[k]/(b*c[k])*h_tip)*180/np.pi )
    #beta= [-5.0, -4.430017801119399, -3.101595932870531, -1.6647863130312146, -0.4747985664598187, -0.47479856645981844, -1.6647863130312128, -3.101595932870531, -4.430017801119398, -5.0]
    #print("beta=",beta)

    a_0=[] #lift curve slope at each wing section (^-1), a(k) for k=1,2,3,4
    for k in range(0,int(N)):
        a_0.append( a_0_root -2* (a_0_tip-a_0_root)/b*y[k]   )
    #print("a_0",a_0)

    alpha_L0=[] # zero-lift angle of attack (deg), alpha_L0(k) for k=1,2,3,4
    for k in range(0,int(N)):
        alpha_L0.append( alpha_L0_tip -2* (alpha_L0_tip-alpha_L0_root)/b*y[k]   )
    #print(alpha_L0)

    #pheta=[] 
    #for k in range(0,int(N)):
    #    pheta.append( np.arccos(-2*y[k]/b  )*180/np.pi)

    #print("pheta",pheta)

    D=[]
    for k in range(0,int(N)):
        D.append( (alpha_i-alpha_L0[k]+beta[k])*np.pi/180) #rads
    #print("D= ",D)

    C = np.zeros((N, N))
    for k in range(0,N):
        for m in range(0,N):
            #handle case where sin(pheta)=0
            if (np.sin(pheta[k])==0):
                C[k][m]=(m+1)**2
            else:
                #C[k][m]=(   (4*b/(a_0[k]*c[k]) +((2*(m+1)-1)/np.sin(pheta[k]*np.pi/180)))*np.sin((2*(m+1)-1)*pheta[k]*np.pi/180))
                #C[k][m]=((2*b/(a_0[k]*c[k]) +((2*(m+1)-1)/np.sin(pheta[k])))*np.sin((2*(m+1)-1)*pheta[k]))
                C[k][m]=((4*b/(a_0[k]*c[k]) +((m+1)/np.sin(pheta[k])))*np.sin((m+1)*pheta[k]))

    #print("C",C)
    A = np.linalg.solve(C,D)  #Fourier Series constants A1, A2 etc

    #print("A=",A)
    #print("")
    Cl=np.pi*AR*A[0]
    #print("Cl =",Cl)
    #print("")

    delta = 0
    for n in range(1,len(A)):
        delta=delta + (n+1)*(A[n]**2/A[0]**2)
        #print("delta=",delta)
    #print("delta=",delta)
    e = 1/(1+delta)
    #print("e =",e)
    Cd_i=Cl**2/(np.pi*AR*e)
    #print("Cd_i =",Cd_i)
    
    alpha_induced=[]
    for k in range(0,N):
        sectional_alpha_induced=0
        for m in range(1,N+1):
                #sectional_alpha_induced=sectional_alpha_induced+(m)*A[m-1]*np.sin((m-1)*pheta[k])/np.sin(pheta[k])
                sectional_alpha_induced=sectional_alpha_induced+(m)*A[m-1]*np.sin((m)*pheta[k])/np.sin(pheta[k])
                #print("sectional_alpha_induced (",pheta[k],")",sectional_alpha_induced)
                
        alpha_induced.append(sectional_alpha_induced*180/np.pi*-1)
    #print("alpha_induced",alpha_induced)

    return(y,A,MAC,Cl,Cd_i,c,e,alpha_induced)

#%% WING CHARACTERISTIC INPUT SECTION
b=1.98 #wing span (m)
AR=3.75 #aspect ratio

#b=0.27 #wing span (m)
#AR=0.39130434782 #aspect ratio

S =(b**2)/AR #wing area (m^2)

print("S :",S)
lamda = 1.5   #taper ratio
N=100#number of spanwise stations along wingspan


alpha_i=4.5+1.5 # angle of incidence(deg)


#twist
beta_t=0 #twist angle at wing tip (deg)
beta_r=0 #twist angle at wing root (deg)

#sectional data
#alpha_L0_root=0.0979
#alpha_L0_tip=0.0979
alpha_L0_root=0.1248
alpha_L0_tip=0.1248


a_0_root=5.9
a_0_tip=5.9  


y,A,MAC,Cl,Cd_i,c,e_0,alpha_induced=LLT(b,AR,S,beta_t,beta_r,alpha_i,alpha_L0_tip,alpha_L0_root,N,a_0_root,a_0_tip)


print("Lift coefficient(Cl) :",Cl)
print("Induced drag coefficient(Cd_i) :",Cd_i)
print("Efficiency factor (e) :",e_0)


#%%
V_inf=88
p_inf = 1.225 #density of air
μ_inf=0.00001789 #dynamic viscosity of air
Re=p_inf*V_inf*MAC/μ_inf
print("Re =",Re)

A=LLT(b,AR,S,beta_t,beta_r,alpha_i,alpha_L0_tip,alpha_L0_root,N,a_0_root,a_0_tip)[1]
y=LLT(b,AR,S,beta_t,beta_r,alpha_i,alpha_L0_tip,alpha_L0_root,N,a_0_root,a_0_tip)[0]

YPos=y[(len(y)//2):]


phetaPos=[]
for k in range(0,len(YPos)):
    phetaPos.append( np.arccos(2*YPos[k]/b) *180/np.pi)



gamma=[]  #circulation
for k in range(0,len(YPos)):
    gammaY = 0
    for n in range(0,N-1):
        gammaY=gammaY + 2*b* V_inf*(A[n]*np.sin(phetaPos[k]*np.pi/180))
        #print("gametemp",gammaY)
    gamma.append(gammaY)
    
    #print(gamma)
    #gamma.append(  2*b* V_inf*(A[0]*np.sin(phetaPos[k]*np.pi/180) + A[1]*np.sin(3*phetaPos[k]*np.pi/180)) )
print("")
#print("gamma ",gamma)


#print("gamma=",gamma)
gamma_0=gamma[0]
gammaNormalised=[]  #circulation
for k in range(0,len(YPos)):
    gammaNormalised.append( gamma[k]/gamma_0 )
#print("gammaNormalised=",gammaNormalised)
#print("c",c)

cRight=(c[len(c)//2:])

Cl_Norm=[]  #normalised lift coefficient
for k in range(0,len(YPos)):
    Cl_Norm.append( 1/Cl*(2*gamma[k])/(V_inf*cRight[k]) )
    
#print("Cl_Norm", Cl_Norm)

Lift=[]
for k in range(0,len(YPos)):
    Lift.append(   0.5* p_inf* V_inf**2 *cRight[k] *Cl_Norm[k]  )
#print("Load", Lift)

alpha_i_array= [0,1,2,3,4,5,6,7,8,9,10,11,12]
#print("alpha_i",alpha_i_array)
Cl_array=[]
for i in range(0,len(alpha_i_array)):
    Cl_array.append(LLT(b,AR,S,beta_t,beta_r,alpha_i_array[i],alpha_L0_tip,alpha_L0_root,N,a_0_root,a_0_tip)[3])
#print(Cl_array)
Cl_array_TAT=[]
for i in range(0,len(alpha_i_array)):
    Cl_array_TAT.append(((a_0_root+a_0_tip)/2)*alpha_i_array[i]*np.pi/180-alpha_L0_root*np.pi/180)
#print(Cl_array_TAT)


plt.plot(alpha_i_array,Cl_array, marker="o",label="LLT")
#plt.plot(alpha_i_array,Cl_array_TAT,label="Cl = CL_α*α + C_l0")


plt.legend(loc="upper left")
plt.xlabel("angle of attack (α)[degrees]")
plt.ylabel("lift coefficient (Cl)")


plt.grid()
plt.show()

#%%

alpha_i_array= [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14]
Cd_array=[]
for i in range(0,len(alpha_i_array)):
    Cd_array.append(LLT(b,AR,S,beta_t,beta_r,alpha_i_array[i],alpha_L0_tip,alpha_L0_root,N,a_0_root,a_0_tip)[4])
Cl_array=[]
for i in range(0,len(alpha_i_array)):
    Cl_array.append(LLT(b,AR,S,beta_t,beta_r,alpha_i_array[i],alpha_L0_tip,alpha_L0_root,N,a_0_root,a_0_tip)[3])
#print(Cd_array)

plt.plot(alpha_i_array,Cd_array, marker="o")



plt.xlabel("angle of attack [degrees]")
plt.ylabel("induced drag coefficient")
plt.grid()
plt.show()

plt.plot( YPos, Lift)
plt.xlabel("Semi span (b/2) [m]")
plt.ylabel("Load distribution (L) [N]")
plt.grid()
plt.show()

plt.plot(Cd_array,Cl_array, marker="o")

plt.xlabel("induced drag coefficient")
plt.ylabel("lift coefficient")


plt.grid()
plt.show()


#%%

Cl_vs_Cd=[]
alpha_i_array= [1,2,3,4,5,6,7,8,9,10,11,12,13,14]
for k in range(0,len(alpha_i_array)):
    Cd_array=[]
    for i in range(0,len(alpha_i_array)):
        Cd_array.append(LLT(b,AR,S,beta_t,beta_r,alpha_i_array[i],alpha_L0_tip,alpha_L0_root,N,a_0_root,a_0_tip)[4])
    Cl_array=[]
    for i in range(0,len(alpha_i_array)):
        Cl_array.append(LLT(b,AR,S,beta_t,beta_r,alpha_i_array[i],alpha_L0_tip,alpha_L0_root,N,a_0_root,a_0_tip)[3])
    
    Cl_vs_Cd.append(Cl_array[k]/Cd_array[k])
plt.plot(alpha_i_array,Cl_vs_Cd, marker="o",label="Cl/Cd_i vs alpha")


plt.xlabel("angle of attack [degrees]")
plt.ylabel("lift coefficient / induced drag coefficient")
#print(Cl_array)
#print(Cd_array)


plt.grid()
plt.show()