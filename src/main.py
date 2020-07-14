from keras.layers import Dense
from keras.layers import LSTM
from keras.models import Sequential
from matplotlib import pyplot
from pandas import DataFrame
from pandas import concat
from pandas import read_csv
from sklearn.model_selection import cross_val_score, KFold
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder

# convert series to supervised learning
from tensorflow.python.keras.wrappers.scikit_learn import KerasRegressor


def series_to_supervised(data, dropnan=True):
    n_vars = 1 if type(data) is list else data.shape[1]
    cols, names, indexes = list(), list(), list()
    df = DataFrame(data)

    counter = 0
    for entry in data:
        if entry[n_vars - 1] > 0 and counter > 600:
            cols.append(df.loc[:][:counter - 1])
            indexes.append(entry[n_vars - 1])
        counter += 1

    cols.append(DataFrame(indexes))
    # put it all together
    agg = concat(cols, axis=1)
    # drop rows with NaN values
    if dropnan:
        agg.dropna(inplace=True)
    return agg


# Hyperparamter
batch_size = 1
amount_of_epochs = 50
lstm_units = 8
# 1000 epochs [-0.26869208 -0.40000001 -0.07393112 -0.05755799 -0.23714375 -0.33280233]
# 100 epochs [-0.29874116 -0.29221344 -0.04607497 -0.17346033 -0.24597952]
cross_validation = False
plot = True
one_hot_encoding = False
# specify the number of lag hours
n_hours = 118
n_features = 16
n_train = 90
k_folds = 5 

# load dataset
dataset = read_csv('resources_hours/u59.csv', delimiter=';', header=0, index_col=0)
values = dataset.values
# ensure all data is float
values = values.astype('float32')
# normalize features
scaler = MinMaxScaler(feature_range=(0, 1))
scaled = scaler.fit_transform(values)
# frame as supervised learning
reframed = series_to_supervised(scaled)
print(reframed.shape)

# split into train and test sets
values = reframed.values
train = values[:n_train, :]
test = values[n_train:, :]
n_observations = n_hours * n_features

# split into input and outputs
train_X, train_y = train[:, :-1], train[:, -1:]
test_X, test_y = test[:, :-1], test[:, -1:]

if one_hot_encoding:
    # one hot encoding for the output label
    # encode class values as integers
    onehotencoder = OneHotEncoder()
    train_y = onehotencoder.fit_transform(train_y).toarray()
    test_y = onehotencoder.fit_transform(test_y).toarray()

print(train_X.shape, len(train_X), train_y.shape)

# reshape input to be 3D [samples, timesteps, features]
train_X = train_X.reshape((train_X.shape[0], n_hours, n_features))
test_X = test_X.reshape((test_X.shape[0], n_hours, n_features))
print(train_X.shape, train_y.shape, test_X.shape, test_y.shape)


def buildmodel():
    # design network
    model = Sequential()
    model.add(LSTM(lstm_units, input_shape=(train_X.shape[1], train_X.shape[2])))
    model.add(Dense(1, activation='relu'))
    model.compile(loss='mae', optimizer='adam')
    return model


buildmodel().summary()

estimator = KerasRegressor(build_fn=buildmodel, epochs=amount_of_epochs, batch_size=batch_size, verbose=2)

if cross_validation:
    # evaluation
    # initialize the cross validation folds api
    kfold = KFold(k_folds)
    results = cross_val_score(estimator, test_X, test_y, cv=kfold)
    print(results)

if plot:
    # fit network
    history = buildmodel().fit(train_X, train_y, batch_size=batch_size, epochs=amount_of_epochs,
                               validation_data=(test_X, test_y),
                               verbose=2,
                               shuffle=False)

    # plot history
    pyplot.plot(history.history['loss'], label='train')
    pyplot.plot(history.history['val_loss'], label='test')

    pyplot.xlabel('''Amount of epochs
    
    Trained with a batch size of ''' + str(batch_size) + ''', amount of epochs ''' + str(amount_of_epochs) + ''', lstm 
    units ''' + str(lstm_units) + ''' and an validation loss of ''' + str(
        "{0:.3f}".format(history.history['val_loss'][amount_of_epochs - 1])))
    pyplot.ylabel('Loss')
    pyplot.legend()
    pyplot.show()
