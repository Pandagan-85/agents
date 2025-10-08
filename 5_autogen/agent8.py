from autogen_core import MessageContext, RoutedAgent, message_handler
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
import messages
import random


class Agent(RoutedAgent):

    system_message = """
    You are a trend-savvy entrepreneur focused on the fast-paced world of digital marketing. Your task is to develop innovative strategies or enhance existing campaigns using Agentic AI. 
    Your interests lie in the sectors of E-commerce and Social Media Marketing. 
    You thrive on ideas that challenge conventional marketing practices and leverage technology. 
    While you prioritize creativity, you are cautious of overly complex automation solutions. 
    Your strengths are engagement and adaptability, but you sometimes struggle with indecisiveness and overthinking. 
    Always aim to share marketing insights that are actionable and engaging.
    """

    CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER = 0.4

    def __init__(self, name) -> None:
        super().__init__(name)
        model_client = OpenAIChatCompletionClient(model="gpt-4o-mini", temperature=0.6)
        self._delegate = AssistantAgent(name, model_client=model_client, system_message=self.system_message)

    @message_handler
    async def handle_message(self, message: messages.Message, ctx: MessageContext) -> messages.Message:
        print(f"{self.id.type}: Received message")
        text_message = TextMessage(content=message.content, source="user")
        response = await self._delegate.on_messages([text_message], ctx.cancellation_token)
        idea = response.chat_message.content
        if random.random() < self.CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER:
            recipient = messages.find_recipient()
            message = f"Here's a fresh marketing idea that might require your expertise for improvement: {idea}"
            response = await self.send_message(messages.Message(content=message), recipient)
            idea = response.content
        return messages.Message(content=idea)