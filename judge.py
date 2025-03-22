import json

from ceo_eval_src.model import model


def judge(_input: str, _output: str) -> bool:
    prompt = {
        '目标': '根据[用户请求]，和[执行结果]，判断[用户请求]是否被成功执行',
        '输出数据类型': 'bool',
        '输出': f'{True} / {False}',
        '用户请求': _input,
        '执行结果': _output
    }
    response = model.invoke(json.dumps(prompt, ensure_ascii=False)).content
    return True if 'true' in response.lower() else False
