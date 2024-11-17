from fastapi import FastAPI, UploadFile, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from models import get_db, Comment, User
from pydantic import BaseModel
import os
from werkzeug.utils import secure_filename

app = FastAPI()

UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

class CommentModel(BaseModel):
    content: str
    user_id: int
    recipe_id: int


@app.post("/upload_comment/")
async def upload_comment(content: str = Form(...), recipe_id: int = Form(...),
                         user_id: int = Form(...), file: UploadFile = None,
                         db: Session = Depends(get_db)):

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=400, detail="User not found")

    image_path = None
    if file and file.filename:
        filename = secure_filename(file.filename)
        image_path = os.path.join("static/uploads", filename)
        with open(image_path, "wb") as image_file:
            image_file.write(await file.read())

    comment = Comment(content=content, user_id=user_id, recipe_id=recipe_id, image_path=image_path)
    db.add(comment)
    db.commit()

    return {"message": "Comment uploaded successfully"}
