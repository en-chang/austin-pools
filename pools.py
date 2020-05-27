import json
import xml.etree.ElementTree as ET
import requests

from flask import request
from flask import Flask, render_template


application = Flask(__name__)
app = application
all_pools = []
source = "https://raw.githubusercontent.com/devdattakulkarni/elements-of-web-programming/master/data/austin-pool-timings.xml"
data = requests.get(source)
root = ET.fromstring(data.text)

@app.route("/pools")
def get_pools():
    pool_data = xmlData()
    if len(all_pools) == 0:
        for pool in pool_data.values():
            all_pools.append(pool)
    return json.dumps(all_pools)

@app.route("/")
def pool_info_website():
    return render_template('index.html')

def xmlData():
    dataDict = {}
    pool_num = 0
    for pool in root.findall('row'):
        pool_name = ''
        pool_type = ''
        status = ''
        open_date = ''
        weekday = ''
        weekend = ''
        try:
            pool_name = pool.find('pool_name').text
            pool_type = pool.find ('pool_type').text
            status = pool.find('status').text
            open_date = pool.find('open_date').text
            weekday = pool.find('weekday').text
            weekend = pool.find('weekend').text
        except AttributeError:
            continue
        poolDict = {}
        poolDict['Name'] = pool_name
        poolDict['Type'] = pool_type
        poolDict['Status'] = status
        poolDict['Open'] = open_date
        poolDict['Weekday'] = weekday
        poolDict['Weekend'] = weekend
        dataDict['pool_%d' %pool_num] = poolDict
        pool_num += 1
    return dataDict

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')
