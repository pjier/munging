#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Module holds all classes to extract day with lowest temp spread """

import argparse
from collections import namedtuple
from functools import reduce

TempSpread = namedtuple('Temp', 'day max min')


class WeatherBuilder:
    """
        Builds a list of namedtuples
        The input file data is aligned by column offset.
    """

    slices = [slice(i, j) for i, j in
              [(2, 4), (5, 8), (9, 14)]]

    def __init__(self):
        self._obj = []

    def build_part(self, line):
        """ Add a temperature observation """
        data_points = []
        try:
            for slc in WeatherBuilder.slices:
                data_points.append(int(line[slc]))
            self._obj.append(TempSpread(*data_points))
        except ValueError:
            return

    def get_result(self):
        """ Just return the results """
        return self._obj


class MinTempSpreadStrategy:
    """
        Calculates the min spread, max temperature minus min temperature,
        for each day and returns the day with the smallest spread.
    """

    def __init__(self):
        pass

    def calculate(self, data):
        """ Expects a list of TempSpread tuples """
        min_entry = reduce(lambda x, y: x if (x.max - x.min) < (y.max - y.min)
                           else y, data)
        return min_entry.day


class FileParser:

    def __init__(self, builder):
        self._builder = builder

    def read(self, filename):
        """ Read the contents of a datafile """
        with open(filename) as f:
            for line in f:
                self._builder.build_part(line)
        return self._builder.get_result()


def main(args):
    """ Main entry point of the app """
    fp = FileParser(WeatherBuilder())
    data = fp.read(args.datafile)
    print(f'Day with minimum spread is\
        {MinTempSpreadStrategy().calculate(data)}')


if __name__ == "__main__":
    PARSER = argparse.ArgumentParser()

    # Required positional argument
    PARSER.add_argument("datafile",
                        help="Path to datafile with temperature readings")

    MYARGS = PARSER.parse_args()
    main(MYARGS)
