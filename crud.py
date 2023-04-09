from sqlalchemy.orm import Session
import models
import schemas


def create_user(db: Session, user: schemas.UserIn, user_type: str):
    db_user = models.User(
        user_id=user.id,
        user_type=user_type,
        username=user.username,
        password=user.password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_student(db: Session, student: schemas.UserIn):
    db_student = models.Student(
        first_name=student.first_name,
        last_name=student.last_name,
        email=student.email,
    )
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


def create_tutor(db: Session, tutor: schemas.UserIn):
    db_tutor = models.Tutor(
        first_name=tutor.first_name,
        last_name=tutor.last_name,
        email=tutor.email,
    )
    db.add(db_tutor)
    db.commit()
    db.refresh(db_tutor)
    return db_tutor


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_user(db: Session, user_id: int, user_type: str):
    if user_type == "Student":
        return db.query(models.Student).filter(models.Student.id == user_id).first()
    elif user_type == "Tutor":
        return db.query(models.Tutor).filter(models.Tutor.id == user_id).first()

# Add more CRUD operations for other models (Lab, LabVariant, LabSolution, LabResult) as needed.
