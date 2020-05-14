from flask import Flask, render_template, Response
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mobiledata"
mongo = PyMongo(app)

@app.route("/")
def home_page():
    antennes = mongo.db.antennes.find()
    return render_template("index_mongo.html", antennes=antennes)


if __name__ == '__main__':
    app.run(port=2002,use_reloader=True)

###################################################################################################
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