import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient
from dotenv import load_dotenv

from tool import search, move, use, check

load_dotenv()


model_client = OpenAIChatCompletionClient(
    model="gpt-4o-mini",
)


agent = AssistantAgent(
    name="agent",
    model_client=model_client,
    tools=[search, move, use, check],
    system_message="You are a helpful assistant.",
    reflect_on_tool_use=True,
    model_client_stream=True,  # Enable streaming tokens from the model client.
)


async def main() -> None:
    await Console(agent.run_stream(task="去厨房看看"))

asyncio.run(main())
