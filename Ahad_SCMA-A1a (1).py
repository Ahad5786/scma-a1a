#!/usr/bin/env python
# coding: utf-8

# In[14]:


import os, pandas as pd, numpy as np


# In[15]:


os.chdir("C:\\Users\\Ahad\\OneDrive\\Pictures\\Documents\\Desktop\\scma")


# In[16]:


df=pd.read_csv("NSSO68.csv",encoding="Latin-1", low_memory=False)


# In[17]:


df.head()


# In[18]:


CHTSD = df[df['state']==22]


# In[19]:


CHTSD.isnull().sum().sort_values(ascending = False)


# In[20]:


df.columns


# In[21]:


CHTSD_new = CHTSD[['state_1', 'District', 'Sector','Region','State_Region','ricetotal_q','wheattotal_q','moong_q','Milktotal_q','chicken_q','bread_q','foodtotal_q','Beveragestotal_v','Meals_At_Home']]


# In[22]:


CHTSD_new.isnull().sum().sort_values(ascending = False)


# In[23]:


CHTSD_clean = CHTSD_new.copy()


# In[24]:


CHTSD_clean.loc[:, 'Meals_At_Home'] = CHTSD_clean['Meals_At_Home'].fillna(CHTSD_new['Meals_At_Home'].mean())


# In[25]:


CHTSD_clean.isnull().any()


# In[26]:


# Outlier Checking


# In[27]:


import matplotlib.pyplot as plt
# Assuming CHTSD_clean is your DataFrame
plt.figure(figsize=(8, 6))
plt.boxplot(CHTSD_clean['ricetotal_q'])
plt.xlabel('ricetotal_q')
plt.ylabel('Values')
plt.title('Boxplot of ricetotal_q')
plt.show()


# In[28]:


rice1 = AP_clean['ricetotal_q'].quantile(0.25)
rice2 = AP_clean['ricetotal_q'].quantile(0.75)
iqr_rice = rice2-rice1
up_limit = rice2 + 1.5*iqr_rice
low_limit = rice1 - 1.5*iqr_rice


# In[ ]:


AP_clean=AP_new[(AP_new['ricetotal_q']<=up_limit)&(AP_new['ricetotal_q']>=low_limit)]


# In[ ]:


plt.boxplot(AP_clean['ricetotal_q'])


# In[29]:


CHTSD_clean['District'].unique()


# In[30]:


# Replace values in the 'Sector' column
CHTSD_clean.loc[:,'Sector'] = CHTSD_clean['Sector'].replace([1, 2], ['URBAN', 'RURAL'])


# In[31]:


#total consumption


# In[32]:


CHTSD_clean.columns


# In[33]:


CHTSD_clean.loc[:, 'total_consumption'] = CHTSD_clean[['ricetotal_q', 'wheattotal_q', 'moong_q', 'Milktotal_q', 'chicken_q', 'bread_q', 'foodtotal_q', 'Beveragestotal_v']].sum(axis=1)


# In[34]:


CHTSD_clean.head()


# In[35]:


CHTSD_clean.groupby('Region').agg({'total_consumption':['std','mean','max','min']})


# In[36]:


CHTSD_clean.groupby('District').agg({'total_consumption':['std','mean','max','min']})


# In[37]:


total_consumption_by_districtcode=CHTSD_clean.groupby('District')['total_consumption'].sum()


# In[38]:


total_consumption_by_districtcode.sort_values(ascending=False).head(3)


# In[39]:


CHTSD_clean.loc[:,"District"] = CHTSD_clean.loc[:,"District"].replace({11: "Raipur", 10: "Durg", 7: "Bilaspur"})


# In[40]:


total_consumption_by_districtname=CHTSD_clean.groupby('District')['total_consumption'].sum()


# In[41]:


total_consumption_by_districtname.sort_values(ascending=False).head(3)


# In[42]:


from statsmodels.stats import weightstats as stests


# In[43]:


rural=CHTSD_clean[CHTSD_clean['Sector']=="RURAL"]
urban=CHTSD_clean[CHTSD_clean['Sector']=="URBAN"]


# In[44]:


rural.head()


# In[45]:


urban.head()


# In[46]:


cons_rural=rural['total_consumption']
cons_urban=urban['total_consumption']


# In[47]:


z_statistic, p_value = stests.ztest(cons_rural, cons_urban)
# Print the z-score and p-value
print("Z-Score:", z_statistic)
print("P-Value:", p_value)


# In[ ]:





# In[ ]:




