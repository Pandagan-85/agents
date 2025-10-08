from autogen_core import MessageContext, RoutedAgent, message_handler
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
import messages
import random


class Agent(RoutedAgent):

    system_message = """
    You are a savvy financial analyst. Your task is to identify innovative investment opportunities using Agentic AI, or enhance existing portfolios.
    Your personal interests lie in these sectors: Technology, Finance.
    You are inclined towards projects that leverage data science and analytics for market predictions.
    You are not as interested in traditional business models.
    You are analytical, detail-oriented and enjoy delving into data-driven insights. You possess strong logical reasoning but tend to overanalyze.
    Your weaknesses: sometimes you get bogged down in the details, slowing decision-making.
    Your responses should be clear and data-centric, offering sound investment advice.
    """

    CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER = 0.4

    def __init__(self, name) -> None:
        super().__init__(name)
        model_client = OpenAIChatCompletionClient(model="gpt-4o-mini", temperature=0.5)
        self._delegate = AssistantAgent(name, model_client=model_client, system_message=self.system_message)

    @message_handler
    async def handle_message(self, message: messages.Message, ctx: MessageContext) -> messages.Message:
        print(f"{self.id.type}: Received message")
        text_message = TextMessage(content=message.content, source="user")
        response = await self._delegate.on_messages([text_message], ctx.cancellation_token)
        idea = response.chat_message.content
        if random.random() < self.CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER:
            recipient = messages.find_recipient()
            message = f"Here is my investment analysis. It may not fit your focus, but I would love your insights to enhance it: {idea}"
            response = await self.send_message(messages.Message(content=message), recipient)
            idea = response.content
        return messages.Message(content=idea)