from flask import Flask,jsonify,request
from flask import render_template
import ast
app = Flask(__name__)


PhoneId = []
x =[]
y =[]

@app.route("/")
def get_chart_page():
    global PhoneId,x,y
    PhoneId = []
    x =[]
    y =[]
    return render_template('index_spark_flask.html', PhoneId=PhoneId, x=x, y=y)


@app.route('/refreshData')
def refresh_graph_data():
    global PhoneId,x,y
    print("PhoneId now: " + str(PhoneId))
    print("x now: " + str(x))
    print("y now: " + str(y))
    return jsonify(sLabel=labels, sData=values)

@app.route('/updateData', methods=['POST'])
def update_data():
    global PhoneId,x,y
    if not request.form or 'data' not in request.form:
        return "error",400
    PhoneId = ast.literal_eval(request.form['PhoneId'])
    x = ast.literal_eval(request.form['x'])
    y = ast.literal_eval(request.form['y'])
    print("labels received: " + str(PhoneId))
    print("data received: " + str(x))
    print("data received: " + str(y))
    return "success",201

if __name__ == "__main__":
    app.run(host='localhost', port=5001)