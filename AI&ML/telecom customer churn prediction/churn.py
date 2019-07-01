from tkinter import *
from tkinter.filedialog import askopenfilename
import csv
import os
import numpy as np
window =Tk()

window.title('Prediction of churn rate')
window.geometry('500x600')

input = np.array([])

#label field
Label(window, text='SeniorCitizen').grid(row=0) 
Label(window, text='tenure').grid(row=1) 
Label(window, text='MonthlyCharges').grid(row=2) 
Label(window, text='TotalCharges').grid(row=3)
Label(window, text ='churn_rate').grid(row = 23,column = 1)

#entry field
e1 = Entry(window) 
e2 = Entry(window)
e3 = Entry(window) 
e4 = Entry(window)
#e5 = Entry(window)

e1.grid(row=0, column=1,pady=20) 
e2.grid(row=1, column=1,pady=10) 
e3.grid(row=2, column=1,pady=10) 
e4.grid(row=3, column=1,pady=10)
#e5.grid(row=23,column=2,pady=10)


#Label(window, text ='churn_rate').grid(row = 23,column = 1)
#e5.grid(row = 23,column = 4,pady = 10)

t1 = Text(window, height=1, width=20)
t1.grid(row=23, column=2, pady=10)

def pred():
    import pandas as pd
    import numpy as np
    

    input = []
    input.append(float(e1.get()))
    input.append(float(e2.get()))
    input.append(float(e3.get()))
    input.append(float(e4.get()))
    print(input)
    input = np.array(input).reshape(1,-1)

    telecom_cust = pd.read_csv("Telco-Customer-Churn.csv")
    telecom_cust.head()
    #print(s)
    telecom_cust.columns.values
    #print(t)
    telecom_cust.TotalCharges = pd.to_numeric(telecom_cust.TotalCharges, errors='coerce')
    telecom_cust.isnull().sum()
    #print(k)
    #Removing missing values 
    telecom_cust.dropna(inplace = True)
    #Remove customer IDs from the data set
    df2 = telecom_cust.iloc[:,1:]
    #Convertin the predictor variable in a binary numeric variable
    df2['Churn'].replace(to_replace='Yes', value=1, inplace=True)
    df2['Churn'].replace(to_replace='No',  value=0, inplace=True)

    #Let's convert all the categorical variables into dummy variables
    df_dummies = pd.get_dummies(df2)
    df_dummies.head()
    #print(h)
    # We will use the data frame where we had created dummy variables
    y = df_dummies['Churn'].values
    X = df_dummies[['SeniorCitizen','tenure','MonthlyCharges','TotalCharges']]
    
# Scaling all the variables to a range of 0 to 1
    from sklearn.preprocessing import MinMaxScaler
    features = X.columns.values
    scaler = MinMaxScaler(feature_range = (0,1))
    scaler.fit(X)
    X = pd.DataFrame(scaler.transform(X))
    X.columns = features
    #print(X.columns)
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=101)
    # Running logistic regression model
    from sklearn.linear_model import LogisticRegression
    model = LogisticRegression()
    result = model.fit(X_train, y_train)
    #print("result is:",result)
    from sklearn import metrics
    prediction_test = model.predict(X_test)
    # Print the prediction accuracy
    #print (metrics.accuracy_score(y_test, prediction_test))



    y_new = model.predict(input)
    print("Predicted=%s" % (y_new[0]))
    t1.insert(END, y_new[0])


Button(window, text='submit', command=pred).grid(row=20, column=1,pady=10)


window.mainloop()