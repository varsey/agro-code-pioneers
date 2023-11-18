import os
import gc
import uuid
import pandas as pd

from .GraphBuilder import GraphBuilder


def select_data_for_anon(data_index_zeroed: pd.DataFrame, anon: str, anon_field: str = "client_id"):
    return (
        data_index_zeroed.loc[
            data_index_zeroed[anon_field] == anon
            ]
    .sort_values(by="prof_id")
    )


def get_url_map(data: pd.DataFrame, job_clmn: str) -> (list, dict):
    url_stream, url_stream_num, clickstream = {}, {}, []
    for anon in list(data["client_id"].unique()):
        anon_data = select_data_for_anon(data, anon)
        clickstream.append(anon_data[job_clmn].to_list())
        for num, selector in enumerate(anon_data[job_clmn].to_list()):
            url_stream[selector] = anon_data["counted_jobs_selected"].to_list()[num]
    for num, v in enumerate(sorted(set(url_stream.values()))):
        url_stream_num[v] = num + 1
    return clickstream, {"stream": url_stream, "enum_stream": url_stream_num}


def first_last_jobs(clickstream) -> tuple:
    first_sel = [x[0] for x in clickstream]
    last_sel = [x[-1] for x in clickstream]

    return first_sel, last_sel


def build_map(data: pd.DataFrame, rfolder: str = os.getcwd()) -> str:
    print("Rendering clickmap started...")
    clickstream, url_map = get_url_map(data, job_clmn='jobs_selected')
    first_sel, last_sel = first_last_jobs(clickstream)
    last_sel_status = {x[-1]: {'Correct': 1} for x in clickstream}

    graph_builder = GraphBuilder(url_map)
    graph = graph_builder.build(clickstream, first_sel, last_sel, last_sel_status)
    fname = uuid.uuid4().__str__()
    graph.render(filename=fname, directory=rfolder, view=False, cleanup=True, format="png")

    print("Done rendering ")
    gc.collect()

    return f"{fname}.png"
