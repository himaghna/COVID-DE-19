"""
@Himaghna
Convert csv file to a data frame then plot.

Package Requirements
------------
    Pandas
    Numpy
    Matplotlib

"""

from argparse import ArgumentParser

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# PATHS
US_CSV = 'us.csv'
CT_CSV = 'us-counties.csv'
ST_CSV = 'us-states.csv'

def format_labels(dates_):
    """Format date to human readable form
    Parameters
    ----------
    dates: numpy.array[str]

    Returns
    -------
    formatted_labels_: numpy.array[str]
        Array with each element being formatted date.
    major_ticks: List[int]
        idx of major tick locations.
    minor_ticks: List[int]
        idx of minor tick locations.

    """
    formatted_labels_ = []
    major_ticks, minor_ticks = [], []
    month_dict = {
        '01': 'Jan',
        '02': 'Feb',
        '03': 'Mar',
        '04': 'Apr',
        '05': 'May',
        '06': 'June',
        '07': 'July',
        '08': 'Aug',
        '09': 'Sep',
        '10': 'Oct',
        '11': 'Nov',
        '12': 'Dec'}
    for id, date_ in enumerate(dates_):
        _, month, day = date_.split('-')
        # Only add days on the first of each month or
        # first entry in data set for clarity
        if id == 0: # first entry
            formatted_labels_.append(day + '-' + month_dict[month])
            major_ticks.append(id)
        elif day == '01': # first of each month
            formatted_labels_.append(
                month_dict[month] + u"\u2192")
            major_ticks.append(id)
        else:
            minor_ticks.append(id)
    return np.array(formatted_labels_), major_ticks, minor_ticks



def get_time_series(df, state):
    """ Get time series of cases and deaths

    Parameters
    ----------
    df: Pandas DataFrame
        Data frame with columns 'date', 'cases' and 'deaths'.
    state: str
        If state id is passed, only entries for that state are returned. If
        'state' is 'us', the netire dataframe is passed.
        Options are 'ny', 'md', 'de', 'nj', 'us.

    Returns
    -------
    cases: np.array[int]
    deaths: np.array[int]
    dates: np.array[str]

    """
    if state == 'us':
        df_out = df
    else:
        state_entries = {
            'de': 'Delaware',
            'nj': 'New Jersey',
            'ny': 'New York',
            'md': 'Maryland'}
        df_out = df.loc[df['state'] == state_entries[state]]
    return df_out.cases.values, df_out.deaths.values, df_out.date.values


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('location', help='[us, md, de, nj, ny]')
    parser.add_argument(
        '-cf',
        '--csv_file',
        required=False,
        default=None,
        help='CSV filepath. If none supplied, hard-coded defaults are used')
    args = parser.parse_args()
    location = args.location
    if location not in ['us', 'md', 'nj', 'ny', 'de']:
        raise NotImplemented('Unknown location entered')
    elif location == 'us':
        csv_fpath = args.csv_file if args.csv_file is not None else US_CSV
    else:
        csv_fpath = args.csv_file if args.csv_file is not None else ST_CSV
    df = pd.read_csv(csv_fpath)
    cases, deaths, dates = get_time_series(df, state=location)
    deaths_in_thousands = np.array([int(int(death)/1000) for death in deaths])
    cases_in_thousands = np.array([int(int(case)/1000) for case in cases])
    formatted_dates, major_ticks, minor_ticks = format_labels(dates)
    # Plot deaths and cases
    plt.title(location.upper(), fontsize=24)
    plt.plot(
        [_ for _ in range(deaths_in_thousands.size)],
        deaths_in_thousands, label='Deaths', c='red', linestyle='--')
    plt.plot([_ for _ in range(cases_in_thousands.size)],
        cases_in_thousands, label='Cases', c='blue')
    plt.ylabel('Count In Thousands', fontsize=20)
    plt.xlabel('Days', fontsize=20)
    plt.legend(fontsize=20)
    ax = plt.gca()
    # format Y axis
    plt.yticks(fontsize=20)
    # format X Axis ticks
    plt.xticks([_ for _ in range(deaths.size)], labels=formatted_dates)
    ax.tick_params(
        axis='x', which='major', labelsize=20, length=5, width=1, color='red')
    ax.tick_params(axis='x', which='minor')
    ax.set_xticks(major_ticks)
    ax.set_xticks(minor_ticks, minor=True)
    plt.tight_layout()
    plt.show()




