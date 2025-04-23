from pydantic import BaseModel

class ProductFeatures(BaseModel):
    Battery_Life: float = 6.0
    Display_Size: float = 1.2
    Price: float = 850
    Weight: float = 1.7
    Screen_Resolution: float = 2.2
    RAM: float = 8.0
    Processor_Speed: float = 13.0
    Storage: float = 256.0
    