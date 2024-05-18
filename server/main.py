# RUN docker-compose build && docker-compose up
# http://localhost/docs (or reconfigure the compose if you need to!)

from typing import List
import uuid

from fastapi import FastAPI, HTTPException, Request
from slowapi.errors import RateLimitExceeded
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from sqlalchemy.orm import sessionmaker

from server.db.init.setup import db_init
from server.db.models.test_model import TestData, TestModel

# rate limiting w slow-api: https://stackoverflow.com/questions/65491184/ratelimit-in-fastapi
limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

engine = db_init()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@app.get("/")
async def read_root():
    return {"message": "Ready."}


@app.post("/test")
async def test_endpoint(name: str):
    db_session = SessionLocal()

    try:
        # unpack the payload, create and add UID
        uid = str(uuid.uuid4())
        test_data = TestData(uid=uid, name=name)

        db_data = TestModel(**test_data.dict())

        db_session.add(db_data)
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        print(e)
        raise HTTPException(status_code=500, detail=str(e)) from e
    finally:
        db_session.close()

    return {"message": "Success.", "uid": uid, "data": test_data}


@app.get("/getnames", response_model=List[TestData])
@limiter.limit("10/minute")  # slowapi limiter example
async def get_names(
    request: Request
):  # NOTE SlowAPI requires the request param, even if unused otherwise.
    db_session = SessionLocal()
    all_data = db_session.query(TestModel).all()

    if not all_data:
        raise HTTPException(status_code=404, detail="No data.")

    return [{"uid": d.uid, "name": d.name} for d in all_data]
