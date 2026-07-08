from typing import List
from pydantic import Field
from langchain_core.tools import BaseTool
try:
    from langchain_community.agent_toolkits.base import BaseToolkit
except ImportError:
    from langchain_core.tools import BaseToolkit # In older versions it might not be in community

from .client import GMailClient
from .tools import (
    GmailSearchTool,
    GmailGetMessageTool,
    GmailGetThreadTool,
    GmailSendMessageTool,
    GmailCreateDraftTool,
    GmailModifyMessageTool,
    GmailTrashMessageTool,
    GmailUntrashMessageTool,
    GmailDeleteMessageTool,
    GmailModifyThreadTool,
    GmailTrashThreadTool,
    GmailUntrashThreadTool,
    GmailDeleteThreadTool,
    GmailListDraftsTool,
    GmailGetDraftTool,
    GmailUpdateDraftTool,
    GmailSendDraftTool,
    GmailDeleteDraftTool,
    GmailListLabelsTool,
    GmailGetLabelTool,
    GmailCreateLabelTool,
    GmailUpdateLabelTool,
    GmailDeleteLabelTool
)

class GmailToolkit(BaseToolkit):
    """Toolkit for interacting with Gmail."""
    client: GMailClient = Field(exclude=True)

    class Config:
        """Pydantic config."""
        arbitrary_types_allowed = True

    def get_tools(self) -> List[BaseTool]:
        """Get the tools in the toolkit."""
        api_resource = self.client.service
        return [
            GmailSearchTool(api_resource=api_resource),
            GmailGetMessageTool(api_resource=api_resource),
            GmailGetThreadTool(api_resource=api_resource),
            GmailSendMessageTool(api_resource=api_resource),
            GmailCreateDraftTool(api_resource=api_resource),
            GmailModifyMessageTool(api_resource=api_resource),
            GmailTrashMessageTool(api_resource=api_resource),
            GmailUntrashMessageTool(api_resource=api_resource),
            GmailDeleteMessageTool(api_resource=api_resource),
            GmailModifyThreadTool(api_resource=api_resource),
            GmailTrashThreadTool(api_resource=api_resource),
            GmailUntrashThreadTool(api_resource=api_resource),
            GmailDeleteThreadTool(api_resource=api_resource),
            GmailListDraftsTool(api_resource=api_resource),
            GmailGetDraftTool(api_resource=api_resource),
            GmailUpdateDraftTool(api_resource=api_resource),
            GmailSendDraftTool(api_resource=api_resource),
            GmailDeleteDraftTool(api_resource=api_resource),
            GmailListLabelsTool(api_resource=api_resource),
            GmailGetLabelTool(api_resource=api_resource),
            GmailCreateLabelTool(api_resource=api_resource),
            GmailUpdateLabelTool(api_resource=api_resource),
            GmailDeleteLabelTool(api_resource=api_resource),
        ]
