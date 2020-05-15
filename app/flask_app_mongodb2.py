from flask import Flask
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo
from flask import Flask, render_template, Response
import json
import plotly
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly.graph_objects as go
import pandas as pd

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'mobiledata'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/mobiledata'
mongo = PyMongo(app)

@app.route('/antennes', methods=['GET'])
def get_fond_data():
  fond = mongo.db.fond
  data_fond = pd.DataFrame(list(fond.find()))
  return data_fond

def get_all_data():
  antennes = mongo.db.antennes
  data = pd.DataFrame(list(antennes.find())[0:500]) ####TO BE CHANNNNGED WITH NEW DATA
  return data

def create_plot_madrid_test(data,fond):
    data['text'] = data['PhoneId'].astype(str)
    fond['text'] = fond['Antenna_Id'].astype(str)
    fig = go.Figure()
    fig.add_trace(
       go.Scattergl(
        x = fond['x']/1000,
        y = fond['y']/1000,
        text = fond['text'],
        mode='markers',
        name="Antennes",
        marker_symbol='triangle-up',
        marker_color="black",
        marker_size=8
    ))

    fig.add_trace(
        go.Scattergl(
            x=data["x"],
            y=data["y"],
            text = data['text'],
            mode="markers",
            marker_color = 'blue',
            name="People",
        )
    )

    # fig = plotly.graph_objs.Figure(data=(scatter_data, scatter_fond))
    return plotly.offline.plot(fig, include_plotlyjs=True, output_type='div')

@app.route('/')
def index():
    """Serve the index HTML"""
    return(render_template('index_mongo.html',chart=create_plot_madrid_test(get_all_data(),get_fond_data())))

if __name__ == '__main__':
    app.run(port=2002,use_reloader=True,debug=True)

###################################################################################################

# @app.route('/antennes', methods=['GET'])
# def get_all_data():
#   antennes = mongo.db.antennes
#   output = []
#   for obs in antennes.find():
#     output.append({'PhoneId' : obs['PhoneId'], 'x' : obs['x']}, 'y' : obs['y'])
#   return jsonify({'result' : output})


# @app.route('/')
# def index():
#     """Serve the index HTML"""
#     return(render_template('index_many_simple.html'))

# @app.route('/topic/antennes_static')
# def get_data():
#   return app.send_static_file('antennes.json')

# @app.route('/topic/antennesOutput')
# def get_messages():
#     client = get_kafka_client()
#     def events():
#         import time
#         res = {}
#         for message in client.topics['antennesOutput'].get_simple_consumer():
#             import json
#             key = str(json.loads(message.value.decode())["PhoneId"])
#             res[key] = json.loads(message.value.decode())
#             output=json.dumps(res)
#             yield 'data:{0}\n\n'.format(output)
#     return Response(events(), mimetype="text/event-stream") 

# if __name__ == '__main__':
#     app.run(port=2002,use_reloader=True)