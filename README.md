# Experiment

The experimental results demonstrate that the `autono` framework significantly outperforms `autogen` and `langchain` in handling tasks of varying complexity, especially in multi-step tasks with possible failures.

| Framework   | Version | Model                                      | one-step-task | multi-step-task | multi-step-task-with-possible-failure |
| ------ | --- |----------------------------------------- | ------------- | --------------- | ---------------------------------------- |
| `autono` | `1.0.0` |gpt-4o-mini<br>qwen-plus<br>deepseek-v3 | 96.7%</br>100%</br>100% | 100%</br>96.7%</br>100% | 76.7%</br>93.3%</br>93.3% |
| `autogen` | `0.4.9.2` |gpt-4o-mini<br>qwen-plus<br>deepseek-v3 |90%</br>90%</br>N/A | 53.3%</br>0%</br>N/A | 3.3%</br>3.3%</br>N/A |
| `langchain` | `0.3.21` |gpt-4o-mini<br>qwen-plus<br>deepseek-v3 | 73.3%</br>73.3%</br>76.7% | 13.3%</br>13.3%</br>13.3% | 10%</br>13.3%</br>6.7% |

- `one-step-task`: Tasks that can be completed with a single tool call.
- `multi-step-task`: Tasks that require multiple tool calls to complete, with no possibility of tool failure.
- `multi-step-task-with-possible-failure`: Tasks that require multiple tool calls to complete, where tools may fail, requiring the agent to retry and correct errors.

> The deepseek-v3 model is not supported by `autogen-agentchat==0.4.9.2`.
