import os

import pandas as pd

from lib.graph_utils import build_map
from lib.processor import Processor
from lib.args_parser import args_parse
from lib.custom_rule import Rule


sample_size, shorts_included, use_rule = args_parse()
print(f'sample_size: {sample_size} shorts_included: {shorts_included} use_rule {use_rule}')

p = Processor('data.csv')
p.process()

data = pd.read_csv('data_selected.csv')
data_sample = data.sample(sample_size, random_state=1)
print(len(data_sample.jobs_selected.unique()))

if use_rule:
    r = Rule()
    data_sample = data_sample.replace({'jobs_selected': r.rule})
    print(len(data_sample.jobs_selected.unique()))

results_folder = os.getcwd() + '/graph'
build_map(data=data_sample, rfolder=results_folder, shorts=shorts_included)
