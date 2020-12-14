import pandas as pd
import joblib
import numpy as np

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
    grid_load_predictor = joblib.load(models_path + 'grid_load_predictor.sav')
    car_model_predictor = joblib.load(models_path + 'car_model_predictor.sav')
    soc_predictor = joblib.load(models_path + 'soc_predictor.sav')
    consumption_predictor = joblib.load(models_path + 'consumption_predictor.sav')

    return grid_load_predictor, car_model_predictor, soc_predictor, consumption_predictor


# an extract from colab
def prepare_gridload_dataset(grid_locations, gridload):
    grid_cadaster_tmp = []
    time_tmp = []
    coordinates = [[], []]
    address_tmp = []
    for j, gc in grid_locations.iterrows():
        for i in range(1, 25):
            grid_cadaster_tmp.append(gc['cadaster'])
            time_tmp.append(i)
            coordinates[0].append(gc['latitude'])
            coordinates[1].append(gc['longitude'])
            address_tmp.append(gc['address'])

    dataset = pd.DataFrame()
    dataset['time'] = time_tmp
    dataset['address'] = address_tmp
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


def prepare_all_chargers_dataset(public_chargers, home_chargers, grid_locations):
    all_charger_locations = pd.concat([home_chargers, public_chargers], axis=0).drop(["x", "y"], axis=1)
    all_charger_locations['is_home_loc'] = all_charger_locations.cadaster.isin(home_chargers.cadaster).astype(int)
    grid_cadasters = []
    for _, charger in all_charger_locations.iterrows():
        all_distances = [haversine_np(charger['longitude'], charger['latitude'], grid['longitude'], grid['latitude'])
                         for _, grid in grid_locations.iterrows()]
        grid_idx = np.argmin(all_distances)
        grid_cadasters.append(grid_locations.iloc[grid_idx][['cadaster', 'longitude', 'latitude']])

    all_charger_locations[['closest_grid', 'grid_longitude', 'grid_latitude']] = grid_cadasters

    return all_charger_locations


def haversine_np(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = np.sin(dlat / 2.0) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2.0) ** 2
    c = 2 * np.arcsin(np.sqrt(a))
    km = 6367 * c
    return km


def prepare_grid_chargers_dataset(grid_locations, all_charger_locations):
    gc_dataset = grid_locations.copy()
    gc_dataset.drop(['address', 'latitude', 'longitude', 'x', 'y', 'max_current'], axis=1, inplace=True)
    chargers = []

    for i, row in gc_dataset.iterrows():
        grid_chargers = all_charger_locations[all_charger_locations['closest_grid'] == row['cadaster']]
        # basically all pairs of charger cadaster/charge need for this grid at this time
        out = [charger['cadaster'] for _, charger in grid_chargers.iterrows()]
        chargers.append(out)

    gc_dataset['chargers'] = chargers

    return gc_dataset
