import numpy as np
from building_acoustics.standards.GBT_3240_1982 import *

#———————声学等响曲线——————————
import matplotlib.pyplot as plt
class Loudness(object):
    """等响曲线计算与绘制：lp=声压级,ln=等响,f=频率,np=（20-12500）中第几个频率   GB/T 4963-2007/ISO 226-2003 声学标准等响曲线"""
    def __init__(self, lp=-1,ln=-1,f=1000,np=-1):
        # AF=响度感觉幂指数
        self.AF=[0.532,0.506,0.48,0.455,0.432,0.409,0.387,0.367,0.349,0.33,0.315,0.301,0.288,0.276,0.267,0.259,0.253,0.25,0.246,0.244,0.243,0.243,0.243,0.242,0.242,0.245,0.254,0.271,0.301]
        # LU=对1kHz归一化线性传递函数的幅值
        self.LU=[-31.6,-27.2,-23,-19.1,-15.9,-13,-10.3,-8.1,-6.2,-4.5,-3.1,-2,-1.1,-0.4,0,0.3,0.5,0,-2.7,-4.1,-1,1.7,2.5,1.2,-2.1,-7.1,-11.2,-10.7,-3.1]
        #TF=听阀，单位dB
        self.TF=[78.5,68.7,29.5,51.1,44,37.5,31.5,26.5,22.1,17.9,14.4,11.4,8.6,6.2,4.4,3,2.2,2.4,3.5,1.7,-1.3,-4.2,-6,-5.4,-1.5,6,12.6,13.9,12.3]
        self.F = f
        self.np=np # 给定频率属于第K+17
        if lp!=-1:
            self.LP = lp
            self.lp_to_ln()
        if ln!=-1:
            self.LN = ln
            self.ln_to_lp()
    def __str__(self):
       return  '频率：%.1fHz；等响度：%.fphon方(%.1fsone宋)；声压级：%.1fdB'%(self.F,self.LN,self.song,self.LP)
    __repr__ = __str__
    #响度转换成声压级
    def ln_to_lp(self):
        if self.np==-1:
            zp=frequency(self.F)
            n=int(zp.K+17)
            self.np=n
        else:
            n=self.np
        af1=4.47*(0.001)*(10**(0.025*self.LN)-1.15)
        af2=(0.4*10**((self.TF[n]+self.LU[n])/10-9))**self.AF[n]
        af=af1+af2
        self.LP=(10*np.log10(af)/self.AF[n])-self.LU[n]+94
        self.ln_to_song()
        return self.LP

    # 声压级转换成响度级
    def lp_to_ln(self):
        if self.np==-1:
            zp=frequency(self.F)
            n=int(zp.K+17)
            self.np = n
        else:
            n=self.np
        bf1 = (0.4 * 10 ** ((self.LP + self.LU[n]) / 10 - 9)) ** self.AF[n]
        bf2 = -(0.4 * 10 ** ((self.TF[n] + self.LU[n]) / 10 - 9)) ** self.AF[n]+0.005135
        bf = bf1 + bf2
        self.LN = 40 * np.log10(bf) + 94
        self.ln_to_song()
        return self.LN

    #响度级LN 转换为 响度N宋
    def ln_to_song(self):
        # self.song=np.e**((self.LN-40.009)/14.424)
        self.song=(2**((self.LN-40)/10))
        # if self.LN==40:  self.song=1
        return self.song
    # 绘制等响曲线图
    def plot_Loudness(self):
        frqL = []  # 横坐标：频率20--12500
        loud = []
        f1 = []
        for i in range(-17, 12):  # 频率20--12500Hz，对应-17--11
            frq1 = frequency(k=i)
            frqL.append(frq1.BF)
            f1.append(i + 17)
        # for i in range(10,100):

        for j in range(len(frqL)):
            # m = Loudness(f=frqL[j], ln=70, np=j)
            n = j
            af1 = 4.47 * (0.001) * (10 ** (0.025 * self.LN) - 1.15)
            af2 = (0.4 * 10 ** ((self.TF[n] + self.LU[n]) / 10 - 9)) ** self.AF[n]
            af = af1 + af2
            lp= (10 * np.log10(af) / self.AF[n]) - self.LU[n] + 94

            # m=ln_to_lp()
            loud.append(lp)

        f=f1[self.np]
        plt.figure(figsize=(10, 5))  # 固定纵横坐标比例
        plt.plot(f1, loud)
        # plt.plot(frqL, ki)
        plt.xticks(f1, frqL, rotation=60)  # 设置横坐标，及倾斜度数
        # 显示坐标点

        plt.scatter(f, self.LP, s=20, marker='x')
        # 显示坐标点横线、竖线
        plt.vlines(f, 0, self.LP, colors="c", linestyles="dashed")
        plt.hlines(self.LP, 0, f, colors="c", linestyles="dashed")
        # 显示坐标点坐标值
        plt.text(f, self.LP, (float('%f' % self.F), float('%.f' % self.LP)), ha='right', va='top', fontsize=11)
        plt.grid()
        plt.show()
        return loud

# a=Loudness(ln=85)
# print(a)
# a.plot_Loudness()

