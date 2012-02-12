#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2011, Mike Taylor
#
# This file is part of datio released under MIT license.
# See the LICENSE for more information.
"""

Test the core module.

"""

import sys
import os
import unittest

libpath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if not libpath in sys.path:
    sys.path.insert(1, libpath)
del libpath

from core import Series
from core import csv2lol
from core import lol2dol
from core import format_values


class Series_TestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_new_none(self):
        self.assertRaises(ValueError, Series)

    def test_new_args(self):
        series = Series('row1', 'row2', 'row3')
        self.assertEquals(series.keys(), ['row1', 'row2', 'row3'])
        self.assertEquals(series.values(), [])

    def test_new_args_num(self):
        series = Series('1', '2', '3')
        self.assertEquals(series.keys(), ['_1', '_2', '_3'])
        self.assertEquals(series._1, [])
        self.assertEquals(series._2, [])
        self.assertEquals(series._3, [])
        self.assertEquals(series.values(), [])

    def test_lol_single(self):
        values = [[0, 'yhoo', 23.0]]
        series = Series('0', '1', '2')
        series.from_values(values)
        self.assertEquals(series._0, [0])
        self.assertEquals(series._1, ['yhoo'])
        self.assertEquals(series._2, [23.0])
        self.assertEquals(len(series), 1)

    def test_lol_multi(self):
        series = Series('0', '1', '2')
        values = [[0, 'yhoo', 23.0], [1, 'goog', 200]]
        series.from_values(values)
        self.assertEquals(series._0, [0, 1])
        self.assertEquals(series._1, ['yhoo', 'goog'])
        self.assertEquals(series._2, [23.0, 200])
        self.assertEquals(len(series), 2)

    def test_lol_args_extra(self):
        series = Series('bar', 'symbol', 'close', 'open')
        values = [[0, 'yhoo', 23.0], [1, 'goog', 200]]
        series.from_values(values)
        self.assertEquals(series.bar, [0, 1])
        self.assertEquals(series.symbol, ['yhoo', 'goog'])
        self.assertEquals(series.close, [23.0, 200])
        self.assertEquals(series.open, [None, None])
        self.assertEquals(len(series), 2)

    def test_lol_kwargs_all(self):
        series = Series('bar', 'symbol', 'close')
        values = [[0, 'yhoo', 23.0], [1, 'goog', 200]]
        series.from_values(values, 'bar', 'symbol')
        self.assertEquals(series.bar, [0, 1])
        self.assertEquals(series.symbol, ['yhoo', 'goog'])
        self.assertEquals(series.close, [None, None])
        self.assertEquals(len(series), 2)

    def test_lol_kwargs_all(self):
        series = Series('bar', 'symbol', 'close')
        values = [[0, 'yhoo', 23.0], [1, 'goog', 200]]
        series.from_values(values, 'bar', close=2, open=1)
        self.assertEquals(series.keys(), ['bar', 'symbol', 'close'])
        self.assertEquals(series.bar, [0, 1])
        self.assertEquals(series.symbol, [None, None])
        self.assertEquals(series.close, [23.0, 200])
        self.assertEquals(len(series), 2)

    def test_lod_single(self):
        values = [dict(bar=0, symbol='yhoo', close=23.0)]
        series = Series('bar', 'symbol', 'close')
        series.from_values(values)
        self.assertEquals(series.keys(), ['bar', 'symbol', 'close'])
        self.assertEquals(series.bar, [0])
        self.assertEquals(series.symbol, ['yhoo'])
        self.assertEquals(series.close, [23.0])
        self.assertEquals(len(series), 1)

    def test_lod_multi(self):
        values = [dict(bar=0, symbol='yhoo', close=23.0)]
        values.append(dict(bar=1, symbol='goog', close=200))
        series = Series('bar', 'symbol', 'close')
        series.from_values(values)
        self.assertEquals(series.keys(), ['bar', 'symbol', 'close'])
        self.assertEquals(series.bar, [0, 1])
        self.assertEquals(series.symbol, ['yhoo', 'goog'])
        self.assertEquals(series.close, [23.0, 200])
        self.assertEquals(len(series), 2)

    def test_lod_args_all(self):
        values = [dict(bar=0, symbol='yhoo', close=23.0)]
        values.append(dict(bar=1, symbol='goog', close=200))
        series = Series('bar', 'symbol', 'close')
        series.from_values(values, 'bar', 'symbol', 'close')
        self.assertEquals(series.keys(), ['bar', 'symbol', 'close'])
        self.assertEquals(series.bar, [0, 1])
        self.assertEquals(series.symbol, ['yhoo', 'goog'])
        self.assertEquals(series.close, [23.0, 200])
        self.assertEquals(len(series), 2)

    def test_lod_args_missing(self):
        values = [dict(bar=0, symbol='yhoo', close=23.0)]
        values.append(dict(bar=1, symbol='goog', close=200))
        series = Series('bar', 'symbol', 'close')
        series.from_values(values, 'bar', 'symbol')
        self.assertEquals(series.keys(), ['bar', 'symbol', 'close'])
        self.assertEquals(series.bar, [0, 1])
        self.assertEquals(series.symbol, ['yhoo', 'goog'])
        self.assertEquals(series.close, [None, None])
        self.assertEquals(len(series), 2)

    def test_lod_kwargs(self):
        values = [dict(bar=0, symbol='yhoo', close=23.0)]
        values.append(dict(bar=1, symbol='goog', close=200))
        series = Series('bar', 'symbol', 'close')
        series.from_values(values, bar='bar', close='close')
        self.assertEquals(series.keys(), ['bar', 'symbol', 'close'])
        self.assertEquals(series.bar, [0, 1])
        self.assertEquals(series.symbol, [None, None])
        self.assertEquals(series.close, [23.0, 200])
        self.assertEquals(len(series), 2)

    def test_clear_series(self):
        values = [[0, 'yhoo', 23.0], [1, 'goog', 200]]
        series = Series('bar', 'symbol', 'close')
        series.from_values(values)
        self.assertEquals(len(series), 2)
        series.clear()
        self.assertEquals(len(series), 0)

    def test_format_float(self):
        values = [[0, 'yhoo', 23.0], [1, 'goog', 200]]
        series = Series('bar', 'symbol', 'close')
        series.from_values(values)
        series.format('close', float)
        self.assertEquals(series.close, [23.0, 200.0])

    def test_format_int(self):
        values = [[0, 'yhoo', 23.0], [1, 'goog', 200]]
        series = Series('bar', 'symbol', 'close')
        series.from_values(values)
        series.format('close', int)
        self.assertEquals(series.close, [23, 200])

    def test_format_str(self):
        values = [[0, 'yhoo', 23.0], [1, 'goog', 200]]
        series = Series('bar', 'symbol', 'close')
        series.from_values(values)
        series.format('close', str)
        self.assertEquals(series.close, ['23.0', '200'])

    def test_append_list_args_none(self):
        values = [[0, 'yhoo', 23.0]]
        series = Series('bar', 'symbol', 'close')
        series.from_values(values)
        series.append([1, 'goog', 200])

        self.assertEquals(series.bar, [0, 1])
        self.assertEquals(series.symbol, ['yhoo', 'goog'])
        self.assertEquals(series.close, [23.0, 200])
        self.assertEquals(len(series), 2)

    def test_append_list_args_some(self):
        values = [[0, 'yhoo', 23.0]]
        series = Series('bar', 'symbol', 'close')
        series.from_values(values)

        series.append([1, 'goog', 200], 'bar', 'symbol')

        self.assertEquals(series.bar, [0, 1])
        self.assertEquals(series.symbol, ['yhoo', 'goog'])
        self.assertEquals(series.close, [23.0, None])
        self.assertEquals(len(series), 2)

    def test_append_list_kwargs_some(self):
        values = [[0, 'yhoo', 23.0]]
        series = Series('bar', 'symbol', 'close')
        series.from_values(values)

        series.append([1, 'goog', 200], symbol=1)

        self.assertEquals(series.bar, [0, None])
        self.assertEquals(series.symbol, ['yhoo', 'goog'])
        self.assertEquals(series.close, [23.0, None])
        self.assertEquals(len(series), 2)

    def test_append_list_args_kwargs(self):
        values = [[0, 'yhoo', 23.0]]
        series = Series('bar', 'symbol', 'close')
        series.from_values(values)

        series.append([1, 'goog', 200], 'bar', symbol=1)

        self.assertEquals(series.bar, [0, 1])
        self.assertEquals(series.symbol, ['yhoo', 'goog'])
        self.assertEquals(series.close, [23.0, None])
        self.assertEquals(len(series), 2)

    def test_append_generator(self):
        values = [[0, 'yhoo', 23.0], [1, 'goog', 200]]
        newvalues = (x for x in values)

        series = Series('bar', 'symbol', 'close')
        series.from_values(values)

        self.assertEquals(series.keys(), ['bar', 'symbol', 'close'])
        self.assertEquals(series[0], (0, 'yhoo', 23.0))
        self.assertEquals(series[1], (1, 'goog', 200))
        self.assertEquals(len(series), 2)

    def test_append_dict_args_none(self):
        values = [dict(bar=0, symbol='yhoo', close=23.0)]
        series = Series('bar', 'symbol', 'close')
        series.from_values(values)
        series.append(dict(bar=1, symbol='goog', close=200))

        self.assertEquals(series.bar, [0, 1])
        self.assertEquals(series.symbol, ['yhoo', 'goog'])
        self.assertEquals(series.close, [23.0, 200])
        self.assertEquals(len(series), 2)

    def test_append_dict_args_some(self):
        values = [dict(bar=0, symbol='yhoo', close=23.0)]
        series = Series('bar', 'symbol', 'close')
        series.from_values(values)
        values = dict(bar=1, symbol='goog', close=200)
        series.append(values, 'bar', 'symbol')

        self.assertEquals(series.bar, [0, 1])
        self.assertEquals(series.symbol, ['yhoo', 'goog'])
        self.assertEquals(series.close, [23.0, None])
        self.assertEquals(len(series), 2)

    def test_append_dict_kwargs_some(self):
        values = [dict(bar=0, symbol='yhoo', close=23.0)]
        series = Series('bar', 'symbol', 'close')
        series.from_values(values)
        values = dict(bar=1, symbol='goog', close=200)
        series.append(values, symbol='symbol')

        self.assertEquals(series.bar, [0, None])
        self.assertEquals(series.symbol, ['yhoo', 'goog'])
        self.assertEquals(series.close, [23.0, None])
        self.assertEquals(len(series), 2)

    def test_append_dict_args_kwargs(self):
        values = [dict(bar=0, symbol='yhoo', close=23.0)]
        series = Series('bar', 'symbol', 'close')
        series.from_values(values)
        values = dict(bar=1, symbol='goog', close=200)
        series.append(values, 'bar', symbol='symbol')

        self.assertEquals(series.bar, [0, 1])
        self.assertEquals(series.symbol, ['yhoo', 'goog'])
        self.assertEquals(series.close, [23.0, None])
        self.assertEquals(len(series), 2)

    def test_sort_default(self):
        series = Series('bar', 'symbol', 'close')
        values = [[0, 'yhoo', 23.0], [1, 'goog', 200]]
        series.from_values(values)
        series.sort('symbol')

        self.assertEquals(series.bar, [1, 0])
        self.assertEquals(series.symbol, ['goog', 'yhoo'])
        self.assertEquals(series.close, [200, 23.0])
        self.assertEquals(len(series), 2)

    def test_sort_ascending(self):
        series = Series('bar', 'symbol', 'close')
        values = [[0, 'yhoo', 23.0], [1, 'goog', 200]]
        series.from_values(values)
        series.sort('symbol', order='a')

        self.assertEquals(series.bar, [1, 0])
        self.assertEquals(series.symbol, ['goog', 'yhoo'])
        self.assertEquals(series.close, [200, 23.0])
        self.assertEquals(len(series), 2)

    def test_sort_descending(self):
        series = Series('bar', 'symbol', 'close')
        values = [[0, 'yhoo', 23.0], [1, 'goog', 200]]
        series.from_values(values)
        series.sort('close', order='d')

        self.assertEquals(series.bar, [1, 0])
        self.assertEquals(series.symbol, ['goog', 'yhoo'])
        self.assertEquals(series.close, [200, 23.0])
        self.assertEquals(len(series), 2)

    def test_index_access(self):
        values = [dict(bar=0, symbol='yhoo', close=23.0)]
        series = Series('bar', 'symbol', 'close')
        series.from_values(values)
        values = dict(bar=1, symbol='goog', close=200)
        series.append(values)

        self.assertEquals(series[0], (0, 'yhoo', 23.0))
        self.assertEquals(series[1], (1, 'goog', 200))
        self.assertEquals(len(series), 2)

    def test_iter(self):
        values = [dict(bar=0, symbol='yhoo', close=23.0)]
        series = Series('bar', 'symbol', 'close')
        series.from_values(values)
        values = dict(bar=1, symbol='goog', close=200)
        series.append(values)

        results = []
        for bar in series:
            results.append(bar)

        self.assertEquals(results, [0, 1])

    def test_initcol_new_default(self):
        values = [dict(bar=0, symbol='yhoo', close=23.0)]
        series = Series('bar', 'symbol', 'close')
        series.from_values(values)
        values = dict(bar=1, symbol='goog', close=200)
        series.append(values)

        series.initcol('open')

        self.assertEquals(series.keys(), ['bar', 'symbol', 'close', 'open'])
        self.assertEquals(series[0], (0, 'yhoo', 23.0, None))
        self.assertEquals(series[1], (1, 'goog', 200, None))
        self.assertEquals(len(series), 2)

    def test_initcol_new_0(self):
        values = [dict(bar=0, symbol='yhoo', close=23.0)]
        series = Series('bar', 'symbol', 'close')
        series.from_values(values)
        values = dict(bar=1, symbol='goog', close=200)
        series.append(values)

        series.initcol('open', 0.0)

        self.assertEquals(series.keys(), ['bar', 'symbol', 'close', 'open'])
        self.assertEquals(series[0], (0, 'yhoo', 23.0, 0.0))
        self.assertEquals(series[1], (1, 'goog', 200, 0.0))
        self.assertEquals(len(series), 2)

    def test_initcol_existing_0(self):
        values = [dict(bar=0, symbol='yhoo', close=23.0)]
        series = Series('bar', 'symbol', 'close')
        series.from_values(values)
        values = dict(bar=1, symbol='goog', close=200)
        series.append(values)

        series.initcol('close', 0.0)

        self.assertEquals(series.keys(), ['bar', 'symbol', 'close'])
        self.assertEquals(series[0], (0, 'yhoo', 0.0))
        self.assertEquals(series[1], (1, 'goog', 0.0))
        self.assertEquals(len(series), 2)

    def test_appendcol_values(self):
        values = [dict(bar=0, symbol='yhoo', close=23.0)]
        series = Series('bar', 'symbol', 'close')
        series.from_values(values)
        values = dict(bar=1, symbol='goog', close=200)
        series.append(values)

        series.appendcol('open', [22.0, 21.0])

        self.assertEquals(series.keys(), ['bar', 'symbol', 'close', 'open'])
        self.assertEquals(series[0], (0, 'yhoo', 23.0, 22.0))
        self.assertEquals(series[1], (1, 'goog', 200, 21.0))
        self.assertEquals(len(series), 2)

    def test_appendcol_valuesbad(self):
        values = [dict(bar=0, symbol='yhoo', close=23.0)]
        series = Series('bar', 'symbol', 'close')
        series.from_values(values)
        values = dict(bar=1, symbol='goog', close=200)
        series.append(values)

        self.assertRaises(ValueError, series.appendcol, 'open', [22.0])


class Csv2lol_TestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_missing_file(self):
        """
        """
        self.assertRaises(IOError, csv2lol, 'testfiles/csv2lol_blah.csv')

    def test_empty_file(self):
        """
        """
        keys, values = csv2lol('testfiles/csv2lol_empty.csv')
        self.assertEquals(keys, [])
        self.assertEquals(values, [])

    def test_header_no(self):
        """
        """
        keys, values = csv2lol('testfiles/csv2lol_header_no.csv')
        self.assertEquals(keys, [0, 1, 2])
        self.assertEquals(values[0], ['2011-11-23', '34.01', 'yhoo'])
        self.assertEquals(values[1], ['2011-11-22', '34.64', 'yhoo'])
        self.assertEquals(len(values), 2)

    def test_header_no_with_header(self):
        """
        """
        keys, values = csv2lol('testfiles/csv2lol_header_yes.csv')
        self.assertEquals(keys, [0, 1, 2])
        self.assertEquals(values[0], ['Date', 'Open', 'Symbol'])
        self.assertEquals(values[1], ['2011-11-23', '34.01', 'yhoo'])
        self.assertEquals(values[2], ['2011-11-22', '34.64', 'yhoo'])
        self.assertEquals(len(values), 3)

    def test_header_yes(self):
        """
        """
        keys, values = csv2lol('testfiles/csv2lol_header_yes.csv', header=True)
        self.assertEquals(keys, ['Date', 'Open', 'Symbol'])
        self.assertEquals(values[0], ['2011-11-23', '34.01', 'yhoo'])
        self.assertEquals(values[1], ['2011-11-22', '34.64', 'yhoo'])
        self.assertEquals(len(values), 2)

    def test_header_yes_with_noheader(self):
        """
        """
        keys, values = csv2lol('testfiles/csv2lol_header_no.csv', header=True)
        self.assertEquals(keys, ['2011-11-23', '34.01', 'yhoo'])
        self.assertEquals(values[0], ['2011-11-22', '34.64', 'yhoo'])
        self.assertEquals(len(values), 1)


class Lol2dol_TestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_none(self):
        """
        """
        dol = lol2dol()
        self.assertEquals(dol, {})

    def test_empty(self):
        """
        """
        values = []
        dol = lol2dol(values)
        self.assertEquals(dol, {})

    def test_lol_single(self):
        """
        """
        values = [0, 'yhoo', 23.0]
        dol = lol2dol([values])
        self.assertEquals(dol[0], [0])
        self.assertEquals(dol[1], ['yhoo'])
        self.assertEquals(dol[2], [23.0])
        self.assertEquals(len(dol), 3)

    def test_lol_multi(self):
        """
        """
        values = [[0, 'yhoo', 23.0], [1, 'goog', 200]]
        dol = lol2dol(values)
        self.assertEquals(dol[0], [0, 1])
        self.assertEquals(dol[1], ['yhoo', 'goog'])
        self.assertEquals(dol[2], [23.0, 200])
        self.assertEquals(len(dol), 3)

    def test_nolol_args_all(self):
        """
        """
        dol = lol2dol([], 'bar', 'symbol', 'close')
        self.assertEquals(dol['bar'], [])
        self.assertEquals(dol['symbol'], [])
        self.assertEquals(dol['close'], [])
        self.assertEquals(len(dol), 3)

    def test_lol_args_all(self):
        """
        """
        values = [[0, 'yhoo', 23.0], [1, 'goog', 200]]
        dol = lol2dol(values, 'bar', 'symbol', 'close')
        self.assertEquals(dol['bar'], [0, 1])
        self.assertEquals(dol['symbol'], ['yhoo', 'goog'])
        self.assertEquals(dol['close'], [23.0, 200])
        self.assertEquals(len(dol), 3)

    def test_lol_args_partial(self):
        """
        """
        values = [[0, 'yhoo', 23.0], [1, 'goog', 200]]
        dol = lol2dol(values, 'bar', 'symbol')
        self.assertEquals(dol['bar'], [0, 1])
        self.assertEquals(dol['symbol'], ['yhoo', 'goog'])
        self.assertEquals(len(dol), 2)

    def test_lol_args_extra(self):
        """
        """
        values = [[0, 'yhoo', 23.0], [1, 'goog', 200]]
        dol = lol2dol(values, 'bar', 'symbol', 'close', 'open')
        self.assertEquals(dol['bar'], [0, 1])
        self.assertEquals(dol['symbol'], ['yhoo', 'goog'])
        self.assertEquals(dol['close'], [23.0, 200])
        self.assertEquals(dol['open'], [None, None])
        self.assertEquals(len(dol), 4)

    def test_lol_kwargs_all(self):
        """
        """
        values = [[0, 'yhoo', 23.0], [1, 'goog', 200]]
        dol = lol2dol(values, bar=0, symbol=1, close=2)
        self.assertEquals(dol['bar'], [0, 1])
        self.assertEquals(dol['symbol'], ['yhoo', 'goog'])
        self.assertEquals(dol['close'], [23.0, 200])
        self.assertEquals(len(dol), 3)

    def test_nolol_kwargs_all(self):
        """
        """
        dol = lol2dol([], bar=0, symbol=1, close=2)
        self.assertEquals(dol['bar'], [])
        self.assertEquals(dol['symbol'], [])
        self.assertEquals(dol['close'], [])
        self.assertEquals(len(dol), 3)

    def test_lol_kwargs_partial(self):
        """
        """
        values = [[0, 'yhoo', 23.0], [1, 'goog', 200]]
        dol = lol2dol(values, bar=0, close=2)
        self.assertEquals(dol['bar'], [0, 1])
        self.assertEquals(dol['close'], [23.0, 200])
        self.assertEquals(len(dol), 2)

    def test_lol_kwargs_extra(self):
        """
        """
        values = [[0, 'yhoo', 23.0], [1, 'goog', 200]]
        dol = lol2dol(values, bar=0, close=2, open=3)
        self.assertEquals(dol['bar'], [0, 1])
        self.assertEquals(dol['close'], [23.0, 200])
        self.assertEquals(dol['open'], [None, None])
        self.assertEquals(len(dol), 3)

    def test_lol_args_and_kwargs(self):
        """
        """
        values = [[0, 'yhoo', 23.0], [1, 'goog', 200]]
        dol = lol2dol(values, 'bar', 'symbol', close=2)
        self.assertEquals(dol['bar'], [0, 1])
        self.assertEquals(dol['symbol'], ['yhoo', 'goog'])
        self.assertEquals(dol['close'], [23.0, 200])
        self.assertEquals(len(dol), 3)

    def test_dol_single(self):
        """
        """
        values = dict(bar=0, symbol='yhoo', close=23.0)
        dol = lol2dol([values])
        self.assertEquals(dol['bar'], [0])
        self.assertEquals(dol['symbol'], ['yhoo'])
        self.assertEquals(dol['close'], [23.0])
        self.assertEquals(len(dol), 3)

    def test_dol_multi(self):
        """
        """
        values = []
        values.append(dict(bar=0, symbol='yhoo', close=23.0))
        values.append(dict(bar=1, symbol='goog', close=200))

        dol = lol2dol(values)
        self.assertEquals(dol['bar'], [0, 1])
        self.assertEquals(dol['symbol'], ['yhoo', 'goog'])
        self.assertEquals(dol['close'], [23.0, 200])
        self.assertEquals(len(dol), 3)

    def test_dol_args_all(self):
        """
        """
        values = []
        values.append(dict(bar=0, symbol='yhoo', close=23.0))
        values.append(dict(bar=1, symbol='goog', close=200))

        dol = lol2dol(values, 'bar', 'symbol', 'close')
        self.assertEquals(dol['bar'], [0, 1])
        self.assertEquals(dol['symbol'], ['yhoo', 'goog'])
        self.assertEquals(dol['close'], [23.0, 200])
        self.assertEquals(len(dol), 3)

    def test_dol_args_partial(self):
        """
        """
        values = []
        values.append(dict(bar=0, symbol='yhoo', close=23.0))
        values.append(dict(bar=1, symbol='goog', close=200))

        dol = lol2dol(values, 'bar', 'symbol')
        self.assertEquals(dol['bar'], [0, 1])
        self.assertEquals(dol['symbol'], ['yhoo', 'goog'])
        self.assertEquals(len(dol), 2)

    def test_dol_args_extra(self):
        """
        """
        values = []
        values.append(dict(bar=0, symbol='yhoo', close=23.0))
        values.append(dict(bar=1, symbol='goog', close=200))

        dol = lol2dol(values, 'bar', 'symbol', 'close', 'open')
        self.assertEquals(dol['bar'], [0, 1])
        self.assertEquals(dol['symbol'], ['yhoo', 'goog'])
        self.assertEquals(dol['close'], [23.0, 200])
        self.assertEquals(dol['open'], [None, None])
        self.assertEquals(len(dol), 4)

    def test_dol_kwargs_all(self):
        """
        """
        values = []
        values.append(dict(bar=0, symbol='yhoo', close=23.0))
        values.append(dict(bar=1, symbol='goog', close=200))

        dol = lol2dol(values, Bar='bar', Symbol='symbol', Close='close')
        self.assertEquals(dol['Bar'], [0, 1])
        self.assertEquals(dol['Symbol'], ['yhoo', 'goog'])
        self.assertEquals(dol['Close'], [23.0, 200])
        self.assertEquals(len(dol), 3)

    def test_dol_kwargs_partial(self):
        """
        """
        values = []
        values.append(dict(bar=0, symbol='yhoo', close=23.0))
        values.append(dict(bar=1, symbol='goog', close=200))

        dol = lol2dol(values, bar='bar', close='close')
        self.assertEquals(dol['bar'], [0, 1])
        self.assertEquals(dol['close'], [23.0, 200])
        self.assertEquals(len(dol), 2)

    def test_dol_kwargs_extra(self):
        """
        """
        values = []
        values.append(dict(bar=0, symbol='yhoo', close=23.0))
        values.append(dict(bar=1, symbol='goog', close=200))

        dol = lol2dol(values, bar='bar', close='close', open='open')
        self.assertEquals(dol['bar'], [0, 1])
        self.assertEquals(dol['close'], [23.0, 200])
        self.assertEquals(dol['open'], [None, None])
        self.assertEquals(len(dol), 3)

    def test_lol_args_and_kwargs(self):
        """
        """
        values = []
        values.append(dict(bar=0, symbol='yhoo', close=23.0))
        values.append(dict(bar=1, symbol='goog', close=200))

        dol = lol2dol(values, 'bar', 'symbol', Close='close')
        self.assertEquals(dol['bar'], [0, 1])
        self.assertEquals(dol['symbol'], ['yhoo', 'goog'])
        self.assertEquals(dol['Close'], [23.0, 200])
        self.assertEquals(len(dol), 3)


class Format_values_TestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_str_to_ints(self):
        values = ['0', '1.0', '2', None, '4.3']
        results = format_values(values, int)
        self.assertEquals(results, [0, 1, 2, None, 4])

    def test_str_to_floats(self):
        values = ['0', '1.1', '2', None, '4.3']
        results = format_values(values, float)
        self.assertEquals(results, [0.0, 1.1, 2.0, None, 4.3])

    def test_str_to_datetimes(self):
        from datetime import datetime

        values = ['19970101', '19970102', '19970103']
        results = format_values(values, datetime.strptime, '%Y%m%d')

        self.assertEquals(results[0].__str__(), '1997-01-01 00:00:00')
        self.assertEquals(results[1].__str__(), '1997-01-02 00:00:00')
        self.assertEquals(results[2].__str__(), '1997-01-03 00:00:00')

    def test_ints_to_ints(self):
        values = [0, 1, 2, None, 4]
        results = format_values(values, int)
        self.assertEquals(results, [0, 1, 2, None, 4])

    def test_ints_to_strs(self):
        values = [0, 1, 2, None, 4]
        results = format_values(values, str)
        self.assertEquals(results, ['0', '1', '2', None, '4'])

    def test_ints_to_floats(self):
        values = [0, 1, 2, None, 4]
        results = format_values(values, float)
        self.assertEquals(results, [0.0, 1.0, 2.0, None, 4.0])

    def test_ints_to_datetimes(self):
        from datetime import datetime

        values = [19970101, 19970102, 19970103]
        results = format_values(values, datetime.strptime, '%Y%m%d')

        self.assertEquals(results[0].__str__(), '1997-01-01 00:00:00')
        self.assertEquals(results[1].__str__(), '1997-01-02 00:00:00')
        self.assertEquals(results[2].__str__(), '1997-01-03 00:00:00')

    def test_floats_to_ints(self):
        values = [0.0, 1.7, 2.22, None, 4.2]
        results = format_values(values, int)
        self.assertEquals(results, [0, 1, 2, None, 4])

    def test_floats_to_strs(self):
        values = [0.0, 1.7, 2.22, None, 4.2]
        results = format_values(values, str)
        self.assertEquals(results, ['0.0', '1.7', '2.22', None, '4.2'])

    def test_floats_to_floats(self):
        values = [0.0, 1.7, 2.22, None, 4.2]
        results = format_values(values, float)
        self.assertEquals(results, [0.0, 1.7, 2.22, None, 4.2])


if __name__ == "__main__":
    unittest.main()
