from langgraph.graph import StateGraph,START,END
from typing import TypedDict,Annotated,List


class AIAgentOrchestrator:

    class MarsAgentState(TypedDict):
        extracted_details = Annotated[str,Field(description="Extracted details from the email")]
        
        