import torch
import os
import ast
import pickle
import hashlib

from cosinetest import find_match6
from typo import fixtypo
from add import operate
from auth import AuthHandler
from schemas import AuthDetails
from add_zip import upload_zip
from add_txt import upload_txt

from transformers import AutoTokenizer, AutoModel,AutoModelForSeq2SeqLM
from fastapi import FastAPI, Depends, HTTPException, File, UploadFile
from dotenv import load_dotenv

similaritytokenizer = AutoTokenizer.from_pretrained("tokenizers/multi-qa-mpnet-base-dot-v1")
similaritymodel = AutoModel.from_pretrained("models/multi-qa-mpnet-base-dot-v1")


tokenizer = AutoTokenizer.from_pretrained("tokenizers/flan_t5_large")
model = AutoModelForSeq2SeqLM.from_pretrained("models/flan_t5_large", pad_token_id = tokenizer.eos_token_id)

typotokenizer =  AutoTokenizer.from_pretrained("tokenizers/spelling-correction-english-base")
typomodel = AutoModelForSeq2SeqLM.from_pretrained("models/spelling-correction-english-base")

app = FastAPI()
touch_dataset = operate()
auth_handler =AuthHandler()
load_dotenv()
my_tuple_str = os.getenv('credentials')
my_list = ast.literal_eval(my_tuple_str)
users = []

for username, password in my_list:
    a = (username, password)
    AuthDetails(username = username, password = password)
    users.append({
    'username': username,
    'password':auth_handler.get_password_hash(password)})


@app.post('/login')
def login(auth_details: AuthDetails):
    user = None
    for x in users:
        if x["username"] == auth_details.username:
            user = x
            break

    if (user is None) or (not auth_handler.verify_password(auth_details.password, user["password"])):
        raise HTTPException(status_code = 481, detail = 'Invalid username and/or password')
    
    token = auth_handler.encode_token(user['username']) 
    return {"token": token}


@app.post("/upload-zip-file")
async def upload_zip_file(file: UploadFile = File(...), username = Depends(auth_handler.auth_wrapper)):
    if file.filename[-4:]!=".zip":
        return {'response' : "The uploaded file is not zip file" }
    else:
        upload_zip(file)
        return {'response' : f"{file.filename} is uploaded"}

@app.post("/upload-txt-file")
async def upload_txt_file(file: UploadFile = File(...), username = Depends(auth_handler.auth_wrapper)):
    if file.filename[-4:]!=".txt":
        return {'response' : "The uploaded file is not txt file" }
    else:
        upload_txt(file)
        return {'response' : f"{file.filename} is uploaded"}

@app.get('/user_ask')
async def chat_user(question : str, username = Depends(auth_handler.auth_wrapper)):
    question = fixtypo(typomodel, typotokenizer, question)
    temptext = find_match6(similaritymodel, similaritytokenizer, question)
    input_ids = tokenizer(temptext, return_tensors="pt").input_ids
    outputs = model.generate(input_ids, max_length = 400)
    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return {'response' : answer}

@app.post('/ask')
async def chat(question : str, chatbot_secret : str): 
    input_password = hashlib.sha256(chatbot_secret.encode())
    env_password = os.getenv('chatbot-hash')
    if input_password.hexdigest() == env_password:
        question = fixtypo(typomodel, typotokenizer, question)
        temptext = find_match6(similaritymodel, similaritytokenizer, question)
        input_ids = tokenizer(temptext, return_tensors="pt").input_ids
        outputs = model.generate(input_ids, max_length = 1000)
        answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return {'response' : answer}
    else:
        return {'response' : 'Inputted password is incorrect.'}

@app.get('/get_titles')
async def display_titles(username = Depends(auth_handler.auth_wrapper)):
    return {'titles' : touch_dataset.get_titles()}

@app.get('/get_all_segments')
async def display_segments(username = Depends(auth_handler.auth_wrapper)):
    return {'segments' : touch_dataset.get_segments()}

@app.get('/add_segments')
async def create_segments(title : str, content : str, username = Depends(auth_handler.auth_wrapper)):
    create = touch_dataset.add_segments(title,content)
    if create=="added":
        return f"{title} is added."
    else:
        return create

@app.get('/delete_segments')
async def delete_segments(title : str, username = Depends(auth_handler.auth_wrapper)):
    delete = touch_dataset.delete_segment(title)
    if delete=="deleted":
        return f"{title} is deleted."
    else:
        return f"No title present {title}"