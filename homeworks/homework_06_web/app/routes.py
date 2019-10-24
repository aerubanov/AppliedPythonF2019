from app import app
from flask import jsonify, abort, request
from marshmallow.exceptions import ValidationError
import flight_data
import validation

data_storage = flight_data.FlightsStorage()
flight_schema = validation.FlightSchema()


@app.route('/flights', methods=['GET', 'POST'])
def flights():
    if request.method == 'GET':
        data = data_storage.get_flights()
        return jsonify(data)
    elif request.method == 'POST':
        try:
            data = flight_schema.load(request.get_json())
            data_storage.add_flight(dep_time=data['dep_time'], arr_time=data['arr_time'],
                                    dest_airp=data['dest_airport'],
                                    airplane=data['airplane'])
            return 'OK'
        except ValidationError as e:
            abort(400, str(e))


@app.route('/flights/<int:flight_id>/', methods=['GET', 'PUT', 'DELETE'])
def flight(flight_id):
    if request.method == 'GET':
        data = data_storage.get_flight(flight_id)
        if data is None:
            abort(404)
        return jsonify(data)
    elif request.method == 'DELETE':
        result = data_storage.delete_flight(flight_id)
        if result is None:
            abort(400, 'Try to delete unexciting element')
        return 'OK'
    elif request.method == 'PUT':
        try:
            data = flight_schema.load(request.get_json())
            result = data_storage.change_flight(flight_id, dep_time=data['dep_time'], arr_time=data['arr_time'],
                                                dest_airp=data['dest_airport'], airplane=data['airplane'])
            if result is None:
                abort(400, 'Try to change unexciting element')
            return 'OK'
        except ValidationError as e:
            abort(400, str(e))
