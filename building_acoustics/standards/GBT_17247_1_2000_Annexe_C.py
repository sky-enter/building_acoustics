"""GB/T17247.1-2000 附录C
    非均匀实际大气的影响时的气象参数发生变化，
    衰减系数变化"""
import numpy as np
from building_acoustics.standards.GBT_17247_1_2000_Annexe_A import *

class High_level(object):
    "GB / T17247.1 - 2000 附录C :非均匀实际大气的影响时的气象参数发生变化，衰减系数变化"
    def __init__(self,H=0):
        self.Pms=101.325# 海平面高度年平均大气压kPa
        self.tms=288.15 # 海平面高度年平均温度K
        self.A=[1.00271,-0.12223,0.04546,-0.031545,0.0076472,-0.00079906,0.000029429,1.8395E-20,5.44894,-0.60683,0.0283643,-0.000474746]

        self.H=H #高度
        if self.H<=11 :
           self.Groposphere()
        elif 11< self.H <=20:
           self.Stratosphere()

    def __str__(self):
        # return  "pass"
        return '结果：%.5f，%.5f，%.5f,%.5f' % (self.Tm,self.Pm,self.hm,self.a)
    __repr__ = __str__

    #计算指数参数G
    def number_G(self):
        if self.H<=11 :
            G=0
            for a in range(1,7):
                G=G+self.A[a]*(self.H**(a))
            return G
        elif 11< self.H <=20:
            G=0
            for a in range(8,12):
                G=G+self.A[a]*(self.H**(a-7))
            return G

    # 计算海平面0-11km的对流层温度，压力，分子浓度的数据
    def Groposphere(self):
        self.Tm=self.tms-6.5*self.H
        self.Pm=self.Pms*(self.Tm/self.tms)**5.25588
        self.hm=self.A[0]*(10**self.number_G())
        return self.Tm,self.Pm,self.hm,self.H_a()
    # 计算海平面11-20km的对流层温度，压力，分子浓度的数据
    def Stratosphere(self):
        self.Tm=216.65
        self.Pm=22.632*np.e**(-0.157688*(self.H-11))
        self.hm=self.A[7]*(10**self.number_G())
        return self.Tm,self.Pm,self.hm,self.H_a()

    def H_a(self):
        at= Atmos_abs(f=63, T=self.Tm, h=self.hm, Pa=self.Pm)
        self.a=at.a
        return self.a


# a=High_level(12)
# print(a)
# # print(ac.a)
# p=Atmos_abs(f=63,T=a.Tm,h=a.hm,Pa=a.Pm)
# print(p)