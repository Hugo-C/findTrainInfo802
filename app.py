import dateutil
from flask import Flask, jsonify, request
from flask_cors import CORS

# configuration
from server import trains
from server.trains import get_journey_price

DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app)


# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pingFLASK!')


@app.route('/', methods=['GET'])
def not_found():
    return jsonify('notFound!')


@app.route('/Trains', methods=['GET'])
def find_train():
    from_city = request.args.get('fromCity')
    to_city = request.args.get('toCity')
    raw_datetime = request.args.get('datetime')
    print(raw_datetime)
    date_wanted = dateutil.parser.parse(raw_datetime)
    print(date_wanted)
    # date_wanted = datetime.datetime.now()
    # print(date_wanted)
    timetable = trains.get_trains(from_city, to_city, date_wanted)
    print(timetable)
    journeys = []
    for journey in timetable["journeys"]:
        departure_date = dateutil.parser.parse(journey['departure_date_time'])
        arrival_date = dateutil.parser.parse(journey['arrival_date_time'])
        journeys.append({"duration": journey['duration'],
                         "departure_date": departure_date.isoformat(),
                         "arrival_date": arrival_date.isoformat()})
    res = {"status": "success",
           "fromCity": from_city,
           "toCity": to_city,
           "journeys": journeys,
           "price": get_journey_price(from_city, to_city)}
    print(res)
    print(f"number of hits : {len(journeys)}")
    res = jsonify(res)
    return res


if __name__ == '__main__':
    app.run()
