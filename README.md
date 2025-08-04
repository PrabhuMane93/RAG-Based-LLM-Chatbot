<div align="center">
  <img src="banner.png" alt="Logo" width="100%">
  
  [![Dev Container](https://img.shields.io/badge/Dev%20Container-Ready-green.svg)](.devcontainer)
  [![Python 3.10](https://img.shields.io/badge/Python-3.10-blue.svg)](https://www.python.org/)
  [![PyTorch](https://img.shields.io/badge/PyTorch-2.7.1-orange.svg)](https://pytorch.org/)
</div>

# 🧠 AI Chatbot with File Ingestion and Semantic Search

This project is a hybrid architecture that combines semantic retrieval with large language model (LLM) generation. Uploaded .txt or .zip files are parsed, and their contents are broken into text segments. Each segment is embedded using a transformer-based sentence encoder (multi-qa-mpnet-base-dot-v1), generating vector representations that are stored for efficient similarity search. When a user submits a query, it is first corrected for typos using a sequence-to-sequence spelling correction model. The corrected query is then embedded in the same vector space, and cosine similarity is used to identify the most semantically relevant document segments. These top-matching segments are passed, along with the original user query, to a generative LLM (flan-t5-large), which synthesizes a final response. This architecture ensures accurate information retrieval from user-uploaded content while leveraging the fluency and reasoning capabilities of LLMs, making it ideal for use cases like document-based chatbots, knowledge assistants, and smart search interfaces.

### How do I get set up? ###

* Setup Environment
```
curent working directory : RAG-Based-LLM-Chatbot
python3 -m venv venv
source venv/bin/activate
```

* Dependencies Set Up
> All the dependencies are in requirements.txt

* Install dependencies
```
cwd RAG-Based-LLM-Chatbot
pip install -r requirements.txt
```

* Load user credentials and chatbot hash as an environment variable
```
cd chatbot
echo -e 'credentials="[(\"user1\", \"password1\"), (\"user2\", \"password2\")]"\nchatbot-hash ="<ENTER-HASH-HERE>"' > .env
```

* Default value of Chatbot Secret is **stkchatbot#11**, Hash for which is **a1fcda9b274166e239d2f48e15809f317496f023f2e5c4a5366a51aeed156638**
* Deployment Instructions
> In the chatbot directory, start the fastapi server
```
current working directory: chatbot
python3 modeldownload.py
uvicorn main:app --host 0.0.0.0 --port 80 --reload
```
> Endpoint for question : 
```
http://0.0.0.0/ask?question=<YOUR QUESTION TO CHATBOT>?chatbot_secret=<CHATBOT SECRET>
```
* Docker Deployment
> In the parent directory of the project, run this command: 
```
docker build -t chatai-image . 
```
> Push the image to docker
```
docker login
docker tag chatai-image <YOUR USERNAME>/chatai-image
docker push <YOUR USERNAME>/chatai-image
```
> After building the image, to get a container up and running run the below command: 
```
docker run\
-e credentials="[(\"user1\", \"password1\"), (\"user2\", \"password2\")]" \
-e chatbot-hash ="<HASH OF CHATBOT SECRET>" \
-d -v <PATH TO TXT FILE DIRECTORY>:/usr/src/app/chatbot/assets/whitepaper \
-p 8000:8000 \
--name chatai-container <YOUR USERNAME>/chatai-image
```

### Who do I talk to? ###

* Prabhu Mane **(dr.prabhumane@gmail.com)**
