#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

"""
This module fetch raw data from BaoStock and try not to manipulate any byte.
The raw data should be feed to other module for further processing, only pd.DataFrame is returned.
"""
from abc import ABCMeta, abstractmethod
import pandas as pd
import baostock as bs
from enum import Enum


# TODO: TWAP/VWAP price calculation. move to utility package
# TODO: provide BaoStock API for daily/N-minutes bar
# TODO: BaoStock origin data provides more K-bar data than other sources,
#  thus there should be an option for switch on/off


class DivAdjType(Enum):
    Backward = '1'
    backward = '1'
    BACKWARD = '1'
    Forward = '2'
    forward = '2'
    FORWARD = '2'
    Non = '3'
    non = '3'
    NON = '3'


class BaoStock(object):
    __metaclass__ = ABCMeta

    def __init__(self, symbols: list, startDate: str, endDate: str, dividend_adjustment: str, use_unique_fields: bool):
        if not isinstance(symbols, list):
            raise TypeError("symbols should be list type.")
        self.symbols = symbols
        self.startDate = startDate
        self.endDate = endDate
        self.dividend_adjustment = dividend_adjustment
        self.use_unique_fields = use_unique_fields
        lg = bs.login()
        if lg.error_code != '0':
            print("login respond error_code: ", lg.error_code)
            print("login respond error_msg: ", lg.error_msg)
            raise RuntimeError("BaoStock login failed, try to subscribe another data sources.")
        else:
            print("BaoStock data subscription succeed.")

    @abstractmethod
    def get_k_bars(self):
        raise NotImplementedError("Should implement get_k_bars()")

    @abstractmethod
    def feed_k_bars(self):
        raise NotImplementedError("Should implement feed_k_bars()")


class GetDailyBars(BaoStock):
    def __init__(self, symbols: list, startDate: str, endDate: str,
                 dividend_adjustment: str = DivAdjType.NON.value,
                 use_unique_fields: bool = False):
        super(GetDailyBars, self).__init__(symbols, startDate, endDate, dividend_adjustment, use_unique_fields)

    def get_k_bars(self):
        data = []
        for symbol in self.symbols:
            singleData = []
            if not self.use_unique_fields:
                rs = bs.query_history_k_data_plus(symbol, "date, code, open, high, low, close, volume, amount",
                                                  start_date=self.startDate, end_date=self.endDate, frequency='D',
                                                  adjustflag=self.dividend_adjustment)
            else:
                rs = bs.query_history_k_data_plus(symbol,
                                                  "date, code, open, high, low, close, volume, amount, preclose, "
                                                  "adjustflag, turn, tradestatus, pctChg, peTTM, psTTM, pcfNcfTTM, "
                                                  "pbMRQ, isST",
                                                  start_date=self.startDate, end_date=self.endDate, frequency='D',
                                                  adjustflag=self.dividend_adjustment)
            while (rs.error_code == '0') & rs.next():
                singleData.append(rs.get_row_data())
            dfResult = pd.DataFrame(singleData, columns=rs.fields)
            data.append(dfResult)
        return pd.concat(data)

    def feed_k_bars(self):
        pass


class GetMinuteBars(BaoStock):
    def __init__(self, symbols: list, startDate: str, endDate: str, use_unique_fields: bool):
        super(GetMinuteBars, self).__init__(symbols, startDate, endDate, use_unique_fields)

    def get_k_bars(self):
        pass

    def feed_k_bars(self):
        pass
