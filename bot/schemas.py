from pydantic import BaseModel, AnyHttpUrl


class URLRequest(BaseModel):
    url: AnyHttpUrl
