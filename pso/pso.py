import random
import numpy as np
import matplotlib.pyplot as plt

class pso() :

    c = 1.494 # 加速度係数
    w = 0.729 # 慣性定数
    tmax = 1000 # 最大繰り返し回数
    stopt = 0 
    cr = 1e-5 # 終了条件
    xmin = -5 # 範囲
    xmax = 5 # 範囲
    plot = list() # 描画用

    fg = float('inf') # gbest 全体で最も良かった評価

    def __init__(self, m, d, func='sphere') : 
        self.m = m # 粒子の数
        self.d = d # 次元の数
        self.func = func # 目的関数の設定
        self.v = np.zeros((m,d)) # 速度
        self.f = np.zeros(m) # 評価関数を格納
        #self.xp = np.empty((m,d)) # pbest 個人が最も良かった位置
        #self.xg = np.empty(d)  # gbest　全体で最も良かった位置
        self.xp = np.full((m,d), float('inf'))
        self.xg = np.full(d, float('inf'))
        self.fp = np.full(m, float('inf'))
        self.x = (self.xmax - self.xmin) * np.random.rand(m,d) + self.xmin # 位置
    
    def sphere_f(self,i) :
        self.f[i] = 0
        for d in range(self.d) :
            xd = self.x[i][d]
            self.f[i] += xd**2

    def rastrigin_f(self,i) :
        self.f[i] = 0
        for d in range(self.d) :
            xd = self.x[i][d]
            self.f[i] += ((xd**2) - 10*np.cos(2*np.pi*xd) + 10)

    def calc(self) :
        each_fg = [] # 実験用
        for self.stopt in range(1,self.tmax+1) :
            for i in range(self.m) :
                # 目的関数
                if self.func == 'sphere' :
                    self.sphere_f(i)
                elif self.func == 'rastrigin' :
                    self.rastrigin_f(i)
                
                if self.f[i] < self.fp[i] :
                    self.fp[i] = self.f[i]
                    self.xp[i] = self.x[i]
                    if self.fp[i] < self.fg :
                        self.fg = self.fp[i]
                        self.xg = self.x[i]
            each_fg.append(self.fg)
            if self.fg < self.cr :
                break
            
            #r1 = np.random.rand()
            #r2 = np.random.rand()
            for i in range(self.m) :
                r1 = np.random.rand()
                r2 = np.random.rand()
                self.v[i] = self.w*self.v[i] + self.c*r1*(self.xp[i] - self.x[i]) + self.c*r2*(self.xg - self.x[i])
                self.x[i] = self.x[i] + self.v[i]
            self.plot.append([self.stopt, self.fg]) # 描画用
        return each_fg

    def pl(self) :
        plt.clf()
        plt.title('spend time and fg')
        plt.xlabel('fg')
        plt.ylabel('spend time')

        self.nplot = np.array(self.plot)
        self.nplot = self.nplot.T
        
        plt.plot(self.nplot[0], self.nplot[1])
        plt.show()
        

if __name__ == '__main__' :
    p1 = pso(30,5)
    p1.calc()

    print("終了時刻t = " + str(p1.stopt))
    print("解の目的関数値Fg = ", end="")
    print(p1.fg)
    print("解Xg = ", end="")
    print(p1.xg)