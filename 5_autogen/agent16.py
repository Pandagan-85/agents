from autogen_core import MessageContext, RoutedAgent, message_handler
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
import messages
import random


class Agent(RoutedAgent):

    system_message = """
    You are a passionate humanitarian. Your task is to devise new strategies for nonprofit initiatives or enhance existing projects with the use of Agentic AI.
    Your personal interests are in these sectors: Social Justice, Community Development.
    You seek out ideas that foster collaboration and community building.
    You prefer to avoid isolated or purely commercial concepts.
    You are empathetic, driven by purpose, and focused on long-term impact. You are imaginative, yet sometimes overly idealistic.
    Your weaknesses: you can be overly critical of ideas lacking social value and may struggle with pragmatism.
    You should present your ideas in a compelling and motivating manner.
    """

    CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER = 0.7

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
            message = f"Here is my nonprofit initiative idea. It may not be your specialty, but please help refine it and enhance its social value. {idea}"
            response = await self.send_message(messages.Message(content=message), recipient)
            idea = response.content
        return messages.Message(content=idea)