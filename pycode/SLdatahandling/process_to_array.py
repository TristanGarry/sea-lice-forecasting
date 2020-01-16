import numpy as np
import pandas as pd

analysis_years = list(range(2003, 2018))
analysis_months = list(range(3, 7))


def unpack_and_create_x_array(dfs_to_process: list[pd.DataFrame]) -> np.array:
    overall_arrays_to_stack = []
    for year in analysis_years:
        year_list = []
        for df in dfs_to_process:
            year_list.append(df[(df.index.get_level_values(1).year == year) &
                             df.index.get_level_values(1).month.isin(analysis_months)].\
                             unstack().T.values, axis=1)
        year_array = np.column_stack(year_list)
        overall_arrays_to_stack.append(year_array)
    x_array = np.stack(overall_arrays_to_stack, axis=0)

    return x_array


def unpack_and_create_y_array(df_to_process: pd.DataFrame) -> np.array:
    overall_arrays_to_stack = []
    for year in analysis_years:
        overall_arrays_to_stack.append(df_to_process[(df_to_process.index.year == year) &
                                       df_to_process.index.month.isin(analysis_months)].values)
    y_array = np.stack(overall_arrays_to_stack, axis=0)

    return y_array
