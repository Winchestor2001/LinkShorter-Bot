from typing import List

from pydantic import BaseModel, AnyHttpUrl


class URLRequest(BaseModel):
    url: AnyHttpUrl | None = None
    keywords: List[str] | None = None
    new_key: str | None = None
