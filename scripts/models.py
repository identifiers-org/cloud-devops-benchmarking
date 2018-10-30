# 
# Project   : cloud-devops-benchmarking
# Timestamp : 30-10-2018 9:45
# Author    : Manuel Bernal Llinares <mbdebian@gmail.com>
# ---
# 

"""
This module contains data models used by the benchmarking scripts
"""


class ResponseTimeEntry:
    def __init__(self, url=None, status=None, error=None, response_time=None):
        self.url = url
        self.status = status
        self.error = error
        self.response_time = response_time