import numpy as np
from building_acoustics.standards.GBT_17247_1_2000_Annexe_A import *
from building_acoustics.standards.GBT_3240_1982 import *
class Attenuation(object):
    def __init__(self):
        pass
    def __str__(self):
        pass
        # return '大气吸收衰减系数a：%.5fdB/m' % (self.a)
    __repr__ = __str__
    #几何发散
    def A_div(self,d,d0=1):
        #d 声源与接受点之间的距离
        self.Adiv=20*np.log10(d/d0)+11
        return self.Adiv
    #大气吸收
    def A_atm(self,d,f,t,hr):
        a=Atmos_abs(f=f,T=t+273.15,hr=hr)
        self.Aatm=a.a*d
        return self.Aatm

    # 特定条件下的地面效应
    def A_grt(self,hm,d,dp,hs,hr):
        a=4.8-(2*hm/d)*(17+(300/d))
        d=10*np.log10(1+(dp**2+(hs-hr)**2)/(dp**2+(hs+hr)**2))
        if a<=0:
            self.Agrt=0
            self.domga=d
        else:
            self.Agrt = a
            self.domga = d

    #地面效应
    def A_gr(self,hs,Gs,hr,Gr,dp,Gm):
        a=np.array(self.A_s(hs,Gs,dp))
        b=np.array(self.A_r(hr,Gr,dp))
        c=np.array(self.A_m(hs,hr,dp,Gm))
        self.Agr=list(a+b+c)
        return self.Agr
    #计算As，Ar的中间公式
    def _abcd(self,h,dp):
        #dp 投影到地面上的声源与接受点之间的距离
        a_h=1.5+3*np.e**(-0.12*(h-5)**2)*(1-np.e**(-dp/50))+5.7*np.e**(-0.09*h**2)*(1-np.e**(-2.8*10**(-6)*dp**2))
        b_h=1.5+8.6*np.e**(-0.09*h**2)*(1-np.e**(-dp/50))
        c_h=1.5+14*np.e**(-0.46*h**2)*(1-np.e**(-dp/50))
        d_h=1.5+5*np.e**(-0.9*h**2)*(1-np.e**(-dp/50))
        return a_h,b_h,c_h,d_h
    def _Amq(self,hs,hr,dp):
        if dp<=30*(hs+hr) :
            Am_q=0
        elif dp> 30*(hs+hr):
            Am_q=1-30*(hs+hr)/dp
        return Am_q
    #声源区域的分衰减
    def A_s(self,hs,Gs,dp):
        self.As=[-1.5]
        for i in range(4):
            a=-1.5+Gs*self. _abcd(hs,dp)[i]
            self.As.append(a)
        for j in range(3):
            b=-1.5*(1-Gs)
            self.As.append(b)
    #接受区域的分衰减
    def A_r(self,hr,Gr,dp):
        self.As = [-1.5]
        for i in range(4):
            a = -1.5 + Gr * self._abcd(hr, dp)[i]
            self.As.append(a)
        for j in range(3):
            b = -1.5 * (1 - Gr)
            self.As.append(b)
    #中间区域的分衰减
    def A_m(self,hs,hr,dp,Gm):
        a=-3*self._Amq(hs,hr,dp)
        b=a*(1-Gm)
        self.Am=[a]
        for i in range(7):
            self.Am.append(b)
        return self.Am


    #屏蔽
    def D_z(self,f,c2=20,dss,dsr,a,d,drs=1,e):
        """a:声源和接受点之间的距离在平行与屏障上边界的分量/m  \
        f,计算频率，c2=20 包括地面反射的影响，c2=40为特殊情况下，可将地面反射作为虚声源单独第考虑，\
        dss:声源到绕射编的距离，dsr：绕射边到接受点的距离，d：声源到接受点的距离，|
        e：在双绕射情况下两个绕射边界之间的距离，drs=1单绕射，drs=2双绕射"""
        f_n=340 / f
        z=self.zz_C3(f_n,dss,dsr,a,d,drs,e)
        kmet=self.Kmet(dss,dsr,z[0],d)
        self.dz=10*np.log10(3+(c2/f_n)*z[1]*z[0]*kmet)
        return self.dz
    #气象修正因子
    def Kmet(self,dss,dsr,z,d):
        if z>0:
            Kmet=np.e**(-np.sqrt(dss*dsr*d/(2*z))/2000)
        else:
            Kmet=1
        return Kmet
    #绕射与直达声之间的路程差z[0]
    def zz_C3(self,fn,dss,dsr,a,d,drs=1,e):
        f_n = fn
        if drs==1:
            c3=1
            e=0
            # z=np.sqrt((dss+dsr)**2+a**2)-d
        elif drs==2:
            e=e
            c3 = (1 + (5 * f_n / e) ** 2) / (1 / 3 + (5 * f_n / e) ** 2)
        z = np.sqrt((dss + dsr+e) ** 2 + a ** 2) - d
        return z,c3



    #气象校正
    def C_met(self,hs,hr,dp,C0):
        hsr=hs+hr
        if dp<= 10*hsr:
            self.Cmet=0
        elif dp>10*hsr:
            self.Cmet=C0*(1-10*hsr/dp)
        return self.Cmet
    #
    def A_misc(self):
        pass
    #树叶
    def A_fol(self,df,f):
        dict_df={63:[0,0.02],125:[0,0.03],250:[1,0.04],500:[1,0.05],1000:[1,0.06],2000:[1,0.08],4000:[2,0.09],8000:[3,0.12]}
        if 10<=df<=20:
            self.Afol=dict_df[f][0]
        elif 20<df<=200:
            self.Afol = dict_df[f][1]
        elif df > 200:
            self.Afol = dict_df[f][1]
        return self.Afol
    #工业场所
    def A_site(self,f):
        dict_site={63:0,125:0.015,250:0.025,500:0.025,1000:0.02,2000:0.02,4000:0.015,8000:0.015}
        self.Asite =  dict_site[f]
        return self.Asite
    #房屋群
    def A_hous(self):
        pass
a= Attenuation()
a.A_fol(df=25,f=1000)
# print(a)
