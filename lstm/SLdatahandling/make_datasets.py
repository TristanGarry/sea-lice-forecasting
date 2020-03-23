import pandas as pd
import datetime
import numpy as np

# these are the years and months that we will run our analysis on
analysis_years = list(range(2003, 2018))
analysis_months = list(range(3, 7))

# a dictionary mapping ISO day of the week to a three letter abbreviation
dow_dict = {
    1: 'MON',
    2: 'TUE',
    3: 'WED',
    4: 'THU',
    5: 'FRI',
    6: 'SAT',
    7: 'SUN'
}

# These are the columns in the Salmoncoast data that indicate motile sea lice (that we want to count)
motile_columns = ['Lep_PAmale', 'Lep_PAfemale', 'Lep_male', 'Lep_gravid', 'Lep_nongravid', 'unid_PA', 'unid_adult']
# These are the columns in the Salmoncoast data that indicate non-motile sea lice (part of the predictors
juvenile_columns = ['Lep_cope', 'chalA', 'chalB', 'Caligus_cope', 'unid_cope', 'chal_unid']

# These are the farms relevant to the salmoncoast stations that exist in the dataset
relevant_farms_iterable = ['Sargeaunt Pass', 'Doctor Islets', 'Humphrey Rock', 'Burdwood', 'Glacier Falls',
                           'Sir Edmund Bay', 'Wicklow Point']

# This is a map of the month number to its name - to be used in the industry data processing
month_map = {
        'January': 1,
        'February': 2,
        'March': 3,
        'April': 4,
        'May': 5,
        'June': 6,
        'July': 7,
        'August': 8,
        'September': 9,
        'October': 10,
        'November': 11,
        'December': 12
    }


def get_dow(dt_obj) -> str:
    """
    A function that takes the ISO day of the week and returns a Pandas-compatible three letter abbreviation
    :param dt_obj: Pandas datetime object
    :return: string
    """
    dow_text = dt_obj.isoweekday()

    return dow_dict[dow_text]


def get_motile_df(salmoncoast_fish_df: pd.DataFrame, motile_cols: list = motile_columns) -> pd.DataFrame:
    """
    Creates a data frame of the motile sea lice counts
    :param salmoncoast_fish_df: Salmoncoast fish data frame
    :param motile_cols: columns that indicate a motile sea lice count
    :return: Single-columned data frame
    """
    motiles = salmoncoast_fish_df[motile_cols].sum(axis=1)
    date_cols = pd.to_datetime(salmoncoast_fish_df[['year', 'day', 'month']])

    response = pd.DataFrame({'count': motiles.values,
                             'location': salmoncoast_fish_df['location'].values,
                             'datetime': date_cols})

    year_df_list = []
    for year in analysis_years:
        subset = response[response['datetime'].dt.year == year]
        subset.loc[0] = np.nan
        subset.loc[0, 'datetime'] = datetime.datetime(year, 1, 1)
        subset.loc[1] = np.nan
        subset.loc[1, 'datetime'] = datetime.datetime(year, 12, 31)
        subset.sort_values('datetime', inplace=True)
        subset_resampled = subset.resample(f'W-{get_dow(datetime.datetime(year, 1, 1))}',
                                           on='datetime', label='left').apply(np.nanmean).interpolate(methods='linear')
        year_df_list.append(subset_resampled)
    y = pd.concat(year_df_list)

    return y


def get_predictor_df(salmoncoast_fish: pd.DataFrame,
                     salmoncoast_site: pd.DataFrame,
                     industry: pd.DataFrame) -> pd.DataFrame:
    """
    Create a data frame of the full predictor data. To be used to standardise data inputs between models
    :param salmoncoast_fish: BroughtonSeaLice_fishData.csv
    :param salmoncoast_site: BroughtonSeaLice_siteData.csv
    :param industry: IndustrySeaLice_Data.csv
    :return: Data frame of full predictor data
    """
    wild_locations = salmoncoast_site['location'].unique()

    juvenile_counts = get_juv_counts(salmoncoast_fish, wild_locations)
    site_temps = get_temps(salmoncoast_site, wild_locations)
    site_sal = get_sals(salmoncoast_site, wild_locations)
    industry_counts = get_industry_counts(industry)

    full_predictor_df = pd.concat([juvenile_counts, site_temps, site_sal, industry_counts], sort=True)

    return full_predictor_df


def get_juv_counts(salmoncoast_fish_df: pd.DataFrame,
                   salmoncoast_locations: list,
                   juvenile_cols: list = juvenile_columns) -> pd.DataFrame:
    """
    Sets up juvenile counts to be used as predictors
    :param salmoncoast_fish_df: BroughtonSeaLice_fishData.csv
    :param salmoncoast_locations: locations possible at salmoncoast
    :param juvenile_cols: columns that indicate a non-motile sea lice count
    :return: a 1 column data frame
    """
    juvenile = pd.DataFrame(salmoncoast_fish_df[juvenile_cols].sum(axis=1)).rename({0: 'count'}, axis=1)
    juvenile['datetime'] = pd.to_datetime(salmoncoast_fish_df[['year', 'day', 'month']])
    juvenile['location'] = salmoncoast_fish_df['location']

    year_juv_list = []
    for year in analysis_years:
        subset = juvenile[juvenile['datetime'].dt.year == year]
        for loc in salmoncoast_locations:
            # Here, I add in dummy dates to makes sure that all resampling runs for the full year and
            # on the same dates
            subset = subset.append({
                'datetime': datetime.datetime(year, 1, 1),
                'location': loc,
                'count': np.nan
            }, ignore_index=True)
            subset = subset.append({
                'datetime': datetime.datetime(year, 12, 31),
                'location': loc,
                'count': np.nan
            }, ignore_index=True)
        subset.sort_values('datetime', inplace=True)
        subset_resample = subset.groupby('location').resample(f'W-{get_dow(datetime.datetime(year, 1, 1))}',
                                                              on='datetime', label='left').apply(
            np.nanmean).interpolate(methods='linear')
        year_juv_list.append(subset_resample)
    wild_juv = pd.concat(year_juv_list)

    return wild_juv


def get_temps(salmoncoast_site_df: pd.DataFrame,
              salmoncoast_locations: list) -> pd.DataFrame:
    """
    Sets up temperature to be used as a predictor
    :param salmoncoast_site_df: BroughtonSeaLice_siteData.csv
    :param salmoncoast_locations: locations possible at salmoncoast
    :return: a 1 column data frame
    """
    salmoncoast_site_df['datetime'] = pd.to_datetime(salmoncoast_site_df[['year', 'month', 'day']])
    year_temp_list = []
    for year in analysis_years:
        subset = salmoncoast_site_df.loc[(salmoncoast_site_df['datetime'].dt.year == year),
                                         ['datetime', 'temp', 'location']]
        for loc in salmoncoast_locations:
            subset = subset.append({
                'datetime': datetime.datetime(year, 1, 1),
                'location': loc,
                'temp': np.nan
            }, ignore_index=True)
            subset = subset.append({
                'datetime': datetime.datetime(year, 12, 31),
                'location': loc,
                'temp': np.nan
            }, ignore_index=True)
        subset.sort_values('datetime', inplace=True)
        subset.sort_values('datetime', inplace=True)
        subset_resample = subset.groupby('location').resample(f'W-{get_dow(datetime.datetime(year, 1, 1))}',
                                                              on='datetime', label='left').apply(
            np.nanmean).interpolate(methods='linear')
        year_temp_list.append(subset_resample)
    x_wild_temp = pd.concat(year_temp_list)

    return x_wild_temp


def get_sals(salmoncoast_site_df: pd.DataFrame,
             salmoncoast_locations: list) -> pd.DataFrame:
    """
    Sets up salinity to be used as a predictor
    :param salmoncoast_site_df: BroughtonSeaLice_siteData.csv
    :param salmoncoast_locations: locations possible at salmoncoast
    :return: a 1 column data frame
    """
    salmoncoast_site_df['datetime'] = pd.to_datetime(salmoncoast_site_df[['year', 'month', 'day']])
    year_sal_list = []
    for year in analysis_years:
        subset = salmoncoast_site_df.loc[(salmoncoast_site_df['datetime'].dt.year == year),
                                         ['datetime', 'salt', 'location']]
        for loc in salmoncoast_locations:
            subset = subset.append({
                'datetime': datetime.datetime(year, 1, 1),
                'location': loc,
                'salt': np.nan
            }, ignore_index=True)
            subset = subset.append({
                'datetime': datetime.datetime(year, 12, 31),
                'location': loc,
                'salt': np.nan
            }, ignore_index=True)
        subset.sort_values('datetime', inplace=True)
        subset_resample = subset.groupby('location').resample(f'W-{get_dow(datetime.datetime(year, 1, 1))}',
                                                              on='datetime', label='left').apply(
            np.nanmean).interpolate(method='linear')
        year_sal_list.append(subset_resample)
    x_wild_sal = pd.concat(year_sal_list)

    return x_wild_sal


def get_industry_counts(industry_df: pd.DataFrame) -> pd.DataFrame:
    """
    Set up industry counts to be used as a predictor
    :param industry_df: IndustrySeaLice_Data.csv
    :return: a data frame of the summarised industry motile counts
    """
    relevant_farm_data = industry_df[industry_df['Site Common Name'].str.contains('|'.join(relevant_farms_iterable))]
    relevant_farm_data['Day'] = 1
    relevant_farm_data['month'] = relevant_farm_data['Month'].map(month_map)
    relevant_farm_data['datetime'] = pd.to_datetime(relevant_farm_data[['Year', 'month', 'Day']])

    relevant_farm_data = relevant_farm_data[relevant_farm_data['datetime'].dt.year.isin(analysis_years)]

    year_industry_list = []
    for year in analysis_years:
        subset = relevant_farm_data.loc[(relevant_farm_data['datetime'].dt.year == year),
                                        ['datetime', 'Site Common Name', 'Average L. salmonis motiles per fish']]

        for i, farm in enumerate(relevant_farms_iterable):
            subset = subset.append({
                'datetime': datetime.datetime(year, 1, 1),
                'Site Common Name': farm,
                'Average L. salmonis motiles per fish': np.nan
            }, ignore_index=True)
            subset = subset.append({
                'datetime': datetime.datetime(year, 12, 31),
                'Site Common Name': farm,
                'Average L. salmonis motiles per fish': np.nan
            }, ignore_index=True)

        subset.sort_values('datetime', inplace=True)
        subset_resample = subset.groupby('Site Common Name').resample(f'W-{get_dow(datetime.datetime(year, 1, 1))}',
                                                                      on='datetime', label='left').apply(
            np.nanmean).interpolate(methods='linear')
        year_industry_list.append(subset_resample)
    x_industry = pd.concat(year_industry_list)

    return x_industry

