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
filepath = "bugs.csv"
df = pandas.read_csv(filepath)
if df.columns[2] == 'Disgust' and df.columns[3] == 'Fear' and df.columns[4] == 'KillRating':
    
    summary_df = {"KillRating": [statistics.mean, statistics.median, min, max, statistics.stdev]}
    grouped_df = df.groupby(["Disgust", "Fear"]).aggregate(summary_df)
    grouped_df_trial = df.groupby(["Disgust", "Fear"])
    print("Summary statistics of the KillRatings for each type of bug:\n\n",grouped_df)

else:
    error_message = """The columns for this particular task should be 'Disgust', 'Fear' 
(the predictor variables) and 'KillRating' (outcome variable), 
whereas the respective columns in the DataFrame are {}, {} and {}.
Maybe check again whether {} stores the correct data"""
    raise ValueError(error_message.format(df.columns[2],
          df.columns[3], df.columns[4], filepath))

#if df.columns[2] != 'Disgust' and df.columns[3] != 'Fear':
#    raise 
# linear regression
#%%
formula_kill = "KillRating ~ 1 + C(Disgust) + C(Fear)"
# adding 1 in the formula is redundant, since the ordinary least squares function
# also works without it. However, I decided to keep it for the sake of clarity and 
# in case there is a program that doesn't automatically search for a constant value
# keeping the 1 in this formula makes this program more easy to implement for others.
# With the same thought I added the C() to Disgust and Fear, which communicates
# the program that the variable at hand is a categorical one. 
m_kill = smf.ols(formula_kill, data = df).fit()
print("""\n\nThe results of a linear model with kill rating as the outcome variable 
and the categories of bug as the predictor variables:\n\n""", m_kill.summary())
#linear model: KillRating = 7.95 - 0.75 * Disgust - 1.43 * Fear (where Disgust
# and Fear take the value 1 if low and 0 if high)
# model-based predictions: 
low_low = m_kill.params[0] + m_kill.params[1] + m_kill.params[2]
low_high = m_kill.params[0] + m_kill.params[1]
high_low = m_kill.params[0] + m_kill.params[2]
high_high = m_kill.params[0]
print("The model based predictions are:\nlow_low: ", low_low,
      "\nlow_high: ", low_high, "\nhigh_low: ", high_low, "\nhigh_high: ", high_high)



#visualizing the data
#%%
# solutions taken from seaborn documentation: https://seaborn.pydata.org/generated/seaborn.boxplot.html ; 
# https://seaborn.pydata.org/generated/seaborn.swarmplot.html and a forum: 
# https://cmdlinetips.com/2019/03/how-to-make-grouped-boxplots-in-python-with-seaborn/
matplotlib.pyplot.figure(figsize=(10,8))
bp = seaborn.boxplot(x = 'Disgust', y = 'KillRating', hue = 'Fear', palette = ["#3498db", "#e74c3c"],
                data = df, showfliers = False)

bp = seaborn.stripplot(x = 'Disgust', y = 'KillRating', hue = 'Fear', dodge = True, palette = ["#3498db", "#e74c3c"],
                  data = df, linewidth=1)
handles, labels = bp.get_legend_handles_labels()
legend = matplotlib.pyplot.legend(handles[0:2], labels[0:2], title = 'Fear', loc = 8)
matplotlib.pyplot.savefig('bp.svg')

#missing: legend outside the diagram, scale of y-axis in steps of one instead of two, 


#plotnine
#%%
#values = ['low', 'high']
#print((
#p9.ggplot(p9.aes(x = "Disgust", y = "KillRating", fill = "Fear"), data = df)
#+ p9.scales.scale_x_discrete(labels = values)
#+ p9.geom_boxplot()

#+ p9.position_identity

#+p9.
#+ p9.scale_x_discrete(labels=values, name='Disgust')
#+ p9.annotate(xmin='low', xmax = 'high')
#))

#p = ggplot(data = df, aes(x = "Disgust", y = "KillRating", hue = "Fear"))
#bugs_plot = p9.ggplot(data = df, mapping = p9.aes(x = "Disgust", y = "KillRating", hue = "Fear") p9.scale_color_hue(l=0.45))
#print( bugs_plot + p9.geom_boxplot() + p9.geom_jitter(show_legend = True))






