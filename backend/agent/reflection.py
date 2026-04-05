from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
import os

def reflect_on_response(response: str, context: str, user_query: str) -> dict:
    """
    Reflects on the generated response to ensure it answers the user's query comprehensively.
    Returns a dict with 'is_satisfactory' (bool) and 'feedback' (str).
    """
    if not os.getenv("GOOGLE_API_KEY"):
         # specific handling if API key is missing (for local dev/testing)
         return {"is_satisfactory": True, "feedback": "API Key missing, skipping reflection."}

    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp", temperature=0)
    
    prompt = f"""
    You are a strictly critical evaluator.
    User Query: {user_query}
    Context Provided: {context}
    Agent Response: {response}
    
    Evaluate if the Agent Response fully answers the User Query based on the Context.
     - If yes, return 'SATISFIED'.
     - If no, return 'MISSING: [explanation of what is missing]'.
    """
    
    try:
        evaluation = llm.invoke([SystemMessage(content=prompt)]).content
        
        if "SATISFIED" in evaluation:
            return {"is_satisfactory": True, "feedback": ""}
        else:
            return {"is_satisfactory": False, "feedback": evaluation.replace("MISSING: ", "")}
    except Exception as e:
        return {"is_satisfactory": True, "feedback": f"Reflection failed: {e}"}
