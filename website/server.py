from flask import Flask, render_template, request, jsonify, Response
import pickle
import pandas as pd

app = Flask(__name__)

@app.route('/', methods = ['GET'])
def home():
	return render_template('home.html')

@app.route('/score', methods = ['GET'])
def score():
    return render_template('score.html')

@app.route('/recommend', methods = ['GET'])
def recommend():
    return render_template('recommend.html')

# model = pickle.load(open('linreg.p', 'rb'))
# @app.route('/inference', methods=['POST'])
# def infernece():
# 	req = request.get_json()
# 	print(req)
# 	c,h,w =req['cylinders'], req['horsepower'], req['weight']
# 	prediction = model.predict([[c,h,w]])
# 	return jsonify({'c':c,'h':h,'w':w,'prediction':prediction[0]})

if __name__ == '__main__':
	app.run(host='0.0.0.0', port = 1770, debug = True)
