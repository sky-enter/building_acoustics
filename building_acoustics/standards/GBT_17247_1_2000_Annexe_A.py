import numpy as np
# import matplotlib.pyplot as plt
# from matplotlib.pyplot import MultipleLocator
# import building_base as bb
# import kelvin_humiture as kh
from building_acoustics.standards.GBT_17247_1_2000_Annexe_B import *
class Atmos_abs(object):
    def __init__(self,f,T=293,hr=50,Pa=101.325,TD=-1,h=-1):
        self.Pr=101.325# 基准环境大气压kPa
        self.To=293.15 #基准大气温度K
        self.T = T  # 温度K
        self.hr = hr  # 湿度%RH
        self.Pa = Pa  # 大气压
        self.f=f #计算频率
        if h==-1:
            self.h=Humiture(T=T,hr=hr,Pa=Pa,TD=TD).h
        else:
            self.h=h
        self.frO()
        self.frN()
        self.absorp()
    def __str__(self):
        # return  "pass"
        return '大气吸收衰减系数a：%.5fdB/m' % (self.a)
    __repr__ = __str__

    #计算氧弛豫频率
    def frO(self):
        # h=kh.Humiture(T=self.T,hr=self.hr,Pa=self.Pa)
        self.fro=(self.Pa/self.Pr)*(24+(4.04*10000)*self.h*(0.02+self.h)/(0.391+self.h))
        return self.fro

    # 计算氮弛豫频率
    def frN(self):
        # h = kh.Humiture(T=self.T, hr=self.hr, Pa=self.Pa)
        a=(self.Pa/self.Pr)*(self.T/self.To)**(-0.5)
        b=9+280*self.h*np.e**(-4.17*((self.T/self.To)**(-1/3)-1))
        self.frN=a*b
        return self.frN

    # 计算大气吸收衰减系数a  dB/m
    def absorp(self):
        # a=1.8*10**-11*(self.Pr/self.Pa)*(self.T/self.To)**(0.5)
        # acr=(1.6*10**-10*(self.T/self.To)**(0.5)*self.f**2)/(self.Pa/self.Pr)

        # b=0.01275*np.e**(-22391/self.T)*(self.fro+self.f**2/self.fro)**(-1)
        # c=0.1068*np.e**(-3352/self.T)*(self.frN+self.f**2/self.frN)**(-1)
        # self.a=8.686*self.f**2*(a+(self.T/self.To)**(-5/2)*(b+c))
        self.a=self.acr()+self.avib(X=0.209,Q=2239.1,fr=self.fro)+self.avib(X=0.781,Q=3352,fr=self.frN)

        return self.a
    #吸收和转动吸收衰减系数
    def acr(self):
        acr = (1.6 * 10 ** -10 * (self.T / self.To) ** (0.5) * self.f ** 2) / (self.Pa / self.Pr)
        return acr
    #振动弛豫
    def avib(self,X,Q,fr):
        avib=self.max_a(X=X,Q=Q)*(self.f/self.speed_c())*(2*(self.f/fr)*(1+(self.f/fr)**2)**(-1))
        return avib
    #振动弛豫引起的一个波长距离上的醉倒衰减
    def max_a(self,X,Q):
        max=1.559*X*(Q/self.T)**2*np.e**(-Q/self.T)
        return max
    #声速计算
    def speed_c(self):
        c=343.2*(self.T/self.To)**(1/2)
        return c
# A=Atmos_abs(f=1000,T=293.15,hr=50,Pa=101.325)
# B=Atmos_abs(f=1000,T=293.15,hr=50,Pa=101.325)
# # p=A.a*4/(10*np.log10(np.e))
# print(A.a)