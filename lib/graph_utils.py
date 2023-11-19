import os
import gc
import uuid

import pandas as pd

from .graph_builder import GraphBuilder


def select_data_for_anon(data_index_zeroed: pd.DataFrame, anon: str, anon_field: str = "client_id"):
    return (
        data_index_zeroed.loc[
            data_index_zeroed[anon_field] == anon
            ]
    .sort_values(by="prof_id")
    )


def get_url_map(data: pd.DataFrame, shorts: bool, job_clmn: str) -> (list, dict):
    url_stream, url_stream_num, jobstreams = {}, {}, []
    for anon in list(data["client_id"].unique()):
        anon_data = select_data_for_anon(data, anon)
        jobstream = anon_data[job_clmn].to_list()
        if shorts:
            jobstreams.append(jobstream)
        elif not shorts and len(jobstream) > 1:
            jobstreams.append(jobstream)
        for num, selector in enumerate(anon_data[job_clmn].to_list()):
            url_stream[selector] = anon_data["counted_jobs_selected"].to_list()[num]
    for num, v in enumerate(sorted(set(url_stream.values()))):
        url_stream_num[v] = num + 1
    return jobstreams, {"stream": url_stream, "enum_stream": url_stream_num}


def first_last_jobs(jobstreams) -> tuple:
    first_sel = [x[0] for x in jobstreams]
    last_sel = [x[-1] for x in jobstreams]

    return first_sel, last_sel


def build_map(data: pd.DataFrame, rfolder: str = os.getcwd(), shorts=True) -> None:
    print("Rendering clickmap started...")
    jobstreams, url_map = get_url_map(data, shorts, job_clmn='jobs_selected')
    first_sel, last_sel = first_last_jobs(jobstreams)

    graph_builder = GraphBuilder(url_map)
    graph = graph_builder.build(jobstreams, first_sel, last_sel)
    graph.render(
        filename=uuid.uuid4().__str__(),
        directory=rfolder,
        view=False,
        cleanup=True,
        format="png"
    )

    print("Done rendering ")
    gc.collect()
