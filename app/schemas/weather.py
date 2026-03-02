from pydantic import BaseModel, Field

class WeatherResponse(BaseModel):
   temperature: float
   windspeed: float
   time: str

class WeatherResult(BaseModel):
   city: str
   temperature_c: float
   wind_speed: float