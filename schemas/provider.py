from pydantic import BaseModel

class ProviderResponse(BaseModel):
    id: int
    name: str
    contact_email: str | None = None
    contact_phone: str | None = None
    is_active: bool

    class Config:
        orm_mode = True
