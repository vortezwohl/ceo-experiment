import time
from concurrent.futures import ThreadPoolExecutor

from ceo import Agent, Personality
from ceo.brain.hook import BeforeActionTaken, AfterActionTaken
from ceo.message import BeforeActionTakenMessage, AfterActionTakenMessage
from dotenv import load_dotenv
import pandas as pd

from ability import search, move, use, check
from dataset import one_step_task, multi_step_task_certain, multi_step_task_uncertain
from model import model

load_dotenv()


def before_action_taken(agent: Agent, message: BeforeActionTakenMessage):
    print(f'Agent: {agent.name}, Next move: {message}')
    return message


def after_action_taken(agent: Agent, message: AfterActionTakenMessage):
    print(f'Agent: {agent.name}, Action taken: {message}')
    return message


def assign_and_run(_agent_and_task: tuple[Agent, str]) -> dict:
    return {
        'task': _agent_and_task[1],
        'result': _agent_and_task[0].assign(_agent_and_task[1]).just_do_it(
            BeforeActionTaken(before_action_taken),
            AfterActionTaken(after_action_taken)
        )
    }


def one_step_test(_agent: Agent):
    task_result_sheet = list()
    task_size = len(one_step_task)
    task_success = 0.0
    agent_and_task_list = [(_agent, f'单步任务: {x}') for x in one_step_task]
    with ThreadPoolExecutor(max_workers=task_size) as executor:
        _all_dones = executor.map(assign_and_run, agent_and_task_list)
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
            task_success += 1.0
    return task_success + 1e-10 / task_size + 1e-10, task_result_sheet


if __name__ == '__main__':
    agent = Agent(abilities=[search, move, use, check], brain=model,
                  personality=Personality.INQUISITIVE)
    success_rate, task_result_sheet = one_step_test(agent)
    pd.DataFrame(task_result_sheet).to_csv(f'./output/ceo_eval_{time.time()}.csv', index=False)
