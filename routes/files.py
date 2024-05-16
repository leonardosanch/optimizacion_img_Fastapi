import os
from fastapi import APIRouter, UploadFile, File, BackgroundTasks
from os import getcwd
from fastapi.responses import JSONResponse
from PIL import Image



routes_files = APIRouter()

PATH_FILES = getcwd() + "/files/"

def resize_image(filename:str):
    sizes = [{
        "width": 1280,
        "height": 720
    }, {
        "width": 640,
        "height": 480,
    }]
    for size  in sizes:
       size_defined = size["width"], size["height"]
       image =Image.open(PATH_FILES + filename, mode="r")
       image.thumbnail(size_defined)
       image.save(PATH_FILES + str(size["height"]) + "_" + filename)
    print("success")
    

@routes_files.post("/upload/file")
async def upload_file(background_task: BackgroundTasks,file:UploadFile=File(...)):
    
    #SAVE FILE ORIGINAL
    with open(os.path.join(PATH_FILES, file.filename), "wb") as myfile:
        content = await file.read()
        myfile.write(content)
        myfile.close()
    
    background_task.add_task(resize_image, filename=file.filename)
    return JSONResponse(content={"message": "success"})
    