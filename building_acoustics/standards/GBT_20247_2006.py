import numpy as np
# import building_base as bb
# import atmosphere_sound_absorption as asb
from building_acoustics.standards.GBT_17247_1_2000_Annexe_A import *
class Aba_room(object):
    def __init__(self,f,t,T=20,Q=50,Pa=101.325,V=242,S=276.9):
        self.t=t#混响时间
        self.T=T +273.15 #摄氏温度
        self.Q=Q #相对湿度
        self.V=V #混响室容积m³
        self.S=S #室内总表面积平方米
        self.f=f #频率
        self.Pa=Pa #大气压力
        self.c = 331.45 + 0.6 * T
        self.k=0.161
        self.Seibin()
        self.GBT20247()
        self.Ilyn()
        self.Ilyn_Noot()

    def __str__(self):

            return '吸声量A:(赛宾AS：%.2fm2；国标AG：%.2fm2；伊林Ai：%.2fm2；伊林-努特生Ain：%.2fm2)' % (self.AS, self.AG,self.Ai,self.Ain)

    __repr__ = __str__

    def speed_CK(self,T):
        self.c=331.45+0.6*T
        self.k=24/(self.c*np.log10(np.e))
        return self.c,self.k
    #声强衰减系数m计算
    def ms(self):
        ms = Atmos_abs(f=self.f, T=self.T, hr=self.Q, Pa=self.Pa)
        m=ms.a/(10*np.log10(np.e))
        return m
    #赛宾公式计算吸声量
    def Seibin(self):
        self.AS=self.k*self.V/self.t
        return self.AS
    #GB/T20247混响室吸声测量
    def GBT20247(self):
        # AS=self.Seibin()
        m=self.ms()
        self.AG=55.3*self.V/(self.c*self.t)-4*m*self.V
        return self.AG
    #伊林公式
    def Ilyn(self):
        AS = self.Seibin()
        self.Ai=self.S*(1-np.e**(-AS/self.S))
        return self.Ai
    #伊林-努特生公式
    def Ilyn_Noot(self):
        m=self.ms()
        AS = self.Seibin()
        self.Ain=self.S*(1-np.e**(-(AS-4*m*self.V)/self.S))
        return self.Ain
#
b=Aba_room(f=1000,t=9.4,T=20,Q=50,V=273)
c=Aba_room(f=1000,t=3.4075,T=20,Q=50,V=273)
# a=b.Seibin()
print(b,c)