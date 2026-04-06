from sqlalchemy.orm import Session
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