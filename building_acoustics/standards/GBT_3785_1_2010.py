
from building_acoustics.standards.GBT_3240_1982 import *
#———————A、C、Z计权声级计算——————————
class Weight_SL(object):
    '计算A、C、Z计权声级,符合GB/T 3785.1-2010'
    def __init__(self,lp,weight="A",star_f=10):
        #A计权修正值
        self.Cor_A=[-70.4,-63.4,-56.7,-50.5,-44.7,-39.4,-34.6,-30.2,-26.2,-22.5,-19.1,-16.1,-13.4,-10.9,-8.6,-6.6,-4.8,-3.2,-1.9,-0.8,0,0.6,1,1.2,1.3,1.2,1,0.5,-0.1,-1.1,-2.5,-4.3,-6.6,-9.3]
        # C计权修正值
        self.Cor_C=[-14.3,-11.2,-8.5,-6.2,-4.4,-3,-2,-1.3,-0.8,-0.5,-0.3,-0.2,-0.1,0,0,0,0,0,0,0,0,0,-0.1,-0.2,-0.3,-0.5,-0.8,-1.3,-2,-3,-4.4,-6.2,-8.5,-11.2]
        # Z计权修正值
        self.Cor_Z=0
        self.LP = lp
        # self.LpW=0
        self.weight=weight
        self.star_f=star_f
        self.end_freq()
        self.calculate_ACZ()

    def __str__(self):
        return '%s声级：Lp%s=%.1fdB(%s)' % (self.weight,self.weight, self.LpW,self.weight)

    __repr__ = __str__
    #取得开始和结束的频率位置，用于寻找修正值所在位置
    def end_freq(self):
        k=frequency(f=self.star_f)
        n=k.K+20
        self.star_f=int(n)
        self.end_f=int(n+len(self.LP))

    def calculate_ACZ(self):
        sum1 = 0
        a = self.star_f
        b = self.end_f
        if self.weight=="A":
            for i in range(a,b,1):
                sum1 = sum1 +10**(0.1*(self.LP[i-a]+self.Cor_A[i]))
            # self.LpW=10* np.log10(sum1)
        elif self.weight=="C":
            for i in range(a,b,1):
                sum1 = sum1 +10**(0.1*(self.LP[i-a]+self.Cor_C[i]))
        else:
            for i in range(a,b,1):
                sum1 = sum1 +10**(0.1*(self.LP[i-a]))
        self.LpW=10* np.log10(sum1)
        return  self.LpW

# m=[86.82,86.845,	86.315,	88.215	,89.935,	90.85,	85.18	,85.895	,90.56	,84.77,	82.82	,85.19,	83.8	,79.31	,81.01	,79.96,	73.665,	70.91]
# b=Weight_SL(m,star_f=100,weight="C")
# print(b)
