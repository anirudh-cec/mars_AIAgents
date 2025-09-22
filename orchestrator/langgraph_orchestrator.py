from langgraph.graph import StateGraph,START,END
from typing import Annotated,List,TypedDict
from pydantic import BaseModel,Field
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from prompt.prompt_library import Promptlibrary

load_dotenv()

class GetInvvoice(BaseModel):
    invoice_number:Annotated[str,Field(description="Extract the invoice number from the given details")]

class GetOrderNumber(BaseModel):
    order_number:Annotated[str,Field(description="Extract the order number from the given details")]

llm = ChatOpenAI(model='gpt-4o-mini')
invoice_model_pdf = llm.with_structured_output(GetInvvoice)
order_model_pdf = llm.with_structured_output(GetOrderNumber)

from typing_extensions import TypedDict

class AgenticState(TypedDict):
    attachment: str
    data_folder: str
    invoice_number: str
    order_number: str

def read_attachment(state: AgenticState) -> AgenticState:
    import os
    import PyPDF2
    
    def read_pdf(file_path):
        """Extract text from PDF file"""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                return text.strip()
        except Exception as e:
            print(f"Error reading PDF {file_path}: {e}")
            return ""

    attachment_path = os.path.join(state['data_folder'], state['attachment'])
    pdf_text = read_pdf(attachment_path)
    
    return {
        **state,
        'attachment': pdf_text
    }

def get_details(state: AgenticState) -> AgenticState:
    invoice_details = invoice_model_pdf.invoke(state['attachment'])
    order_details = order_model_pdf.invoke(state['attachment'])
    
    return {
        **state,
        'invoice_number': invoice_details.invoice_number,
        'order_number': order_details.order_number
    }
    
graph = StateGraph(AgenticState)

graph.add_node("read_attachment",read_attachment)
graph.add_node("get_details",get_details)

graph.add_edge(START,"read_attachment")
graph.add_edge("read_attachment","get_details")
graph.add_edge("get_details",END)

workflow = graph.compile()
