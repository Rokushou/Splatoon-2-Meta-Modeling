'''imports'''
import os
import collections
import glob
import pandas as pd

'''functions'''
def splatoon_drop(df):
    """
    Drops unnessecary features in stat.ink dataframes

    Parameters:
    df (DataFrame): pandas or koalas dataframe on which to drop values

    Returns:
    DataFrame: the dataframe with dropped features

    """
    # initialize list with first features
    drop_lst = ['# period','time', 'knockout']
    # concatanate player statistics features for each player
    for player in ['A1', 'A2', 'A3', 'A4', 'B1', 'B2', 'B3', 'B4']:
        drop_lst += [player+'-kill-assist', player+'-kill', player+'-assist',
                     player+'-death', player+'-special', player+'-inked']
    # drop features in list
    return df.drop(drop_lst, axis=1)

def splatoon_explode(df, drop=True):
    """
    Explodes rows of stat.ink dataframes into one row for each player.
    This function is intended to be run after splatoon_drop and
    is hardcoded to accept its output features.

    Parameters:
    df (DataFrame): Pandas dataframe on which to explode

    Returns:
    koalas: Exploded dataframe stored in a koalas database

    """
    # get feature names
    features = df.columns.tolist()
    # features for all players
    shared = features[:5]
    # features for specific player
    a1 = features[6:9]
    a2 = features[9:12]
    a3 = features[12:15]
    a4 = features[15:18]
    b1 = features[18:21]
    b2 = features[21:24]
    b3 = features[24:27]
    b4 = features[27:]
    # group players by team
    if drop:
        a_team = [a2, a3, a4]
    else:
        a_team = [a1, a2, a3, a4]
    b_team = [b1, b2, b3, b4]

    # initialize temporaty storage list
    tmp = collections.deque()
    # iterate through rows
    for index, row in df.iterrows():
        # get features common to both teams
        both = [index] + row[shared].tolist()
        # append features for each a team player
        for player in a_team:
            tmp.append(both + row[player].tolist() + [row.win == 'alpha'])
        # append features for each b team player
        for player in b_team:
            tmp.append(both + row[player].tolist() + [row.win == 'bravo'])

    #create new column names, including the index of the match the data was from
    new_cols = ['match'] + shared + ['weapon', 'rank', 'level', 'win']
    # return new koalas database
    return pd.DataFrame(list(tmp), columns=new_cols)

'''main'''
# create paths
in_path = os.path.join(os.pardir, 'data/raw/')
out_path = os.path.join(os.pardir , 'data/dump/')
# get length of path for slicing filename out of path
l = len(in_path)
# get list of files
files = glob.glob(os.path.join(in_path, '*.csv'))
# process and pickle every file
for file in files:
    filename = file[l:-4] + '.pkl'
    splatoon_explode(splatoon_drop(pd.read_csv(file))).to_pickle(out_path + filename)
    # print progress
    print('Created ' + filename)
