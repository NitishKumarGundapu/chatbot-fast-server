from fastapi import *
from test import get_res
from states import get_address
from pydantic import BaseModel
from googletrans import Translator
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


@app.get("/translater")
async def translater(msg,lang):
    result = translator.translate(msg,dest=lang)
    return str(result.text)


@app.get("/translation")
async def translation(msg,lang):
    res = []
    messages = msg.split(",")
    for a in messages:
        res.append(translator.translate(a,dest=lang).text)
    return res

@app.get("/address")
async def getAddress(pincode,lang):
    res = []
    result1 = translator.translate("The Nearest Store is : ",dest=lang).text
    messages = get_address(int(pincode))
    for a in messages:
        res.append(translator.translate(a,dest=lang).text)
    return result1 + res[0]

@app.get("/get_response")
async def getResponse(msg,lang):
    index = -5
    if "help" in msg:
        index=2
    elif "hi" in msg or "hello" in msg:
        index=1
    elif "bye" in msg:
        index=3
    else:
        index=4

    if index == 4:
        res = translator.translate("please enter the correct input",dest=lang).text
    else:
        r = get_res(index)
        res = translator.translate(r,dest=lang).text
    return res