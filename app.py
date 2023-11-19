import os

import pandas as pd

from lib.graph_utils import build_map
from lib.processor import Processor
from lib.args_parser import args_parse
from lib.custom_rule import Rule
from lib.woker_utils import print_legend


sample_size, shorts_included, use_rule = args_parse()

p = Processor('data.csv')
p.process()

data = pd.read_csv('data_selected.csv')
data_sample = data.sample(sample_size, random_state=1)
print(len(data_sample.jobs_selected.unique()))

if use_rule:
    r = Rule()
    data_sample = data_sample.replace({'jobs_selected': r.rule})
    print(len(data_sample.jobs_selected.unique()))

print_legend(data_sample)

results_folder = os.getcwd() + '/graph'
build_map(data=data_sample, rfolder=results_folder, shorts=shorts_included)
