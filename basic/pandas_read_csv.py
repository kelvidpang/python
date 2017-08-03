
# coding: utf-8

# In[4]:


import pandas as pd
import numpy as np
import os

#index_col=0 means not to use column header
#header=0 means no header
#squeeze=True translate the column into Series if only one column


# In[ ]:


#common checking on df
df.head(n=10)
df.index
df.ndim
df.dtypes
df.shape
df.columns
len(df)
cols = df.columns.tolist()
len(cols) #number of columns
df.iloc[0] #first record
df.describe()


# In[7]:


raw_data = {'first_name': ['Jason', 'Molly', 'Tina', 'Jake', 'Amy'],
        'last_name': ['Miller', 'Jacobson', ".", 'Milner', 'Cooze'],
        'age': [42, 52, 36, 24, 73],
        'preTestScore': [4, 24, 31, ".", "."],
        'postTestScore': ["25,000", "94,000", 57, 62, 70]}
df = pd.DataFrame(raw_data, columns = ['first_name', 'last_name', 'age', 'preTestScore', 'postTestScore'])
df


# ### Save dataframe as csv in the working director

# In[9]:


df.to_csv('./example.csv')


# ### Load a csv

# In[10]:


df = pd.read_csv('./example.csv')
df


# ### Load a csv with no headers

# In[11]:


df = pd.read_csv('./example.csv', header=None)
df


# ### Load a csv while specifying column names

# In[12]:


df = pd.read_csv('./example.csv', names=['UID', 'First Name', 'Last Name', 'Age', 'Pre-Test Score', 'Post-Test Score'])
df


# ### Load a csv with setting the index column to UID

# In[14]:


df = pd.read_csv('./example.csv', index_col='UID', names=['UID', 'First Name', 'Last Name', 'Age', 'Pre-Test Score', 'Post-Test Score'])
df


# ### Load a csv while setting the index columns to First Name and Last Name

# In[15]:


df = pd.read_csv('./example.csv', index_col=['First Name', 'Last Name'], names=['UID', 'First Name', 'Last Name', 'Age', 'Pre-Test Score', 'Post-Test Score'])
df


# ### Load a csv while specifying "." and "NA" as missing values in the Last Name column and "." as missing values in Pre-Test Score column

# In[3]:


sentinels = {'last_name': ['.', 'NA'], 'preTestScore': ['.']}


# In[4]:


df = pd.read_csv('./example.csv', na_values=sentinels)
pd.isnull(df)


# ### Convert Non Standard Date to date format

# In[6]:


import datetime as dt
import pandas as pd
import io

#change date format in pandas
def parser(x):
	return pd.datetime.strptime('190'+x, '%Y-%m')

output = io.StringIO()
output.write('x\n')
output.write('1-01\n')
output.seek(0)
df = pd.read_csv(output, header=0,  index_col=0,  parse_dates=[0], date_parser=parser)

df


# In[20]:


import datetime as dt
import pandas as pd
import io

#change date format in pandas
def parser(x):
	return pd.datetime.strptime(x, '%d%b%Y')

del output
output = io.StringIO()
output.write('x\n')
output.write('30MAR1990\n')
output.write('28FEB1990\n')
output.seek(0)
df = pd.read_csv(output, header=0,  index_col=0,  parse_dates=[0], date_parser=parser)

df


# ### Times Series - Rolling Windows (Decrease months)

# In[31]:


import datetime as dt
import pandas as pd
import io

#change date format in pandas
def parser(x):
	return pd.datetime.strptime(x, '%d%b%Y')

del output
output = io.StringIO()
output.write('x\n')
output.write('30MAR1990\n')
output.write('28FEB1990\n')
output.seek(0)
df = pd.read_csv(output, header=0,  index_col=0,  parse_dates=[0], date_parser=parser)


from datetime import datetime  
import pandas as pd

def decrease_month(date, n):
    assert(n <= 12)

    new_month = date.month - n
    year_offset = 0
    if new_month <= 0:
        year_offset = -1
        new_month = 12 + new_month

    return datetime(date.year + year_offset, new_month, 1)

rolling_period=5
for n in range(rolling_period):
    df['m_' + str(n)] = df.index.map(lambda x: decrease_month(x, n))
    
df


# ### Times Series - Rolling Windows (Increase months)

# In[36]:


import datetime as dt
import pandas as pd
import io

#change date format in pandas
def parser(x):
	return pd.datetime.strptime(x, '%d%b%Y')

del output
output = io.StringIO()
output.write('x\n')
output.write('30Sep1990\n')
output.write('28oct1990\n')
output.seek(0)
df = pd.read_csv(output, header=0,  index_col=0,  parse_dates=[0], date_parser=parser)


from datetime import datetime  
import pandas as pd

def increase_month(date, n):
    assert(n <= 12)

    new_month = date.month + n
    year_offset = 0
    if new_month >= 13:
        year_offset = +1
        new_month = new_month - 12

    return datetime(date.year + year_offset, new_month, 1)

rolling_period=5
for n in range(rolling_period):
    df['m_' + str(n)] = df.index.map(lambda x: increase_month(x, n))
    
df


# In[55]:


import numpy as np
import pandas as pd
from IPython.display import display

# let's create some fake data
date_range = pd.date_range('2005-01-01', '2008-12-31', freq='9min')
l = len(date_range)
df = pd.DataFrame({'normal': np.random.randn(l), 'uniform':np.random.rand(l), 
    'datetime':date_range, 'integer':range(l)}, index=date_range)

display(df.head(n=5))

# let's identify the periods we want
desired = [('2005-10-27 14:30','2005-10-27 15:15'), 
           ('2006-04-14 14:40','2006-04-14 15:20'), 
           ('2008-01-25 14:30','2008-01-25 15:30')]

# let's loop through the desired ranges and compile our selection           
x = pd.DataFrame()
for (start, stop) in desired:
    selection = df[(df.index >= pd.Timestamp(start)) & 
        (df.index <= pd.Timestamp(stop))]
    x = x.append(selection)

# and let's have a look at what we found ...
display(print(x))


# ### Create blank dataframe

# In[5]:


columns = ['product', 'item']
df=pd.DataFrame(data=np.zeros((0,len(columns))), columns=columns)
df


# ### Insert into dataframe

# In[6]:


for i in [50,100,200]:
    for j in ['a','b',6]:
        df = df.append({'product':i, 'item':j},ignore_index=True)

df.head()


# ### Create dataframe with 2 index

# In[14]:


a=range(5)
b=range(5)
df=pd.DataFrame({'col1':a,'col2':b})
df

