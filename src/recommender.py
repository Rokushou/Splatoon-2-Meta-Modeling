from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np

class ItemRecommender():
    '''
    Content based item recommender
    '''
    def __init__(self, similarity_measure=None, path='data/weapon_winrate.pkl'):
        self.score = pd.read_pickle(path)
        self.similarity_matrix = None
        self.item_names = None

        if similarity_measure == None:
            self.similarity_measure = cosine_similarity
        else:
            self.similarity_measure = similarity_measure


    def fit(self, X, index=None):
        '''
        Takes a numpy array of the item attributes and creates the similarity matrix

        INPUT -
            X: NUMPY ARRAY - Rows are items, columns are feature values / or DF
            index: LIST - List of the item names/titles in order of the numpy arrray

        OUTPUT - None


        Notes:  You might want to keep titles and X as attributes to refer to them later

        Create the a similarity matrix of item to item similarity
        '''

        # While keeping this as a sparse matrix would be best the cosign sim
        # function returns a array so there is no reason.

        if isinstance(X, pd.DataFrame):
            self.item_counts = X
            self.item_names = X.index
            self.similarity_df = pd.DataFrame(self.similarity_measure(X.values, X.values),
                 index = self.item_names)
        else:
            self.item_counts = X
            self.similarity_df = pd.DataFrame(self.similarity_measure(X, X),
                 index = index)
            self.item_names = self.similarity_df.index


    def get_recommendations(self, item, n=5):
        '''
        Returns the top n items related to the item passed in
        INPUT:
            item    - STRING - Name of item in the original DataFrame
            n       - INT    - Number of top related items to return
        OUTPUT:
            items - List of the top n related item names

        For a given item find the n most similar items to it (this can be done using the similarity matrix created in the fit method)
        '''
        return self.item_names[self.similarity_df.loc[item].values.argsort()[-(n+1):-1]].values[::-1]


    def get_user_profile(self, items):
        '''
        Takes a list of items and returns a user profile. A vector representing the likes of the user.
        INPUT:
            items  -   LIST - list of item names user likes

        OUTPUT:
            user_profile - NP ARRAY - array representing the likes of the user
                    The columns of this will match the columns of the trained on matrix


        Using the list of items liked by the user create a profile which will be a 1 x number of features array.  This should be the addition of the values for all liked item features (you can choose how to normalize if you think it is needed)
        '''
        user_profile = np.zeros(self.item_counts.shape[1])
        for item in items:
            user_profile += self.item_counts.loc[item].values

        return user_profile


    def get_user_recommendation(self, items, n=5):
        '''
        Takes a list of items user liked and returns the top n items for that user

        INPUT
            items  -   LIST - list of item names user likes
            n -  INT - number of items to return

        OUTPUT
            items - LIST - n recommended items


        Make use of the get_user_profile method to create a user profile that will be used to get the similarity to all items and recommend the top n.
        '''
        num_items = len(items)
        user_profile = self.get_user_profile(items)

        user_sim =  self.similarity_measure(self.item_counts, user_profile.reshape(1,-1))

        return self.item_names[user_sim[:,0].argsort()[-(num_items+n):-num_items]].values[::-1]

    def get_weapon_recommendation(self, weapon, modes='Turf War'):
        '''
        Takes a list of item user liked and returns the top n items for that user

        INPUT
            items - LIST - list of item names user likes

        OUTPUT
            out - STR - recommendation formatted as a quote


        Make
        '''
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
            recs = self.get_user_recommendation(weapon, 10)
            # take predictions from scored list and sort by winrate
            recs = self.score[self.score.key.isin(recs)].sort_values(mode + '_winrate', ascending=False)
            # get the name of the highest winrate weapon
            best = recs.key.iloc[0]

            # calculate % winrate increase
            current = self.score[self.score.key.isin(weapon)].sort_values(mode + '_winrate', ascending=False).iloc[0]
            new = float(recs[mode + '_winrate'].iloc[0])
            percent = (new - float(current[mode + '_winrate'])) * 100

            # only make a recommendation if it is an improvement
            if percent <= 0:
                out = 'The {} is already a great choice for {}!'.format(current['key'], mode)
            else:
                out = 'Try the {} for a {:.2f}% win rate increase in {}!'.format(best, percent, mode)
            print(out)
        return(out)
