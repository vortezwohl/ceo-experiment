import json
import os
import time
from concurrent.futures import ThreadPoolExecutor

from ceo import Agent, Personality
from ceo.brain.hook import BeforeActionTaken, AfterActionTaken
from ceo.message import BeforeActionTakenMessage, AfterActionTakenMessage
from dotenv import load_dotenv
import pandas as pd

from ability import search, move, use, check, model
from dataset import one_step_task, multi_step_task_certain, multi_step_task_uncertain

load_dotenv()


def before_action_taken(agent: Agent, message: BeforeActionTakenMessage):
    # print(f'Agent: {agent.name}, Next move: {message}')
    return message


def after_action_taken(agent: Agent, message: AfterActionTakenMessage):
    # print(f'Agent: {agent.name}, Action taken: {message}')
    return message


def assign_and_run(task: str) -> dict:
    agent = Agent(abilities=[search, move, use, check], brain=model,
                  personality=Personality.INQUISITIVE)
    print(f'{task} assign to {agent.name}.')
    res = dict()
    while True:
        try:
            res = {
                'task': task,
                'result': agent.assign(task).just_do_it(
                    BeforeActionTaken(before_action_taken),
                    AfterActionTaken(after_action_taken)
                )
            }
            break
        except json.decoder.JSONDecodeError:
            continue
    final_res = 'success' if res['result'].success else 'failed'
    print(f'{task} {final_res}.', res['result'].conclusion)
    return res


def eval_tasks(tasks: list):
    task_result_sheet = list()
    task_size = len(tasks)
    task_success = 0
    with ThreadPoolExecutor(max_workers=8) as executor:
        _all_dones = executor.map(assign_and_run, tasks)
    for _re in _all_dones:
        _res = _re['result']
        task_result_sheet.append({
            'task': _re['task'],
            'success': _res.success,
            'conclusion': _res.conclusion,
            'step_count': _res.step_count,
            'time_used': _res.time_used
        })
        if _res.success:
            task_success += 1
    success_rate = task_success / task_size + 1e-3
    task_result_sheet.append({
        'task': f'success_rate={success_rate}',
        'success': '',
        'conclusion': '',
        'step_count': '',
        'time_used': ''
    })
    return success_rate, task_result_sheet


# noinspection PyStatementEffect
if __name__ == '__main__':
    os.environ['CERTAIN'] = 'true'
    _success_rate, task_result_sheet = eval_tasks(one_step_task)
    print('[one-step] success_rate:', _success_rate)
    pd.DataFrame(task_result_sheet).to_csv(f'./output/ceo_eval_one_step_{time.time()}.csv', index=False)
    _success_rate, task_result_sheet = eval_tasks(multi_step_task_certain)
    print('[multi-step-certain] success_rate:', _success_rate)
    pd.DataFrame(task_result_sheet).to_csv(f'./output/ceo_eval_multi_step_certain_{time.time()}.csv', index=False)
    os.environ['CERTAIN'] = 'false'
    _success_rate, task_result_sheet = eval_tasks(multi_step_task_uncertain)
    print('[multi-step-uncertain] success_rate:', _success_rate)
    pd.DataFrame(task_result_sheet).to_csv(f'./output/ceo_eval_multi_step_uncertain_{time.time()}.csv', index=False)
