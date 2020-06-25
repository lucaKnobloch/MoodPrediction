import numpy as np
import pandas as pd
from keras import Sequential
from keras.layers import Dense
from keras.utils import np_utils
from keras.wrappers.scikit_learn import KerasClassifier
from sklearn.model_selection import KFold, cross_val_score
from sklearn.preprocessing import LabelEncoder


def handle_non_numerical_data(df):
    columns = df.columns.values
    for column in columns:
        text_digit_vals = {}

        def convert_to_int(val):
            return text_digit_vals[val]

        if df[column].dtype != np.int64 and df[column].dtype != np.float64:
            column_contents = df[column].values.tolist()
            unique_elements = set(column_contents)
            x = 0
            for unique in unique_elements:
                if unique not in text_digit_vals:
                    text_digit_vals[unique] = x
                    x += 1

            df[column] = list(map(convert_to_int, df[column]))

    return df


dataframe = pd.read_csv('resources_hours/u45.csv', delimiter=';', header=0)
df = handle_non_numerical_data(dataframe)

dataset = dataframe.values

# extract the label
X_data = dataset[:, 0:16]
Y_data = dataset[:, 16]

# prints current state of the data
print(X_data)
print(Y_data)

# encode class values as integers
encoder = LabelEncoder()
encoder.fit(Y_data)
encoded_Y = encoder.transform(Y_data)

# convert integers to dummy variables (i.e. one hot encoded)
dummy_y = np_utils.to_categorical(encoded_Y)
output_dim = dummy_y.shape[1]
input_dim = X_data.shape[1]

# Hyperparameter
hidden_units = 150
epochs = 200
batch_size = 2

# # define baseline model
def baseline_model():
    # create model
    model = Sequential()
    model.add(Dense(hidden_units, input_dim=input_dim, activation='relu'))
    model.add(Dense(output_dim, activation='softmax'))
    # Compile model
    model.compile(loss='mae', optimizer='adam', metrics=['accuracy'])
    return model


# Verbose = 0 silent fitting
# Verbose = 1 represented in a progress bar
# Verbose = 2 shows one line per epoch

estimator = KerasClassifier(build_fn=baseline_model, epochs=epochs, batch_size=batch_size, verbose=2)
# evaluation
kfold = KFold(n_splits=10, shuffle=True)

results = cross_val_score(estimator, X_data, dummy_y, cv=kfold)
print("Baseline: %.2f%% (%.2f%%)" % (results.mean() * 100, results.std() * 100))
