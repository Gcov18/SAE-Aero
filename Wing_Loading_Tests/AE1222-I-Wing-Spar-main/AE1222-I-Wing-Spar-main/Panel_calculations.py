import matplotlib.pyplot as plt
import math
from scipy.optimize import curve_fit
import numpy as np


# To manipulate the design parameters, either change the global defintions of the stiffeners/ web plate, 
# or plot correpsonding graphs by changing the function in the Configuration class


class TSB:
    def __init__(self, n, body, stringer, height, stress) -> None:
        self.pitch = (  height - n*stringer.l) / (n -1 + 1/3.6728*2)

        self.sigma =   3.4 * body.E * (body.w / (self.pitch )) ** 2 * 1e-6
        output ="current pitch ->" + str(self.pitch) + " current stress ->" + str(stress) + " buckling stress ->" +  str(self.sigma)
        print(output)
        if(stress > self.sigma):
            self.buckles = True
        else:
            self.buckles = False


#class for storing stiffener data
class L:
    #area moment for one side of the stiffener
    def _sideI(self):
        self.Is = self.w**3 * self.h/12

    def __init__(self, l, w, h, r) -> None:
        self.l = l
        self.w = w
        self.h = h
        self.m1 = w * h
        self.m2 = (l - w) * w
        self.m = self.m1 + self.m2
        self.y = (self.m1 * (h / 2) + self.m2 * (w / 2)) / (self.m1 + self.m2)
        self.x = (self.m1 * (w / 2) + self.m2 * ((l+w) / 2)) / (self.m1 + self.m2)
        self.I = w * h ** 3 / 12 + self.m1 * (self.y - h/2)**2  + (l - w) * w ** 3 / 12 + self.m2 * (self.y - w / 2)**2
        self.X = r[0]
        self.Y = r[1]
        self.Z = r[2]
        self._sideI()
    def _info_(self):
        print(" \n Stringer -> I = " + str(self.I) +  " x = " + str(self.x) +  " y = " + str(self.y) + "m =  " + str(self.m)+ "\n")

#class for the main Sheet
class Sheet:
    # thickness, height, length, E
    def __init__(self, w, l, h, E) -> None:
        self.w = w
        self.I = l*w**3 /12 
        self.x = 0
        self.y = 0
        self.m = w*l
        self.E = E
    def _info_(self):
        print(" \n Sheet -> I = " + str(self.I) +  " x = " + str(self.x) +  " y = " + str(self.y) + " m = " + " " +"\n")

#buckling load
def Pmin(self, c, E, L, I):
        return I *  (c * math.pi**2 * E / (L*L))

#class for the panel configuration
class Configuration:
    #minimum I to avoid column buckling
    def Imin(self, c, E, L, P):
        return P /  (c * math.pi**2 * E / (L*L))
    
    def __init__(self, L, body, P) -> None:
        self.L = L #stiffener type
        self.body = body #sheet
        self.P = P # design load
        self.min = self.Imin(4, 71.7*1E9, 0.496, self.P) #minimum 2nd moment of area
    #centroid of the entire panel
    def centroid(self, stringers, panel):
        x = 0
        y = 0
        m = panel.m
        for i in stringers:
            y += (i.y + i.Y) * i.m
            x += (i.x + i.X)  * i.m
            m  += i.m
        x /= m
        y /= m
        return (x, y)
    #total 2nd moment of area for the entire panel
    def areaInertia(self, stringers, panel, centroid):
        Iy = 0
        for i in stringers:
            Iy += i.I + i.m*(centroid[1] - i.y) ** 2
        Iy += panel.I + panel.m*(centroid[1]) ** 2
        return Iy

    
    #calculates stiffener count for buckling failure type 1
    #input -> base object + stiffener array
    def _config_Stiffeners(self, stiffener):
        currentI = 0 #current I
        lastI = 0 # previous I
        plot =  ([], [])
        for i in range(1, 10):
            l =[]
            for j in range(0, i):
                l.append(stiffener)

            currentI = self.areaInertia(l, self.body, self.centroid(l, self.body))
            #print(currentI)
            print("at" + str(i))
            print(currentI/self.min*100)
            plot[0].append(i)
            plot[1].append(currentI)
            if(self.min < currentI):
                k = 0
                #print( "required stiffeners -> " + str(i) + "minimum I -> " + str(self.min) + " current I -> " + str(currentI) + " last  -> " + str(lastI))
                #break
            lastI = currentI

    def _config_TSB(self, stiffener):
        #loop through stiffener count
        state = True
        data = ([], [], [], [], [])
        #range can be adjusted here
        for i in range(2, 8):      
            stress = self.P / (stiffener.m * i + self.body.m) *1e-6 
            #now create TSB object for configuration 
            buckling  = TSB(i, self.body,stiffener, .400, stress)
            rivet_count =  0.400 /  ((self.body.w**2 / (stress * 1e6 / (0.9 * 2.1 * self.body.E )))**(0.5))
            data[0].append(i)
            data[1].append(stress)
            data[2].append(buckling.sigma)
            data[4].append(rivet_count*i)
            if(not buckling.buckles):
                stiffener.min = i
                state = False
                data[3].append(i * stiffener.m * 2780 * 0.495 + self.body.m * 2780 * 0.495)
            else:
                data[3].append(0)
        return data
    
    #graphs. Data to be graphed can be chosen manually
    def Graph_stiffeners(self):
        figure, data = plt.subplots(2, 2)
        self.index = 1
        for i in self.L:
            # returns an array in the format : number of stiffeners, current stress, buckling stress, mass
            points = self._config_TSB(i)
            print(points)
            data[0, 0].plot(points[0], points[1],  label = "stress L" + str(self.index))
            data[0, 0].plot(points[0], points[2],  label = "crit L" + str(self.index))
            data[0, 1].plot(points[0], points[3], label = "L" + str(self.index))
            data[1, 1].plot(points[0], points[4], label = "L" + str(self.index))
            data[0, 0].set_title("Inter Sheet Buckling")
            data[0, 1].set_title("Inter Sheet Buckling")
            data[0, 1].legend()
            data[0, 0].legend()
            self.index += 1
        data[0, 0].set_xlabel("Stiffeners Used")
        data[0, 0].set_ylabel("Stress, Mpa")
        data[0, 1].set_xlabel("Stiffeners Used")
        data[0, 1].set_ylabel("Mass, kg")
        plt.legend()
        plt.show()
        
 #global variables defining the given stiffeners and the main sheet:
P = 100000 * 0.4 #design load

L1 = L(.020, .0015, .020, (0, 0.0005, 0))
L2 = L(.020, .002, .020, (0, 0.0005, 0))
L3 = L(.015, .002, .015, (0, 0.0005, 0))
L4 = L(.015, .0015, .015, (0, 0.0005, 0))
body = Sheet(.001, .400, .400, 71.7*1E9)

cnf = Configuration((L1, L2, L3, L4), body, P)
cnf._config_Stiffeners(cnf.L[0])
#cnf.Graph_stiffeners()
print(L2.m * 6 + body.m)
P_Stiff = P/0.000856
P_crit = Pmin(L2, 4, 72e9, 0.435, L2.Is)
print(L2.m)



#figure, axis = plt.subplots(2, 2)

