import pandas as pd
import pycode.SLdatahandling.make_datasets as datahandling
import pycode.SLdatahandling.process_to_array as arrayfuncs

data_dir = '../data/'

# importing the Salmoncoast and Industry data
fish_data = pd.read_csv(f'{data_dir}BroughtonSeaLice_fishData.csv', encoding='ISO-8859-1', low_memory=False)
site_data = pd.read_csv(f'{data_dir}BroughtonSeaLice_siteData.csv', encoding='ISO-8859-1', low_memory=False)
industry_data = pd.read_csv(f'{data_dir}IndustrySeaLice_Data.csv', encoding='ISO-8859-1', low_memory=False)

wild_locations = site_data['location'].unique()

# Get data frames to convert to numpy arrays
juvenile_df = datahandling.get_juv_counts(fish_data, wild_locations)
temp_df = datahandling.get_temps(site_data, wild_locations)
salinity_df = datahandling.get_sals(site_data, wild_locations)
industry_counts_df = datahandling.get_industry_counts(industry_data)
Y_df = datahandling.get_motile_df(fish_data)

X_array = arrayfuncs.unpack_and_create_x_array([juvenile_df, temp_df, salinity_df, industry_counts_df])
Y_array = arrayfuncs.unpack_and_create_y_array(Y_df)
