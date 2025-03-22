import os
import time
from concurrent.futures import ThreadPoolExecutor

import pandas as pd
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub
from langchain_openai import ChatOpenAI

from dataset import one_step_task, multi_step_task, multi_step_task_with_possible_failure
from tools import tools
from judge import judge, api_key, model_name, base_url

base_prompt = hub.pull("langchain-ai/react-agent-template")
prompt = base_prompt.partial(instructions="")


def assign_and_run(task: str) -> dict:
    llm = ChatOpenAI(
        temperature=0,
        base_url=base_url,
        model=model_name,
        api_key=api_key
    )
    agent = create_react_agent(
        prompt=prompt,
        llm=llm,
        tools=tools
    )
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=False)
    print(f'{task} assigned')
    try:
        response = agent_executor.invoke({"input": task})
    except Exception:
        response = {'output': 'tool call failed'}
    success = judge(task, response['output'])
    final_res = 'success' if success else 'failed'
    print(f'{task} {final_res}.')
    return {
        'task': task,
        'success': success,
        'result': response['output']
    }


def eval_tasks(tasks: list):
    task_result_sheet = list()
    task_size = len(tasks)
    task_success = 0
    with ThreadPoolExecutor(max_workers=8) as executor:
        _results = executor.map(assign_and_run, tasks)
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
