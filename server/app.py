import dateutil
from flask import Flask, jsonify, request
from flask_cors import CORS

# configuration
from server import trains

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


BOOKS = [
    {
        'title': 'On the Road',
        'author': 'Jack Kerouac',
        'read': True
    },
    {
        'title': 'Harry Potter and the Philosopher\'s Stone',
        'author': 'J. K. Rowling',
        'read': False
    },
    {
        'title': 'Green Eggs and Ham',
        'author': 'Dr. Seuss',
        'read': True
    }
]


@app.route('/books', methods=['GET', 'POST'])
def all_books():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        print(request.get_json())
        BOOKS.append({
            'title': post_data.get('title'),
            'author': post_data.get('author'),
            'read': post_data.get('read')
        })
        response_object['message'] = 'Book added!'
    else:
        response_object['books'] = BOOKS
    return jsonify(response_object)


@app.route('/', methods=['GET'])
def not_found():
    return jsonify('notFound!')


@app.route('/Trains', methods=['GET'])
def find_train():
    from_city = request.args.get('fromCity')
    to_city = request.args.get('toCity')
    timetable = trains.getTains(from_city, to_city)
    journeys = []
    for journey in timetable["journeys"]:
        departure_date = dateutil.parser.parse(journey['departure_date_time'])
        arrival_date = dateutil.parser.parse(journey['arrival_date_time'])
        journeys.append({"duration": journey['duration'],
                         "departure_date": departure_date,
                         "arrival_date": arrival_date})
    res = {"status": "success",
           "fromCity": from_city,
           "toCity": to_city,
           "journeys": journeys}
    print(res)
    print(f"number of hits : {len(journeys)}")
    res = jsonify(res)
    return res


if __name__ == '__main__':
    app.run()
