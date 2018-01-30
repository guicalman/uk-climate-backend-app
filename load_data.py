import json
import sqlite3
import requests


def read_regions(json_fname):
    with open(json_fname) as json_data:
        regions_dic = json.load(json_data)
    return regions_dic

def parse_w_conditions_txt(conditions_url):
    url_data = requests.get(conditions_url).text.splitlines()
    conditions_data = [row.split() for row in url_data[7:]]
    return conditions_data

def get_w_conditions_tuples(conditions_path, region, w_condition):
    c_array=parse_w_conditions_txt(conditions_path)
    w_condition = w_condition.replace("/date", "")
    w_tuples = []
    months=c_array[0][1:]
    for row in c_array[1:]:
        year = int(row[0])
        year_values = row[1:]
        for i in range(len(months)):
            month = months[i]

            if year_values[i] == '---':
                month_value = None
            else:
                month_value = float(year_values[i])

            w_tuples.append((region, year, month, w_condition, month_value ))
    return w_tuples

def get_weather_tuples(json_fname):
    r_dic = read_regions(json_fname)
    regions = r_dic['regions']
    w_conditions = r_dic['weather_conditions']
    c_tuples=[]
    repo_url = r_dic['url']
    for region in regions:
        for w_condition in w_conditions:
            w_conditions_url = "{}{}/{}.txt".format(repo_url, w_condition, region)
            c_tuples.extend(get_w_conditions_tuples(w_conditions_url, region, w_condition))
    return c_tuples

def create_db(db_path):

    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    create_table = "CREATE TABLE IF NOT EXISTS w_conditions (region_name text, c_year int, c_month text, w_condition, " \
                                                                "text, w_value real, " \
                                                                "PRIMARY KEY(region_name, c_year, c_month, w_condition))"
    cursor.execute(create_table)
    connection.commit()
    connection.close()


def populate_db(db_path, tuples):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    query = "INSERT OR REPLACE INTO w_conditions (region_name,c_year, c_month, w_condition, w_value)" \
            "VALUES(?,?,?,?,?)"
    cursor.executemany(query,tuples)
    connection.commit()
    connection.close()

def load_all_data():
    insert_tuples = get_weather_tuples("uk_regions.json")
    create_db('data.db')
    populate_db('data.db', insert_tuples)