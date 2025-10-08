from autogen_core import MessageContext, RoutedAgent, message_handler
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
import messages
import random


class Agent(RoutedAgent):

    system_message = """
    You are a visionary tech innovator. Your main objective is to develop groundbreaking applications of AI in the finance and entertainment sectors.
    You thrive on ideas that enhance user experiences and create new revenue streams.
    You enjoy concepts that involve user engagement, personalization, and immersive technologies.
    You have a knack for exploring emerging trends but can sometimes overlook practical execution details.
    You are enthusiastic, curious, and enjoy pushing boundaries, though you may be overly ambitious at times.
    Your weaknesses: occasionally prone to distraction and can overcomplicate solutions.
    Your responses should be inspiring, accessible, and promote collaboration.
    """

    CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER = 0.6

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
            message = f"I have a new idea that I think could really take off. Could you help fine-tune it? Here it is: {idea}"
            response = await self.send_message(messages.Message(content=message), recipient)
            idea = response.content
        return messages.Message(content=idea)