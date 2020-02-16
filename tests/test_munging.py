#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Module documentation goes here."""

import os
import pytest
from src.munging import *

def get_weather_builder():
    return DataBuilder(temperature_file_slices, TempSpread, temp_field_types)

class TestWeatherBuilder:

    def test_build_one_line(self):
        builder = get_weather_builder()
        builder.build_part("   1  88    59    74          53.8       0.00 F       280  9.6 270  17  1.6  93 23 1004.5")
        t = TempSpread(1, 88, 59)
        assert builder.get_result() == [t]

    def test_erroneous_line(self):
        builder = get_weather_builder()
        builder.build_part(" abc  88    59    74          53.8       0.00 F       280  9.6 270  17  1.6  93 23 1004.5")


class TestFootballBuilder:

    def test_build_one_line(self):
        builder = DataBuilder(football_file_slices, GoalSpread, football_field_types)
        builder.build_part("    1. Arsenal         38    26   9   3    79  -  36    87")
        g = GoalSpread('Arsenal', 79, 36)
        assert builder.get_result() == [g]

class TestFileParser:

    def test_file_exception(self):
        parser = FileParser(get_weather_builder())
        with pytest.raises(FileNotFoundError):
            parser.read('nonsense')

    def test_read_file(self):
        datafile = os.path.dirname(os.path.abspath(__file__)) + '/../data/weather.dat'
        parser = FileParser(get_weather_builder())
        assert 30 == len(parser.read(datafile))


class TestMinTempSpreadStrategy:

    def test_min_temp_oneline(self):
        strategy = MinTempSpreadStrategy()
        data = [TempSpread(31, 90, 50)]
        assert 31 == strategy.calculate(data)

    def test_min_temp_threelines(self):
        strategy = MinTempSpreadStrategy()
        data = [TempSpread(1, 50, 40),
                TempSpread(2, 90, 50),
                TempSpread(8, 55, 42)]
        assert 1 == strategy.calculate(data)
