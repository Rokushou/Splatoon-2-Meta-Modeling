import pandas as pd
import pickle

with open('data/model.pkl', 'rb') as f:
    model = pickle.load(f)

scorer = pd.read_pickle('data/scorer.pkl')

def rec_weapon(weapon, modes='Turf War'):

    # data assignement shenanigans
    if type(weapon) == str:
        weapon = [weapon]
    if modes == 'debug':
        modes = ['Turf War', 'Splat Zones', 'Tower Control', 'Rainmaker', 'Clam Blitz']
    elif type(modes) == str:
        modes = [modes]

    # loop through every mode
    for mode in modes:
        # get predictions
        recs = model.get_user_recommendation(weapon, 10)
        # take predictions from scored list and sort by winrate
        recs = scorer[scorer.key.isin(recs)].sort_values(mode + '_winrate', ascending=False)
        # get the name of the highest winrate weapon
        best = recs.name.iloc[0]

        # calculate % winrate increase
        current = scorer[scorer.key.isin(weapon)].sort_values(mode + '_winrate', ascending=False).iloc[0]
        new = float(recs[mode + '_winrate'].iloc[0])
        percent = (new - float(current[mode + '_winrate'])) * 100

        # only make a recommendation if it is an improvement
        if percent <= 0:
            print ('The {} is already a great choice for {}!'.format(current['name'], mode))
        else:
            print('Try the {} for a {:.2f}% win rate increase in {}!'.format(best, percent, mode))
