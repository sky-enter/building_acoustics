import numpy as np
# import matplotlib.pyplot as plt
# from matplotlib.pyplot import MultipleLocator
# import building_base as bb
#温湿度转换为克分子浓度计算过程
class Humiture(object):
    'GBT_17247_1_2000_Annexe_B:温湿度转换为克分子浓度计算过程'
    def __init__(self,T=293,hr=50,Pa=101.325,TD=-1):
        self.Pr=101.325# 基准环境大气压kPa
        self.To=293.15 #基准大气温度K
        self.T01=273.16#三相点等温温度K(0.01摄氏度)
        self.T=T    #温度K
        self.hr=hr  #湿度%RH
        self.Pa=Pa  #大气压
        self.TD=TD  #露点温度
        if self.TD!=-1:
            self.h_TD()
        else:
            self.h_MC()

        # self.Saturated_vp(self.T,self.TO1)
    def __str__(self):
        return '克分子浓度：%.1f' % (self.h)
    __repr__ = __str__

    #饱和蒸汽压比Psat/pt的计算
    def Saturated_vp(self,t,t01):
        C=-6.8346*(t01/t)**1.261+4.6151
        self.Svp=10**C
        return self.Svp

    #通过相对湿度hr确定克分子浓度h
    def h_MC(self):
        svp=self.Saturated_vp(t=self.T,t01=self.T01)
        self.h=self.hr*svp*(self.Pa/self.Pr)
        return self.h

    #通过露点温度确定克分子浓度h
    def h_TD(self):
        svp=self.Saturated_vp(t=self.T,t01=self.TD)
        self.h = 100 * svp * (self.Pa / self.Pr)
        return self.h

# ac=Humiture(T=293.15,hr=50,Pa=101.325)
# #
# print(ac.h)