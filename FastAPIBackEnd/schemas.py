from pydantic import BaseModel

class ArticleBase(BaseModel):
    title: str
    url_path: str
    
class ArticleCreate(ArticleBase):
    pass

class Article(ArticleBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True


class ItemBase(BaseModel):
    title: str
    description: str | None = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    items: list[Item] = []
    articles: list[Article] = []

    class Config:
        from_attributes = True
