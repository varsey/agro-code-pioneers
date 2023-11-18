import pandas as pd
from lib.plotting_utils import build_map
from lib.Prosessor import Processor

p = Processor('data.csv')
p.process()
data = pd.read_csv('data_selected.csv')
data_sample = data.sample(700)
print(len(data_sample.jobs_selected.unique()))
build_map(data_sample)
