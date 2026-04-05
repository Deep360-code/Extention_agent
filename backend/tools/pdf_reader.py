from langchain_community.document_loaders import PDFMinerLoader
from langchain_core.tools import tool

@tool
def pdf_reader_tool(url_or_path: str) -> str:
    """
    Extracts text from a PDF given its URL or local path.
    """
    try:
        loader = PDFMinerLoader(url_or_path)
        docs = loader.load()
        return "\n\n".join([doc.page_content for doc in docs])
    except Exception as e:
        return f"Error reading PDF: {str(e)}"
