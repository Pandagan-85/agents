import asyncio
from dotenv import load_dotenv
from agents import Runner
from clarification_agent import clarification_agent
from planner_agent import planner_agent

load_dotenv(override=True)


async def test_individual_agents():
    query = "Latest AI Agent frameworks in 2025"

    print("Testing clarification agent...")
    try:
        result1 = await Runner.run(clarification_agent, f"Query: {query}")
        print("✅ Clarification agent works")
        print(f"Questions: {len(result1.final_output.questions)} generated")
    except Exception as e:
        print(f"❌ Clarification agent failed: {e}")

    print("\nTesting planner agent...")
    try:
        result2 = await Runner.run(planner_agent, f"Query: {query}")
        print("✅ Planner agent works")
        print(f"Searches planned: {len(result2.final_output.searches)}")
    except Exception as e:
        print(f"❌ Planner agent failed: {e}")

asyncio.run(test_individual_agents())
