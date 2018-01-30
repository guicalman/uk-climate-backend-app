import sqlite3
from flask_restful import Resource, reqparse

class RegionConditions(Resource):
    def get(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT  region_name FROM w_conditions"
        result = cursor.execute(query)
        resultset=result.fetchall()
        pass



class RegionList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT DISTINCT region_name FROM w_conditions"
        result = cursor.execute(query)
        resultset=result.fetchall()
        regions=[region[0] for region in resultset]
        return {'regions': regions}
