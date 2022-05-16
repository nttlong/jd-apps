from django.http import HttpResponse
import ReCompact.web
@ReCompact.web.template("index.html")
def index(request):
    return request.template.model({"request":request}).render()
