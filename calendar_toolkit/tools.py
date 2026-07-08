from langchain.tools import BaseTool
from googleapiclient.discovery import Resource
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Literal, Any, Type

class CalendarTool(BaseTool):
    api_resource: Resource
    
##################################################################################
#                               Pydantic Schemas
##################################################################################

# ------------------------------------ Events ------------------------------------
class CreateEventSchema(BaseModel):
    calendarId: str = Field(default="primary", description="The Id of the calendar where the event has to be created")
    body: Dict[str, Any] = Field(
        description=(
            "The body of the event as follows: \n"
            "{\n"
            "    'summary': 'Project Sync Meeting',\n"
            "    'location': 'Conference Room A','description': 'Reviewing toolkit development milestones.',\n"
            "    'start': {\n"
            "        'dateTime': '2026-07-04T21:38:20.905084Z',\n"
            "        'timeZone': 'Asia/Calcutta',\n"
            "    },\n"
            "    'end': {\n"
            "        'dateTime': '2026-07-04T21:40:09.905084Z',\n"
            "        'timeZone': 'Asia/Calcutta',\n"
            "    },\n"
            "    'attendees': [\n"
            "        {'email': 'kasaharsha2007@gmail.com'},\n"
            "    ],\n"
            "}\n"
            "You can get timezone and datetime format using other tools or can default to America/New_York"
        )
    )
    sendUpdates: Optional[Literal["all", "externalOnly", "none"]] = Field(
        default=None, 
        description=(
            "This option decides whom to send updates\n"
            "`all`: send updates to everyone\n"
            "`externalOnly`: send updates to external only\n"
            "`none`: send updates to no one." 
        )
    )  
    
class QuickAddEventSchema(BaseModel):
    calendarId: str = Field(default="primary", description="The Id of the calendar where the event has to be created")
    text: str = Field(..., 
        description=(
            "Natural language text describing the event\n"
            "Example: `Dentist appointment on July 10 at 3pm`"
        )
    )
    sendUpdates: Optional[Literal["all", "externalOnly", "none"]] = Field(
        default=None, 
        description=(
            "This option decides whom to send updates\n"
            "`all`: send updates to everyone\n"
            "`externalOnly`: send updates to external only\n"
            "`none`: send updates to no one." 
        )
    )  
    
class ListEventsSchema(BaseModel):
    calendarId: str = Field(default="primary", description="The Id of the calendar from where the events has to be obtained")
    timeMin: Optional[str] = Field(default=None, description="The lower bound(inclusive) for an event's start time formatted as an RFC3339 timestamp (e.g.,  '2026-07-04T00:00:00")
    singleEvents: Optional[bool] = Field(
        default=False, 
        description=""" Crucial for recursive events. If set to it expands recurive events into individual
instances. If  False returns only the recurring event."""
    )
    orderBy: Optional[str] =Field(default=None,
        description="""The sorting sequence for the items returned. 
        Acceptable values:
            - `startTime` (Requires singleEvents=True)
            - `updated`  (Sorts by last modification chronological time)"
        """
    )
    maxResults: Optional[int] = Field(default=10, description="Maximum number of events returned on a single page")
    detail: bool = Field(
        default=False, 
        description=(
            "Decides whether the tool should return all the details of the events or only the events ids as a list.\n"
            "- True: Provide complete details"
            "- False: Provide only the ids."
            "Use this only ocassionally and with caution."
        )
    )
    
class GetEventSchema(BaseModel):
    calendarId: str = Field(default="primary", description="The Id of the calendar from where the events has to be obtained")
    eventId: str = Field(..., description="The Id of the event whose details has to be obtained")
    
class PatchEventSchema(BaseModel):
    calendarId: str = Field(default="primary", description="The Id of the calendar from where the events has to be obtained")
    eventId: str = Field(..., description="The Id of the event whose details has to be obtained")
    body: Dict[str, Any] = Field(
        description=(
            "The body of the event as follows: \n"
            "{\n"
            "    'summary': 'Project Sync Meeting',\n"
            "    'location': 'Conference Room A','description': 'Reviewing toolkit development milestones.',\n"
            "    'start': {\n"
            "        'dateTime': '2026-07-04T21:38:20.905084Z',\n"
            "        'timeZone': 'Asia/Calcutta',\n"
            "    },\n"
            "    'end': {\n"
            "        'dateTime': '2026-07-04T21:40:09.905084Z',\n"
            "        'timeZone': 'Asia/Calcutta',\n"
            "    },\n"
            "    'attendees': [\n"
            "        {'email': 'kasaharsha2007@gmail.com'},\n"
            "    ],\n"
            "}\n"
            "You can get timezone and datetime format using other tools or can default to America/New_York\n"
            "Only some fields can be part of the body. Only the fields specified in the body will get updated."
        )
    )

class DeleteEventSchema(BaseModel):
    calendarId: str = Field(default="primary", description="The Id of the calendar where the event has to be created")
    eventId: str = Field(..., description="The Id of the event that has to be deleted")
    sendUpdates: Optional[Literal["all", "externalOnly", "none"]] = Field(
        default="none", 
        description=(
            "This option decides whom to send updates\n"
            "`all`: send updates to everyone\n"
            "`externalOnly`: send updates to external only\n"
            "`none`: send updates to no one." 
        )
    )  
    
# --------------------------------- CalendarList ---------------------------------
class ListCalendarsSchema(BaseModel):
    maxResults: Optional[int] = Field(default=10, description="Maximum number of events returned on a single page")
    detail: bool = Field(
        default=False, 
        description=(
            "Decides whether the tool should return all the details of the calendars or only the calendar ids as a list.\n"
            "- True: Provide detauls like `id`, `title`, `description`, `timezone`"
            "- False: Provide only the ids."
            "Use this only when all the calendar specs should be simultaneously known."
        )
    )
    showHidden: bool = Field(default=False, description="Whether to return hidden calendars or not. `False` doesn't return hidden ones.")
    showDeleted: bool = Field(default=False, description="Whether to return deleted calendars or not. `False` doesn't return deleted ones.")

class GetCalendarSchema(BaseModel):
    calendarId: str = Field(default="primary", description="The Id of the calendar from whose details has to be obtained")

class SubscribeCalendarSchema(BaseModel):
    body: Dict[str, Any] = Field(..., description=(
        "A detailed body about the settings of the subscribed calendar with a mandatory calendarId (id) as flowwlows\n"
        "{"
        "   'id': 'marketing-team-calendar-id@group.calendar.google.com',\n"
        "   'selected': True # Automatically check the box to show it in the UI\n"
        "}"
    ))

class UnsubscribeCalendarSchema(BaseModel):
    calendarId: str = Field(..., description="The Id of the calendar to be unscubscribed")
    
# ---------------------------------- Calendars ----------------------------------
class CreateCalendarSchema(BaseModel):
    body: Dict[str, Any] = Field(..., description=(
        "The body of the calendar as follows:\n"
        "{\n"
        "   'summary': 'Company Marketing Calendar',  # Required\n"
        "   'description': 'Tracking all social media and email campaigns.',\n"
        "   'timeZone': 'America/Los_Angeles',\n"
        "   'location': 'San Francisco, CA'\n"
        "}"
    ))

class ClearEventsSchema(BaseModel):
    calendarId: str = Field(..., description="The Id of the calendar from which all the events has to be deleted")

class PatchCalendarSchema(BaseModel):
    calendarId: str = Field(default="primary", description="The Id of the calendar which has to be patched")
    body: Dict[str, Any] = Field(..., description=(
        "The body of the calendar as follows:\n"
        "{\n"
        "   'summary': 'Company Marketing Calendar',  # Required\n"
        "   'description': 'Tracking all social media and email campaigns.',\n"
        "   'timeZone': 'America/Los_Angeles',\n"
        "   'location': 'San Francisco, CA'\n"
        "}"
    ))

# ------------------------------- FreeBusy ---------------------------------------
class CheckFreeBusySchema(BaseModel):
    body: Dict[str, Any] = Field(..., description=(
        "A detailed body about the free/busy check as follows:\n"
        "{\n"
        "   'timeMin': '2025-01-01T00:00:00Z',  # Required\n"
        "   'timeMax': '2025-01-01T00:00:00Z',  # Required\n"
        "   'items': [\n"
        "       {\n"
        "           'id': 'primary',  # Required\n"
        "       }\n"
        "   ]\n"
        "}"
    ))

##################################################################################
#                                   Tools
##################################################################################


# ------------------------------------ Events ------------------------------------
class CreateEventTool(CalendarTool):
    name: str = "create_event_tool"
    description:str = "Creates an event based on the provided json event body"
    args_schema: Type[BaseModel] = CreateEventSchema
    
    def _run(self, body: Dict[str, Any], calendarId: str = "primary", sendUpdates: Optional[str] = None, **kwargs: Any) -> Dict[str, Any]:
        return self.api_resource.events().insert(
            calendarId=calendarId,
            body=body,
            sendUpdates="none" if not sendUpdates else sendUpdates 
        ).execute()

class ListCalendarEventsTool(CalendarTool):
    name: str = "list_calendar_events_tool"
    description:str = "Creates an event based on the provided details"
    args_schema: Type[BaseModel] = ListEventsSchema
    
    def _run(
        self, 
        calendarId: str = "primary", 
        timeMin: Optional[str] = None,
        singleEvents: Optional[bool] = False,
        orderBy: Optional[str] = None,
        maxResults: Optional[int] = 10,
        detail: bool = False,
        **kwargs: Any
    ) -> List[Any]:
        params = {
            "calendarId": calendarId,
            "maxResults": maxResults,
            "singleEvents": singleEvents
        }
        if timeMin:
            params["timeMin"] = timeMin
        if orderBy:
            params["orderBy"] = orderBy

        try:
            events = self.api_resource.events().list(**params).execute().get("items", [])
            if not events:
                return f"No events exists in this calendar {calendarId}"
            if detail:
                return [{
                    "id": event["id"],
                    "title": event["summary"],
                    "description": event.get("description", "")[:100],
                    "location": event.get("location", ''),
                    "start": event["start"],
                    "end": event["end"],
                } for event in events] 
            else:
                return [event["id"] for event in events]
        except Exception as e:
            return f"Error occured: {str(e)}"
        
class GetEventTool(CalendarTool):
    name: str = "get_event_tool"
    description: str = "Retireves complete details about an event"
    args_schema: Type[BaseModel] = GetEventSchema
    
    def _run(self, eventId: str, calendarId: str = "primary"): 
        try:
            return self.api_resource.events().get(calendarId=calendarId, eventId=eventId).execute()
        except Exception as e:
            return f"Error getting the event: {str(e)}"
    
class QuickAddEventTool(CalendarTool):
    name: str = "quickadd_event_tool"
    description: str = "Creates an event directly from natural language text"
    args_schema: Type[BaseModel] = QuickAddEventSchema
    
    def _run(
        self, 
        text: str,
        calendarId: str = "primary",
        sendUpdates: str = "none"
    ) -> Dict[str, Any]:
        try:
            return self.api_resource.events().quickAdd(
                calendarId=calendarId, 
                text=text, 
                sendUpdates=sendUpdates
            ).execute()
        except Exception as e:
            return f"Error creating the event: {str(e)}"
        
class PatchEventTool(CalendarTool):
    name: str = "patch_event_tool"
    description: str = (
        "Updates the event details based on the provided body\n"
        "NOTE: Only the fields provided in the body will be updated"
    )
    args_schema: Type[BaseModel] = PatchEventSchema
    
    def _run(self, eventId: str, body: Dict[str, Any], calendarId: str = "primary", **kwargs: Any) -> Dict[str, Any]:
        try:
            return self.api_resource.events().patch(
                eventId=eventId,
                calendarId=calendarId,
                body=body
            ).execute()
        except Exception as e:
            return f"Error updating the event: {str(e)}"
        
class UpdateEventTool(CalendarTool):
    name: str = "update_event_tool"
    description: str = (
        "Updates the event details based on the provided body\n"
        "NOTE: Only the fields provided in the body will be remain in the event. All other fields get deleted.\n"
        "In simple words, completely replaces the event body with the new body provided."
    )
    args_schema: Type[BaseModel] = PatchEventSchema
    
    def _run(self, eventId: str, body: Dict[str, Any], calendarId: str = "primary", **kwargs: Any) -> Dict[str, Any]:
        try:
            return self.api_resource.events().update(
                eventId=eventId,
                calendarId=calendarId,
                body=body
            ).execute()
        except Exception as e:
            return f"Error updating the event: {str(e)}"
        
        
class DeleteEventTool(CalendarTool):
    name: str = "delete_event_tool"
    description: str = " Deletes an event completely from the calendar"
    args_schema: Type[BaseModel] = DeleteEventSchema
    
    def _run(self, eventId: str, calendarId: str = "primary", sendUpdates: str = "none"):
        try:
            self.api_resource.events().delete(
                calendarId=calendarId,
                eventId=eventId,
                sendUpdates=sendUpdates
            ).execute()
            return f"Event {eventId} deleted successfully"
        except Exception as e:
            return f"Error deleting the event: {str(e)}"
    
# ------------------------------------ CalenderList ------------------------------------
class ListCalendarsTool(CalendarTool):
    name: str = "list_calendars_tool"
    description: str = "Return the details about the calendars or calendar ids."
    args_schema: Type[BaseModel] = ListCalendarsSchema
    
    def _run(self, maxResults: int=10, detail: bool = False, showHidden: bool = False, showDeleted: bool = False):
        calendars = self.api_resource.calendarList().list(
            maxResults=maxResults,
            showHidden=showHidden,
            showDeleted=showDeleted,
        ).execute().get("items", [])
        if not calendars:
            return "No calendars exist"
        if detail:
            return [{
                "id": calendar["id"],
                "title": calendar["summary"],
                "description": calendar.get("description", ''),
                "timeZone": calendar["timeZone"]
            } for calendar in calendars]
        return [calendar["id"] for calendar in calendars]
    
class GetCalendarTool(CalendarTool):
    name: str = "get_calendar_tool"
    description: str = "Provide complete details about a calendar"
    args_schema: Type[BaseModel] = GetCalendarSchema
    
    def _run(self, calendarId: str = "primary"):
        return self.api_resource.calendarList().get(calendarId=calendarId).execute()
    
class SubscribeCalendarTool(CalendarTool):
    name: str = "subscribe_calendar_tool"
    description: str = "Subscibes to a secondary external calendar given the calendar Id"
    args_schema: Type[BaseModel] = SubscribeCalendarSchema
    
    def _run(self, body: Dict[str, Any]):
        try:
            return self.api_resource.calendarList().insert(body=body).execute()
        except Exception as e:
            return f"Error during subscribing: {str(e)}"
        
class UnsubscribeCalendarTool(CalendarTool):
    name: str = "unsubscribe_calendar_tool"
    description: str = "Unsubscibes to a secondary external calendar given the calendar Id"
    args_schema: Type[BaseModel] = UnsubscribeCalendarSchema
    
    def _run(self, calendarId: str):
        try:
            self.api_resource.calendarList().delete(calendarId=calendarId).execute()
            return f"Successfully unsubscribed from calendar {calendarId}"
        except Exception as e:
            return f"Error during unsubscribing: {str(e)}"
            
# ------------------------------------- Calendars -------------------------------------
class CreateCalendarTool(CalendarTool):
    name: str = "create_calendar_tool"
    description: str = "Creates a secondary calendar given the essential details in a JSON body"
    args_schema: Type[BaseModel] = CreateCalendarSchema
    
    def _run(self, body: Dict[str, Any]):
        try:
            return self.api_resource.calendars().insert(body=body).execute()
        except Exception as e:
            return f"Error during creating a calendar: {str(e)}"
        
class ClearEventsTool(CalendarTool):
    name: str = "clear_events_tool"
    description: str = "Deletes all the events in a calendar"
    args_schema: Type[BaseModel] = ClearEventsSchema
    
    def _run(self, calendarId):
        try:
            self.api_resource.calendars().clear(calendarId=calendarId).execute()
            return f"Successfully deleted all events from calendar {calendarId}"
        except Exception as e:
            return f"Error during creating a calendar: {str(e)}"
        
class PatchCalendarTool(CalendarTool):
    name: str = "patch_calendar_tool"
    description: str = (
        "Updates the calendar details based on the provided body\n."
        "The updates can be viewd by anyone asscociated with the calendar\n"
        "NOTE: Only the fields provided in the body will be updated"
    )
    args_schema: Type[BaseModel] = PatchCalendarSchema
    
    def _run(self, calendarId: str, body: Dict[str, Any]):
        try:
            return self.api_resource.calendars().patch(calendarId=calendarId, body=body).execute()
        except Exception as e:
            return f"Error during updating a calendar: {str(e)}"

# ---------------------------------- FreeBusy ---------------------------------
class CheckFreeBusyTool(CalendarTool):
    name: str = "check_free_busy_tool"
    description: str = "Checks the free/busy status of use during a period and also overlappings accross the events"
    args_schema: Type[BaseModel] = CheckFreeBusySchema
    
    def _run(self, body: Dict[str, Any]):
        try:
            return self.api_resource.freebusy().query(body=body).execute()
        except Exception as e:
            return f"Error checking free/busy status: {str(e)}"