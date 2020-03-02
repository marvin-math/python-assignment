# -*- coding: utf-8 -*-
"""
Created on Tue Feb 25 17:40:23 2020

@author: marvi
"""
import pandas
import matplotlib.pyplot
import statistics
import seaborn
import statsmodels.formula.api as smf


# summary statistics
#%%
filepath = 'bugs.csv'
df = pandas.read_csv(filepath)
summary_df = {'KillRating': [statistics.mean, statistics.median, min, max, statistics.stdev]}
grouped_df = df.groupby(['Disgust', 'Fear']).aggregate(summary_df)
grouped_df_trial = df.groupby(['Disgust', 'Fear'])
print(grouped_df)

# linear regression
#%%
formula_kill = "KillRating ~ 1 + C(Disgust) + C(Fear)"
m_kill = smf.ols(formula_kill, data = df).fit()
print(m_kill.summary())
#linear model: KillRating = 7.95 - 0.75 * Disgust - 1.43 * Fear (where Disgust
# and Fear take the value 1 if low and 0 if high)
# results: 
# low, low: 7.95 - 0.75 - 1.43 = 5.77
# low, high: 7.95 - 0.75 = 7.2
# high, low: 7.95 - 1.43 = 6.52
# high, high: 7.95 - 0 = 7.95
# question: what does he exactly mean with 'the results of a linear model'?

#visualizing the data
#%%
# solutions taken from seaborn documentation: https://seaborn.pydata.org/generated/seaborn.boxplot.html ; 
# https://seaborn.pydata.org/generated/seaborn.swarmplot.html and a forum: 
# https://cmdlinetips.com/2019/03/how-to-make-grouped-boxplots-in-python-with-seaborn/

bp = seaborn.boxplot(x = 'Disgust', y = 'KillRating', hue = 'Fear', palette = ['r', 'b'],
                data = df, showfliers = False)
bp = seaborn.stripplot(x = 'Disgust', y = 'KillRating', hue = 'Fear', dodge = True, palette = ['r', 'b'],
                  data = df, linewidth=1)
handles, labels = bp.get_legend_handles_labels()
legend = matplotlib.pyplot.legend(handles[0:2], labels[0:2], title = 'Fear', loc = 8)

#missing: legend outside the diagram, scale of y-axis in steps of one instead of two, 












