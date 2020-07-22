'''
Reed-Frost모형을 기준으로 모델을 구사함.
날짜: t
'''
import numpy as np
def BulildReedFrost(I,p,N):
    q = 1 - (1 - p) ** (I)#편균확률의 이항을 분산을 구하기 위해 최신 정보를 갖옴
    INew = np.random.binomial(N-I, q)# 이항 분포의 생략
    S=N-INew
    return (S, INew)

