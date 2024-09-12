# Name : Mmasechaba Justicia Francesca Seopa
# Student no : 834758
# Date : 10 May 2015

"""
Background info of the program:
This code is created to open a csv file, then create a matrix of our distances. then it is bound to go to an extent where it uses the Gaussian elimination method to get
the inverse and then multiplying that with the necessary matrix to get the distributed load. Then from there it needs to integrate the function to get coefficients
for the shear and the bending moment, then get the constants, and then after this, this code is going to allow us to know the bending moment of an aircraft wing. Then
we create an output csv file. From this, we can deduce the mechanical stresses using the correct equation and many more stuffs.
"""

# Function for opening and reading a csv file
import csv
def openningFile():
    user=input('Please enter the the file name only,please do not add the extension: ')
    mycsv=open(user+".csv", 'r')
    FileReader=csv.reader(mycsv)
    Distances = []
    Loads = []
    b= []
    #formation of a matrix
    for i in FileReader:
        Distances.append(float(i[0]))
        b.append(float(i[1]))
        Loads.append(b)
        b = []
    return Distances, Loads,user


#/////////////////////////////////////////////////function for matrix creation\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

def matrixCreation(Distances):
    degree=int(input("Please enter the degree of polynomial you have at heart: "))
    matrix=[]
    for points in range(len(Distances)):
        Length=[]
        for k in range(int(degree)+1):
            Length.append(Distances[points]**k)
        matrix.append(Length)
    t =len(matrix)-1
    x= matrix[t][1]
    return matrix,x


#/////////////////////////////////////////////////function for matrix transposing\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

def interchangingMatrix(matrix):
    trans1=[]
    me=list(map(list,zip(*matrix)))
    trans1.append(me)
    trans=trans1[0]
    return trans


#/////////////////////////////////////////////////function for matrix multiplication\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\


def multiplication(trans,matrix):
    row=[]
    for k in range(len(trans)):
        sub= []
        for j in range(len(matrix[0])):
            temp=0
            for i in range(len(trans[0])):
                temp+=(trans[k][i]*matrix[i][j])
            sub.append(temp)
        row.append(sub)
        sub = []
    return row


#/////////////////////////////////////////////////function for matrix of zeros\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\


def identityMatrix(row):
    Row = len(row)
    Column = len(row[0])
    eye = []
    for i in range(Column):
        new=[]
        for j in range(Column):
            if i==j:
                new.append(1)
            else:
                new.append(0)
        eye.append(new)
    return eye


#/////////////////////////////////////////////////function for matrix inversion\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\


def antithesis(eye,row):
    me = 0
    ice = 0
    for n in range(len(row)):
        big = row[n][me]
        for k in range(me ,len(row[n])):
                row[n][k] = row[n][k]/big
        while ice <len(row[n]):
                eye[n][ice] = eye[n][ice]/big
                ice +=1
        ice = 0
        if me < len(row)-1:
            for z in range(me+1,len(row)):
                submatrix =row[n][me]*row[z][me]
                for t in range(len(row[z])):
                    row[z][t] = row[z][t] - row[n][t]*submatrix
                    eye[z][t] = eye[z][t] - eye[n][t]*submatrix
            me +=1
    mat = len(row)-1
    the = mat
    while mat > 0:
        while the > 0:
            music = row[the-1][mat]*row[mat][mat]
            row[the-1][mat] = row[the-1][mat] -music 
            for f in range(len(eye[the-1])):
                eye[the-1][f] = eye[the-1][f] - eye[mat][f]*music
            the = the-1
        mat  = mat-1
        the = mat
    return eye


#///function for creating a list to make it easy to integrate the list many times\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\


def matrixSorting(tot):
    Sorted = []
    for w in range(len(tot)):
        Sorted.append(tot[w][0])
    return Sorted


#/////////////////////////////////////////////////function for integration\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\


def integral(j,x):
    you= []
    integral = []
    m = 0
    for i in range(len(j)):
        you.append(j[i]/(i+1))
    for k in range(len(you)):
        m += you[k]*x**(k+1)
    integral.append(-m)
    for j in range(len(you)):
        integral.append(you[j])
    return integral


#/////////////////////////////////////////////////function for co-efficients for matrix\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\


def coefficient (j):
    for g in range(len(j)):
        if g == 0:
            CoEf = str(j[g])+"x^"+str(g)
        else:
            CoEf = CoEf +" + "+str(j[g])+"x^"+str(g)
    return CoEf


#/////////////////////////////////////////////////function for writing a file to csv\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\


def grace (j,h,p,name):
    info = open(name+"out.csv","w")#lecture slides 18, 30 April by 
    for l in range(len(j)):
        if l ==0:
            info.write(str(j[l]))
        else:
            info.write(","+str(j[l]))
    for w in range(len(h)):
        if w ==0:
            info.write("\n"+str(h[w]))
        else:
            info.write(","+str(h[w]))
    for m in range(len(p)):
        if m ==0:
            info.write("\n"+str(p[m]))
        else:
            info.write(","+str(p[m]))
    info.close()

    
#/////////////////////////////////////////////////function for main code\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\


def main():
    a   = openningFile()
    m   = matrixCreation(a[0])
    i   = interchangingMatrix(m[0])
    row = multiplication(i,m[0])
    I   = identityMatrix(row)
    eye = antithesis(I,row)
    x   = multiplication(eye,i)
    tot = multiplication(x,a[1])
    j   = matrixSorting(tot)
    h   = integral (j,m[1])
    pie = integral (h,m[1])
    kip = coefficient (j)
    toe = coefficient (h)
    Zip   = coefficient (pie)
    print("\n\n"+"Load Distribution :")
    print("W ="+kip)
    print("Shear Force :")
    print("V ="+toe)
    print("Bending Moment :")
    print("M ="+Zip)
    print()
    grace(j,h,pie,a[2])

    
    
if __name__== "__main__":
    main()
