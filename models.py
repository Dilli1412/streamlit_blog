from dataclasses import dataclass
from datetime import datetime

@dataclass
class User:
    id: int
    username: str
    email: str
    role: str

@dataclass
class Post:
    id: int
    title: str
    content: str
    author_id: int
    publish_date: datetime
    category: str
    tags: list
    featured_image: str

@dataclass
class Comment:
    id: int
    post_id: int
    user_id: int
    content: str
    comment_date: datetime