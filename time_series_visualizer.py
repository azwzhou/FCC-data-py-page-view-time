import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.) 
df = pd.read_csv('fcc-forum-pageviews.csv', index_col='date', parse_dates=True)

# Clean data
mask = (df['value'] > df['value'].quantile(0.025)) & (df['value'] < df['value'].quantile(0.975))
df = df[mask]

def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots(figsize=(12,5))
    ax.plot(df.index, df['value'])

    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot'
    df_bar = df.copy()
    df_bar['year'] = pd.DatetimeIndex(df.index).year
    df_bar['month'] = pd.DatetimeIndex(df.index).month
    df_bar = df_bar.groupby(['year', 'month']).mean()
    df_bar = df_bar.reset_index()
    df_bar = df_bar.pivot(index='year', columns='month', values='value')
    
    # Draw bar plot
    fig = df_bar.plot.bar(figsize=(9,7), xlabel='Years', ylabel='Average Page Views')
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    fig = fig.legend(months, title='Months')
    fig = fig.figure


    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    #df_box['year'] = df_box['year'].astype(str)
    fig, ax = plt.subplots(1, 2, figsize=(25,9))
    ax[0] = sns.boxplot(x='year', y='value', data=df_box, ax=ax[0])
    ax[0].set_xlabel('Year')
    ax[0].set_ylabel('Page Views')
    ax[0].set_title('Year-wise Box Plot (Trend)')


    ax[1] = sns.boxplot(x='month', y='value', data=df_box, ax=ax[1], order=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    ax[1].set_xlabel('Month')
    ax[1].set_ylabel('Page Views')
    ax[1].set_title('Month-wise Box Plot (Seasonality)')
    

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
