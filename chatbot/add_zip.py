import os
import shutil
from zipfile import ZipFile

def upload_zip(file):
    file_path = os.path.join("assets",file.filename)
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    shutil.rmtree(os.path.join("assets","whitepaper"))
    with ZipFile(file_path) as zipObject:
        zipObject.extractall(path=os.path.join("assets","whitepaper"))
    os.remove(file_path)