import uvicorn
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

from langchain_core.runnables import RunnablePassthrough

from langchain_core.output_parsers import StrOutputParser

from langchain_core.prompts import ChatPromptTemplate

from retriever.retrieval import Retriever

from utils.model_loader import ModelLoader

from prompt_library.prompt import PROMPT_TEMPLATES
import os
import json
import inspect
import time
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# region agent log
DEBUG_LOG_PATH = "/Users/rishabh013/prod_new/genai/customer_support_system/.cursor/debug-3bca29.log"
DEBUG_SESSION_ID = "3bca29"


def _debug_log(run_id: str, hypothesis_id: str, location: str, message: str, data: dict):
    payload = {
        "sessionId": DEBUG_SESSION_ID,
        "runId": run_id,
        "hypothesisId": hypothesis_id,
        "location": location,
        "message": message,
        "data": data,
        "timestamp": int(time.time() * 1000),
    }
    with open(DEBUG_LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(payload) + "\n")
# endregion


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

templates = Jinja2Templates(directory="templates")
# Allow CORS (optional for frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv()

retriever_obj = Retriever()

model_loader = ModelLoader()

def invoke_chain(query:str):
    
    retriever=retriever_obj.load_retriever()
    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATES["product_bot"])
    llm= model_loader.load_llm()
    
    chain=(
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    
    )
    
    output=chain.invoke(query)
    
    return output

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """
    Render the chat interface.
    """
    # region agent log
    _debug_log(
        run_id="pre-fix",
        hypothesis_id="H1",
        location="main.py:index:entry",
        message="Index handler invoked",
        data={"path": str(request.url.path), "method": request.method},
    )
    _debug_log(
        run_id="pre-fix",
        hypothesis_id="H2",
        location="main.py:index:template_response_signature",
        message="Observed Jinja2Templates.TemplateResponse signature",
        data={"signature": str(inspect.signature(templates.TemplateResponse))},
    )
    # endregion
    try:
        response = templates.TemplateResponse(request, "chat.html", {"request": request})
        # region agent log
        _debug_log(
            run_id="post-fix",
            hypothesis_id="H4",
            location="main.py:index:template_success",
            message="Template render succeeded",
            data={"status_code": response.status_code},
        )
        # endregion
        return response
    except Exception as exc:
        # region agent log
        _debug_log(
            run_id="pre-fix",
            hypothesis_id="H3",
            location="main.py:index:template_exception",
            message="Template render failed",
            data={"error_type": type(exc).__name__, "error": str(exc)},
        )
        # endregion
        raise

@app.post("/get",response_class=HTMLResponse)
async def chat(msg:str=Form(...)):
    result=invoke_chain(msg)
    print(f"Response: {result}")
    return result