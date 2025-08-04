import os
import shutil

def upload_txt(file):
    file_path = os.path.join("assets","whitepaper",file.filename)
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)