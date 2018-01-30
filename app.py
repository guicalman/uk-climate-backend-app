from flask import Flask
from flask_restful import Api
from services import RegionList, RegionConditions
from load_data import load_all_data

# Exceutes the method that populate the database
load_all_data()

# Configures the Climate Backend endpoints
app = Flask(__name__)
api = Api(app)
# Endpoint that returns a list of regions
api.add_resource(RegionList, '/regions')
# Endpoint that returns a json with all the Climate conditions for all years
api.add_resource(RegionConditions, '/region/<string:name>')

app.run(port=5000, debug=True)