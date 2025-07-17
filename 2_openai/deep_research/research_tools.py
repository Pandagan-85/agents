from agents import function_tool, Runner
from clarification_agent import clarification_agent
from planner_agent import planner_agent
from search_agent import search_agent
from writer_agent import writer_agent


@function_tool
async def generate_clarifications(query: str) -> str:
    """Generate 3 clarifying questions for a research query"""
    result = await Runner.run(clarification_agent, f"Query: {query}")
    questions = []
    for i, q in enumerate(result.final_output.questions, 1):
        questions.append(f"{i}. {q.question} (Reason: {q.reason})")
    return "\n".join(questions)


@function_tool
async def plan_searches(query: str) -> str:
    """Plan web searches for a research query"""
    result = await Runner.run(planner_agent, f"Query: {query}")
    searches = []
    for i, search in enumerate(result.final_output.searches, 1):
        searches.append(
            f"{i}. Search: '{search.query}' (Reason: {search.reason})")
    return "\n".join(searches)


@function_tool
async def perform_search(search_term: str, reason: str) -> str:
    """Perform a single web search and summarize results"""
    input_text = f"Search term: {search_term}\nReason for searching: {reason}"
    result = await Runner.run(search_agent, input_text)
    return result.final_output


@function_tool
async def write_report(query: str, search_results: str) -> str:
    """Write a comprehensive research report from search results"""
    input_text = f"Original query: {query}\nSummarized search results: {search_results}"
    result = await Runner.run(writer_agent, input_text)
    return result.final_output.markdown_report

# Lista di tutti i tools
research_tools = [generate_clarifications,
                  plan_searches, perform_search, write_report]
