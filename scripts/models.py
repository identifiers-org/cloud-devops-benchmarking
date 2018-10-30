# 
# Project   : cloud-devops-benchmarking
# Timestamp : 30-10-2018 9:45
# Author    : Manuel Bernal Llinares <mbdebian@gmail.com>
# ---
# 

"""
This module contains data models used by the benchmarking scripts
"""

import pandas as pd
from scipy import stats


# NOTE - I think I won't need this level of abstraction, I can remove it later
class ResponseTimeEntry:
    def __init__(self, url=None, status=None, error=None, response_time=None):
        self.url = url
        self.status = status
        self.error = error
        self.response_time = response_time


class ResponseTimeDataset:
    RESPONSE_TIME_DATASET_KEY_URL = 'url'
    RESPONSE_TIME_DATASET_KEY_STATUS = 'status'
    RESPONSE_TIME_DATASET_KEY_ERROR = 'error'
    RESPONSE_TIME_DATASET_KEY_RESPONSE_TIME = 'Response_Time(ms)'
    RESPONSE_TIME_DATASET_VALUE_STATUS_ERROR = 'ERROR'
    RESPONSE_TIME_DATASET_VALUE_STATUS_OK = 'OK'
    # Columns
    RESPONSE_TIME_DATASET_COLUMNS = [RESPONSE_TIME_DATASET_KEY_STATUS,
                                     RESPONSE_TIME_DATASET_KEY_RESPONSE_TIME,
                                     RESPONSE_TIME_DATASET_KEY_URL,
                                     RESPONSE_TIME_DATASET_KEY_ERROR]

    def __init__(self):
        self.entries = pd.DataFrame(columns=self.RESPONSE_TIME_DATASET_COLUMNS)

    def get_new_index(self):
        self.__index += 1
        return self.__index - 1

    def get_data_entry_from_response_time_entry(self, response_time_entry):
        return {self.RESPONSE_TIME_DATASET_KEY_STATUS: response_time_entry.status,
                self.RESPONSE_TIME_DATASET_KEY_RESPONSE_TIME: response_time_entry.response_time,
                self.RESPONSE_TIME_DATASET_KEY_URL: response_time_entry.url,
                self.RESPONSE_TIME_DATASET_KEY_ERROR: response_time_entry.error}

    def add_entry(self, response_time_entry):
        self.entries = self.entries.append(self.get_data_entry_from_response_time_entry(response_time_entry), ignore_index=True)

    def get_entries_dataframe(self):
        return self.entries

    def get_number_of_entries(self):
        return self.entries.shape[0]

    def get_successful_entries(self):
        return self.entries[self.entries[self.RESPONSE_TIME_DATASET_KEY_RESPONSE_TIME].notnull()]

    def get_error_entries(self):
        return self.entries[self.entries[self.RESPONSE_TIME_DATASET_KEY_RESPONSE_TIME].isnull()]

    def get_number_success_entries(self):
        return len(self.get_successful_entries())

    def get_number_error_entries(self):
        return len(self.get_error_entries())

    def get_response_time_arithmetic_mean(self):
        return self.get_successful_entries()[self.RESPONSE_TIME_DATASET_KEY_RESPONSE_TIME].mean()

    def get_response_time_median(self):
        return self.get_successful_entries()[self.RESPONSE_TIME_DATASET_KEY_RESPONSE_TIME].median()

    def get_response_time_mode(self):
        return self.get_successful_entries()[self.RESPONSE_TIME_DATASET_KEY_RESPONSE_TIME].mode()

    def get_response_time_standard_deviation(self):
        return self.get_successful_entries()[self.RESPONSE_TIME_DATASET_KEY_RESPONSE_TIME].std()

    def to_csv(self, file_path):
        self.entries.to_csv(file_path)

    def stats_to_csv(self, file_path):
        columns = ['# Tests',
                   '# Success',
                   '# Error',
                   'Mean Response Time(ms)',
                   'Mode Response Time(ms)',
                   'Median Response Time(ms)',
                   'Standard Deviation(ms)']
        data = [self.get_number_of_entries(),
                self.get_number_success_entries(),
                self.get_number_error_entries(),
                self.get_response_time_arithmetic_mean(),
                self.get_response_time_mode(),
                self.get_response_time_median(),
                self.get_response_time_standard_deviation()]
        df = pd.DataFrame(data, columns=columns)
        df.to_csv(file_path)




if __name__ == '__main__':
    print("")