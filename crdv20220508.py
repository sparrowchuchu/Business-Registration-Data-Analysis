#視覺化專題>>>公司登記數據分析
import pandas as pd
import matplotlib.pyplot as plt

#可顯示中文的字體
plt.rcParams['font.family']='Microsoft YaHei'
plt.rcParams['font.size']=12

# >>>載入資料。
def crdv(year,month):
    #讀取csv檔
    #總計資本額(含在臺營運資金、以新台幣百萬元為單位)
    if month!=12:
        month='0'+str(month)
    name=str(year)+str(month)
    crdv=pd.read_csv('%s.csv'%(name),encoding='utf8')
    return crdv

#使用dict與迴圈儲存datafram資料(201206-202203)。
dataName=dict()
for year in range(2012,2023):
    for month in range(3,13,3):
        if (year==2022) & (month==6):
            break
        elif (year==2012) & (month==3):
            continue
        elif month!=12:
            dataName[str(year)+'0'+str(month)]=crdv(year,month)
        else:
            dataName[str(year)+str(month)]=crdv(year,month)

taipeiData=pd.read_csv('taipeiData.csv',encoding='ansi')

# >>>定義 index 與 column 。
# "cc": CountyCity，"Ca": Capital，"Co": Count
indexByCC=[byCountyCity.lstrip() for byCountyCity in dataName['202203']['縣 市 別']]  #移除空白字元
ccCa202203=dataName['202203'].iloc[:,2]
ccCo202203=dataName['202203'].iloc[:,1]

indexByYM=[data for data in dataName.keys()]
totalCapital=[data.iloc[0,2] for data in dataName.values()]
totalCount=[data.iloc[0,1] for data in dataName.values()]
ccCapital=dict()
ccCount=dict()
for iCC in range(len(indexByCC)):
    if (iCC>1) & (iCC<23) :
        ccCapital[iCC]=[]
        ccCount[iCC]=[]
        for data in dataName.values():
            ccCapital[iCC].append(data.iloc[iCC,2])
            ccCount[iCC].append(data.iloc[iCC,1])

specialCity=['臺北市','新北市','桃園市','臺中市','臺南市','高雄市']
area={'北部地區':['臺北市','新北市','基隆市','新竹市','桃園市','新竹縣','宜蘭縣'],
      '中部地區':['臺中市','苗栗縣','彰化縣','南投縣','雲林縣'],
      '南部地區':['高雄市','臺南市','嘉義市','嘉義縣','屏東縣','澎湖縣'],
      '東部與金馬地區':['花蓮縣','臺東縣','金馬地區']}
totalCoArea202203=[427291,162102,144591,5575+1637]
totalCaArea202203=[19732671.99,3182199.655,3494344.788,97965.49962+25957.80423]

indexTaipeiIndustry=[data for data in taipeiData['行業別'][:21]]
taipeiCo109=[int(data) for data in taipeiData.groupby('年底別').get_group('109年').iloc[:,2]]
taipeiCa109=[int(data) for data in taipeiData.groupby('年底別').get_group('109年').iloc[:,3]]
taipeiCo110=[int(data) for data in taipeiData.groupby('年底別').get_group('110年').iloc[:,2]]
taipeiCa110=[int(data) for data in taipeiData.groupby('年底別').get_group('110年').iloc[:,3]]

# >>>色彩設定。
colors4=['cornflowerblue','slateblue','mediumorchid','palevioletred']

# >>>開始圖表輸出。
figTcAndTc='公司登記現有家數及實收資本額變化趨勢'
figTCaTCo=plt.figure(figsize=(14,7))
figTCa=figTCaTCo.add_subplot(111)                            #使用add_subplot設置雙y軸
figTCa.plot(indexByYM,totalCapital,'c-',label='總計資本額')
figTCa.set_ylabel('總計資本額  (百萬元)',fontsize=14)
figTCa.ticklabel_format(axis='y',style='plain',useOffset=False) #y軸不使用科學記號表示法
plt.xticks(rotation=90)                                      #調整x軸設定執行順序在.twinx()之前
plt.legend(loc=2)                                            #設定figTCa圖例位置參數                         
plt.grid()                                                   #網格
figTCo=figTCa.twinx()                                        #共同x軸
figTCo.plot(indexByYM,totalCount,'r--',label='公司登記家數')
figTCo.set_ylabel('公司登記家數',fontsize=14)
plt.legend(loc=6)                                            #設定figTCo圖例位置參數 
plt.title('%s'%figTcAndTc,fontsize=18)
plt.savefig('%sN.png'%figTcAndTc,dpi=300,bbox_inches='tight') #bbox_inches='tight' 文字不被切掉
plt.show()
plt.close()

for cc,ccCa,ccCo in zip(indexByCC[2:23],ccCapital.values(),ccCount.values()):
    if cc in specialCity:                                     #輸出'六都'的圖表
        figccCaAndccCo='%s 公司登記現有家數及實收資本額變化趨勢'%cc
        figccCaTCo=plt.figure(figsize=(14,7))
        figccCa=figccCaTCo.add_subplot(111)                   #使用add_subplot設置雙y軸
        figccCa.plot(indexByYM,ccCa,'c-',label='總計資本額')
        figccCa.set_ylabel('總計資本額  (百萬元)',fontsize=14)                 
        figccCa.ticklabel_format(axis='y',style='plain',useOffset=False)
        plt.xticks(rotation=90)                               #調整x軸設定執行順序在.twinx()之前
        plt.legend(loc=2)                                     #設定figTCa圖例位置參數                         
        plt.grid()                                            #網格
        figccCo=figccCa.twinx()                               #共同x軸
        figccCo.plot(indexByYM,ccCo,'r--',label='公司登記家數')
        figccCo.set_ylabel('公司登記家數',fontsize=14)
        plt.legend(loc=6)                                     #設定figTCo圖例位置參數 
        plt.title('%s'%figccCaAndccCo,fontsize=18)
        plt.savefig('%sN.png'%figccCaAndccCo,dpi=300)
        plt.show()
        plt.close()
    else:
        pass

figccCa202203='2022年03月 各縣市公司登記實收資本額'
plt.figure(figsize=(14,7))
plt.bar(indexByCC[2:-2],ccCa202203[2:-2],color='slateblue')
plt.ticklabel_format(axis='y',style='plain',useOffset=False)
plt.xticks(rotation=90,fontsize=14)
plt.yticks(fontsize=14)
plt.title('%s'%figccCa202203,fontsize=18)
pctCa202203=[ca/ccCa202203[0]*100 for ca in ccCa202203[2:-2]]
for x,y,pct in zip(indexByCC[2:-2],ccCa202203[2:-2],pctCa202203):   #顯示百分比
    plt.text(x,y+10000,'%2.2f%%'%pct,color='mediumslateblue',ha='center', va='bottom')
plt.ylabel('總計資本額  (百萬元)',fontsize=14)
plt.savefig('%sN.png'%figccCa202203,dpi=300,bbox_inches='tight')
plt.show()
plt.close()

figccCo202203='2022年03月 各縣市公司登記現有家數'
plt.figure(figsize=(14,7))
plt.bar(indexByCC[2:-2],ccCo202203[2:-2],color='slateblue')
plt.ticklabel_format(axis='y',style='plain',useOffset=False)
plt.xticks(rotation=90,fontsize=14)
plt.yticks(fontsize=14)
plt.title('%s'%figccCo202203,fontsize=18)
pctCo202203=[co/ccCo202203[0]*100 for co in ccCo202203[2:-2]]
for x,y,pct in zip(indexByCC[2:-2],ccCo202203[2:-2],pctCo202203):   #顯示百分比
    plt.text(x,y+200,'%2.2f%%'%pct,color='mediumslateblue',ha='center', va='bottom')
plt.ylabel('登記家數',fontsize=14)
plt.savefig('%sN.png'%figccCo202203,dpi=300,bbox_inches='tight')
plt.show()
plt.close()

figCaArea202203='2022年03月 各地區公司登記實收資本額'
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13,5))
fig.subplots_adjust(wspace=.5)                                       #wspace調整子圖表距離
ax1.pie(totalCaArea202203,labels=area.keys(),colors=colors4,autopct='%2.2f%%',
        pctdistance=.8,startangle=-80,textprops = {"fontsize" : 12}) #startangle調整輸出角度
ax1.set_title('%s\n'%figCaArea202203,fontsize=18)
ax1.axis('equal')
ax2.barh(list(area.keys()),totalCaArea202203,color=colors4)          #使用barh()製作水平長條圖
ax2.ticklabel_format(axis='x',style='plain',useOffset=False)
ax2.set_xlabel('總計資本額  (百萬元)',fontsize=14)
plt.savefig('%sN.png'%figCaArea202203,dpi=300,bbox_inches='tight')   #bbox_inches='tight'
plt.show()
plt.close()

figCoArea202203='2022年03月 各地區公司登記現有家數'
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13,5))
fig.subplots_adjust(wspace=.5)
ax1.pie(totalCoArea202203,labels=area.keys(),colors=colors4,autopct='%2.2f%%',
        pctdistance=.8,startangle=-70,textprops = {"fontsize" : 12}) #startangle調整輸出角度
ax1.set_title('%s\n'%figCoArea202203,fontsize=18)
ax1.axis('equal')
ax2.barh(list(area.keys()),totalCoArea202203,color=colors4)          #使用barh()製作水平長條圖
ax2.ticklabel_format(axis='x',style='plain',useOffset=False)
ax2.set_xlabel('登記家數',fontsize=14)
plt.savefig('%sN.png'%figCoArea202203,dpi=300,bbbox_inches='tight')
plt.show()
plt.close() 

# >>>輸出並列長條圖
y=[p for p in range(len(indexTaipeiIndustry[1:]))]                        

figTaipeiCa='2020年與2021年 臺北市 各行業公司登記實收資本額比較'
plt.figure(figsize=(14,7))
height=0.4
plt.barh([p + height for p in y],taipeiCa109[1:],label='2020年',color='palevioletred',height=0.4) #設定y軸偏移量
plt.barh(y,taipeiCa110[1:],label='2021年',color='slateblue',height=0.4)
plt.yticks([p + height/2 for p in y], indexTaipeiIndustry[1:])       #設定y軸刻度標籤
plt.ticklabel_format(axis='x',style='plain',useOffset=False)
plt.title('%s'%figTaipeiCa)
plt.xlabel('總計資本額  (千元)',fontsize=14)         
plt.legend() 
plt.savefig('%sN.png'%figTaipeiCa,dpi=300,bbox_inches='tight')
plt.show()
plt.close()

figTaipeiCo='2020年與2021年 臺北市 各行業公司登記現有家數比較'
plt.figure(figsize=(14,7))
height=0.4
plt.barh([p + height for p in y],taipeiCo109[1:],label='2020年',color='palevioletred',height=0.4)  
plt.barh(y,taipeiCo110[1:],label='2021年',color='slateblue',height=0.4)
plt.yticks([p + height/2 for p in y], indexTaipeiIndustry[1:])       #設定y軸刻度標籤
plt.ticklabel_format(axis='x',style='plain',useOffset=False)
plt.title('%s'%figTaipeiCo)
plt.xlabel('登記家數',fontsize=14)         
plt.legend() 
plt.savefig('%sN.png'%figTaipeiCo,dpi=300,bbox_inches='tight') 
plt.show()
plt.close()



