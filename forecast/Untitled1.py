
# coding: utf-8

# In[47]:


import pandas as pd

df = pd.read_csv('score_result.txt',  sep='|')
df.pivot_table(index='epoch',columns='neuron',aggfunc=('count','mean'))

