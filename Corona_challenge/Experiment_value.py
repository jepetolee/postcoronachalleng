def Experiment(temperature,humility):
    return temp(temperature)*hum(humility)


def temp(temperature):
    if(temperature>=38):
        return 1
    else:
        return (1-temperature/38)

'''
 코로나 바이러스와 유전자율이 거의 일치한 사스 바이러스는 38도
이상의 온도에서 급격이 감염률이 낮아진다.
그러나 온도가 38도 이상이 된다면 변수값이 0이하의 값이 되기에
값의 오류가 일어나며, 실제 환경변수랑 무관하기에 1로 설정했다. 
'''

def hum(humility):
    if (humility >= 80):
        return 1
    else:
        return (1 - humility/80)

'''
 상대 습도가 높을수록 코로나바이러스가 빠르게 사멸했다는 연구 결과가 있는데,
같은 온도에서 상대습도가 20%일 때는 120시간을 생존했지만 80%로 상대습도를 
높이자 6시간으로 바이러스 생존시간이 급격히 줄어들었다.
'''
