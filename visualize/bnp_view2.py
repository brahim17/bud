import matplotlib.pyplot as plt
import pandas as pd

import releve.bnp_releve as releve
import tools.yaml_config as yc

import matplotlib.dates as md

directory_path = yc.get_path()


def filter_data_frame(df_bnp):
    filter_periode = (df_bnp['date'] >= '2020-1-1') & (df_bnp['date'] <= '2020-12-31')
    # filter_tier = ((df_bnp['tier'] == 'TCS') | (df_bnp['tier'] == 'BR'))
    filter_tier = True
    filter_category = (df_bnp['category'] == 'GARDE')

    return filter_periode & filter_tier & filter_category


def add_value_labels(ax, spacing=5):
    """Add labels to the end of each bar in a bar chart.

    Arguments:
        ax (matplotlib.axes.Axes): The matplotlib object containing the axes
            of the plot to annotate.
        spacing (int): The distance between the labels and the bars.
    """

    # For each bar: Place a label
    for rect in ax.patches:
        # Get X and Y placement of label from rect.
        y_value = rect.get_height()
        x_value = rect.get_x() + rect.get_width() / 2

        # Number of points between bar and label. Change to your liking.
        space = spacing
        # Vertical alignment for positive values
        va = 'bottom'

        # If value of bar is negative: Place label below bar
        if y_value < 0:
            # Invert space to place label below
            space *= -1
            # Vertically align label at top
            va = 'top'

        # Use Y value as label and format number with one decimal place
        label = "{:.1f}".format(y_value)

        # Create annotation
        ax.annotate(
            label,  # Use `label` as label
            (x_value, y_value),  # Place label at end of the bar
            xytext=(0, space),  # Vertically shift label by `space`
            textcoords="offset points",  # Interpret `xytext` as offset in points
            ha='center',  # Horizontally center label
            va=va)  # Vertically align label differently for
        # positive and negative values.


def plot_bar(df_bnp):

    df_bnp = df_bnp[filter_data_frame(df_bnp)]

    resample = df_bnp.resample('Y', on='date').amount.sum()

    ax = resample.plot.bar(
        width=10,
        color="green", rot=45,
        title='TUTUTUUT',
        x='Time',
        y='Amount'
    )

    ax.xaxis.set_major_formatter(md.DateFormatter("%d-%m-%Y"))

    '''
    for p in ax.patches:
        ax.annotate( str(p.get_height()), (p.get_x() * 1.005, p.get_height() * 1.005) )
    '''
    # Call the function above. All the magic happens there.
    add_value_labels(ax)

    # # plt.savefig("image.png")
    # ax.set_xticklabels([x.strftime("%Y-%m") for x in df_months.index], rotation=45)
    # plt.show()


def plot_pie(df_bnp):
    # delete columns : solde
    filter_periode = (df_bnp['date'] >= '2020-1-1') & (df_bnp['date'] <= '2020-12-31')
    filter_category = ((df_bnp['category'] != 'ACHAT') & (df_bnp['category'] != 'APPORT') & (
            df_bnp['category'] != 'CAPITAL') & (df_bnp['category'] != 'KO'))

    df_bnp = df_bnp[filter_category & filter_periode]

    gk = df_bnp.groupby('category').sum()
    print(gk.info())
    print(gk)

    gk['amount'] = -gk['amount']
    gk.plot.pie(y='amount', x='category',
                autopct='%1.1f%%',
                startangle=90)
    plt.show()
