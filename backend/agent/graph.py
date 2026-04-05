import os
import operator
from typing import Annotated, TypedDict, Union, List

from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, END

from tools.search import search_tool
from tools.wikipedia import wikipedia_tool
from tools.pdf_reader import pdf_reader_tool
from tools.youtube import youtube_transcript_tool
from memory.vector_store import vector_memory
from agent.planner import get_planner_prompt
from agent.reflection import reflect_on_response

# Define Agent State
class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]
    mode: str
    context: str
    next_step: str
    tool_output: str
    final_response: str

# Initialize LLM
# Note: In a real app, you'd likely inject this or handle API key errors more gracefully
if os.getenv("GOOGLE_API_KEY"):
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp", temperature=0.7)
else:
    llm = None # Handle this case in nodes

# --- NODES ---

def planning_node(state: AgentState):
    """
    Decides the plan based on the mode and user input.
    """
    if not llm:
        return {"next_step": "respond", "final_response": "Error: GOOGLE_API_KEY not found."}
        
    mode = state.get("mode", "Research Assistant")
    context = state.get("context", "")
    messages = state["messages"]
    
    # Simple logic: If we have no tool output and request implies research, search.
    # Otherwise, just respond.
    # A real planner would be more complex.
    
    system_prompt = get_planner_prompt(mode, context)
    
    # We ask the LLM what to do
    response = llm.invoke([SystemMessage(content=system_prompt)] + messages)
    
    # Heuristic for tool usage based on specific keywords or explicit instruction
    # In a full agent, we'd use bind_tools or structured output.
    last_msg = messages[-1].content.lower()
    
    if "search" in last_msg or "find" in last_msg:
        return {"next_step": "tool_selection", "context": context}
    else:
        return {"next_step": "respond", "final_response": response.content}

def tool_selection_node(state: AgentState):
    """
    Selects the appropriate tool.
    """
    # Simply defaulting to search for this demo or determining via LLM
    # A robust implementation would use llm.bind_tools()
    return {"next_step": "tool_execution", "tool_name": "search"}

def tool_execution_node(state: AgentState):
    """
    Executes the selected tool.
    """
    query = state["messages"][-1].content
    # Using the search tool primarily for this demo flow
    try:
        result = search_tool.invoke(query)
        # Store in vector memory for long-term retention
        vector_memory.store(str(result), meta={"query": query})
        return {"tool_output": str(result), "next_step": "reflection"}
    except Exception as e:
        return {"tool_output": f"Error executing tool: {e}", "next_step": "reflection"}

def reflection_node(state: AgentState):
    """
    Reflects on the findings.
    """
    tool_output = state.get("tool_output", "")
    user_query = state["messages"][-1].content
    
    # If using LLM for reflection
    reflection = reflect_on_response(tool_output, state.get("context", ""), user_query)
    
    if reflection["is_satisfactory"]:
        return {"next_step": "respond"}
    else:
        # Retry or just proceed with what we have for now to avoid infinite loops in demo
        return {"next_step": "respond"} 

def response_node(state: AgentState):
    """
    Generates the final response.
    """
    if state.get("final_response"):
        return {} # Already have it
    
    if not llm:
        return {"final_response": "Error: GOOGLE_API_KEY not found."}

    mode = state.get("mode", "Research Assistant")
    context = state.get("context", "")
    tool_output = state.get("tool_output", "")
    messages = state["messages"]
    
    system_prompt = get_planner_prompt(mode, context + "\nTool Results: " + tool_output)
    response = llm.invoke([SystemMessage(content=system_prompt)] + messages)
    
    return {"final_response": response.content}

# --- GRAPH ---

workflow = StateGraph(AgentState)

workflow.add_node("planning", planning_node)
workflow.add_node("tool_selection", tool_selection_node)
workflow.add_node("tool_execution", tool_execution_node)
workflow.add_node("reflection", reflection_node)
workflow.add_node("respond", response_node)

workflow.set_entry_point("planning")

# Conditional Edges
def route_step(state):
    return state["next_step"]

workflow.add_conditional_edges(
    "planning",
    route_step,
    {
        "tool_selection": "tool_selection",
        "respond": "respond"
    }
)

workflow.add_edge("tool_selection", "tool_execution")
workflow.add_edge("tool_execution", "reflection")

workflow.add_conditional_edges(
    "reflection",
    route_step,
    {
        "respond": "respond",
        # "planning": "planning" # Could loop back here
    }
)

workflow.add_edge("respond", END)

# Compile
app_graph = workflow.compile()
