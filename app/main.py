from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas, models
from app.database import engine, get_db
from app.config import settings

# Создаём таблицы
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="FSTR Pereval API", version="1.0.0")


@app.post("/submitData/", response_model=schemas.SubmitDataResponse)
def submit_data(pereval_data: schemas.PerevalCreateSchema, db: Session = Depends(get_db)):
    """
    Добавление нового перевала в базу данных
    """
    try:
        # Проверяем, существует ли уже перевал с такими же данными
        # (можно добавить более сложную логику)

        pereval = crud.create_pereval(db, pereval_data)

        return {
            "status": 200,
            "message": "Успех. Перевал добавлен",
            "id": pereval.id
        }
    except Exception as e:
        return {
            "status": 500,
            "message": f"Ошибка при добавлении: {str(e)}",
            "id": None
        }


@app.get("/submitData/{pereval_id}", response_model=schemas.PerevalResponseSchema)
def get_pereval(pereval_id: int, db: Session = Depends(get_db)):
    """
    Получение информации о перевале по ID
    """
    pereval = crud.get_pereval_by_id(db, pereval_id)
    if not pereval:
        raise HTTPException(status_code=404, detail="Перевал не найден")

    return schemas.PerevalResponseSchema(
        id=pereval.id,
        beauty_title=pereval.beauty_title,
        title=pereval.title,
        other_titles=pereval.other_titles,
        connect=pereval.connect,
        add_time=pereval.add_time,
        status=pereval.status,
        user=schemas.UserSchema(
            email=pereval.user.email,
            phone=pereval.user.phone,
            full_name=pereval.user.full_name
        ),
        coords=schemas.CoordsSchema(
            latitude=pereval.coords.latitude,
            longitude=pereval.coords.longitude,
            height=pereval.coords.height
        ),
        level=schemas.LevelSchema(
            winter=pereval.level.winter,
            summer=pereval.level.summer,
            autumn=pereval.level.autumn,
            spring=pereval.level.spring
        ),
        images=[schemas.ImageSchema(data=img.data, title=img.title) for img in pereval.images]
    )


@app.patch("/submitData/{pereval_id}/status")
def update_status(pereval_id: int, status: str, db: Session = Depends(get_db)):
    """
    Обновление статуса модерации перевала
    """
    pereval = crud.get_pereval_by_id(db, pereval_id)
    if not pereval:
        raise HTTPException(status_code=404, detail="Перевал не найден")

    if status not in ["new", "pending", "accepted", "rejected"]:
        raise HTTPException(status_code=400, detail="Недопустимый статус")

    pereval.status = status
    db.commit()

    return {"status": "ok", "message": "Статус обновлён"}


@app.get("/")
def root():
    return {
        "message": "FSTR Pereval API",
        "endpoints": {
            "POST /submitData/": "Добавить новый перевал",
            "GET /submitData/{id}": "Получить информацию о перевале",
            "PATCH /submitData/{id}/status": "Обновить статус модерации"
        }
    }