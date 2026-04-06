from sqlalchemy.orm import Session
from sqlalchemy import and_
from app import models, schemas


def create_user(db: Session, user: schemas.UserSchema):
    db_user = models.User(
        email=user.email,
        phone=user.phone,
        full_name=user.full_name
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def create_coords(db: Session, coords: schemas.CoordsSchema):
    db_coords = models.Coords(
        latitude=coords.latitude,
        longitude=coords.longitude,
        height=coords.height
    )
    db.add(db_coords)
    db.commit()
    db.refresh(db_coords)
    return db_coords


def update_coords(db: Session, coords_id: int, coords: schemas.CoordsSchema):
    db_coords = db.query(models.Coords).filter(models.Coords.id == coords_id).first()
    if db_coords:
        db_coords.latitude = coords.latitude
        db_coords.longitude = coords.longitude
        db_coords.height = coords.height
        db.commit()
        db.refresh(db_coords)
    return db_coords


def create_level(db: Session, level: schemas.LevelSchema):
    db_level = models.Level(
        winter=level.winter,
        summer=level.summer,
        autumn=level.autumn,
        spring=level.spring
    )
    db.add(db_level)
    db.commit()
    db.refresh(db_level)
    return db_level


def update_level(db: Session, level_id: int, level: schemas.LevelSchema):
    db_level = db.query(models.Level).filter(models.Level.id == level_id).first()
    if db_level:
        db_level.winter = level.winter
        db_level.summer = level.summer
        db_level.autumn = level.autumn
        db_level.spring = level.spring
        db.commit()
        db.refresh(db_level)
    return db_level


def create_images(db: Session, images: list[schemas.ImageSchema], pereval_id: int):
    db_images = []
    for img in images:
        db_img = models.Image(
            data=img.data,
            title=img.title,
            pereval_id=pereval_id
        )
        db.add(db_img)
        db_images.append(db_img)
    db.commit()
    return db_images


def delete_images(db: Session, pereval_id: int):
    db.query(models.Image).filter(models.Image.pereval_id == pereval_id).delete()
    db.commit()


def create_pereval(db: Session, pereval: schemas.PerevalCreateSchema):
    # Проверяем, есть ли пользователь с таким email
    user = get_user_by_email(db, pereval.user.email)
    if not user:
        user = create_user(db, pereval.user)

    # Создаём координаты
    coords = create_coords(db, pereval.coords)

    # Создаём уровень сложности
    level = create_level(db, pereval.level)

    # Создаём перевал
    db_pereval = models.Pereval(
        beauty_title=pereval.beauty_title,
        title=pereval.title,
        other_titles=pereval.other_titles,
        connect=pereval.connect,
        user_id=user.id,
        coords_id=coords.id,
        level_id=level.id,
        status=models.StatusEnum.new
    )
    db.add(db_pereval)
    db.commit()
    db.refresh(db_pereval)

    # Создаём изображения
    if pereval.images:
        create_images(db, pereval.images, db_pereval.id)

    return db_pereval


def get_pereval_by_id(db: Session, pereval_id: int):
    return db.query(models.Pereval).filter(models.Pereval.id == pereval_id).first()


def get_perevals_by_user_email(db: Session, email: str):
    return db.query(models.Pereval).join(models.User).filter(models.User.email == email).all()


def update_pereval(db: Session, pereval_id: int, pereval_data: schemas.PerevalUpdateSchema):
    db_pereval = db.query(models.Pereval).filter(models.Pereval.id == pereval_id).first()
    if not db_pereval:
        return None, "Перевал не найден"

    # Проверяем статус: редактировать можно только new
    if db_pereval.status != models.StatusEnum.new:
        return None, f"Редактирование недоступно. Текущий статус: {db_pereval.status.value}"

    # Обновляем поля перевала (кроме user_id)
    if pereval_data.beauty_title is not None:
        db_pereval.beauty_title = pereval_data.beauty_title
    if pereval_data.title is not None:
        db_pereval.title = pereval_data.title
    if pereval_data.other_titles is not None:
        db_pereval.other_titles = pereval_data.other_titles
    if pereval_data.connect is not None:
        db_pereval.connect = pereval_data.connect

    # Обновляем координаты
    if pereval_data.coords:
        update_coords(db, db_pereval.coords_id, pereval_data.coords)

    # Обновляем уровень сложности
    if pereval_data.level:
        update_level(db, db_pereval.level_id, pereval_data.level)

    # Обновляем изображения (удаляем старые и создаём новые)
    if pereval_data.images is not None:
        delete_images(db, pereval_id)
        create_images(db, pereval_data.images, pereval_id)

    db.commit()
    db.refresh(db_pereval)
    return db_pereval, "Успешно обновлено"