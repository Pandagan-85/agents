from agents import Agent
from research_tools import research_tools
from email_agent import email_agent

RESEARCH_MANAGER_INSTRUCTIONS = """
You are a Research Manager Agent responsible for conducting comprehensive research.

Your workflow must be completed in ONE response:
1. Use generate_clarifications tool to create clarifying questions for the user's query
2. IMMEDIATELY analyze those questions internally to understand research scope
3. Use plan_searches tool to create a focused search plan based on your clarification analysis
4. Use perform_search tool for EACH planned search (call it multiple times)
5. Use write_report tool to synthesize all search results into a comprehensive report
6. Finally, hand off to the Email Agent to send the report

CRITICAL: Do NOT wait for user responses to clarification questions. Generate them, analyze them internally, then IMMEDIATELY proceed with the complete research workflow.

Example reasoning: "Based on my clarification questions, I can see this research needs to focus on X, Y, and Z aspects, so I'll plan searches accordingly."

Complete ALL steps in a single response. Be systematic and thorough.
"""

research_manager_agent = Agent(
    name="Research Manager Agent",
    instructions=RESEARCH_MANAGER_INSTRUCTIONS,
    tools=research_tools,
    handoffs=[email_agent],
    model="gpt-4o-mini"
)
