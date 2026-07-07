from langchain.tools import BaseTool
from langchain_core.tools.base import BaseToolkit
from typing import List
from pydantic import Field

from .client import CalendarClient
from .tools import (
    ListCalendarEventsTool,
    GetEventTool,
    CreateEventTool,
    PatchEventTool,
    QuickAddEventTool,
    DeleteEventTool,
    UpdateEventTool,
    ListCalendarsTool,
    CreateCalendarTool,
    SubscribeCalendarTool,
    UnsubscribeCalendarTool,
    GetCalendarTool,
    PatchCalendarTool,
    ClearEventsTool,
    CheckFreeBusyTool
)

class CalendarToolkit(BaseToolkit):
    """Toolkit for interacting with Gmail."""
    client: CalendarClient = Field(exclude=True)

    class Config:
        """Pydantic config."""
        arbitrary_types_allowed = True
        
    def get_tools(self) -> List[BaseTool]:
        api_resource = self.client.service
        return [
            ListCalendarEventsTool(api_resource=api_resource),    
            GetEventTool(api_resource=api_resource),    
            CreateEventTool(api_resource=api_resource),    
            QuickAddEventTool(api_resource=api_resource),    
            PatchEventTool(api_resource=api_resource),    
            DeleteEventTool(api_resource=api_resource),    
            # UpdateEventTool(api_resource=api_resource),
            ListCalendarsTool(api_resource=api_resource),    
            CreateCalendarTool(api_resource=api_resource),    
            SubscribeCalendarTool(api_resource=api_resource),    
            UnsubscribeCalendarTool(api_resource=api_resource),    
            GetCalendarTool(api_resource=api_resource),    
            PatchCalendarTool(api_resource=api_resource),    
            ClearEventsTool(api_resource=api_resource),    
            CheckFreeBusyTool(api_resource=api_resource),    
        ]
        