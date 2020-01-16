import numpy as np
from typing import Dict
from sklearn.preprocessing import MinMaxScaler


def scale_x_array(xarray: np.array) -> (np.array, Dict):
    X_scale = np.copy(xarray)
    scalers_x = {}
    for i in range(xarray.shape[1]):
        scalers_x[i] = MinMaxScaler(feature_range=(-1, 1))
        X_scale[:, i, :] = scalers_x[i].fit_transform(xarray[:, i, :])
    X_scale = np.nan_to_num(X_scale)
    scaled_with_scalers = (X_scale, scalers_x)

    return scaled_with_scalers


def scale_y_array(yarray: np.array) -> (np.array, Dict):
    Y_scale = np.copy(yarray)
    scalers_y = {}
    for i in range(yarray.shape[1]):
        scalers_y[i] = MinMaxScaler(feature_range=(-1, 1))
        Y_scale[:, i, :] = scalers_y[i].fit_transform(yarray[:, i, :])
    Y_scale = np.nan_to_num(Y_scale)
    scaled_with_scalers = (Y_scale, scalers_y)

    return scaled_with_scalers
