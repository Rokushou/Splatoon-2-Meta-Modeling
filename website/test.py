import pickle
with open('recommender.pkl', 'rb') as f:
    model2 = pickle.load(f)

model2.get_weapon_recommendation(['Custom Dualie Squelchers'], 'debug')

with open('scorer.pkl', 'rb') as f:
    scorer2 = pickle.load(f)

f = scorer2.predict_proba([[5, 1, 4, 2, 1000]])[0, 1]
print('Your score is {}'.format(int(f*10000)))
