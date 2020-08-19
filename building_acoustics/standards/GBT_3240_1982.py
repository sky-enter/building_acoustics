import numpy as np

class frequency(object):
    'GB/T 3240-1982 声学测量中的常用频率 ；GB/T 3241-1998 倍频程和分数倍频程滤波器   k=0为1000Hz，频率选择是一个整数, b=1为倍频程；b=1/3为1/3倍频程'

    def __init__(self,f=-1,k=-100,b=1/3):
        self.B = b  # 频程（b=1为倍频程；b=1/3为1/3倍频程）
        if k!=-100:self.judgement_int(k)
        if f==-1 :
            self.calculate_F()
            self.calculate_BF()
        elif f!=-1:
            self.BF=f
            self.calculate_K()
            self.calculate_F()


    def __str__(self):
        if self.B==1:
            return  '倍频程=>准确值：%.2fHz；标称值：%.fHz'%(self.F,self.BF)
        else:
            return '1/3倍频程=>准确值：%.2fHz；标称值：%.fHz'%(self.F,self.BF)

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
        if -28 <= self.K < -20:
            self.BF=round((self.F*100)/5)*0.05
            if self.K == -21: self.BF = self.BF + 0.05
            return self.BF
        elif -20 <= self.K < -10:
            self.BF = round((self.F * 10) / 5) * 0.5
            if self.K == -11: self.BF = self.BF + 0.5
            return self.BF
        elif -10 <= self.K < 0:
            self.BF = round((self.F) / 5) * 5
            if self.K == -1: self.BF = self.BF + 5
            return self.BF
        elif 0 <= self.K < 10:
            self.BF=round((self.F/10)/5)*50
            if self.K == 9: self.BF = self.BF + 50
            return self.BF
        elif 10 <= self.K < 20:
            self.BF=round((self.F/100)/5)*500
            if self.K == 19: self.BF = self.BF + 500
            return self.BF
        elif 20 <= self.K <=22:
            self.BF=round((self.F/1000)/5)*5000
            return self.BF

# x=frequency(f=250)
# Z=x.K
# print(x,Z)


