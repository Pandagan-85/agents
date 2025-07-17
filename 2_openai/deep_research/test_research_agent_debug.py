# test_research_agent_debug.py
import asyncio
from dotenv import load_dotenv
from agents import Runner, trace
from research_agent_manager import research_manager_agent

load_dotenv(override=True)


async def test_research_agent_debug():
    query = "Latest AI Agent frameworks in 2025"

    print(f"Testing Research Manager Agent with query: {query}")
    print("Available tools:", [
          tool.name for tool in research_manager_agent.tools])
    print("-" * 50)

    try:
        result = await Runner.run(research_manager_agent, query)
        print("✅ Research completed successfully!")
        print("Final result length:", len(result.final_output))
        print("Final result preview:", result.final_output[:200] + "...")
    except Exception as e:
        print(f"❌ Research failed: {e}")
        import traceback
        traceback.print_exc()

asyncio.run(test_research_agent_debug())
