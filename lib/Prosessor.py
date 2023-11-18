import nltk
import pandas as pd
from collections import Counter
from pymystem3 import Mystem
from .utils import extract, check_adj

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger_ru')

ms = Mystem()


class Processor:
    def __init__(self, filename: str):
        self.data = pd.read_csv(filename)

    def process(self):
        d = self.data
        d["jobs_selected"] = d["job"].apply(extract)
        d = d.explode(['jobs_selected'])
        d["jobs_selected"] = d["jobs_selected"].astype('str')
        d["counted_jobs_selected"] = d["jobs_selected"]

        print(len(d.job.unique()))
        conter_dict = Counter(",".join(d['jobs_selected']).split(',')).most_common(len(d.job.unique()))
        dct_corr = {k: v for k, v in dict(conter_dict).items() if isinstance(v, int)}
        d = d.replace({"counted_jobs_selected": dct_corr})

        d.dropna(inplace=True)
        d['counted_jobs_selected'] = pd.to_numeric(d['counted_jobs_selected'], errors='coerce')
        d = d.drop_duplicates(subset=['client_id', 'prof_id', 'jobs_selected'])
        d = d[d.counted_jobs_selected > 20]

        d["adj"] = d["jobs_selected"]
        d["adj"] = d["adj"].apply(lambda x: check_adj(x))
        d = d[d.adj != 'A=m']
        d[
            [
                'client_id', 'prof_id', 'jobs_selected', 'counted_jobs_selected',
                'job', 'counted_jobs_selected', 'description', 'months'
            ]
        ].to_csv('data_selected.csv')
        print(d.jobs_selected.unique())
        print(d.shape)
