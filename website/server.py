from flask import Flask, render_template, request, jsonify, Response, send_from_directory
import pickle
import pandas as pd

app = Flask(__name__)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'favicon.ico')

@app.route('/', methods = ['GET'])
def home():
	return render_template('home.html')

@app.route('/score', methods = ['GET'])
def score():
    return render_template('score.html')

@app.route('/recommend', methods = ['GET'])
def recommend():
    return render_template('recommend.html')

@app.route('/recommend_a', methods = ['GET'])
def recommend_a():
    return render_template('recommend_a.html')

@app.route('/recommend_s', methods = ['GET'])
def recommend_i():
    return render_template('recommend_s.html')

scorer = pickle.load(open('scorer.pkl', 'rb'))

@app.route('/inference', methods=['POST'])
def inference():
	req = request.get_json()
	k,a,d,s,i = req['kill'],req['assist'],req['death'],req['special'],req['inked']
	prediction = scorer.predict_proba([[k,a,d,s,i]])
	return jsonify({'k':k,'a':a,'s':s,'d':d,'i':i,'prediction':int(prediction[0, 1]*1000)})

recommender = pickle.load(open('recommender.pkl', 'rb'))

@app.route('/rec', methods=['POST'])
def rec():
	req = request.get_json()
	w, m= req['weapon'].split(", "), req['mode']
	prediction = recommender.get_weapon_recommendation(w, m)
	return jsonify({'w':w,'m':m,'prediction':prediction})

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=1770, debug=True)
