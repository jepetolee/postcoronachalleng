import Experiment_value as ev
import Inspect_value as iv
import corona_finder as cf
import pandas as pd
import numpy as np

immigrant = 'roaming.csv'  # 일별 대한민국 입국자 수
immigrant_names = ['returndate', 'iso', 'arrival', 'departure', 'count']
immigrant_data = pd.read_csv(immigrant,names=immigrant_names,encoding='euc-kr')
del immigrant_data['iso']  # 위 줄과 같은 효과
immigrant_info = immigrant_data.values
immigrants=[]
temp=immigrant_info[1][0]
loop_saver =0
sum=0
for i in range(len(immigrant_info)-1):
    if(immigrant_info[i+1][0]==temp):
        sum +=int(immigrant_info[i+1][3])
    else:
        immigrants.append(sum)
        temp = immigrant_info[i+1][0]
        sum=0
        loop_saver+=1

print(immigrants)

popualtion=7716600000
Korean=5164000
popforKo=Korean/popualtion

confirm = 'confirmer.csv'  # 국가별 일별 확진자 수
confirm_names = ['date','day','month','year','cases','deaths','countriesAndTerritories','geoId','countryterritoryCode','popData2018','continentExp']
confirm_data = pd.read_csv(confirm,names=confirm_names,encoding='euc-kr')
confirm_info = confirm_data.values
confirmers=[]
temp=confirm_info[1][0]
sum=0
for i in range(len(confirm_info)-1):
    if(confirm_info[i+1][0]==temp):
        sum +=int(confirm_info[i+1][4])
    else:
        confirmers.append(sum)
        temp = confirm_info[i+1][0]
        sum=0
confirmers.append(sum)
print(confirmers)

Kconfirm = 'korean_confirmer.csv'  # 한국 일별 확진자 수
kconfirm_names = ['date','day','month','year','cases','deaths','countriesAndTerritories','geoId','countryterritoryCode','popData2018','continentExp']
kconfirm_data = pd.read_csv(Kconfirm,names=kconfirm_names,encoding='euc-kr')
kconfirm_info = kconfirm_data.values
KO_confirmers=[]
data_confirmers=[]
for i in range(len(kconfirm_info)-1):
    a=[]
    a.append(int(kconfirm_info[i+1][4]))
    if i <127:
        data_confirmers.append(a)
    KO_confirmers.append(a)
print(KO_confirmers)


print(popualtion)

humid = 'humility.csv'  # 국가별 일별 습도
hum_names = ['spot', 'spot_name', 'date', 'humility']
hum_data = pd.read_csv(humid,names=hum_names,encoding='euc-kr')
hum_info = hum_data.values
humility=[]
temp=hum_info[1][2]
loop_saver =0
sum=0
k=0
for i in range(len(hum_info)-1):
    if(str(hum_info[i+1][2])[:10]==str(temp)[:10]):
        sum +=float(hum_info[i+1][3])
        k+=1
    else:
        humility.append(sum/k)
        temp = hum_info[i+1][2]
        sum=0
        k=0
humility.append(sum/k)
print(humility)

temper = 'temp.csv'  # 국가별 일별 기온
temper_names = ['spot', 'spot_name', 'date', 'temperature']
temper_data = pd.read_csv(temper,names=temper_names,encoding='euc-kr')
temper_info = temper_data.values
temperature=[]
temp=temper_info[1][2]
sum=0
k=0
for i in range(len(temper_info)-1):
    if(str(temper_info[i+1][2])[:10]==str(temp)[:10]):
        sum +=float(temper_info[i+1][3])
        k+=1
    else:
        temperature.append(sum/k)
        temp = temper_info[i+1][2]
        sum=0
        k=0
temperature.append(sum/k)
print(temperature)

enviroment_values =[]
for i in range(len(temperature)):
    enviroment_value=ev.Experiment(temperature[i],humility[i])*immigrants[i]
    enviroment_values.append(enviroment_value)

print(enviroment_values)

Infection_rates = []
infect=0
for i in range(len(confirmers)):
        infect = confirmers[i]/popualtion
        coforim=confirmers[i]*immigrants[i]/popualtion
        A=iv.BulildReedFrost(coforim,infect,immigrants[i])
        Infection_rates.append(A[1])
print(Infection_rates)

xtotal = []
for i in range(len(confirmers)):
    A=[]
    A.append(confirmers[i])
    A.append(enviroment_values[i])
    A.append(Infection_rates[i])
    xtotal.append(A)
print(xtotal)

corm_data = cf.normalization(xtotal)
koreancon= cf.normalization(data_confirmers)
KO_con =cf.normalization(KO_confirmers)
x= np.concatenate((corm_data,koreancon),axis=1)
print(x)

y=koreancon
print(y)
z=KO_con
dataX=[]
dataY=[]
newZ=[]
trainz=[]
for i in range(0, len(x) - 2):
    _x = x[i: i + 2]
    _y = y[i + 2] # 다음 나타날 확진자(정답)
    dataX.append(_x) # dataX 리스트에 추가
    dataY.append(_y) # dataY 리스트에 추가

for i in range(0, len(z) - 2):
    _z = z[i: i + 2]
    _z2 =z[i+2]
    newZ.append(_z)
    trainz.append(_z2)
trainX = np.array(dataX)
print(trainX)
trainY = np.array(dataY)
Zinput=np.array((newZ))
Ztrain = np.array(trainz)
print(Zinput)
cf.train(trainX,trainY,x,KO_confirmers,z,Zinput,Ztrain,60000)