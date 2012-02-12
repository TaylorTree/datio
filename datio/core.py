#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2011, Mike Taylor
#
# This file is part of datio released under MIT license.
# See the LICENSE for more information.
"""

Efficiently process data by column or row.

Terminology used
================
    * dol -- dict of lists
    * lod -- list of dicts
    * lol -- list of lists or tuples
"""

import csv


class Series(object):
    """
    Column-based data structure.

    Once loaded, data can be accessed by rows or columns.

    Usage:
    >>> prices = [['1997-01-01', 35, 36], ['1997-01-02', 36, 37]]
    >>> series = Series('dates', 'opens', 'closes')
    >>> series.from_values(prices, dates=0, opens=1, closes=2)
    >>> series[0]
    ('1997-01-01', 35, 36)
    >>> series.closes
    [36, 37]
    >>> series.dates[1]
    '1997-01-02'
    >>> series.append(['1997-01-03', 37])
    >>> series[2]
    ('1997-01-03', 37, None)
    
    >>> prices_lol = []
    >>> prices_lol.append(['1997-01-01', 'goog', '32.00'])
    >>> prices_lol.append(['1997-01-02', 'goog', '33.00'])
    >>> prices_lol.append(['1997-01-03', 'goog', '34.00'])
    
    >>> series = Series('dates', 'symbols', 'closes')
    >>> series.from_values(prices_lol)
    >>> series.dates
    ['1997-01-01', '1997-01-02', '1997-01-03']
    
    >>> series[1]
    ('1997-01-02', 'goog', '33.00')

    >>> series.closes[0]
    '32.00'
    
    >>> series.format('closes', float)
    >>> series.closes
    [32.0, 33.0, 34.0]
    
    >>> series.appendcol('opens', [31.00, 33.0, 35])
    >>> series.opens
    [31.0, 33.0, 35]
    
    >>> series.initcol('sma_closes')
    >>> series.sma_closes
    [None, None, None]
    
    >>> series.append(['1997-01-04', 'goog', 38, 37])
    >>> series[3]
    ('1997-01-04', 'goog', 38, 37, None)
    
    >>> series.sma_closes[3] = 0.0
    >>> series[3]
    ('1997-01-04', 'goog', 38, 37, 0.0)
    
    >>> from datetime import datetime
    >>> series.format('dates', datetime.strptime, '%Y-%m-%d')
    >>> series.dates[0].__str__()
    '1997-01-01 00:00:00'
    
    >>> series.sort('closes', order='d')
    >>> series.closes
    [38, 34.0, 33.0, 32.0]
    """
    def __init__(self, *keys):
        """
        """
        self._keys = []
        self._barcnt = 0

        if not keys:
            msg = "Missing *keys to Series"
            raise ValueError(msg)

        self._newkeys(*keys)

    def _newkeys(self, *keys):
        """
        Setup the column keys for the new Series.
        :param *keys: names for your columns.
        """
        for key in keys:
            try:
                float(key)
                newkey = ''.join(('_', str(key)))

            except ValueError:
                newkey = key

            if newkey in self.__dict__:
                msg = "'%s' already defined as key to Series" % (newkey,)
                raise KeyError(msg)

            self._keys.append(newkey)
            self.__dict__[newkey] = []

    def clear(self):
        """
        Initialize class dict with any previously defined attributes.
        """
        self._barcnt = 0
        values = self.__dict__
        for key in self._keys:
            values[key][:] = []

    def __len__(self):
        """
        Returns number of values in your series.
        """
        return self._barcnt

    def keys(self):
        """
        Returns a list of column names from your series.
        """
        return self._keys

    def values(self):
        """
        Returns list of tuples from your series.
        """
        barcnt = self._barcnt

        return [self.__getitem__(i) for i in xrange(self._barcnt)]

    def __getitem__(self, index):
        """
        Returns a row from the series in tuple form.
        :param index: row index (zero-based indexing).
        """
        result = tuple([self.__dict__[k][index] for k in self._keys])
        return result

    def __iter__(self):
        """
        Returns the range of the series for index access.
        """
        return iter(xrange(self._barcnt))

    def from_values(self, values=None, *args, **kwargs):
        """
        Loads the series from a list of values.
        :param values: list of lists or dicts.
        :param *args: positional keys of the columns.
        :param **kwargs: map series key to list of values position or name.
        """
        self._barcnt = 0

        newargs = args
        if not args and not kwargs:
            newargs = self._keys

        dol = lol2dol(values, *newargs, **kwargs)

        barcnt = 0
        if dol:
            barcnt = len(dol[dol.keys()[0]])

        keyfound = False
        for key in self._keys:
            if key in dol:
                self.__dict__[key][:] = dol[key]
                keyfound = True

            else:
                self.__dict__[key][:] = [None] * barcnt

        if keyfound:
            self._barcnt = barcnt

    def initcol(self, key, value=None):
        """
        Initialize a column to a default value. Can be a new column or
        an existing column in your series.

        :param key: name of new or existing column for the series.
            * new column will be appended to the series.
        :param value: default value to initialize the column with.
        """
        if key in self.__dict__:
            self.__dict__[key][:] = [value] * self._barcnt

        else:
            self._keys.append(key)
            self.__dict__[key] = [value] * self._barcnt

    def appendcol(self, key, values):
        """
        Appends a column of values to your series.

        :param key: append new column to the series.
        :param values: values to initialize the column with.
        """
        if key in self.__dict__:
            msg = "'%s' already defined as key to series" % (key,)
            raise KeyError(msg)

        if len(values) != self._barcnt:
            msg = "values mismatch length of series."
            raise ValueError(msg)

        self._keys.append(key)
        self.__dict__[key] = values

    def append(self, values, *args, **kwargs):
        """
        Append a row to your series.

        :param values: dict or list to append to end of series.
        :param *args: positional key names of value columns.
        :param **kwargs: map series key names to value position or key name.
        """
        newargs = args
        if not args and not kwargs:
            newargs = self._keys

        dol = lol2dol([values], *newargs, **kwargs)

        barcnt = 0
        if dol:
            barcnt = len(dol[dol.keys()[0]])

        keyfound = False
        for key in self._keys:
            if key in dol:
                self.__dict__[key].extend(dol[key])
                keyfound = True

            else:
                self.__dict__[key].extend([None] * barcnt)

        if keyfound:
            self._barcnt += barcnt

    def format(self, key, atype, aformat=None):
        """
        Format a column of data to a specified type such as float, int, or str.
        :param key: name of your column to format.
        :param atype: type to format data within column to.
        :param aformat: (optional) additional format spec useful with
            datetime.strptime
        """
        if key not in self.__dict__:
            msg = "'%s' not defined as key to series" % (key,)
            raise KeyError(msg)

        values = self.__dict__[key]

        self.__dict__[key][:] = format_values(values, atype, aformat)

    def sort(self, *args, **kwargs):
        """
        Sort the series in place.

        :param args: keys of your columns to sort by.
        :param kwargs: options you can use in python sort.
            * order can be passed with 'd' for descending or
              'a' for ascending (default).
        """
        keys = [self.__dict__[key] for key in args]

        uids = range(self._barcnt)
        keys.append(uids)

        rows = zip(*keys)

        reverse = False
        if 'order' in kwargs:
            orderflag = kwargs['order'].lower()
            if orderflag.startswith('d'):
                reverse = True

        rows.sort(reverse=reverse)

        uids[:] = zip(*rows)[-1]

        adict = self.__dict__
        for key in self._keys:
            adict[key][:] = [adict[key][i] for i in uids]


def lol2dol(lol=None, *args, **kwargs):
    """
    Returns a dict of lists (dol) from a list of lists or dicts (lol).

    :param lol: (optional) list of lists or dicts to convert to dict of lists.
    :param *args: (optional) key names for dol.
    :param **kwargs: (optional) key name for dol and associated key in row.

    Usage:
    >>> values = [[0, 'yhoo', 32.0], [1, 'goog', 200]]
    >>> dol = lol2dol(values, bar=0, symbol=1, close=2)
    >>> dol['bar']
    [0, 1]
    >>> dol['symbol']
    ['yhoo', 'goog']
    >>> dol['close']
    [32.0, 200]
    """
    labels = {}
    lolkeys = []

    if lol:
        try:
            lolkeys = lol[0].keys()
            isdict = True

        except AttributeError:
            lolkeys = xrange(len(lol[0]))
            isdict = False

    if args:
        if lol and not isdict:
            cnts = xrange(len(args))
            labels = dict(zip(cnts, args))

        else:
            labels = dict(zip(args, args))

    if kwargs:
        for label, key in kwargs.iteritems():
            labels[key] = label

    if not labels:
        labels = dict(zip(lolkeys, lolkeys))

    results = {}
    for label in labels.values():
        results[label] = []

    if lol is None:
        return results

    for row in lol:
        for key, label in labels.iteritems():
            try:
                value = row[key]

            except IndexError:
                value = None

            except KeyError:
                value = None

            results[label].append(value)

    return results


def csv2lol(filename, header=False, **kwargs):
    """
    Returns a list of lists from csv file.

    :param filename: full path of filename to read.
    :param header: set to True if 1st record is header record.
        (optional - default is False.)
    :param **kwargs: keyargs you can pass to csv.reader module.
    :rtype: (tuple of [list of keys] and [list of lists])
    """
    keys = []
    results = []
    with open(filename, 'rb') as f1:
        rdr = csv.reader(f1, **kwargs)
        if header:
            try:
                keys[:] = next(rdr)

            except StopIteration:
                pass

        results[:] = list(rdr)

    if results and not keys:
        keys[:] = list(xrange(len(results[0])))

    return keys, results


def format_values(values, atype, aformat=None):
    """
    Returns a list of values formatted according to type.

    :param values: list of values to format.
    :param atype: type of value to format to. ex. int, float, str.
    :param aformat: (optional) additional formatting for the type such as
                    '%Y%m%d' when using datetime.strptime.

    Usage:
    >>> values = [21.73, 16.2, 20, '21', None]
    >>> results = format_values(values, int)
    >>> results
    [21, 16, 20, 21, None]
    >>>
    """
    results = []

    if atype == int:
        for field in values:
            if field is None:
                results.append(field)
                continue

            try:
                field = int(field)

            except ValueError:
                field = int(float(field))

            results.append(field)

    elif aformat:
        results[:] = [None if x is None else \
                    atype(str(x), aformat) for x in values]

    else:
        results[:] = [None if x is None else atype(x) for x in values]

    return results


def _testit(verbose=None):
    import doctest
    doctest.testmod(verbose=verbose)

if __name__ == "__main__":
    """
    >>> prices_lol = []
    >>> prices_lol.append(['1997-01-01', 'goog', '32.00'])
    >>> prices_lol.append(['1997-01-02', 'goog', '33.00'])
    >>> prices_lol.append(['1997-01-03', 'goog', '34.00'])
    
    >>> series = datio.Series('dates', 'symbols', 'closes')
    >>> series.from_values(prices_lol)
    >>> series.dates
    
    """
    _testit()
