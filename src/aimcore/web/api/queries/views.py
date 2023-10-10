from fastapi.responses import StreamingResponse

from typing import Optional, Iterable

from aimcore.web.api.runs.pydantic_models import QuerySyntaxErrorOut
from aimcore.web.api.utils import APIRouter, collect_streamable_data, get_project_repo, \
    checked_query  # wrapper for fastapi.APIRouter

from aim import Container, Sequence

from aim._core.storage.treeutils import encode_tree

query_router = APIRouter()


async def sequence_search_result_streamer(query_collection, sample_count):
    for sequence in query_collection:
        seq_dict = {
            'name': sequence.name,
            'context': sequence.context,
            'item_type': sequence.type,
            'axis_names': sequence.axis_names,
            'axis': {}
        }
        if sample_count is None:
            seq_dict['steps'] = list(sequence.steps())
            seq_dict['values'] = list(sequence.values())
            for axis_name in sequence.axis_names:
                seq_dict['axis'][axis_name] = list(sequence.axis(axis_name))
        else:
            steps, value_dicts = list(zip(*sequence.sample(sample_count)))
            value_lists = {k: [d[k] for d in value_dicts] for k in value_dicts[0]}
            seq_dict['steps'] = steps
            seq_dict['values'] = value_lists.pop('val')
            seq_dict['axis'] = value_lists

        encoded_tree = encode_tree(seq_dict)
        yield collect_streamable_data(encoded_tree)


async def container_search_result_streamer(query_collection: Iterable[Container]):
    for container in query_collection:
        cont_dict = {
            'hash': container.hash,
            'params': container[...]
        }
        encoded_tree = encode_tree(cont_dict)
        yield collect_streamable_data(encoded_tree)


def container_query_response(repo, query: Optional[str], type_: str):
    qresult = repo.containers(query, type_)
    streamer = container_search_result_streamer(qresult)
    return StreamingResponse(streamer)


def sequence_query_response(repo, query: Optional[str], type_: str, sample_count: int):
    qresult = repo.sequences(query, type_)
    streamer = sequence_search_result_streamer(qresult, sample_count)
    return StreamingResponse(streamer)


@query_router.get('/fetch/', responses={400: {'model': QuerySyntaxErrorOut}})
def data_fetch_api(type_: str, q: Optional[str] = None, p: Optional[int] = 500):
    repo = get_project_repo()
    query = checked_query(q)
    if type_ in Container.registry:
        return container_query_response(repo, query, type_)
    elif type_ in Sequence.registry:
        return sequence_query_response(repo, query, type_, p)
