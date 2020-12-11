from flask import Flask, request, jsonify
from initializer import prepare_gridload_dataset, load_datasets, load_models

app = Flask(__name__)

ev_history, ev_home_locations, ev_models, grid_locations, gridload, public_chargers_locations = load_datasets()
grid_load_prediction_dataset = prepare_gridload_dataset(grid_locations, gridload)

grid_load_rf_model = load_models()


# link/api/gridload?time=24

@app.route('/api/gridload')
def grid_load():
    time = int(request.args.get("time"))
    res = []
    grids = grid_load_prediction_dataset[grid_load_prediction_dataset['time'] == time]

    for i, grid_data in grids.iterrows():
        prediction = grid_load_rf_model.predict([grid_data[['time', 'longitude', 'latitude', 'base_load', 'max_load']]])[0]
        is_overloaded = prediction > grid_data['max_load']

        res.append({'lat': grid_data['latitude'],
                    'lon': grid_data['longitude'],
                    'time': grid_data['time'],
                    'predictedLoad': prediction,
                    'isOverloaded': str(is_overloaded),
                    'baseLoad': grid_data['base_load'],
                    'maxLoad': grid_data['max_load'],
                    'cadaster': grid_data['grid_cadaster']})

    return jsonify(res)


@app.route('/api/charging')
def smart_charging():
    return 'TODO'


if __name__ == '__main__':
    app.run()
