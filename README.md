# Splatoon 2: ΛBSOLUTΞ ΛDVΛNTΛGΞ

## Description

#### Motivation and Goals

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;This project started as an attempt to predict win rate based on various factors that can be determined pre-match such as game mode, weapon choice, and rank. However, it quickly became evident that Splatoon 2, in the words of a certain British gamer, is a perfectly balanced game with no exploits. After taking player skill out of the equation, there were practically no difference in the distributions between wins and losses.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;With that path closed, the only other option was to do predictions using post-match statistics. While predicting the outcome of a match with information obtained after the fact is next to useless, modeling it allows a better understanding of what contributes most to a win as well as being able to score and compare players after a match. Useful for answering the question of "How hard was I carried by my friend Jeff?"

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;The second part of the project was creating a weapon recommender, mainly driven by personal desire for one. It recommends players new weapons that are both familiar and proven to be successful. Another important goal of was to create a website to get some web design experience as well as provide public access to the models.

#### Overview

- Gathered player data from stat.ink, a site where players can voluntarily upload their match data. The data is freely available on the website and schema can be found in [schema.md](https://github.com/Rokushou/Splatoon-2-Meta-Modeling/blob/master/schema.md).

- Predicted win rate by creating a binary classifier for win/loss and using predict percent.

- Used inferential regression and gradient boosting feature importance to determine most important factors contributing to winning.

- Developed a neural network classifier with 81% accuracy to perform scoring.

- Designed a recommender that would suggest a weapon similar to a user's favorites with a a higher win rate.

- Created a Flask website hosted on AWS to run both the predictor and recommender.

## EDA (Experimental Data Analysis)
My first dead end model came about because of improper EDA. I thought I had enough domain knowledge, so used intuition to decide which features to use. Turns out that the distributions between win and loss were nearly identical for all my features. I did find a few things worth noting though.

#### Wins and Losses by Rank

![](img/rankx.png)

Rank X has significantly more wins than losses. This is not surprising as they are the top players and must continually win to stay in the rank. However, it is interesting that S+ (the precursor to X) did not exhibit this.

#### Wins and Losses by Weapon Category

![](img/charger.png)

* Note: `maneuver` is the dualie category and `reelgun` is the nozzlenose family.

Somewhat confirming the belief that charger (sniper) players are dead weight, the charger weapon category has the highest proportion of losses of all weapon types, with rollers coming in a distant second.

![](https://cdn.wikimg.net/en/splatoonwiki/images/a/ad/S2_Weapon_Main_Splatterscope.png)

### Actual Proper EDA

I was initially planning on modeling with features such like the ones shown above, which showed little if any difference in distribution between win and lose. Eventually I decided that this would never produce any meaningful predictions and decided to resort to post-match results. these are some of the more interesting overlapped histograms.

#### Kills

![](img/kill.png)

Kills have two peaks in the distribution for both win and lose. This may be because there are objective focused players that only fight when necessary and kill focused players that hunt down the enemy.

#### Assists

![](img/assist.png)

Assists are very low compared to kills due to the fast paced nature (fights usually end before a teammate can notice and contribute). The peaks are very distinct between win and lose which means that assists still matter.

#### Turf Inked

![](img/inked.png)

Turf inked has a lot of overlap and the shape of the distribution is almost identical for win and lose. Is inking the cause of the win or does the winning team get more opportunity to ink when momentum is in their favor?

## Modeling

#### Logistic Regression

I decided to throw `mode, kill, assist, death, special, inked, level` into a simple logistic model with L1 penalty for a quick initial estimate. It did surprisingly well with 80.2% accuracy and could be kept for inferential regression.

![](img/roc.png)

#### Gradient Boosting

After optimizing a gradient boosting classifier with a gridsearch, I only managed a slight accuracy increase to 80.4%. This model is more accurate and I can draw inferences from feature importance.

![](img/gbroc.png)

#### Neural Network

I spent a lot of time manually tuning hyperparameters and managed to get 80.5% accuracy. This means that my initial logistic regression was plenty good even though I just threw it together. I would use a neural net if I wanted a purely predictive model but will still stick to the logistic regression as I can better draw inferences with it.

![](img/nnroc.png)

## Interpretations

#### Effect Size with Inferential Regression

The Linear Regression Assumptions:
- Linearity
    - My logistic regression model does almost well as Gradient Boosting and Neural Net. This would not be true if the data was non-linear.
- Linear Independence
    - Predictors chosen in a way that do not overlap, Kill-Assist was not chosen for this reason.
- Independence
    - Given a large enough sample of matches and 8 players per match, observations should be independent even if they were uploaded by a small subset of players.
- Homoscedasticity
    - Data has similar distributions across both classes.
- Normal Distribution of Errors
    - There should be minimal error due to data being directly exported from the game API.

With these conditions satisfied, I can properly use inferential regression. First I get the coefficients of the logistic regression.

![](img/coef.png)

It seems like death and kill are the most important by a large margin, no surprise there. However it does appear that death (not dying) is more important than getting kills. According to this model a 1 for 1 trade is not worth it. Inked and special are also good predictors and it is interesting that inked is more important than special because one of the main motivations for inking is to build special meter.

![](img/pvalues.png)

* x1 - x11 correspond to `Kill, Assist, Death, Special, Inked, Level, Game Mode: Splat Zones, Game Mode: Clam Blitz, Game Mode: Rainmaker, Game Mode: Turf War, Game Mode: Tower Control`

The p-values show that Kill, Assist, Death, Special, and Inked are all good predictors while the game modes are particularly poor predictors.

#### Feature importance with Gradient Boosting

My gradient boosting model was a little more accurate than my logistic regression, and while it is not as easy to understand as coefficients, I can still make inferences using feature importance.

![](img/feat.png)

Deaths and kills are also the most important here, however they are more evenly weighted. Inked has dropped in proportional importance but is still 3rd and handily beats special. Surprisingly, level is now a relatively useful predictor, indicating that it may have a nonlinear correlation to win rate.

## Recommender

#### Item-Item Similarity

The first step of creating the recommender was to get a list of weapons most similar to the user's favorites. To do this, I used a custom item to item based cosine similarity recommender on weapon metadata. Since the metadata does not contain information on weapon performance, this segment of the model only serves to ensure recommend weapons are functionally similar to the user's preferences.

#### Ranking predictions

![](img/weaponwr.png)

As seen in the table of aggregate statistics shown above, there are plenty of ways to rank the predictions. I decided to use Win Percent to keep the model simple and I feel it is the best single statistic to determine weapon performance.

My model recommends the highest win rate weapon from the recommendations list and also shows the win rate increase. If there are no recommendations that provide a win rate increase, it instead recommends the highest win rate item from the user's favorites.

#### No error metric

There is no accuracy score for this model as it is supposed to encourage users to try new weapons. I could feed it data based on what weapons users performed best with, but in order to validate the predictions, I would either need to be able to influence the user's choices or hope that the user just happens to use the recommended weapon.

## Future Work

- Improve my recommender by adding more features to the ranking system. This would likely be a complex neural network and was out of the scope of this project as I had no way of measuring the error.

- Incorporate user metadata into the recommender to create a better user-item recommender. This was not possible with my current dataset as users were not identified.

- Upgrade the website with a more modern javascript-heavy style to improve visual aesthetics and enhance the user interface.

#### Acknowledgments
This project would not have been possible without the data from [fetus-hina](https://github.com/fetus-hina)'s website [stat.ink](https://stat.ink/).
