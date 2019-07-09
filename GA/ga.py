import numpy as np

# MAXW = 9   # 最大重量
# MINW = 1   # 最小重量
# MAXV = 10  # 最大価値
# MINV = 100 # 最小価値

class ga :

    # 変数宣言
    pm = 0.05 # 突然変異確率
    tmax = 100 # 最大繰り返し回数

    # ナップサックの最大重量
    # wmax = 15 # 品物5個 
    wmax = 20 # 品物10個

    fbest = 0 # 郡全体の最適解

    def __init__(self, m, d, w, v) :
        self.m = m # 個体数
        self.d = d # 解の次元数
        self.weight = w # 各重さ
        self.value = v # 各価値

        # 染色体
        self.x = np.random.randint(0,2,(m,d)) # 初期世代の染色体
        self.xnext = np.zeros((m,d)) # 次世代の染色体

        self.f = np.empty(m) # 評価関数を格納
        self.calc_value() # fの計算
        self.fbest = max(self.f) # 郡全体の最適解(評価関数)(初期化)
        self.xbest = self.x[np.argmax(self.f)] # 郡全体の最適解(染色体)(初期化)


    def calc_value(self) :
        for i in range(self.m) :
            self.f[i] = 0
            tmpw = 0
            for j in range(self.d) :
                if self.x[i][j] == 0 :
                    continue
                else :
                    self.f[i] += self.value[j]
                    tmpw += self.weight[j]
            if tmpw > self.wmax :
                self.f[i] = 1

    def choice_parent(self) : # 親選択
        sumf = self.f / sum(self.f)
        return np.random.choice(range(20),2,replace=False,p=sumf)

    def two_point_crossing(self, i) : # 2点交叉
        p1, p2 = self.choice_parent() # 親を選択
        d1, d2 = np.random.choice(range(d),2,replace=False) # 2点交叉用
        # 使いやすいように入れ替え
        if d1 > d2 : 
            d1, d2 = d2, d1 
        self.xnext[i] = np.concatenate([np.concatenate([self.x[p1][0:d1+1],self.x[p2][d1+1:d2+1]]),self.x[p1][d2+1:self.d]]) # 次世代の子供

    def calc(self) :
        for self.stopt in range(1,self.tmax) :
            self.calc_value() # fの更新
            if max(self.f) > self.fbest :
                self.fbest = max(self.f) # fbestの更新
                self.xbest = self.x[np.argmax(self.f)] # xbestの更新
            for i in range(0,self.m) :
                self.two_point_crossing(i) # 2点交叉
                # 突然変異
                if np.random.rand() < self.pm :
                    self.xnext[i] = 1 - self.xnext[i]
            self.x = self.xnext

if __name__ == '__main__' :
    # weight = (MAXW - MINW) * np.random.randn(d) + MINW # 各重さをランダムで
    # value = (MAXV - MINV) * np.random.randn(d) + MINV # 各価値をランダムで

    # weight = np.array([7,5,1,9,6]) # 品物5個
    weight = np.array([3,6,5,4,8,5,3,4,8,2]) # 品物5個
    # value = np.array([50,40,10,70,55]) # 品物10個
    value = np.array([70,120,90,70,130,80,40,50,30,70]) # 品物10個

    m = 20 # 個体数
    d = len(weight)  # 解の次元数もとい品物数
    cnt = 0 # カウント

    for i in range(100) :
        ga1 = ga(m,d,weight,value) # イニシャライズ
        ga1.calc() # 最適化
        if int(ga1.fbest) == 420 :
            cnt += 1
        if i % 10 == 0 :
            print(f'{i} is done. cnt = {cnt}')

    print(f'最適解を求めた回数{cnt}')
    # print(f"終了時刻t = {ga1.stopt}")
    # print(f"解の目的関数値Fg = {ga1.fbest}")
    # print(f'最適解 Xbest = {ga1.xbest}')