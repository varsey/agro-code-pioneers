import os

import pandas as pd

from lib.graph_utils import build_map
from lib.processor import Processor

p = Processor('data.csv')
p.process()

data = pd.read_csv('data_selected.csv')
data_sample = data.sample(700)

print(len(data_sample.jobs_selected.unique()))
results_folder = os.getcwd() + '/graph'
build_map(data=data_sample, rfolder=results_folder)
