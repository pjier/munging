#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Module holds all classes to extract day with lowest temp spread """

import argparse
from collections import namedtuple
from functools import reduce
import logging

# TODO PI 2020-02-16
# - Arrange the temperature and goal metadata into classes
# - Break out DataBuilder.build_part() into at least another method

TempSpread = namedtuple('Temp', 'day max min')
temperature_file_slices = [slice(i, j) for i, j in
                           [(2, 4), (5, 8), (9, 14)]]
temp_field_types = (int, int, int)

GoalSpread = namedtuple('SeasonResult', 'team for_goals against_goals')
football_file_slices = [slice(i, j) for i, j in
                        [(7, 23), (43, 45), (50, 52)]]
football_field_types = (str, int, int)


class DataBuilder:
    """
        Builds an object that contains 0..n observations on which we can
        subsequently calculate some metric.
    """

    def __init__(self, slices, namedtuple_to_build, field_types):
        assert len(slices) == len(field_types)
        self._observations = []
        self._slices = slices
        self._namedtuple = namedtuple_to_build
        self._field_types = field_types

    def build_part(self, line):
        """ Add a temperature observation """
        data_points = []
        try:
            for this_type, this_slice in zip(self._field_types, self._slices):
                data_point = this_type(line[this_slice])
                if type(data_point) == str:
                    data_point = data_point.strip()
                data_points.append(data_point)
            self._observations.append(self._namedtuple(*data_points))
        except ValueError:
            logging.info(f'Unable to parse line {line}')
            return

    def get_result(self):
        """ Just return a list of TempSpread tuples """
        return self._observations


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


class MinGoalDifferenceStrategy:
    """
        Returns the name of the team with the smallest difference between
        for_goals and against_goals.
    """

    def __init__(self):
        pass

    def calculate(self, data):
        """ Expects a list of GoalSpread tuples """
        min_entry = reduce(lambda x, y: x if abs(x.for_goals - x.against_goals)
                           < abs(y.for_goals - y.against_goals)
                           else y, data)
        return min_entry.team


class FileParser:
    """
        Read the contents of a datafile. Pass each row to the builder that is
        responsible for building the object with observations.
    """

    def __init__(self, builder):
        self._builder = builder

    def read(self, filename):
        with open(filename) as f:
            for line in f:
                self._builder.build_part(line)
        return self._builder.get_result()


def main(args):
    if args.datatype == 'weather':
        fp = FileParser(DataBuilder(temperature_file_slices, TempSpread,
                                    temp_field_types))
        data = fp.read(args.datafile)
        print(f'Day with minimum spread is\
            {MinTempSpreadStrategy().calculate(data)}')
    else:
        fp = FileParser(DataBuilder(football_file_slices, GoalSpread,
                                    football_field_types))
        data = fp.read(args.datafile)
        print(f'The team with the smallest goal spread is\
            {MinGoalDifferenceStrategy().calculate(data)}')


if __name__ == "__main__":
    PARSER = argparse.ArgumentParser(
        description='Calculate a metric based on a data file')

    PARSER.add_argument('datafile',
                        help='Path to datafile with temperature readings')
    PARSER.add_argument('--datatype',
                        help='Type of data contained in the file',
                        choices=['weather', 'football'],
                        default='weather')
    # TODO: Add argument for log level

    MYARGS = PARSER.parse_args()
    main(MYARGS)
