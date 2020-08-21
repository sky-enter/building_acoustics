# -*- coding: UTF-8 -*-
import numpy as np
# import matplotlib.pyplot as plt
from building_acoustics.standards.GBT_3238_1982 import *
# xx="52.65563892	58.00903566	57.9644538	57.1740584	55.92687624	56.91365809	55.71854617	53.19799057	51.70899077	50.1736509	48.44291975	46.17176094	47.41973023	49.28125457	52.67156172	51.02405567	43.38321645	42.11296939"
# xx=xx.split("	")
# xi=[]
# for i in xx:
#     x=round(float(i),1)
#     xi.append(x)
# print (xi)
# # strki =" -19 -16 -13 -10 -7  -4  -1  0   1   2   3   4   4   4   4   4 "
# ki=[-19, -16, -13, -10, -7, -4, -1, 0, 1, 2, 3, 4, 4, 4, 4, 4]
# i=0
# while i<len(strki):
#     k=int(strki[i:i+4])
#     ki.append(k)
#     i=i+4
# print (ki)
#
# 空气声隔声倍频程Rw
class Rw_1_3(object):
    """ 计算Rw;计算Rw+C,Rw+Ctr"""
    def __init__(self,xi):
        # self.star_f=Star_f,Star_f=100,End_f=3150
        # self.end_g = End_f
        # self.xi=Xi
        self.Rww(xi)#计算Rw，计算频率在 100 Hz and 3.15 kHz之间
        self.C_100_3150(xi)
        self.ctr(xi)
    def __str__(self):
            return '1/3倍频程=>Rw(C;Ctr)=%d(%d;%d)dB'%(self.Rw,self.C,self.Ctr)
    __repr__ = __str__
    # 空气声隔声1/3倍频程Rw
    def Rww(self,xi):
        """ 计算Rw，计算频率在 100 Hz and 3.15 kHz之间"""
        ki = [-19, -16, -13, -10, -7, -4, -1, 0, 1, 2, 3, 4, 4, 4, 4, 4]
        xw = int(sum(xi) / len(xi) - 5)
        pi = []
        pic = list(map((lambda x: x[0] - x[1]), zip(ki, xi)))
        while sum(pi) <= 32:
            pi = [xw + x for x in pic if xw + x > 0]
            # b = sum(pi)
            # print(sum(pi))
            xw += 1
            # print(xw)
        self.Rw = (xw-2)
        return self.Rw

    def C_50_3150(self, xi):
        if len(xi)==19:
            k = np.array([-40,-36,-33,-29, -26, -23, -21, -19, -17, -15, -13, -12, -11, -10, -9, -9, -9, -9, -9])
            tl = np.array(xi)
            self.C_50_3150 = round(-10 * np.log10(np.sum(10 ** ((k - tl) / 10))) - self.Rw)
        else:
            self.C_50_3150=0
        return self.C_50_3150

    def C_100_3150(self,xi):
        k = np.array([-29, -26, -23, -21, -19, -17, -15, -13, -12, -11, -10, -9, -9, -9, -9, -9])
        tl=np.array(xi)
        self.C = round(-10 * np.log10(np.sum(10 ** ((k - tl) / 10)))-self.Rw)
        return self.C

    def C_100_5000(self, xi):
        if len(xi) == 18:
            k = np.array([-30, -27, -24, -22, -20, -18, -16, -14, -13, -12, -11, -10, -10, -10, -10, -10, -10, -10])
            tl = np.array(xi)
            self.C_100_5000 = round(-10 * np.log10(np.sum(10 ** ((k - tl) / 10))) - self.Rw)
        else:
            self.C_100_5000 = 0
        return self.C_100_5000

    def C_50_5000(self, xi):
        if len(xi) == 21:
            k = np.array([-41,-37,-34,-30, -27, -24, -22, -20, -18, -16, -14, -13, -12, -11, -10, -10, -10, -10, -10, -10, -10])
            tl = np.array(xi)
            self.C_100_5000 = round(-10 * np.log10(np.sum(10 ** ((k - tl) / 10))) - self.Rw)
        else:
            self.C_100_5000 = 0
        return self.C_100_5000

    def ctr(self,xi):
        k=[-25,-23,-21,-20, -20, -18, -16, -15, -14, -13, -12, -11, -9, -8, -9, -10, -11, -13, -15,-16,-18]
        if len(xi)==19:
            k_tr = np.array(k[0:19])
            tl = np.array(xi)
            self.Ctr_50_3150 = round(-10 * np.log10(np.sum(10 ** ((k_tr - tl) / 10))) - self.Rw)
            return self.Ctr_50_3150
        elif len(xi)==16:
            k_tr = np.array(k[3:19])
            tl = np.array(xi)
            self.Ctr = round(-10 * np.log10(np.sum(10 ** ((k_tr - tl) / 10))) - self.Rw)
            return self.Ctr
        elif len(xi) == 18:
            k_tr = np.array(k[3:21])
            tl = np.array(xi)
            self.Ctr_100_5000 = round(-10 * np.log10(np.sum(10 ** ((k_tr - tl) / 10))) - self.Rw)
            return self.Ctr_100_5000
        elif len(xi) == 21:
            k_tr = np.array(k[0:21])
            tl = np.array(xi)
            self.Ctr_50_5000 = round(-10 * np.log10(np.sum(10 ** ((k_tr - tl) / 10))) - self.Rw)
            return self.Ctr_50_5000

# rw =Rw_1_3(xi)
# print (rw)
def R_to_R_oct(R):
    Roct=round(-10*np.log10((10**(-R[0]/10)+10**(-R[1]/10)+10**(-R[2]/10))/3),1)
    return Roct

# xioct=[xi[0:3],xi[3:6],xi[6:9],xi[9:12],xi[12:15]]
# print(xioct)
# qq=[]
# for i in xioct:
#     # r=xioct[i]
#     n=R_to_R_oct(i)
#     qq.append(n)
# print(qq)

class Rw_1_1(object):
    """ 计算Rw;计算Rw+C,Rw+Ctr"""
    def __init__(self,xi):
        # self.star_f=Star_f,Star_f=100,End_f=3150
        # self.end_g = End_f
        # self.xi=Xi
        self.Rww(xi)#计算Rw，计算频率在 100 Hz and 3.15 kHz之间
        self.C_100_3150(xi)
        self.ctr(xi)
    def __str__(self):
            return '1/1倍频程=>Rw(C;Ctr)=%d(%d;%d)dB'%(self.Rw,self.C,self.Ctr)
            # return '1/1倍频程=>Rw(C;Ctr)=(%d,%d)dB' % (self.Rw,self.C)
    __repr__ = __str__
    # 空气声隔声1/3倍频程Rw
    def Rww(self,xi):
        """ 计算Rw，计算频率在 100 Hz and 3.15 kHz之间"""
        ki = [-16, -7, 0, 3, 4]
        xw = int(sum(xi) / len(xi) - 5)
        pi = []
        pic = list(map((lambda x: x[0] - x[1]), zip(ki, xi)))

        while sum(pi) <= 10:
            pi = [xw + x for x in pic if xw + x > 0]
            # print(sum(pi))
            xw += 1
            # print(xw)
        self.Rw = (xw - 2)
        return self.Rw

    def C_50_3150(self, xi):
        if len(xi)==6:
            k = np.array([-31,-21, -14, -8, -5, -4])
            tl = np.array(xi)
            self.C_50_3150 = round(-10 * np.log10(np.sum(10 ** ((k - tl) / 10))) - self.Rw)
        else:
            self.C_50_3150=0
        return self.C_50_3150

    def C_100_3150(self,xi):
        k = np.array([-21, -14, -8, -5, -4])
        tl=np.array(xi)
        self.C = round(-10 * np.log10(np.sum(10 ** ((k - tl) / 10)))-self.Rw)
        return self.C

    def C_100_5000(self, xi):
        if len(xi) == 6:
            k = np.array([-22,-15,-9,-6,-5,-5])
            tl = np.array(xi)
            self.C_100_5000 = round(-10 * np.log10(np.sum(10 ** ((k - tl) / 10))) - self.Rw)
        else:
            self.C_100_5000 = 0
        return self.C_100_5000

    def C_50_5000(self, xi):
        if len(xi) == 7:
            k = np.array([-32,-22,-15,-9,-6,-5,-5])
            tl = np.array(xi)
            self.C_100_5000 = round(-10 * np.log10(np.sum(10 ** ((k - tl) / 10))) - self.Rw)
        else:
            self.C_100_5000 = 0
        return self.C_100_5000

    def ctr(self,xi):
        k=[-18,-14,-10,-7, -4, -6, -11]
        if len(xi)==6:
            k_tr = np.array(k[0:7])
            tl = np.array(xi)
            self.Ctr_50_3150 = round(-10 * np.log10(np.sum(10 ** ((k_tr - tl) / 10))) - self.Rw)
            return self.Ctr_50_3150
        elif len(xi)==5:
            k_tr = np.array(k[1:6])
            tl = np.array(xi)
            self.Ctr = round(-10 * np.log10(np.sum(10 ** ((k_tr - tl) / 10))) - self.Rw)
            return self.Ctr
        elif len(xi) == 6:
            k_tr = np.array(k[1:])
            tl = np.array(xi)
            self.Ctr_100_5000 = round(-10 * np.log10(np.sum(10 ** ((k_tr - tl) / 10))) - self.Rw)
            return self.Ctr_100_5000
        elif len(xi) == 7:
            k_tr = np.array(k)
            tl = np.array(xi)
            self.Ctr_50_5000 = round(-10 * np.log10(np.sum(10 ** ((k_tr - tl) / 10))) - self.Rw)
            return self.Ctr_50_5000

# rw =Rw_1_1(qq)
# print (rw)

# 撞击声隔声1/3倍频程Lw
class Lw_1_3(object):
    def __init__(self, xi):
        self.Lww(xi)  # 计算Rw，计算频率在 100 Hz and 3.15 kHz之间
        self.C_I(xi)
        # self.ctr(xi)

    def __str__(self):
        return '1/3倍频程=>Lw(CI)=%d(%d)dB' % (self.Lw, self.ci)
        # return '1/3倍频程=>Lw(C;Ctr)=%ddB' % (self.Lw)
    __repr__ = __str__
    def Lww(self,xi):
        ki = [2, 2, 2, 2, 2, 2, 1, 0, -1, -2, -3, -6, -9, -12, -15, -18]
        xw = int(sum(xi) / len(xi) - 5)
        pi = [80]
        pic = list(map((lambda x: -x[0] + x[1]), zip(ki, xi)))
        while sum(pi) >32:
            pi = [-xw + x for x in pic if -xw + x > 0]
            # print(sum(pi))
            xw += 1
            # print(xw)
            self.Lw = xw-1
        return self.Lw

    def C_I(self,xi):
        self.ci=round(ssum(xi)[1]-15-self.Lw)
        return self.ci
# rw =Lw_1_3(xi)
# print (rw)


# 撞击声隔声倍频程Lw
class Lw_1_1(object):
    def __init__(self, xi):
        self.Lww(xi)  # 计算Rw，计算频率在 100 Hz and 3.15 kHz之间
        self.C_I(xi)
        # self.ctr(xi)

    def __str__(self):
        return '倍频程=>Lw(CI)=%d(%d)dB' % (self.Lw, self.ci)
        # return '1/3倍频程=>Lw(C;Ctr)=%ddB' % (self.Lw)
    __repr__ = __str__
    def Lww(self,xi):
        ki = [2, 2, 0, -3, -16]
        xw = int(sum(xi) / len(xi) - 5)
        pi = [33]
        pic = list(map((lambda x: -x[0] + x[1]), zip(ki, xi)))
        while sum(pi) >10:
            pi = [-xw + x-5 for x in pic if -xw + x-5 > 0]
            # print(sum(pi))
            xw += 1
            # print(xw)
            self.Lw = xw-1
        return self.Lw

    def C_I(self,xi):
        self.ci=round(ssum(xi)[1]-15-self.Lw)
        return self.ci

# rw = Lw_1_1(qq)
# print (rw)


#撞击声改善量
class delta_Lw(object):
    def __init__(self, xi):
        self.delta_Lww(xi)  # 计算Lw，计算频率在 100 Hz and 3.15 kHz之间
        # self.C_Idelta(xi)
        # self.ctr(xi)

    def __str__(self):
        return '=>ΔLLin=ΔLw+C_IΔ=%d + %d=%ddB' % (self.deltaLw, self.cidelta,self.deltaLlin)
        # return '1/3倍频程=>Lw(C;Ctr)=%ddB' % (self.Lw)

    __repr__ = __str__

    def delta_Lww(self, xi):
        #基准楼板的规范化撞击声压级Lnro
        Lnro = np.array([67,67.50,68.00,68.50,69,69.5,70,70.5,71,71.5,72,72,72,72,72,72])
        delta_L = np.array(xi)
        Lnr=list(Lnro-delta_L)
        Lnrw=Lw_1_3(Lnr).Lw
        self.deltaLw=78-Lnrw
        self.C_Idelta(Lnr)# 计算CIdelta
        return self.deltaLw
    def C_Idelta(self, xi):
        Cir=Lw_1_3(xi)
        self.cidelta = -Cir.ci-10
        self.delta_Llin()
        return self.cidelta

    def delta_Llin(self):
        self.deltaLlin=self.deltaLw + self.cidelta
        return self.deltaLlin
# pp=[8,7.23,5.20,3.31,7.316237989,6.564983919,6.8,13.6,18.4 ,21.0,27.9,	34.67 ,39.91 ,44.27637268,47.6,46.6 ]
# rw = delta_Lw(pp)
# print (rw)


#光裸重质楼板铺设面层后计权规范化撞击声压级的计算
class cal_Lnw(object):
    """ 光裸重质楼板铺设面层后计权规范化撞击声压级的计算"""
    def __init__(self, Ln0,deltalw):
        self.L_n1w(Ln0)  # 计算Rw，计算频率在 100 Hz and 3.15 kHz之间
        self.L_nw(deltalw)
        # self.ctr(xi)

    def __str__(self):
        return '倍频程=>Lnw=%d' % (self.Lnw)
        # return '1/3倍频程=>Lw(C;Ctr)=%ddB' % (self.Lw)
    __repr__ = __str__

    def L_n1w(self,Ln0):
        #基准面层的撞击声压级降低量
        delta_Lr=np.array([0,0,0,2,6,10,14,18,22,26,30,30,30,30,30,30])
        L_n0=np.array(Ln0)
        Ln1=list(L_n0-delta_Lr)
        Ln1w=Lw_1_3(Ln1)
        self.Ln1w=Ln1w.Lw
        return self.Ln1w
    def L_nw(self,deltalw):
        self.Lnw=self.Lnlw+19-deltalw
        return self.Lnw



# rw =ISO_Rw(xi)
# print (ISO_Rw(xi))
# hz=[]
# for i in range(16):
#     hz.append(i)
# ki=[ki[i]+rw for i in range(16)]
# f1 =['100','125','160','200','250','315','400','500','630','800','1K','1.25K','1.6K','2K','2.5K','3.15K','4K','5K']
# plt.figure(figsize=(5,5))#固定纵横坐标比例
# plt.plot(hz,xi)
# plt.plot(hz,ki)
# plt.xticks(hz, f1,rotation=60)#设置横坐标，及倾斜度数
# plt.ylim(20, 80)
# plt.grid()
# plt.show()
# "=============NR计算========="
# import numpy as np
# a=np.array(5)
# print (a)
