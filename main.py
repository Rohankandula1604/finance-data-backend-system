from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import engine, Base, SessionLocal
import models
import schemas

app = FastAPI()

Base.metadata.create_all(bind=engine)


# ---------------- DATABASE ----------------

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------- ROLE CHECK ----------------

def check_role(user_id: int, allowed_roles: list, db: Session):
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.role not in allowed_roles:
        raise HTTPException(status_code=403, detail="Access Denied")

    return user


# ---------------- HOME ----------------

@app.get("/")
def home():
    return {"message": "Finance Backend API is running"}


# ---------------- USERS ----------------

@app.post("/users", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")

    new_user = models.User(
        name=user.name,
        email=user.email,
        role=user.role,
        is_active=True
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get("/users", response_model=list[schemas.UserResponse])
def get_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()


# ---------------- RECORDS ----------------

@app.post("/records", response_model=schemas.RecordResponse)
def create_record(record: schemas.RecordCreate, db: Session = Depends(get_db)):
    
    # ONLY ADMIN CAN CREATE
    check_role(record.created_by, ["admin"], db)

    new_record = models.Record(
        amount=record.amount,
        type=record.type,
        category=record.category,
        date=record.date,
        notes=record.notes,
        created_by=record.created_by
    )
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    return new_record


@app.get("/records", response_model=list[schemas.RecordResponse])
def get_records(
    user_id: int,
    type: str | None = Query(None),
    category: str | None = Query(None),
    db: Session = Depends(get_db)
):
    # ALL ROLES CAN VIEW
    check_role(user_id, ["viewer", "analyst", "admin"], db)

    query = db.query(models.Record)

    if type:
        query = query.filter(models.Record.type == type)

    if category:
        query = query.filter(models.Record.category == category)

    return query.all()


@app.put("/records/{record_id}", response_model=schemas.RecordResponse)
def update_record(record_id: int, record: schemas.RecordCreate, db: Session = Depends(get_db)):

    # ONLY ADMIN CAN UPDATE
    check_role(record.created_by, ["admin"], db)

    existing_record = db.query(models.Record).filter(models.Record.id == record_id).first()
    if not existing_record:
        raise HTTPException(status_code=404, detail="Record not found")

    existing_record.amount = record.amount
    existing_record.type = record.type
    existing_record.category = record.category
    existing_record.date = record.date
    existing_record.notes = record.notes
    existing_record.created_by = record.created_by

    db.commit()
    db.refresh(existing_record)
    return existing_record


@app.delete("/records/{record_id}")
def delete_record(record_id: int, user_id: int, db: Session = Depends(get_db)):

    # ONLY ADMIN CAN DELETE
    check_role(user_id, ["admin"], db)

    existing_record = db.query(models.Record).filter(models.Record.id == record_id).first()
    if not existing_record:
        raise HTTPException(status_code=404, detail="Record not found")

    db.delete(existing_record)
    db.commit()
    return {"message": "Record deleted successfully"}


# ---------------- DASHBOARD ----------------

@app.get("/dashboard/summary")
def dashboard_summary(user_id: int, db: Session = Depends(get_db)):

    # ANALYST + ADMIN ONLY
    check_role(user_id, ["analyst", "admin"], db)

    total_income = db.query(func.sum(models.Record.amount)).filter(models.Record.type == "income").scalar() or 0
    total_expense = db.query(func.sum(models.Record.amount)).filter(models.Record.type == "expense").scalar() or 0
    net_balance = total_income - total_expense

    category_data = (
        db.query(models.Record.category, func.sum(models.Record.amount))
        .group_by(models.Record.category)
        .all()
    )

    category_totals = {category: total for category, total in category_data}

    recent_records = db.query(models.Record).order_by(models.Record.id.desc()).limit(5).all()

    return {
        "total_income": total_income,
        "total_expense": total_expense,
        "net_balance": net_balance,
        "category_totals": category_totals,
        "recent_activity": recent_records
    }