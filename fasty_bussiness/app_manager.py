from fastapi import Depends
from .models import Models
def create_app( models: Models = Depends(Models(),use_cache= True)):
    pass