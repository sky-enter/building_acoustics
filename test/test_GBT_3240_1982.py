from building_acoustics.standards.GBT_3240_1982 import *
for i in range(-20,14):
    x = frequency(k=i, b=1/3)
    # Z = x.K
    print(x)

for i in range(-6,4):
    x = frequency(k=i, b=1)
    # Z = x.K
    print(x)

print(x.BF,x.K,x.F) #(标称评率，K值，准确频率)输入的K是倍频程系数，输出的K就是什么系数，默认是1/3倍频程K系数