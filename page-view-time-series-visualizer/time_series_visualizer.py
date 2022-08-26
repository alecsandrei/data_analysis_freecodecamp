import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.ticker import MaxNLocator
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv',
                 index_col='date',
                 parse_dates=True)

# Clean data
condition = (df.value >= df.value.quantile(.025)) & (df.value <= df.value.quantile(.975))
df = df[condition]


def draw_line_plot():
    fig, ax = plt.subplots(figsize=(14, 5))
    plt.plot(df, color="r")
    plt.xlabel('Date')
    plt.ylabel('Page Views')
    plt.title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig


def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()

    # Creating a month and year column
    df_bar['month'] = df_bar.index.strftime('%B')
    df_bar['year'] = df_bar.index.strftime('%Y')

    # Grouping by the year and month column in order to compute the average for each month of the year
    newdf = df_bar.groupby(['year', 'month']).mean()
    newdf = newdf.reset_index()

    # Adding the missing months for the year of 2016 in order to be able to sort month values from Jan to Dec
    months_df = pd.DataFrame([['2016', 'January'], ['2016', 'February'], ['2016', 'March'], ['2016', 'April']],
                             columns=['year', 'month'])
    newdf = pd.concat([months_df, newdf])

    # Sorting month values from Jan to Dec and creating the pivot table
    newdf.value = newdf.value.fillna(0)
    newdf = newdf.sort_index().reset_index(drop=True)
    newdf = newdf.pivot(index='month', columns='year', values='value')
    sort_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
                  'November', 'December']
    newdf.index = pd.CategoricalIndex(newdf.index, categories=sort_order, ordered=True)
    newdf = newdf.sort_index()

    # Draw bar plot
    plt.rcParams.update({'font.size': 22})
    fig = newdf.T.plot(kind='bar',
                       figsize=(18, 18))
    plt.legend(fontsize=25, title='Months', title_fontsize=25, edgecolor='pink')
    plt.xlabel('Years')
    plt.ylabel('Average Page Views')
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
    f, ax = plt.subplots(1, 2, figsize=(15, 5))
    sns.boxplot(ax=ax[0], data=df_box, x='year', y='value')
    ax[0].set(ylim=(0, 200000))
    ax[0].yaxis.set_major_locator(MaxNLocator(11))
    ax[0].set_xlabel('Year')
    ax[0].set_ylabel('Page Views')
    ax[0].set_title('Year-wise Box Plot (Trend)')

    sort_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct',
                  'Nov', 'Dec']
    df_box.index = pd.CategoricalIndex(df_box['month'], categories=sort_order, ordered=True)
    df_box = df_box.sort_index()

    sns.boxplot(ax=ax[1], data=df_box, x='month', y='value')
    ax[1].set(ylim=(0, 200000))
    ax[1].yaxis.set_major_locator(MaxNLocator(11))
    ax[1].set_xlabel('Month')
    ax[1].set_ylabel('Page Views')
    ax[1].set_title('Month-wise Box Plot (Seasonality)')

    # Save image and return fig (don't change this part)
    fig = f.figure
    fig.savefig('box_plot.png')
    return fig
