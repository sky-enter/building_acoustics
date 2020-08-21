import numpy as np
#——————分贝/声压级的加，减计算——————
class SPL(object):
    "GB/T 3238-1982	声学量的级及其基准值 。Sound pressure level,声压级的加，减计算；气体中声压级的定义“Lp=20log（p/p0）;Lp：输入声压级参数"
    def __init__(self,lp):
        # if isinstance(lp,numpy.ndarray):
        self.spL = lp #气体中声压级的定义“Lp=20log（p/p0）”
        self.P0=20E-6#基准声压
        self.P=10**(self.spL/20)*self.P0 #声压
        self.SPratio=(self.P/self.P0)**2 #声压比的平方/倍数

    def __str__(self):
        return  '%.2fdB'%self.spL
        # return  self.spL
    __repr__=__str__
    def __add__(self,other):
        if isinstance(other, SPL):

            return self.__class__(10 * np.log10(self.SPratio + other.SPratio))
        else:
            raise (TypeError,'类型不匹配')
    def __sub__(self,other):
        if isinstance(other, SPL):

            return self.__class__(10 * np.log10(self.SPratio - other.SPratio))
        else:
            raise (TypeError,'类型不匹配')

#计算声压级列表求和
def ssum(list=[]):
    # list=(sorted(list))
    m=[]
    for i in range(len(list)):
        m.append(SPL(list[i]))
    n=m[0]
    print(m)
    for i in range(1,len(list)):
        n=n+m[i]
    return  n.n

#计算声压级列表平均值
def saverage(list=[]):
    sum=ssum(list)
    average=10 * np.log10(sum.SPratio/len(list))
    return average

# m=[75.2 ,76.0 ,76.9 ,	75.8 ,	78.8 ,	78.4 ,	76.0 ,	76.6 ,	75.2 ,	75.2 ]
# x=SPL(20)
# x=x+x
# p=ssum(m)
# s=saverage(m)
