import numpy as np
import pandas as pd

class TimeSeriesKFold():

    """Time series cross-validator with time-based field
    
    Parameters
    ----------
        time_colname: str
            name of column with timestamps to rely on
        train_period: int, default=1
            number of unique time points from X[time_colname] series
            to use for train iteration
        blocking: bool, default=False
            wether to use block concept (expand training period or not)
    """
    
    def __init__(self, time_colname, train_period=1, blocking=False):
        self.time_colname = time_colname
        self.train_period = train_period
        self.block = blocking
    
    def get_n_splits(self, X, y, groups):
        return self.n_splits
    
    def split(self, X, y=None, groups=None):
        dt_arr = X[self.time_colname].sort_values().unique()
        n_samples = X[self.time_colname].nunique()
        self.n_splits = n_samples - self.train_period

        for i in range(self.n_splits):
            j = i if self.block else 0
            dt_train_arr = dt_arr[j:i+self.train_period]
            dt_test_arr = dt_arr[i+self.train_period]
            train_idx = X[X[self.time_colname].isin(dt_train_arr)].index.values
            test_idx = X[X[self.time_colname] == dt_test_arr].index.values
            yield train_idx, test_idx
