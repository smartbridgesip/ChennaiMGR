from tkinter import *
from tkinter import ttk
import numpy as np

master = Tk()

master.title('WINE QUALITY')

master.geometry('350x410')
master.configure(background='#FBE2F0')

def sol():

    from sklearn.linear_model import LinearRegression, LogisticRegression
    from sklearn.model_selection import train_test_split
    import seaborn as sns
    import pandas as pd
    import matplotlib.pyplot as pit
   
    input = []
    input.append(float(e1.get()))
    input.append(float(e2.get()))
    input.append(float(e3.get()))
    input.append(float(e4.get()))
    input.append(float(e5.get()))
    input.append(float(e6.get()))
    input = np.array(input).reshape(1,-1)
    
    chemical1 = pd.read_csv('wine_chemical_analysis1.csv')
    white_wine = chemical1[chemical1['type']=='white']
    red_wine = chemical1[chemical1['type']=='red']
    feature = ['alcohol','density','volatile acidity','free sulfur dioxide','total sulfur dioxide','sulphates']

    sensory1 = pd.read_csv('wine_sensory_analysis1.csv',engine='python', error_bad_lines=False)
    sensory2 = pd.read_csv('wine_sensory_analysis2.csv',engine='python', error_bad_lines=False)

    white_varieties = ['Aligoté','Alvarinho', 'Auxerrois', 'Bacchus','Bual','Chardonnay','Chasselas','Chenin','Blanc','Colombard','Emerald','Riesling','Fumé','Blanc','Folle','Blanche','Furmint','Gewürztraminer','Grüner Veltliner','Hárslevelü','Jacquère','Kerner','Malvasia','Marsanne','Morio-Muscat','Müller-Thurgau','Muscadelle','Muscadet','Moscato','Palomino','Pedro Ximenez','Picolit','Pinot Blanc','Pinot Gris','Riesling','Rkatsiteli','Sacy','Savagnin','Sauvignon Blanc','Scheurebe','Sémillon','Sercial','Seyval Blan','Silvaner','Trebbiano','Verdelho','Verdicchio','Vidal','Viognier','Viura','Welschriesling']
    red_varieties = ['Aglianico','Alicante','Baco','Noir','Barbera','Cabernet Franc','Cabernet Sauvignon','Carignan','Cinsault','de Chaunac','Dolcetto','Freisa','Gamay','Gamay Beaujolais','Grenache','Grignolino','Kadarka','Lambrusco','Malbec','Maréchal Foch','Merlot','Mourvèdre','Nebbiolo','Petite Sirah','Pinot Noir','Pinot','Meunier','Pinotae','primitivo','Ruby Cabernet','Sangiovese','Syrah','Tempranillo,''Touriga Naçional','Xynomavro','Zinfandel']

    white = pd.concat([sensory1[sensory1['variety'].isin(white_varieties)] ,sensory2[sensory2['variety'].isin(white_varieties)]],sort=False)
    white = white[np.isfinite(white['price'])]
    red = pd.concat([sensory1[sensory1['variety'].isin(red_varieties)] ,sensory2[sensory2['variety'].isin(red_varieties)]],sort=False)
    red = red[np.isfinite(red['price'])]

    new_min = 80
    new_max = 100
    
    
    predicted_q=0
    var = str(v.get())
    if(var=='1'):
        x = white_wine[feature]
        y_q = white_wine['quality']
        x.fillna(0, inplace=True)
        model_white = LogisticRegression() #RandomForestClassifier(n_estimators=10)
        model_white.fit(x,y_q)
        predicted_q =  model_white.predict(input)
        x = white[['points']]
        y = white[['price']]
        old_min = white_wine['quality'].min()
        old_max = white_wine['quality'].max()
        qq = (((y_q - old_min) * (new_max - new_min)) / (old_max - old_min)) + new_min
        q = (((predicted_q - old_min) * (new_max - new_min)) / (old_max - old_min)) + new_min
        x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.3)
        model_price_white = LinearRegression()
        model_price_white.fit(x_train,y_train)
        predicted_p= model_price_white.predict([q])
        y_pred = model_price_white.predict(np.array(qq).reshape(-1,1))
    elif(var=='2'):
        x = red_wine[feature]
        y_q = red_wine['quality']
        x.fillna(0, inplace=True)
        model_red = LogisticRegression() #RandomForestClassifier(n_estimators=10)
        model_red.fit(x,y_q)
        predicted_q =  model_red.predict(input)
        old_min = red_wine['quality'].min()
        old_max = red_wine['quality'].max()
        qq = (((y_q - old_min) * (new_max - new_min)) / (old_max - old_min)) + new_min
        q = (((predicted_q - old_min) * (new_max - new_min)) / (old_max - old_min)) + new_min
        x = red[['points']]
        y = red[['price']]
        x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.3)
        model_price_red = LinearRegression()
        model_price_red.fit(x_train,y_train)
        predicted_p= model_price_red.predict([q])
        y_pred = model_price_white.predict(np.array(qq).reshape(-1,1))

    Label(master, text='Quality of the wine: '+ str(predicted_q[0])).grid(row=22,pady=10)
    Label(master, text='Price of the wine: $'+ str("{0:.2f}".format(predicted_p[0][0]))).grid(row=23,pady=10)
    pit.scatter(x, y,c='#F5B6DA', label='Known price vs quality')
    pit.scatter(q,predicted_p, c='#B00020',label='Given data')
    pit.title('Price vs quality')
    pit.xlabel('quality points')
    pit.ylabel('price in $')
    pit.legend()
    pit.show()

Label(master, text='Alcohol',background='#FBE2F0').grid(row=0)
Label(master, text='density',background='#FBE2F0').grid(row=1)
Label(master, text='volatile acidity',background='#FBE2F0').grid(row=2)
Label(master, text='free sulfur dioxide',background='#FBE2F0').grid(row=3)
Label(master, text='total sulfur dioxide',background='#FBE2F0').grid(row=4) 
Label(master, text='sulphates',background='#FBE2F0').grid(row=5)

e1 = Entry(master) 
e2 = Entry(master)
e3 = Entry(master) 
e4 = Entry(master)
e5 = Entry(master) 
e6 = Entry(master)


e1.grid(row=0, column=1,pady=10) 
e2.grid(row=1, column=1,pady=10) 
e3.grid(row=2, column=1,pady=10) 
e4.grid(row=3, column=1,pady=10)
e5.grid(row=4, column=1,pady=10) 
e6.grid(row=5, column=1,pady=10)
 

Label(master, text='8-14gms/100ml',background='#FBE2F0').grid(row=0, column=2)

Label(master, text='Type',background='#FBE2F0').grid(row=7)
v = IntVar() 
Radiobutton(master, text='white', variable=v, value=1,background='#FBE2F0').grid(row=7,column=1,pady=10)
Radiobutton(master, text='red', variable=v, value=2,background='#FBE2F0').grid(row=7,column=2,pady=10)



Button(master, text='Solution', command=sol).grid(row=20, column=1,pady=10)

master.mainloop() 
