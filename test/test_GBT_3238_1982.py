from building_acoustics.standards.GBT_3238_1982 import *

#声压级计算
sound=75.6
a=SPL(sound)#转换成声压级格式
print(a)
print( a.P)  #声压
print(a.P0)#基准声压
print(a.spL)#声压级
print(a.SPratio)#声压比的平方/倍数
b=SPL(60)


c=a+b #声压级的加法运算
print(c)

m=[75.2 ,76.0 ,76.9 ,	75.8 ,	78.8 ,	78.4 ,	76.0 ,	76.6 ,	75.2 ,	75.2 ]
p=ssum(m) #多个声压级的求和
print(p,p.spL)#(86.60dB, 86.5963792078135)：（修约带单位的数据，不经过修约的数据）

s=saverage(m)#多个声压级的求均值
print(s)
