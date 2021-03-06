
# coding: utf-8

# In[1]:


from pandas import DataFrame
from pandas import Series
from pandas import concat
from pandas import read_csv
from pandas import datetime
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from math import sqrt
from matplotlib import pyplot
import numpy
import pandas as pd

# load dataset
def parser(x):
	return datetime.strptime('190'+x, '%Y-%m')

# frame a sequence as a supervised learning problem
def timeseries_to_supervised(data, lag=1):
	df = DataFrame(data)
	columns = [df.shift(i) for i in range(1, lag+1)]
	columns.append(df)
	df = concat(columns, axis=1)
	df.fillna(0, inplace=True)
	return df

# create a differenced series
def difference(dataset, interval=1):
	diff = list()
	for i in range(interval, len(dataset)):
		value = dataset[i] - dataset[i - interval]
		diff.append(value)
	return Series(diff)

# invert differenced value
def inverse_difference(history, yhat, interval=1):
	return yhat + history[-interval]

# scale train and test data to [-1, 1]
def scale(train, test):
	# fit scaler
	scaler = MinMaxScaler(feature_range=(-1, 1))
	scaler = scaler.fit(train)
	# transform train
	train = train.reshape(train.shape[0], train.shape[1])
	train_scaled = scaler.transform(train)
	# transform test
	test = test.reshape(test.shape[0], test.shape[1])
	test_scaled = scaler.transform(test)
	return scaler, train_scaled, test_scaled

# inverse scaling for a forecasted value
def invert_scale(scaler, X, value):
	new_row = [x for x in X] + [value]
	array = numpy.array(new_row)
	array = array.reshape(1, len(array))
	inverted = scaler.inverse_transform(array)
	return inverted[0, -1]

# fit an LSTM network to training data
def fit_lstm(train, batch_size, nb_epoch, neurons):
	X, y = train[:, 0:-1], train[:, -1]
	X = X.reshape(X.shape[0], 1, X.shape[1])
	model = Sequential()
	model.add(LSTM(neurons, batch_input_shape=(batch_size, X.shape[1], X.shape[2]), stateful=True))
	model.add(Dense(1))
	model.compile(loss='mean_squared_error', optimizer='adam')
	for i in range(nb_epoch):
		model.fit(X, y, epochs=1, batch_size=batch_size, verbose=0, shuffle=False)
		model.reset_states()
	return model

# make a one-step forecast
def forecast_lstm(model, batch_size, X):
	X = X.reshape(1, 1, len(X))
	yhat = model.predict(X, batch_size=batch_size)
	return yhat[0,0]


# In[11]:


f = open( 'score_result.txt', 'w' )
f.write('epoch|neuron|rmse \n' )
f.close()


# In[4]:


print('hello1')


# fit_lstm(train_scaled, batch_size=1, nb_epoch=500, neurons=4)  Test RMSE: 162.512916 <br>
# fit_lstm(train_scaled, batch_size=1, nb_epoch=1000, neurons=4) Test RMSE: 153.572175 <br>
# fit_lstm(train_scaled, batch_size=1, nb_epoch=1500, neurons=4) Test RMSE: 187.092256 <br>
# fit_lstm(train_scaled, batch_size=1, nb_epoch=2000, neurons=4) Test RMSE: 141.697755 <br>
# fit_lstm(train_scaled, batch_size=1, nb_epoch=2500, neurons=4) Test RMSE: 197.744168 <br>
# fit_lstm(train_scaled, batch_size=1, nb_epoch=3000, neurons=4) Test RMSE: 155.637825 <br>
# <br>
# fit_lstm(train_scaled, batch_size=1, nb_epoch=500, neurons=6) Test RMSE:  153.067551 <br>
# fit_lstm(train_scaled, batch_size=1, nb_epoch=1000, neurons=6) Test RMSE: 129.917576 <br>
# fit_lstm(train_scaled, batch_size=1, nb_epoch=1500, neurons=6) Test RMSE: 148.941757 <br>
# fit_lstm(train_scaled, batch_size=1, nb_epoch=2000, neurons=6) Test RMSE: 155.630252 <br>
# fit_lstm(train_scaled, batch_size=1, nb_epoch=2500, neurons=6) Test RMSE:  <br>
# fit_lstm(train_scaled, batch_size=1, nb_epoch=3000, neurons=6) Test RMSE:  <br>

# In[2]:


series = read_csv('shampoo-sales.csv', header=0, parse_dates=[0], index_col=0, squeeze=True, date_parser=parser)
# transform data to be stationary
raw_values = series.values
diff_values = difference(raw_values, 1)

# transform data to be supervised learning
supervised = timeseries_to_supervised(diff_values, 1)
supervised_values = supervised.values

# split data into train and test-sets
train, test = supervised_values[0:-12], supervised_values[-12:]

# transform the scale of the data
scaler, train_scaled, test_scaled = scale(train, test)

#nb_epoch_range=range(100,1100,100)
nb_epoch_range=[700]
neuron_range=range(1,11)
for i1 in nb_epoch_range:
    for i2 in neuron_range:
        # repeat experiment
        repeats = 10
        error_scores = []
        for r in range(repeats):
            # fit the model
            lstm_model = fit_lstm(train_scaled, 1, i1, i2)
            # forecast the entire training dataset to build up state for forecasting
            train_reshaped = train_scaled[:, 0].reshape(len(train_scaled), 1, 1)
            lstm_model.predict(train_reshaped, batch_size=1)
            # walk-forward validation on the test data
            predictions = list()
            for i in range(len(test_scaled)):
                # make one-step forecast
                X, y = test_scaled[i, 0:-1], test_scaled[i, -1]
                yhat = forecast_lstm(lstm_model, 1, X)
                # invert scaling
                yhat = invert_scale(scaler, X, yhat)
                # invert differencing
                yhat = inverse_difference(raw_values, yhat, len(test_scaled)+1-i)
                # store forecast
                predictions.append(yhat)
            # report performance
            rmse = sqrt(mean_squared_error(raw_values[-12:], predictions))
            #print('%d) Test RMSE: %.3f' % (r+1, rmse))
            #error_scores.append([rmse])
 
            f = open( 'score_result.txt', 'a' )
            f.write(str(i1)+'|'+str(i2)+'|'+str(rmse)+'\n' )
            f.close()

print("done")
# summarize results
#results = DataFrame()
#results['rmse'] = error_scores
#mean=results.mean()
#print(results.describe())
#results.boxplot()
#pyplot.show()


# In[1]:


import pandas as pd

#DataFrame.pivot_table(values=None, index=None, columns=None, aggfunc='mean',fill_value=None, margins=False, dropna=True)

df = pd.read_csv('score_result.txt',  sep='|')
df.pivot_table(index='epoch',columns='neuron',aggfunc=('count','mean'))


# In[2]:


get_ipython().magic('matplotlib inline')
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()  # use seaborn styles

df.pivot_table(index='epoch',columns='neuron',aggfunc=('mean')).plot()
plt.ylabel('rmse');


# ### Conclusion:
# - the increase in epoch doesn't lower the rmse

# In[3]:


get_ipython().magic('matplotlib inline')
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()  # use seaborn styles

df.pivot_table(index='neuron',columns='epoch',aggfunc=('mean')).plot()
plt.ylabel('rmse');


# ### Conclusion:
# - The increase in neuron does decrease rmse for epoch =100
# - The increase in neuron does not decrease rmse for epoch >=200
