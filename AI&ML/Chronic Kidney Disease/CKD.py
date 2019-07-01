
# coding: utf-8

# In[28]:



import types
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from botocore.client import Config
import ibm_boto3

def __iter__(self): return 0

# @hidden_cell
# The following code accesses a file in your IBM Cloud Object Storage. It includes your credentials.
# You might want to remove those credentials before you share your notebook.
client_615887cdf63b4d15b786ad57f6e840c4 = ibm_boto3.client(service_name='s3',
    ibm_api_key_id='CmnyNTkkpkHcFgY-ulSHs668HeXFbRKD4Y6t-pewTL1D',
    ibm_auth_endpoint="https://iam.bluemix.net/oidc/token",
    config=Config(signature_version='oauth'),
    endpoint_url='https://s3-api.us-geo.objectstorage.service.networklayer.com')

body = client_615887cdf63b4d15b786ad57f6e840c4.get_object(Bucket='projectckd-donotdelete-pr-hhtv0x7kcgph0l',Key='ckd.csv')['Body']
# add missing __iter__ method, so pandas accepts body as file-like object
if not hasattr(body, "__iter__"): body.__iter__ = types.MethodType( __iter__, body )

data = pd.read_csv(body)
data.head()
print (data)


# In[22]:


print("Size of data is:",data.shape)
data.columns


# In[23]:


data.head()


# In[24]:


data.describe(include=['object'])


# In[25]:


print("pcv value counts:\n",data['pcv'].value_counts())
print("rc value counts:\n",data['rc'].value_counts())
print("wc value counts:\n",data['wc'].value_counts())


# In[29]:


data['pcv']=data['pcv'].replace('\t?',np.nan)
data['pcv']=data['pcv'].replace('\t43',43)
data['wc']=data['wc'].replace('\t8400',8400)
data['wc']=data['wc'].replace('\t6200',6200)
data['wc']=data['wc'].replace('\t?',np.nan)
data['rc']=data['rc'].replace('\t?',np.nan)


# In[30]:


print(data['pcv'].dtype)
print(data['wc'].dtype)
print(data['rc'].dtype)


# In[31]:


for x in data['pcv']:
    if type(x)!=float:
        data['pcv']=data['pcv'].replace(x,int(x))
for x in data['wc']:
    if type(x)!=float:
        data['wc']=data['wc'].replace(x,int(x))
for x in data['rc']:
    if type(x)!=float:
        data['rc']=data['rc'].replace(x,float(x))


# In[33]:


sns.heatmap(data.isnull(),cmap='plasma')


# In[34]:


data.isnull().sum()


# In[35]:


print("rbc:\n",data['rbc'].value_counts())
print('pc:\n',data['pc'].value_counts())
print('pcc:\n',data['pcc'].value_counts())
print('ba:\n',data['ba'].value_counts())
print('htn:\n',data['htn'].value_counts())
print('dm:\n',data['dm'].value_counts())
print('cad:\n',data['cad'].value_counts())
print('appet:\n',data['appet'].value_counts())
print('pe:\n',data['pe'].value_counts())
print('ane:\n',data['ane'].value_counts())


# In[36]:


data['rbc'].fillna('normal',inplace=True)
data['pc'].fillna('normal',inplace=True)
data['pcc'].fillna('notpresent',inplace=True)
data['ba'].fillna('notpresent',inplace=True)
data['htn'].fillna('no',inplace=True)
data['dm'].fillna('no',inplace=True)
data['cad'].fillna('no',inplace=True)
data['appet'].fillna('good',inplace=True)
data['pe'].fillna('no',inplace=True)
data['ane'].fillna('no',inplace=True)


# In[37]:


data.fillna(data.mean(),inplace=True)
data.isnull().sum()


# In[38]:


sns.heatmap(data.isnull(),cmap='plasma')


# In[44]:


data.head()


# In[46]:


sns.set_style('whitegrid')
plt.subplots(figsize=(10,7))
sns.countplot(x='classification',hue='sg',data=data,color='green',edgecolor=sns.color_palette("dark", 3))


# In[47]:


data.plot(kind='scatter',x='rc',y='classification',figsize=(10,7))


# In[48]:


data.plot(kind='scatter',x='hemo',y='classification',figsize=(10,7))


# In[49]:


data.plot(kind='scatter',x='classification',y='su',figsize=(10,7))


# In[50]:


data.corr()


# In[82]:


plt.subplots(figsize=(10,10))
sns.heatmap(data.corr(),linewidths=0.6)


# In[52]:


datan=data.drop(columns=['age'])
datan.head()


# In[53]:


ar=datan.values
x=ar[:,0:23]
y=ar[:,23]


# In[60]:


#Logistic Regression
from sklearn.model_selection import train_test_split
X_train,X_test,Y_train,Y_test=train_test_split(x,y,test_size=0.3,random_state=1)


# In[61]:


from sklearn.linear_model import LogisticRegression
lr=LogisticRegression()
lr.fit(X_train,Y_train)
prediction=lr.predict(X_test)
from sklearn.metrics import accuracy_score
np.set_printoptions(precision=3)
accuracy_score(Y_test,prediction)


# In[62]:


from sklearn.metrics import confusion_matrix
confusion_matrix(Y_test,prediction)


# In[63]:


#Naive Bayes
from sklearn.naive_bayes import GaussianNB 
gnb = GaussianNB() 
gnb.fit(X_train, Y_train) 
NY_predict=gnb.predict(X_test)
accuracy_score(Y_test,NY_predict)


# In[75]:


#KNN
from sklearn.neighbors import KNeighborsClassifier
seed = 7
kfold = model_selection.KFold(n_splits=101, random_state=seed)
model = KNeighborsClassifier()
results = model_selection.cross_val_score(model,x,y, cv=kfold)
print(results.mean())

