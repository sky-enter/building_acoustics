import numpy as np

class frequency(object):
    'GB/T 3240-1982 声学测量中的常用频率 ；GB/T 3241-1998 倍频程和分数倍频程滤波器   k=0为1000Hz，频率选择是一个整数, b=1为倍频程；b=1/3为1/3倍频程'

    def __init__(self,f=None,k=None,b=1/3):
        """k, 为1/3倍频程数k=0时为1000Hz，\
           n, 为1/1倍频程数，n=0时为1000Hz"""
        self.B = b  # 频程（b=1为倍频程；b=1/3为1/3倍频程）
        if f==None and k!=None:
            self.judgement_int(k)
            self.calculate_F()
            self.calculate_BF()
        elif f!=None and k==None:
            self.BF=f
            self.calculate_K()
            self.calculate_F()
        else:
            # input("警告：f,k不能同时输入数据")
            exit("警告：f,k不能同时输入数据!!!")


    def __str__(self):
        if self.B==1:
            return  '倍频程=>准确值：%.2fHz；标称值：%.2fHz'%(self.F,self.BF)
        else:
            return '1/3倍频程=>准确值：%.2fHz；标称值：%.2fHz'%(self.F,self.BF)

    __repr__ = __str__

    def judgement_int(self,k):
        if isinstance(k, int):# k=0为1000Hz，频率选择是一个整数
            if -28<= k <=22:
                self.K = k
            else:
                input("输入数据超出常用频率范围，请在-28至22之间选择K值")
            return  self.K
        else:
            raise (TypeError, '类型不匹配；你输入（k）的不是整数')

    def calculate_F(self):
        self.F=(1000 * (10 ** (3 * self.B / 10)) ** self.K)
        return self.F
        # return self.__class__(1000 * (10 ** (3 * self.B / 10)) ** self.K)
    def calculate_K(self):
        kf=10*np.log10(self.BF/1000)
        kn=round(10*np.log10(self.BF/1000))
        # 添加一个判断是否为标称值的程序
        self.K = kn
        return self.K

    def calculate_B(self):
        self.B=10*np.log10(self.F/1000)/(3*self.K)
        return self.B

    def calculate_BF(self):
        if self.B==1/3:
            if -28 <= self.K < -20:
                self.BF=self.f_round(self.F*100)/100
                return self.BF
            elif -20 <= self.K < -10:
                self.BF=self.f_round(self.F*10)/10
                return self.BF
            elif -10 <= self.K < 0:
                self.BF = self.f_round(self.F)
                return self.BF
            elif 0 <= self.K < 10:
                self.BF = self.f_round(self.F/10)*10
                return self.BF
            elif 10 <= self.K < 20:
                self.BF = self.f_round(self.F/100)*100
                return self.BF
            elif 20 <= self.K <=22:
                self.BF = self.f_round(self.F/1000)*1000
                return self.BF
        else:
            if -7 < self.K <=-4:
                self.BF = self.f_round(self.F*10)/10
                return self.BF
            elif  -3 <= self.K < 0:
                self.BF = self.f_round(self.F)
                return self.BF
            elif 0 <= self.K < 4:
                self.BF = self.f_round(self.F / 10) * 10
                return self.BF
            elif 4 <= self.K < 7:
                self.BF = self.f_round(self.F / 100) * 100
                return self.BF
    def f_round(self,f):
        BF = round(f / 5) * 5
        if BF==795:BF=800
        return BF  

