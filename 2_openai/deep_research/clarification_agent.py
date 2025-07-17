from pydantic import BaseModel, Field
from agents import Agent
from typing import List


class ClarificationQuestion(BaseModel):
    reason: str = Field(
        description="Your reasoning for why this clarification question is important for the research query.")
    question: str = Field(
        description="The clarification question to ask the user.")


class ClarificationQuestions(BaseModel):
    questions: List[ClarificationQuestion] = Field(
        description="3 clarifying questions to better understand the research query.")


INSTRUCTIONS = """
You are a research assistant that helps clarify research queries.
Given a research query, generate exactly 3 clarifying questions that would help:
1. Narrow down the scope of research
2. Understand the specific angle or perspective needed
3. Identify the target audience or use case for the research

For each question, provide a clear reasoning for why that clarification is important.
The questions should be concise and help produce more focused and relevant research results.

Example:
Query: "Latest AI Agent frameworks in 2025"
Questions could focus on:
- Technical depth vs overview
- Specific use cases or industries
- Comparison criteria or focus areas
"""

clarification_agent = Agent(
    name="ClarificationAgent",
    instructions=INSTRUCTIONS,
    model="gpt-4o-mini",
    output_type=ClarificationQuestions,
)
