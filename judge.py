import json

from autono_eval_src.model import *


def judge(_input: str, _output: str) -> bool:
    prompt = {
        '目标': '根据[任务要求]和[执行反馈]，判断[任务要求]中设计的动作是否已被**全部**执行(将要执行的动作，算是未执行的)',
        '输出数据类型': 'bool',
        '输出': f'{True} / {False}',
        '任务要求': _input,
        '执行反馈': _output
    }
    response = model.invoke(json.dumps(prompt, ensure_ascii=False)).content
    return True if 'true' in response.lower() else False
