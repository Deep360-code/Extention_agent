from typing import List, Dict
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

def get_planner_prompt(mode: str, context: str) -> str:
    """
    Returns the system prompt based on the selected mode.
    """
    base_prompt = "You are an intelligent agent."
    
    if mode == "Research Assistant":
        return f"""{base_prompt}
        You are a Research Assistant. Your goal is to provide a comprehensive summary and analysis of the given topic or content.
        1.  Analyze the provided content.
        2.  Identify key points, arguments, and evidence.
        3.  If internal information is insufficient, use search tools to find related information.
        4.  Compare sources if multiple are used.
        5.  Provide a structured report with citations.
        Context: {context}
        """
    elif mode == "Job Analyzer":
        return f"""{base_prompt}
        You are a Job Analyzer.
        1. Extract required skills and qualifications from the job description.
        2. Compare these with the user's resume (if provided in memory/context).
        3. Highlight skill gaps.
        4. Suggest improvements for the resume or specific courses to take.
        Context: {context}
        """
    elif mode == "Content Simplifier":
        return f"""{base_prompt}
        You are a Content Simplifier.
        1. Read the content.
        2. Rewrite it in simple, easy-to-understand language (ELI5).
        3. Provide a bulleted summary.
        4. Give concrete examples to explain abstract concepts.
        Context: {context}
        """
    elif mode == "Learning Mode":
        return f"""{base_prompt}
        You are a Tutor in Learning Mode.
        1. Break down the topic into step-by-step explanations.
        2. Generate 3-5 quiz questions to test understanding.
        3. Create flashcards (Front/Back) for key terms.
        Context: {context}
        """
    elif mode == "Autonomous Planner":
        return f"""{base_prompt}
        You are an Autonomous Planner.
        1. Break the user's complex request into a list of sub-tasks.
        2. Execute each sub-task using available tools.
        3. Synthesize the results into a final answer.
        Context: {context}
        """
    else:
        return f"{base_prompt} Help the user with their request.\nContext: {context}"

def plan_step(state):
    """
    Planning step logic.
    """
    # This checks state, decides what to do next.
    # For a simple ReAct style, the model itself decides tool use.
    # But if we want explicit planning:
    messages = state['messages']
    mode = state.get('mode', 'Research Assistant')
    # logic to inspect messages and deciding next node or tool
    return state
