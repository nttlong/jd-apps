from api_models import ModelApps
class Models:
    def __init__(self):
        self.apps = ModelApps.sys_applications()
    def __call__(self, *args, **kwargs):
        return self