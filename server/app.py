from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from initializer import prepare_gridload_dataset, load_datasets, load_models, \
    prepare_all_chargers_dataset, prepare_grid_chargers_dataset

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

ev_history, ev_home_locations, ev_models, grid_locations, gridload, public_chargers_locations = load_datasets()
grid_load_prediction_dataset = prepare_gridload_dataset(grid_locations, gridload)
all_chargers_dataset = prepare_all_chargers_dataset(public_chargers_locations, ev_home_locations, grid_locations)
grid_chargers_dataset = prepare_grid_chargers_dataset(grid_locations, all_chargers_dataset)

grid_load_predictor, car_model_predictor, soc_predictor, consumption_predictor = load_models()


# example: /api/gridload?time=24

@app.route('/api/gridload')
@cross_origin()
def grid_load():
    time = int(request.args.get("time"))
    res = []
    grids = grid_load_prediction_dataset[grid_load_prediction_dataset['time'] == time]

    for i, grid_data in grids.iterrows():
        prediction = \
        grid_load_predictor.predict([grid_data[['time', 'longitude', 'latitude', 'base_load', 'max_load']]])[0]
        is_overloaded = prediction > grid_data['max_load']

        res.append({'lat': grid_data['latitude'],
                    'lon': grid_data['longitude'],
                    'address': grid_data['address'],
                    'time': grid_data['time'],
                    'predictedLoad': round(prediction, 2),
                    'isOverloaded': str(is_overloaded),
                    'baseLoad': round(grid_data['base_load'], 2),
                    'maxLoad': round(grid_data['max_load'], 2),
                    'cadaster': grid_data['grid_cadaster']})

    return jsonify(res)

# example: /api/charging?time=15&cadaster=79514:037:0108&baseLoad=100&maxLoad=110

@app.route('/api/charging')
@cross_origin()
def smart_charging():
    time = int(request.args.get('time'))
    grid_cadaster = str(request.args.get('cadaster'))
    base_load = float(request.args.get('baseLoad'))
    max_load = float(request.args.get('maxLoad'))

    chargers = grid_chargers_dataset[grid_chargers_dataset['cadaster'] == grid_cadaster].iloc[0]['chargers']
    out = []

    for charger_cadaster in chargers:
        charger_data = all_chargers_dataset[all_chargers_dataset['cadaster'] == charger_cadaster] \
            .iloc[0][['cadaster', 'longitude', 'latitude', 'is_home_loc', 'address']]

        charger_data['time'] = time
        # predict car model
        predicted_car_model = car_model_predictor.predict([charger_data[['time', 'longitude', 'latitude', 'is_home_loc']]])[0]

        # then predict soc
        bat_size = ev_models.iloc[int(predicted_car_model)]['battery_size']
        charge_power = ev_models.iloc[predicted_car_model]['charge_power']
        charger_data['battery_size'] = bat_size
        charger_data['charge_power'] = charge_power
        predicted_soc = soc_predictor.predict([charger_data[['time', 'longitude', 'latitude', 'is_home_loc', 'battery_size', 'charge_power']]])[0]

        # then predict charge need
        charger_data['soc'] = predicted_soc
        # predicted_charge_need = consumption_predictor.predict([charger_data[['time', 'longitude', 'latitude', 'soc']]])[0]
        predicted_charge_need = min(charger_data['battery_size'] - charger_data['soc'], charger_data['charge_power'])

        # append all the data to the list
        out.append({
            'lon': charger_data['longitude'],
            'lat': charger_data['latitude'],
            'carModel': ev_models.iloc[predicted_car_model]['models'],  # the human name
            'chargeNeed': round(predicted_charge_need, 2),
            'optimizedCharge': round(predicted_charge_need, 2),
            'decreasePercent': 0,
            'address': charger_data['address'],
            'cadaster': charger_data['cadaster']
        })

    # get sum of all charge need predictions
    total = sum([entity['optimizedCharge'] for entity in out])
    decrease_rate = 0.1

    if base_load > max_load:
        for i, _ in enumerate(out):
            out[i]['optimizedCharge'] = 0
            out[i]['decreasePercent'] = 100
        return jsonify(out)

    while base_load + total > max_load:
        # decrease charge outputs by decrease rate
        for i, _ in enumerate(out):
            out[i]['optimizedCharge'] = round(out[i]['chargeNeed'] * (1.0 - decrease_rate), 2)
            out[i]['decreasePercent'] = decrease_rate * 100

        total = sum([entity['optimizedCharge'] for entity in out])
        decrease_rate += 0.1

    return jsonify(out)


@app.route('/api/modelcheck')
@cross_origin()
def check_models():
    return jsonify({
        'gridload': type(grid_load_predictor).__name__,
        'car_model': type(car_model_predictor).__name__,
        'soc': type(soc_predictor).__name__,
        'consumption': type(consumption_predictor).__name__
    })


if __name__ == '__main__':
    app.run()
