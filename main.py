from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from random import choices
from sqlalchemy.orm import Session

from constants import CHARACTERS, URL_LENGTH
from database import Base, engine, session
from models import Url
from schemas import UrlCreate


app = FastAPI()


Base.metadata.create_all(bind=engine)


def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()


@app.post('/')
async def create_short(url: UrlCreate, db: Session = Depends(get_db)) -> dict:
    db_url = db.query(Url).filter(Url.full_url == url.full_url).first()
    if db_url is None:
        links = db.query(Url).all()
        while True:
            short_link = ''.join(choices(CHARACTERS, k=URL_LENGTH))
            if Url(short_url=short_link) not in links:
                break
        db_url = Url(full_url=url.full_url, short_url=short_link)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return {'data': db_url.short_url}

@app.get('/{short_url}')
async def get_full_url(short_url: str, db: Session = Depends(get_db)):
    db_url = db.query(Url).filter(Url.short_url == short_url).first()
    if db_url is None:
        raise HTTPException(status_code=404, detail='Link not found')
    full_url = str(db_url.full_url)
    return RedirectResponse(url=full_url, status_code=307)
