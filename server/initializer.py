import pandas as pd
import pickle

data_path = './data/'
models_path = './models/'


def load_datasets():
    # read the data
    ev_history = pd.read_csv(data_path + 'ev_history.csv')
    ev_home_locations = pd.read_csv(data_path + 'ev_home_locations.csv')
    ev_models = pd.read_csv(data_path + 'ev_models.csv')
    grid_locations = pd.read_csv(data_path + 'grid_locations.csv')
    gridload = pd.read_csv(data_path + 'gridload.csv')
    public_chargers_locations = pd.read_csv(data_path + 'public_chargers_locations.csv')
    ev_history.drop(['Unnamed: 0'], axis=1, inplace=True)
    ev_home_locations.drop(['Unnamed: 0'], axis=1, inplace=True)
    ev_models.drop(['Unnamed: 0'], axis=1, inplace=True)
    grid_locations.drop(['Unnamed: 0'], axis=1, inplace=True)
    gridload.drop(['Unnamed: 0'], axis=1, inplace=True)
    public_chargers_locations.drop(['Unnamed: 0'], axis=1, inplace=True)

    return ev_history, ev_home_locations, ev_models, grid_locations, gridload, public_chargers_locations


def load_models():
    # read ML models
    grid_load_model = pickle.load(open(models_path + 'gridload_model.pickle', 'rb'))
    return grid_load_model


# an extract from colab
def prepare_gridload_dataset(grid_locations, gridload):
    grid_cadaster_tmp = []
    time_tmp = []
    coordinates = [[], []]
    for j, gc in grid_locations.iterrows():
        for i in range(1, 25):
            grid_cadaster_tmp.append(gc['cadaster'])
            time_tmp.append(i)
            coordinates[0].append(gc['latitude'])
            coordinates[1].append(gc['longitude'])

    dataset = pd.DataFrame()
    dataset['time'] = time_tmp
    dataset['latitude'] = coordinates[0]
    dataset['longitude'] = coordinates[1]
    dataset['grid_cadaster'] = grid_cadaster_tmp

    base_loads = []
    max_loads = []

    for i, row in dataset.iterrows():
        base = \
            gridload[(gridload['cadaster'] == row['grid_cadaster']) & (gridload['time'] == row['time'])][
                'baseload'].iloc[0]
        max_ = grid_locations[(grid_locations['cadaster'] == row['grid_cadaster'])]['max_current'].iloc[0]
        base_loads.append(base)
        max_loads.append(max_)

    dataset['base_load'] = base_loads
    dataset['max_load'] = max_loads
    return dataset
