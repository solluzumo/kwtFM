from app.schemas.WithIDSchema import WithIDSchema

from pydantic import Field

#Полная версия информации о треке
#название, основной автор, дополнительные авторы ремикса, длина, обложка, все теги
class FullTrackSchema(WithIDSchema):

   

    class Config:
        from_attributes = True
