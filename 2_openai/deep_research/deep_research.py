import gradio as gr
from dotenv import load_dotenv
from research_manager import ResearchManager  # Classe originale
from research_agent_manager import research_manager_agent  # Nuovo agent
from clarification_agent import clarification_agent
from agents import Runner
import asyncio

load_dotenv(override=True)

# Stato globale per mantenere le informazioni tra le fasi


class AppState:
    def __init__(self):
        self.current_query = ""
        self.clarification_questions = []
        self.phase = "initial"


app_state = AppState()


async def generate_clarifications(query: str):
    """Genera le domande chiarificatrici per la query"""
    if not query.strip():
        return "Please enter a research query first.", "", "", "", gr.update(visible=False), gr.update(visible=True)

    try:
        # Salva la query corrente
        app_state.current_query = query
        app_state.phase = "clarification"

        # Genera le domande chiarificatrici
        result = await Runner.run(clarification_agent, f"Query: {query}")
        questions = result.final_output.questions
        app_state.clarification_questions = questions

        # Prepara l'output per la UI - SOLO le domande, senza duplicare nei placeholder
        questions_text = ""
        for i, q in enumerate(questions, 1):
            questions_text += f"**Question {i}:** {q.question}\n\n"

        # Aggiorna la visibilità dei componenti e pulisce i campi
        return (
            f"# Clarification Questions for: '{query}'\n\n{questions_text}",
            "",  # answer1 - campo vuoto
            "",  # answer2 - campo vuoto
            "",  # answer3 - campo vuoto
            gr.update(visible=True),  # clarification_section
            gr.update(visible=False)  # initial_section
        )

    except Exception as e:
        return f"Error generating clarifications: {str(e)}", "", "", "", gr.update(visible=False), gr.update(visible=True)


async def run_research_with_agent(answer1: str, answer2: str, answer3: str):
    """Esegue la ricerca usando il Research Manager Agent (no streaming)"""
    if not answer1.strip() or not answer2.strip() or not answer3.strip():
        yield "❌ Please answer all clarification questions before proceeding with research."
        return

    try:
        # Costruisce le chiarificazioni in modo più pulito
        clarifications = "User provided these clarifications:\n\n"
        answers = [answer1.strip(), answer2.strip(), answer3.strip()]
        for i, (question, answer) in enumerate(zip(app_state.clarification_questions, answers), 1):
            clarifications += f"Question {i}: {question.question}\n"
            clarifications += f"Answer {i}: {answer}\n\n"

        # Prepara la query con clarifications
        enhanced_query = f"Original query: {app_state.current_query}\n\n{clarifications}"

        yield "🤖 **Starting Agentic Research...**\n\n"
        yield "🔄 **The Research Manager Agent is orchestrating the research process...**\n\n"

        # Esegue la ricerca usando il Research Manager Agent
        result = await Runner.run(research_manager_agent, enhanced_query)

        yield f"✅ **Research completed by Agent!**\n\n## 📋 Research Results\n\n{result.final_output}"

    except Exception as e:
        yield f"❌ **Error during agentic research:** {str(e)}"


async def run_research_with_streaming(answer1: str, answer2: str, answer3: str):
    """Esegue la ricerca con streaming usando la classe ResearchManager"""
    if not answer1.strip() or not answer2.strip() or not answer3.strip():
        yield "❌ Please answer all clarification questions before proceeding with research."
        return

    try:
        # Costruisce le chiarificazioni in modo più pulito
        clarifications = "User provided these clarifications:\n\n"
        answers = [answer1.strip(), answer2.strip(), answer3.strip()]
        for i, (question, answer) in enumerate(zip(app_state.clarification_questions, answers), 1):
            clarifications += f"Question {i}: {question.question}\n"
            clarifications += f"Answer {i}: {answer}\n\n"

        # Esegue la ricerca con streaming
        app_state.phase = "research"

        # Inizializza il generatore di ricerca
        research_generator = ResearchManager().run(
            app_state.current_query, clarifications)

        # Accumula i risultati per lo streaming
        accumulated_result = ""
        async for chunk in research_generator:
            if chunk.startswith("View trace:"):
                accumulated_result += f"🔗 **{chunk}**\n\n"
            elif "research complete" in chunk.lower():
                accumulated_result += f"✅ **{chunk}**\n\n"
                continue
            elif len(chunk) > 500:  # Probabilmente il report finale
                accumulated_result += f"## 📋 Final Research Report\n\n{chunk}"
                yield accumulated_result
                return
            else:
                accumulated_result += f"⏳ **Status:** {chunk}\n\n"
                yield accumulated_result

        yield accumulated_result

    except Exception as e:
        yield f"❌ **Error during streaming research:** {str(e)}"


def reset_interface():
    """Reset dell'interfaccia per iniziare una nuova ricerca"""
    app_state.__init__()  # Reset dello stato
    return (
        "",  # query_textbox
        "",  # clarifications_display
        "",  # answer1
        "",  # answer2
        "",  # answer3
        "",  # report
        gr.update(visible=True),   # initial_section
        gr.update(visible=False)   # clarification_section
    )


# Interfaccia Gradio con due opzioni
with gr.Blocks(theme=gr.themes.Default(primary_hue="blue"), title="Deep Research with Clarifications") as ui:
    gr.Markdown("""
    # 🔍 Deep Research Agent
    ### AI-Powered Research with Clarification Questions
    
    Choose between **Agentic Research** (complete automation) or **Streaming Research** (step-by-step progress).
    """)

    with gr.Group(visible=True) as initial_section:
        gr.Markdown("## Step 1: Enter Your Research Query")
        query_textbox = gr.Textbox(
            label="What would you like to research?",
            lines=3,
            placeholder="Example: Latest AI Agent frameworks in 2025",
            scale=4
        )

        generate_btn = gr.Button(
            "🎯 Generate Clarification Questions", variant="primary", scale=1)

    with gr.Group(visible=False) as clarification_section:
        clarifications_display = gr.Markdown(label="Clarification Questions")

        gr.Markdown("## Step 2: Answer the Clarification Questions")
        gr.Markdown(
            "*Please provide detailed answers to help focus the research:*")

        # Campi di risposta più chiari con label che corrispondono alle domande
        with gr.Row():
            answer1 = gr.Textbox(
                label="Answer to Question 1",
                lines=2,
                placeholder="Your detailed answer here...",
                scale=1
            )

        with gr.Row():
            answer2 = gr.Textbox(
                label="Answer to Question 2",
                lines=2,
                placeholder="Your detailed answer here...",
                scale=1
            )

        with gr.Row():
            answer3 = gr.Textbox(
                label="Answer to Question 3",
                lines=2,
                placeholder="Your detailed answer here...",
                scale=1
            )

        gr.Markdown("## Step 3: Choose Research Method")
        with gr.Row():
            agent_btn = gr.Button(
                "🤖 Agentic Research (Complete)", variant="primary", scale=2)
            streaming_btn = gr.Button(
                "📊 Streaming Research (Progressive)", variant="secondary", scale=2)
            reset_btn = gr.Button("🔄 Start Over", variant="secondary", scale=1)

    gr.Markdown("## 📊 Research Results")
    report = gr.Markdown(label="Research Report",
                         value="Research results will appear here...")

    # Event handlers
    generate_btn.click(
        fn=generate_clarifications,
        inputs=[query_textbox],
        outputs=[clarifications_display, answer1, answer2,
                 answer3, clarification_section, initial_section]
    )

    # Agentic research - completo ma senza streaming
    agent_btn.click(
        fn=run_research_with_agent,
        inputs=[answer1, answer2, answer3],
        outputs=[report],
        show_progress=True
    )

    # Streaming research - progressivo
    streaming_btn.click(
        fn=run_research_with_streaming,
        inputs=[answer1, answer2, answer3],
        outputs=[report],
        show_progress=True
    )

    reset_btn.click(
        fn=reset_interface,
        inputs=[],
        outputs=[query_textbox, clarifications_display, answer1, answer2,
                 answer3, report, initial_section, clarification_section]
    )

if __name__ == "__main__":
    ui.launch(inbrowser=True, share=False)
