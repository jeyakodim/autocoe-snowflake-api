# Using flask to make an api
# import necessary libraries and functions
from flask import Flask, jsonify, request, make_response
from flask_cors import cross_origin
import requests
import snowflake.connector
from configparser import ConfigParser
import json

# creating a Flask app
app = Flask(__name__)


@app.route('/post', methods=['POST'])
@cross_origin()
def check_admin():
    data = request.json
    return make_response(jsonify({'Result': str(data)}))


'''def getDetails(string):

    Dictionary = {'digital': {'tableId': 'bhspmv42w', 'URL': 'https://api.quickbase.com/v1/reports/36/run', 'Query': 'QKB_JSON_DATA'},
                    'maintenance': {'tableId': 'brksg8rfj', 'URL': 'https://api.quickbase.com/v1/reports/10/run', 'Query': 'SURF_MAINTENANCE'},
                    'risk': {'tableId': 'brkvaxnwi', 'URL': 'https://api.quickbase.com/v1/reports/6/run', 'Query': 'SURF_RISK_REPORT'},
                    'spend': {'tableId': 'briyy8zey', 'URL': 'https://api.quickbase.com/v1/reports/6/run', 'Query': 'SURF_SPEND'},
                    'works': {'tableId': 'brkvcdw65', 'URL': 'https://api.quickbase.com/v1/reports/6/run', 'Query': 'SURF_SOW_REPORT'}
                 }
    return Dictionary[string]'''


@app.route('/', methods=['GET'])
def display():
    return jsonify({'message': 'Home'})


@app.route('/qb/<string:name>', methods=['GET', 'POST'])
def digital(name):
    post_req = name
    data = request.json
    config_object = ConfigParser()
    config_object.read('user.cfg')

    headers = {
        'QB-Realm-Hostname': config_object.get('ApplicationDetails', 'QB-Realm-Hostname'),
        'User-Agent': config_object.get('ApplicationDetails', 'User-Agent'),
        'Authorization': config_object.get('ApplicationDetails', 'Authorization')
        }

    params = {
        'tableId': data['tableId'],
        'skip': config_object.get('ApplicationDetails', 'skip'),
        'top': config_object.get('ApplicationDetails', 'top')
    }
    URL = data['URL']
    r = requests.post(
        URL, params=params, headers=headers
    )
    json_data = json.dumps(r.json(), indent=4)
    # Connect to your Snowflake account
    ctx = snowflake.connector.connect(
        account=config_object.get('ApplicationDetails', 'account'),
        user=config_object.get('ApplicationDetails', 'user'),
        password=config_object.get('ApplicationDetails', 'password'),
        database=config_object.get('ApplicationDetails', 'database'),
        schema=config_object.get('ApplicationDetails', 'schema'),
        role=config_object.get('ApplicationDetails', 'role'),
        warehouse=config_object.get('ApplicationDetails', 'warehouse')
    )
    cs = ctx.cursor()
    try:
        cs.execute("Insert into "+data['Query'] +
                   " SELECT parse_json($$" + json_data + "$$);"
                   )
    finally:
        cs.close()
    ctx.close()
    return jsonify({'message': post_req+' Responded'})


# driver function
if __name__ == '__main__':
    app.run(debug=True)
