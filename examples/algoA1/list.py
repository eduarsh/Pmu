import math
from numpy import double



list2 = [4.0, 29.432700000000004, 49.97641645552949, 2396.878181701731, -2.3221587301779554,
          2396.878315975625, -122.3221675152621, 2396.8779305656003, 117.67783409757415,
           24.930546915814453, -2.3221587301779283, 24.930548312431235, -122.32216751526235,
            24.93054430368274, 117.67783409757389, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
             0.0, 0.0, 0.0, 24.930546915814453, 177.67784126982207, 24.930548312431235, 57.67783248473767
             , 24.93054430368274, -62.32216590242612, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

listVA = []
listVB = []
listVC = []
vaCosSum = 0
vaSinSum = 0
# list3.append(list2(range(0,37,4)))
for i in range(3,45,6):
    listVA.append(list2[i])
    listVA.append(list2[i+1])
    
for i in range(5,45,6):
    listVB.append(list2[i])
    listVB.append(list2[i+1])
    
for i in range(7,45,6):
    listVC.append(list2[i])
    listVC.append(list2[i+1])
for check in range(2,14,2):
    abs(listVA[0])*abs(listVA[check])*math.cos(math.radians(listVA[1])-(math.radians(listVA[check+1])))
#     print(check)
#     print(listVA[check],listVA[check+1])
#     print("--------------------------------")
             
    print(abs(listVA[0])*abs(listVA[check])*math.cos(math.radians(listVA[1])-(math.radians(listVA[check+1]))))
for check in range(2,13,2):
            vaSinSum += abs(listVA[0])*abs(listVA[check])*math.sin(math.radians(listVA[1])-math.radians(listVA[check+1]))
            print(vaSinSum)
# print(abs(double(listVA[0]))*abs(double(listVA[8]))*math.cos(math.radians(listVA[1])-math.radians(listVA[9])) )
# print(abs(listVA[0])*abs(listVA[8])*math.cos(listVA[1]-listVA[9]) )
# print(math.cos(math.pi))
# print(math.cos(math.radians(180)))
# print(math.degrees(3.14))
# print(double(2397.0*24.93*math.cos(-2.322-(-2.322)))+double(2397.0*24.93*math.cos(-2.322-177.7)))
# print(type(abs(listVA[0])*abs(listVA[8])*math.cos(listVA[1]-listVA[9])))
# print(vaCosSum)
# print(vaSinSum)
print(listVA)
print(listVB)
print(listVC)