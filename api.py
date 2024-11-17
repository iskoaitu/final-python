from fastapi import FastAPI, UploadFile, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from models import get_db, Comment, User
from pydantic import BaseModel
import os
from werkzeug.utils import secure_filename

app = FastAPI()

# Проверяем, что папка для загрузок существует, и создаем ее, если нужно
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
    # Временный фиксированный user_id для отладки
    user_id = 1  # Замените 1 на фактический ID пользователя в базе данных

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=400, detail="User not found")

    # Сохраняем файл, если он предоставлен
    image_path = None
    if file:
        filename = secure_filename(file.filename)
        image_path = os.path.join("static/uploads", filename)
        with open(image_path, "wb") as image_file:
            image_file.write(await file.read())

    # Создаем комментарий и сохраняем его в базе данных
    comment = Comment(content=content, user_id=user_id, recipe_id=recipe_id, image_path=image_path)
    db.add(comment)
    db.commit()

    return {"message": "Comment uploaded successfully"}
