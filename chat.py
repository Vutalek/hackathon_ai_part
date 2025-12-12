from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

from prompts import HR_PROMPT


class Chat:
    def __init__(
        self,
        llm: BaseChatModel,
        grade: str,
        category: str,
        type: str
    ):
        self.llm = llm
        self.prompt = HR_PROMPT.format(grade=grade, category=category, type=type)
        self.messages = []
        self.messages.append(SystemMessage(self.prompt))

    async def __call__(self, message: str) -> str:
        self.messages.append(HumanMessage(message))
        result = await self.llm.ainvoke(self.messages)
        self.messages.append(result)
        return str(result.content)
    
    def clear(self):
        self.messages.clear()
        self.messages.append(SystemMessage(self.prompt))