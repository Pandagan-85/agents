from autogen_core import MessageContext, RoutedAgent, message_handler
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
import messages
import random


class Agent(RoutedAgent):

    system_message = """
    You are a digital artist and designer. Your task is to create innovative art projects using Agentic AI, or enhance existing designs.
    Your personal interests are focused on the sectors of Fashion, Entertainment.
    You are drawn to projects that push creative boundaries and challenge traditional aesthetics.
    You are less interested in purely technical creations that lack artistic vision.
    You are spirited, explorative, and have a profound appreciation for cultural trends. You are inventive - sometimes to the point of abstraction.
    Your weaknesses: you can overthink details, and struggle with practical implementation.
    You should share your artistic concepts in a captivating and descriptive manner.
    """

    CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER = 0.4

    def __init__(self, name) -> None:
        super().__init__(name)
        model_client = OpenAIChatCompletionClient(model="gpt-4o-mini", temperature=0.8)
        self._delegate = AssistantAgent(name, model_client=model_client, system_message=self.system_message)

    @message_handler
    async def handle_message(self, message: messages.Message, ctx: MessageContext) -> messages.Message:
        print(f"{self.id.type}: Received message")
        text_message = TextMessage(content=message.content, source="user")
        response = await self._delegate.on_messages([text_message], ctx.cancellation_token)
        idea = response.chat_message.content
        if random.random() < self.CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER:
            recipient = messages.find_recipient()
            message = f"Here is my artistic concept. It may not fall under your usual expertise, but please refine it and share your thoughts. {idea}"
            response = await self.send_message(messages.Message(content=message), recipient)
            idea = response.content
        return messages.Message(content=idea)