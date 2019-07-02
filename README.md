# REMOVE THIS
1. high-level description of the project, including motivation, goals, etc.
2. EDA:  data source + visualizations + feature engineering
3. description of your model and results (possible tables & visualization)
4. summary / interpretations
5. [optional] future work

<span style="color:white">‌‌&nbsp;&nbsp;&#9650;<br>&#9650;&nbsp;&#9650;<br>You found the secret Triforce!</span>

# Splatoon-2-Meta-Modeling

#### Acknowledgments
This project would not have been possible without the data from [fetus-hina](https://github.com/fetus-hina)'s website [stat.ink](https://stat.ink/).

## Description
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;This project started as an attempt to predict win rate based on various factors that can be determined pre-match such as game mode, weapon choice, and rank. I wanted to do this less for the end result of the prediction, but so I could better understand what contributes most to a win in Splatoon 2 and how it varied across different game modes.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;However, I quickly found that contrary what some might believe, Splatoon 2 is a perfectly balanced game with no exploits. Without hyperbole, there were practically no differences in win rate across all the factors I considered. Due to that, I was unable to get any useful models, but my process is documented in [Processing and Cleaning](https://github.com/Rokushou/Splatoon-2-Meta-Modeling/blob/master/Processing%20and%20Cleaning.ipynb) and [Modeling](https://github.com/Rokushou/Splatoon-2-Meta-Modeling/blob/master/Modeling.ipynb) if anyone else would like to attempt this.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Pivoting from my dead end, I decided to do predictions on aggregated post-match statistics. While predicting the outcome of a match with information obtained after the match is next to useless, modeling it allows me to use inferential statistics to determine the most important factors for winning as well as being able to score and compare players using their post-match statistics. Useful for answering the age old question of "How hard did I (or in most cased my friend Jeff) carry the team?"

#### Overview <span style="color:white">a.k.a. tl;dr</span>
-Player data gathered from stat.ink, a site where players can voluntarily upload their match data. It is located in `data/raw` and schema can be found in [schema.md](https://github.com/Rokushou/Splatoon-2-Meta-Modeling/blob/master/schema.md).

-Predict win rate by modeling binary win/loss and using predict percent.

-Used logistic regression and gradient boosting to determine most important factors contributing to winning, and a neural network to perform predictions with 81% accuracy.

-As a future project, create a simple interface like a flask website to output predictions based on user inputted data.

## EDA (Experimental Data Analysis)
My first dead end model came about because of improper EDA. I thought I had enough domain knowledge, so used intuition to decide which features to use. Turns out that the distributions between win and loss were nearly identical for all my features. I did find a few things worth noting though.

![](img/rankx.png)
Rank X has significantly more wins than losses. This is not surprising as they are the top players but it is interesting that S+ did not exhibit this.

![](img/charger.png)
* Note: `maneuver` is the dualie category and `reelgun` is the nozzlenose family.
<div style="text-align:center"><img src="https://cdn.wikimg.net/en/splatoonwiki/images/a/ad/S2_Weapon_Main_Splatterscope.png" /></div>
Confirming the belief that charger (sniper) players are dead weight, the charger weapon category has the highest proportion of losses of all weapon types, with rollers coming in a distant second.

#### Actual Proper EDA
I was initially planning on modeling with features such like the ones shown above, which showed little if any difference in distribution between win and lose. Eventually I decided that this would never produce any meaningful predictions and decided to resort to post-match results.

![](img/kill.png)
Kills have an interesting two peaks for both win and lose.

![](img/assist.png)
Assists are very low compared to kills due to the fast paced nature (fights usually end before a teammate can notice and contribute). The peaks are very distinct between win and lose.

![](img/inked.png)
Turf inked has a lot of overlap and the shape of the distribution is almost identical for win and lose.

## Modeling
