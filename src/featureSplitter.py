import pandas

if __name__ == "__main__":
    file = pandas.read_csv('resources_hours/u59.csv', delimiter=';')
    samples = file.query('mood > 0').get('date').index.values

    count = 0
    for sample in samples:
        file = pandas.read_csv('resources_hours/u59.csv', delimiter=';', nrows=sample)
        file.to_csv('train/train_' + str(count) + '.csv', index=False)
        print('train_' + str(count) + '.csv')
        count += 1
