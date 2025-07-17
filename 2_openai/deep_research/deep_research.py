import gradio as gr
from dotenv import load_dotenv
from research_manager import ResearchManager  # Classe originale
from research_agent_manager import research_manager_agent  # Nuovo agent
from agents import Runner

load_dotenv(override=True)


async def run_research_with_agent(query: str):
    """Esegue la ricerca usando il Research Manager Agent (no streaming)"""
    if not query.strip():
        return "Please enter a research query first."

    try:
        result = await Runner.run(research_manager_agent, query)
        return result.final_output
    except Exception as e:
        return f"Error during research: {str(e)}"


async def run_research_with_streaming(query: str, clarifications: str = ""):
    """Esegue la ricerca con streaming usando la classe ResearchManager"""
    if not query.strip():
        yield "Please enter a research query first."
        return

    async for chunk in ResearchManager().run(query, clarifications):
        yield chunk

with gr.Blocks(theme=gr.themes.Default(primary_hue="sky")) as ui:
    gr.Markdown("# Deep Research - Choose Your Approach")

    query_textbox = gr.Textbox(
        label="What topic would you like to research?",
        lines=3,
        placeholder="Enter your research topic..."
    )

    with gr.Row():
        agent_button = gr.Button(
            "🤖 Agent Research (Complete)", variant="primary")
        streaming_button = gr.Button(
            "📊 Streaming Research (Progressive)", variant="secondary")

    clarifications_input = gr.Textbox(
        label="Optional: Clarifications for Streaming Research",
        lines=2,
        placeholder="Add clarifications to focus the streaming research..."
    )

    report = gr.Markdown(label="Research Report")

    # Event handlers
    agent_button.click(
        fn=run_research_with_agent,
        inputs=[query_textbox],
        outputs=[report]
    )

    streaming_button.click(
        fn=run_research_with_streaming,
        inputs=[query_textbox, clarifications_input],
        outputs=[report]
    )

ui.launch(inbrowser=True)
