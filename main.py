from fastapi import *
from test import get_res
from states import get_address
from googletrans import Translator
from fastapi.responses import PlainTextResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

translator = Translator()
app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    msg:str
    lang:str

class Address(BaseModel):
    pincode : str
    lang : str

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=400)

@app.get("/translater")
async def translater(message:Message):
    print(message)
    result = translator.translate(message.msg,dest=message.lang)
    return str(result.text)


@app.get("/translation")
async def translation(message:Message):
    res = []
    print(message)
    messages = message.msg.split(",")
    for a in messages:
        res.append(translator.translate(a,dest=message.lang).text)
    return res

@app.get("/address")
async def getAddress(address : Address):
    res = []
    result1 = translator.translate("The Nearest Store is : ",dest=address.lang).text
    messages = get_address(int(address.pincode))
    for a in messages:
        res.append(translator.translate(a,dest=address.lang).text)
    return result1 + res[0]

@app.get("/get_response")
async def getResponse(message:Message):
    print(message)
    index = -5
    msg1 = message.msg
    if "help" in msg1:
        index=2
    elif "hi" in msg1 or "hello" in msg1:
        index=1
    elif "bye" in msg1:
        index=3
    else:
        index=4

    if index == 4:
        res = translator.translate("please enter the correct input",dest=message.lang).text
    else:
        r = get_res(index)
        res = translator.translate(r,dest=message.lang).text
    return res

@app.get("/")
async def root():
    return {"message": "this is chatbot-response-server"}