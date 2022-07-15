import repositories.files
from .base import BaseService
from kink import inject
class FilesService:
    @inject(files_repository=repositories.files.FilesRepository)
    def __init__(self,files_repository:repositories.files.FilesRepository):
        self.files_repository:repositories.files.FilesRepository=files_repository

    def __call__(self, *args, **kwargs):
        pass