import asyncio
import os
import time
import traceback
from concurrent.futures import ThreadPoolExecutor

import pandas as pd
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from dotenv import load_dotenv
from openai import BadRequestError

from dataset import one_step_task, multi_step_task, multi_step_task_with_possible_failure
from judge import judge, api_key, base_url, model_name
from tools import search, move, use, check

load_dotenv()


model_client = OpenAIChatCompletionClient(
    model=model_name,
    base_url=base_url,
    api_key=api_key
)


def assign_and_run(task: str) -> dict:
    agent = AssistantAgent(
        name="agent",
        model_client=model_client,
        tools=[search, move, use, check],
        system_message="You are a helpful assistant.",
        reflect_on_tool_use=True
    )
    print(f'{task} assigned')
    try:
        _res = asyncio.run(agent.run(task=task))
        _res_str = _res.messages[-1].content
    except BadRequestError:
        _res_str = traceback.format_exc()
    success = judge(task, _res_str)
    final_res = 'success' if success else 'failed'
    print(f'{task} {final_res}.', _res_str)
    return {
        'task': task,
        'success': success,
        'result': _res_str
    }


def eval_tasks(tasks: list):
    task_result_sheet = list()
    task_size = len(tasks)
    task_success = 0
    # with ThreadPoolExecutor(max_workers=8) as executor:
    #     _results = executor.map(assign_and_run, tasks)
    _results = []
    for task in tasks:
        _results.append(assign_and_run(task))
    for _re in _results:
        task_result_sheet.append({
            'task': _re['task'],
            'success': _re['success'],
            'result': _re['result']
        })
        if _re['success']:
            task_success += 1
    success_rate = task_success / task_size + 1e-3
    task_result_sheet.append({
        'task': f'success_rate={success_rate}',
        'success': '',
        'result': ''
    })
    return success_rate, task_result_sheet


# noinspection PyStatementEffect
if __name__ == '__main__':
    if not os.path.exists('./output'):
        os.mkdir('./output')
    _dir = f'./output/{time.time()}'
    if not os.path.exists(_dir):
        os.mkdir(_dir)
    os.environ['CERTAIN'] = 'true'
    _success_rate, task_result_sheet = eval_tasks(one_step_task)
    print('[one-step] success_rate:', _success_rate)
    pd.DataFrame(task_result_sheet).to_csv(f'{_dir}/ceo_eval_one_step_{time.time()}.csv', index=False)
    _success_rate, task_result_sheet = eval_tasks(multi_step_task)
    print('[multi-step-certain] success_rate:', _success_rate)
    pd.DataFrame(task_result_sheet).to_csv(f'{_dir}/ceo_eval_multi_step_certain_{time.time()}.csv', index=False)
    os.environ['CERTAIN'] = 'false'
    _success_rate, task_result_sheet = eval_tasks(multi_step_task_with_possible_failure)
    print('[multi-step-uncertain] success_rate:', _success_rate)
    pd.DataFrame(task_result_sheet).to_csv(f'{_dir}/ceo_eval_multi_step_uncertain_{time.time()}.csv', index=False)
