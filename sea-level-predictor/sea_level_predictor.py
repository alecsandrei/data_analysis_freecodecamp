import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress


def draw_plot():
    # Read data from file
    df = pd.read_csv('epa-sea-level.csv')

    # Create scatter plot
    x = df['Year']
    y = df['CSIRO Adjusted Sea Level']
    plt.figure(figsize=(10, 10))
    plt.scatter(x, y)

    for i in range(2014, 2051):
        df.loc[len(df.index)] = [i, None, None, None, None]
    df_2000_2050 = df.copy()

    # Create first line of best fit
    slope, intercept, r_value, p_value, std_err = linregress(x, y)
    line_mask = df['Year'] > 2013
    df['CSIRO Adjusted Sea Level'][line_mask] = df[line_mask]['Year'] * slope + intercept
    x_predicted = df['Year']
    plt.plot(x_predicted, intercept + slope * x_predicted, 'r', label='1850-2050')

    # Create second line of best fit
    df_2000_2050 = df_2000_2050[df_2000_2050['Year'] >= 2000]
    x_2000_2050 = df_2000_2050[df_2000_2050['Year'] <= 2013]['Year']
    y_2000_2050 = df_2000_2050[df_2000_2050['Year'] <= 2013]['CSIRO Adjusted Sea Level']
    slope_2000_2050, intercept_2000_2050, r_value_2000_2050, p_value_2000_2050, std_err_2000_2050 = linregress(
        x_2000_2050, y_2000_2050)
    df_2000_2050['CSIRO Adjusted Sea Level'][line_mask] = df_2000_2050['Year'][line_mask] * \
                                                          slope_2000_2050 + \
                                                          intercept_2000_2050
    x_predicted_ax2 = df_2000_2050['Year']
    plt.plot(x_predicted_ax2, intercept_2000_2050 + slope_2000_2050 * x_predicted_ax2, 'g', label='2000-2050')

    # Add labels and title
    plt.legend()
    plt.title('Rise in Sea Level')
    plt.ylabel('Sea Level (inches)')
    plt.xlabel('Year')
    
    # Save plot and return data for testing (DO NOT MODIFY)
    plt.savefig('sea_level_plot.png')
    return plt.gca()
