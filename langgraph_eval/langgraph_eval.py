from langgraph import Agent, Tool, start_session
from langgraph.llms import OpenAIChat

# 定义计算器工具
@Tool
def calculator(a: float, b: float, operator: str) -> str:
    """Perform a calculation with two numbers and an operator."""
    try:
        if operator == '+':
            return str(a + b)
        elif operator == '-':
            return str(a - b)
        elif operator == '*':
            return str(a * b)
        elif operator == '/':
            if b == 0:
                return 'Error: Division by zero'
            return str(a / b)
        else:
            return 'Error: Invalid operator. Please use +, -, *, or /'
    except Exception as e:
        return f'Error: {str(e)}'

# 创建智能体
agent = Agent(
    name="assistant",
    llm=OpenAIChat(model="gpt-4"),
    tools=[calculator],
    system_message="You are a helpful assistant that can perform calculations using the provided calculator tool.",
)

# 启动会话并处理用户消息
async def main():
    async for msg in start_session(agent):
        print(f"Assistant: {msg.content}")

# 发送用户消息并运行会话
asyncio.run(agent.send_message("What is the result of 123.45 * 67.89?"))
asyncio.run(main())