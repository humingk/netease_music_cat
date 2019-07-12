# !/usr/bin/env python
# -*- coding: utf-8 -*-

# author: humingk
# ----------------------

import os
import sys
from my_tools.database_tool import database_tool
from surprise import evaluate, KNNBasic, Reader, dump
from surprise import SVD
from surprise import Dataset
from surprise import evaluate, print_perf
from surprise.model_selection import cross_validate
from surprise import NormalPredictor
from surprise import KNNBasic, KNNBaseline, KNNWithMeans, KNNWithZScore
import pandas
from surprise import AlgoBase
import config
import numpy
from my_tools.logger_tool import loggler_tool

logger = loggler_tool()

data = Dataset.load_builtin('ml-100k')
perf = cross_validate(algo=KNNBasic(), data=data, measures=['RMSE', 'MAE'], cv=5, verbose=True)
print(perf)
