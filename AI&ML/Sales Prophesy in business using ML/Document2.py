from tkinter import *
root=Tk()
root.title("BLACK FRIDAY PREDICTOR")

label1= Label(root,text="Product_ID")
label1.grid(row=1, column=0)
pro_id_txt=Entry(root)
pro_id_txt.grid(row=1, column=1)

label2= Label(root,text="Age")
label2.grid(row=2, column=0)
age_txt=Entry(root)
age_txt.grid(row=2, column=1)

label3= Label(root,text="Gender")
label3.grid(row=3, column=0)
gender_txt=Entry(root)
gender_txt.grid(row=3, column=1)

answer_label1=Label(root, text="---")
answer_label1.grid(row=4, column=0)

answer_label2=Label(root, text="---")
answer_label2.grid(row=4, column=1)

answer_label3=Label(root, text="---")
answer_label3.grid(row=5, column=0)

answer_label4=Label(root, text="---")
answer_label4.grid(row=5, column=1)

answer_label5=Label(root, text="---")
answer_label5.grid(row=6, column=0)

answer_label6=Label(root, text="---")
answer_label6.grid(row=6, column=1)


def predicting():
	if (pro_id_txt.get() != " " and age_txt.get() != " " and gender_txt.get()!= " "):
		try:
			global yp1
			global yp2
			global yp3
			p1=float(pro_id_txt.get())
			a1=float(age_txt.get())
			g1=float(gender_txt.get())
			import pandas as pd
			import sklearn
			import matplotlib.pyplot as plt
			from sklearn import preprocessing
			import numpy as np
			data=pd.read_csv("blackfriday-edited1.csv")
			#print (data.head())
			df=data.fillna(0)
			#print (df)
			from sklearn.model_selection import train_test_split
			from sklearn.linear_model import LinearRegression 
			from sklearn.metrics import mean_squared_error
			from sklearn.preprocessing import LabelEncoder
			from sklearn import metrics
			from sklearn.metrics import  accuracy_score
			p=df['Product_ID'].values
			le=preprocessing.LabelEncoder()
			p_encoded=le.fit_transform(p)
			p_encode=p_encoded.tolist()
			#print(p_encode)
			#print ("product_id:",p_encode)
			g=df['Gender'].values
			g_encoded=le.fit_transform(g)
			g_encode=g_encoded.tolist()
			#print ("Gender:",g_encode)
			a=df['Age'].values
			a_encoded=le.fit_transform(a)
			a_encode=a_encoded.tolist()
			#print ("age:",a_encode)
			x =list(zip(p_encoded,g_encoded,a_encoded))
			#print(x)


			#print ("product 1")
			y=df['Product_Category_1'].values
			x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.25)
			clf=LinearRegression()
			#print (clf)
			clf=clf.fit(x_train,y_train)
			yp1=clf.predict([[p1,a1,g1]])
			#yp1=yp1.tolist()
			#print ("predicted y")
			#print (yp1)


			#print ("product 2")
			y1=df['Product_Category_2'].values
			x_train,x_test,y_train,y_test=train_test_split(x,y1,test_size=0.25)
			clf1=LinearRegression()
			#print (clf1)
			clf1.fit(x_train,y_train)
			yp2=clf1.predict([[p1,a1,g1]])
			#yp2=yp2.tolist()
			#print ("predicted y")
			#print (yp2)


			#print("product 3")
			y5=df['Product_Category_3'].values
			x_train,x_test,y_train,y_test=train_test_split(x,y5,test_size=0.25)
			clf=LinearRegression()
			#print (clf)
			clf=clf.fit(x_train,y_train)
			yp3=clf.predict([[p1,a1,g1]])
			#yp3=yp3.tolist()
			#print ("predicted y")
			#print (yp3)
			
			answer_label1.configure(text="Product_Category_1")
			answer_label2.configure(text=yp1)
			answer_label3.configure(text="Product_Category_2")
			answer_label4.configure(text=yp2)
			answer_label5.configure(text="Product_Category_3")
			answer_label6.configure(text=yp3)
			status_label.configure(text="successfully completed")
		except:
			status_label.configure(text="invalid input")
	else:
			status_label.configure(text="fill in all the required fields")

calculate_button =Button(root,text="Predict",command= predicting)
calculate_button.grid(row =7,column=0,columnspan =2)

status_label=Label(root, height=5, width=25, bg="black", fg="#00FF00", text="---",wraplength=150)
status_label.grid(row=8, column=0, columnspan=2)
root.mainloop()


