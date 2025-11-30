from app.schemas.WithIDSchema import WithIDSchema

from pydantic import Field

#Более короткая версия информации о треке:
#название, автор ремикса, длина, обложка
class TrackSchema(WithIDSchema):

   

    class Config:
        from_attributes = True
