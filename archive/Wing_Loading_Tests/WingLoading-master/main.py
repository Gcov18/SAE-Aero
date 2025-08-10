from LoadingDiagram import LoadingDiagram as LD
import matplotlib.pyplot as plt

def saveToFile(filename , diagram, lift=None, stiffnesses = False):
    outfile = open(filename, "w")
    outfile.write("Lift[N], moment[Nm], shear[N], torque[Nm], moment of inertia, polar moment of inertia\n")
    if lift != None:
        if stiffnesses == True:
            for i in range(len(lift["Ls"])):
                line = "{}, {}, {}, {}, {}, {}\n".format(lift["Ls"][i], diagram["Moment"]["Ms"][i],diagram["Shear"]["Vs"][i],diagram["Torque"]["Ts"][i],diagram["BendStiffness"]["Is"][i],diagram["TorStiffness"]["Js"][i])
                outfile.write(line)
        else : 
            for i in range(len(lift["Ls"])):
                line = "{}, {}, {}, {}\n".format(lift["Ls"][i], diagram["Moment"]["Ms"][i],diagram["Shear"]["Vs"][i],diagram["Torque"]["Ts"][i])
                outfile.write(line)
    else:
        for i in range(len(diagram["Torque"]["Ts"])):
            line = "{}, {}, {}, {}, {}\n".format(diagram["Moment"]["Ms"][i],diagram["Shear"]["Vs"][i],diagram["Torque"]["Ts"][i],diagram["BendStiffness"]["Is"][i],diagram["TorStiffness"]["Js"][i])
            outfile.write(line)

    outfile.close()

def plotStiffnessDift(filename, diagram, segments):
    if "BendStiffness" in diagram:
        Xs = []
        for i in range(len(segments)):
            seg = segments[i]
            Xs.append((seg[4]+seg[5])/2)

        ax1 = plt.subplot(211)
        plt.title("stiffness distribution along the wing for "+ filename.split("_")[0])
        plt.plot(Xs, diagram["BendStiffness"]["Is"])
        plt.xlim(xmin=0.0)
        plt.ylim(ymin=0.0)
        plt.ylabel("Bending stiffness I [m^4]")
        plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
        plt.setp(ax1.get_xticklabels(), visible=False)

        plt.subplot(212, sharex=ax1)
        plt.plot(Xs, diagram["TorStiffness"]["Js"])
        plt.xlim(xmin=0.0)
        plt.ylim(ymin=0.0)
        plt.ylabel("Torsional stifness J [m^4]")
        plt.xlabel("x position along the wing [m]")
        plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
        plt.setp(ax1.get_xticklabels(), visible=False)

        plt.savefig(filename)
        #plt.show()
        plt.close()

    else:
        print("nothing to save")
        return False

def calculateCases():
    case2 = LD(
                41.1,   #wingspan [m]
                6.76,      #rootchord [m]
                0.29,   #taperratio
                31.2,     #sweep0.25c [deg]
                0.0,    #AoA [deg]
                1.0,    #load factor
                [(0.675, 6.06189, 0.0), (0.55, 5.723848, 0.7)],  # (cl, clalpha, x) assumed to be linear between two points and constant if otherwise 
                [(-0.1507, 0.252101, 0.0),(-0.1147, 0.257831, 0.7)],      #cms, same as cls just not given yet
                [( 0.14 ,0.0),(0.1,0.7)] #T/C's for the airfoils
                #c_l_alpha = 5.723848
                )
    case2.loadFactor = -1.0
    case2.fuelLevel = 0.0
    lift2 = case2.genLiftDist(118.4, 1.225)
    
    case2.fuelLevel = 0.7
    diagram2b =case2.genDiagrams(118.4, 1.225, filename="case2b.tex")
    case2.fuelLevel = 0.7
    diagram2c =case2.genDiagrams(118.4, 1.225, filename="case2c.tex")
    
    diagram2 =case2.genDiagrams(118.4, 1.225, filename="case2.tex")
    case2.getRequiredThickness(6.16, 10.0)
    saveToFile("case2.txt", diagram2, lift2, stiffnesses=True)
    plotStiffnessDift("case2_stiffness.png", case2.diagrams,case2.getSegments())


    case3 = LD(
                41.1,   #wingspan [m]
                6.76,      #rootchord [m]
                0.29,   #taperratio
                31.2,     #sweep0.25c [deg]
                0.0,    #AoA [deg]
                1.0,    #load factor
                [(0.675, 6.06189, 0.0), (0.55, 5.723848, 0.7)],  # (cl, clalpha, x) assumed to be linear between two points and constant if otherwise 
                [(-0.1507, 0.252101, 0.0),(-0.1147, 0.257831, 0.7)],      #cms, same as cls just not given yet
                [( 0.14 ,0.0),(0.1,0.7)] #T/C's for the airfoils
                #c_l_alpha = 5.723848
                )
    case3.loadFactor = 2.5
    case3.fuelLevel = 0.0
    lift3 = case3.genLiftDist(118.38, 1.225)
    
    case3.fuelLevel = 0.7
    diagram3b =case3.genDiagrams(118.38, 1.225, filename="case3b.tex")
    case3.fuelLevel = 1.0
    diagram3c =case3.genDiagrams(118.38, 1.225, filename="case3c.tex")

    diagram3 =case3.genDiagrams(118.38, 1.225, filename="case3.tex")
    case3.getRequiredThickness(6.16, 10.0)
    saveToFile("case3.txt", diagram3, lift3,stiffnesses=True)
    plotStiffnessDift("case3_stiffness.png", case3.diagrams,case3.getSegments())


    case4 = LD(
                41.1,   #wingspan [m]
                6.76,      #rootchord [m]
                0.29,   #taperratio
                31.2,     #sweep0.25c [deg]
                0.0,    #AoA [deg]
                1.0,    #load factor
                [(0.675, 6.06189, 0.0), (0.55, 5.723848, 0.7)],  # (cl, clalpha, x) assumed to be linear between two points and constant if otherwise 
                [(-0.1507, 0.252101, 0.0),(-0.1147, 0.257831, 0.7)],      #cms, same as cls just not given yet
                [( 0.14 ,0.0),(0.1,0.7)] #T/C's for the airfoils
                #c_l_alpha = 5.723848
                )
    case4.loadFactor = 2.0
    lift4 = case4.genLiftDist(147.98, 1.225,)
    diagram4 = case4.genDiagrams(147.98, 1.225, filename="case4.tex")
    case4.getRequiredThickness(6.16, 10.0)
    case4.fuelLevel = 0.7
    diagram4b =case4.genDiagrams(147.98, 1.225, filename="case4b.tex")
    case4.fuelLevel = 1.0
    diagram4c =case4.genDiagrams(147.98, 1.225, filename="case4c.tex")
    

    saveToFile("case4.txt", diagram4, lift4, stiffnesses=True)
    plotStiffnessDift("case1_stiffness.png", case3.diagrams,case3.getSegments())

def main():
    case1 = LD(
                4.572,   #wingspan [m]
                0.9144,      #rootchord [m]
                0.33,   #taperratio
                0,     #sweep0.25c [deg]
                5,    #AoA [deg]
                1.0,    #load factor
                [(1.165, 5, 0.0), (0.55, 5.723848, 0.7)],  # (cl, clalpha, x) assumed to be linear between two points and constant if otherwise 
                [(-0.1507, 0.252101, 0.0),(-0.1147, 0.257831, 0.7)],      #cms, same as cls just not given yet
                [( 0.14 ,0.0),(0.1,0.7)] #T/C's for the airfoils
                #c_l_alpha = 5.723848
                )
    case1.loadFactor = 3.1
    case1.fuelLevel = 0.0
    lift1 = case1.genLiftDist(148, 1.225)
    diagram1 = case1.genDiagrams(148, 1.225, filename="case1.tex")

    print(case1.tipDeflection(0.001))
    print(case1.getRequiredThicknessDefl(6.16))
    print(case1.getRequiredThickness(6.16, 10.0))
    print(case1.diagrams["BendStiffness"]["Is"])
    saveToFile("case1.txt", diagram1, lift1, stiffnesses=True)
    plotStiffnessDift("case1_stiffness.png", case1.diagrams,case1.getSegments())

    case1.fuelLevel = 0.7
    diagram1b = case1.genDiagrams(148, 1.225, filename="case1b.tex")
    case1.fuelLevel = 1.0
    diagram1c = case1.genDiagrams(148, 1.225, filename="case1c.tex")
    
    #calculateCases()


if __name__ == "__main__":
    main()