import matplotlib.pyplot as plt
fl = open("C:/Users/domin/Data_Test_SPAR_test.txt")
fl = fl.read().split("\n")
fl.reverse()
X = []
Y = []
i = (len(fl)) - 2
outbuffer1 = ""
outbuffer2 = ""
while i > 0:
    data = (fl)[i].split(" ")
    if(len(data) != 2):
         i-= 2
         continue
    print(data)
    outbuffer1 += data[0] + "\n"
    outbuffer2 += data[1] + "\n"
    X.append(abs(float(data[0])*10 / 1000))
    Y.append(float(data[1]))
    i -= 2
print("maximum sustained load is : " + str(max(X)))
out1 = open("C:/Users/domin/loads.txt", "w")
out2 = open("C:/Users/domin/displacement.txt", "w")
out1.write(outbuffer1)
out2.write(outbuffer2)
plt.plot(Y, X)
plt.show()


