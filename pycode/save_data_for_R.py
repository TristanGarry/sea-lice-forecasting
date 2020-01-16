import pandas as pd
import pycode.SLdatahandling as datahandling

data_dir = '../data/'

# importing the Salmoncoast and Industry data
fish_data = pd.read_csv(f'{data_dir}BroughtonSeaLice_fishData.csv', encoding='ISO-8859-1', low_memory=False)
site_data = pd.read_csv(f'{data_dir}BroughtonSeaLice_siteData.csv', encoding='ISO-8859-1', low_memory=False)
industry_data = pd.read_csv(f'{data_dir}IndustrySeaLice_Data.csv', encoding='ISO-8859-1', low_memory=False)

# Save the data for R
datahandling.get_predictor_df(fish_data, site_data, industry_data).to_csv(f'../xdata/predictor_data.csv')
datahandling.get_motile_df(fish_data).to_csv(f'../xdata/response_data.csv')


