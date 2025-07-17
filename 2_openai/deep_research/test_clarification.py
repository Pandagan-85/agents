import asyncio
from dotenv import load_dotenv
from agents import Runner
from clarification_agent import clarification_agent

load_dotenv(override=True)


async def test_clarification():
    test_query = "Latest AI Agent frameworks in 2025"

    print(f"Testing clarification agent with query: '{test_query}'")
    print("-" * 50)

    try:
        result = await Runner.run(clarification_agent, f"Query: {test_query}")

        print("✅ Clarification agent works!")
        print(f"Generated {len(result.final_output.questions)} questions:")
        print()

        for i, q in enumerate(result.final_output.questions, 1):
            print(f"**Question {i}:** {q.question}")
            print(f"*Reason:* {q.reason}")
            print()

    except Exception as e:
        print(f"❌ Clarification agent failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_clarification())
