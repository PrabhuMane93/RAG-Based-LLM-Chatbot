#!/bin/bash

cd usr/src/app

pip install -r requirements.txt

cd chatbot/

echo -e 'credentials="[(\"prabhu\", \"password1\"), (\"atharva\", \"password2\")]"\nchatbot-hash ="a1fcda9b274166e239d2f48e15809f317496f023f2e5c4a5366a51aeed156638"' > .env

python modeldownload.py

uvicorn main:app --host 0.0.0.0 --port 80 --reload