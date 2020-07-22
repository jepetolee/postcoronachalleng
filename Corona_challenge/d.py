import pandas as pd
immigrant = 'roaming.csv'  # 일별 대한민국 입국자 수
immigrant_names = ['returndate', 'iso', 'arrival', 'departure', 'count']
immigrant_data = pd.read_csv(immigrant,names=immigrant_names,encoding='euc-kr')
immigrant_data.info()  # 데이터 정보 출력
del immigrant_data['iso']  # 위 줄과 같은 효과
immigrant_data.info()  # 데이터 정보 출력
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

confirm = 'confirmer.csv'  # 국가별 일별 확진자 수
confirm_names = ['date','day','month','year','cases','deaths','countriesAndTerritories','geoId','countryterritoryCode','popData2018','continentExp']
confirm_data = pd.read_csv(confirm,names=confirm_names,encoding='euc-kr')
confirm_data.info()
confirm_info = confirm_data.values
confimers=[]
temp=confirm_info[1][0]
loop_saver =0
sum=0
for i in range(len(confirm_info)-1):
    if(confirm_info[i+1][0]==temp):
        sum +=int(confirm_info[i+1][4])
    else:
        confimers.append(sum)
        temp = confirm_info[i+1][0]
        sum=0
        loop_saver+=1
print(confimers)
popualtion=7,716,600,000#위키백과 출처 전세계 인구수 데이터
print(popualtion)

humid = 'humility.csv'  # 국가별 일별 습도
hum_names = ['spot', 'spot_name', 'date', 'humility']
hum_data = pd.read_csv(humid,names=hum_names,encoding='euc-kr')
hum_data.info()
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
        loop_saver+=1
print(len(humility))

temper = 'temp.csv'  # 국가별 일별 기온
temper_names = ['spot', 'spot_name', 'date', 'temperature']
temper_data = pd.read_csv(temper,names=temper_names,encoding='euc-kr')
temper_data.info()  # 데이터 정보 출력
temper_info = temper_data.values
temperature=[]
temp=temper_info[1][2]
loop_saver =0
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
        loop_saver+=1
print(temperature)



