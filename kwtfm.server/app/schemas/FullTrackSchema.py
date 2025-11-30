from app.schemas.WithIDSchema import WithIDSchema

from pydantic import Field

#Полная версия информации о треке
#название, автор ремикса, длина, обложка, все теги
class FullTrackSchema(WithIDSchema):

   

    class Config:
        from_attributes = True
