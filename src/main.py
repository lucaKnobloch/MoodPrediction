from math import sqrt
from numpy import concatenate
from matplotlib import pyplot
from pandas import read_csv
from pandas import DataFrame
from pandas import concat
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM


# convert series to supervised learning
def series_to_supervised(data, dropnan=True):
    n_vars = 1 if type(data) is list else data.shape[1]
    cols, names, indexes = list(), list(), list()
    df = DataFrame(data)

    counter = 0
    for entry in data:
        if entry[n_vars-1] > 0 and counter > 600:
            cols.append(df.loc[:][:counter - 1])
            indexes.append(entry[n_vars-1])
        counter += 1

    cols.append(DataFrame(indexes))
    # put it all together
    agg = concat(cols, axis=1)
    # drop rows with NaN values
    if dropnan:
        agg.dropna(inplace=True)
    return agg


# load dataset
dataset = read_csv('resources_hours/u59.csv', delimiter=';', header=0, index_col=0)
values = dataset.values
# ensure all data is float
values = values.astype('float32')
# normalize features
scaler = MinMaxScaler(feature_range=(0, 1))
scaled = scaler.fit_transform(values)
# specify the number of lag hours
n_hours = 118
n_features = 16
# frame as supervised learning
reframed = series_to_supervised(scaled)
print(reframed.shape)

# split into train and test sets
values = reframed.values
n_train = 100
train = values[:n_train, :]
test = values[n_train:, :]
n_observations = n_hours * n_features

# split into input and outputs
train_X, train_y = train[:, :-1], train[:,-1:]
test_X, test_y = test[:, :-1], test[:,-1:]
print(train_X.shape, len(train_X), train_y.shape)
# reshape input to be 3D [samples, timesteps, features]
train_X = train_X.reshape((train_X.shape[0], n_hours, n_features))
test_X = test_X.reshape((test_X.shape[0], n_hours, n_features))
print(train_X.shape, train_y.shape, test_X.shape, test_y.shape)

# design network
model = Sequential()
model.add(LSTM(100, input_shape=(train_X.shape[1], train_X.shape[2])))
model.add(Dense(1, activation='relu'))
model.compile(loss='mae', optimizer='adam')
# fit network
history = model.fit(train_X, train_y, epochs=50, validation_data=(test_X, test_y), verbose=2,
                    shuffle=False)

# plot history
pyplot.plot(history.history['loss'], label='train')
pyplot.plot(history.history['val_loss'], label='test')
pyplot.legend()
pyplot.show()
