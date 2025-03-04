from pydantic import BaseModel


class UrlCreate(BaseModel):
    full_url: str

    class Config:
        orm_mode = True
