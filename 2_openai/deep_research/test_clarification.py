import asyncio
from dotenv import load_dotenv
from agents import Runner
from clarification_agent import clarification_agent

load_dotenv(override=True)


async def test_clarification():
    test_query = "Latest AI Agent frameworks in 2025"
    result = await Runner.run(clarification_agent, f"Query: {test_query}")

    print("Generated questions:")
    for i, q in enumerate(result.final_output.questions, 1):
        print(f"{i}. {q.question}")
        print(f"   Reason: {q.reason}")
        print()

# Per eseguire il test
asyncio.run(test_clarification())
