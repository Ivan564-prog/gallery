from django.middleware.csrf import get_token
from apps.config.models import RootSettings
from django.http import HttpResponse, FileResponse
import os 


def admin_script(request, filename):
    filepath = f'/app/admin_scripts/{filename}'
    if request.user.is_superuser and os.path.exists(filepath):
        return FileResponse(open(filepath, 'rb'), content_type='application/javascript')
    
def admin_style(request, filename):
    filepath = f'/app/admin_styles/{filename}'
    if request.user.is_superuser:
        return FileResponse(open(filepath, 'rb'), content_type='text/css')

def csrf_gen(request):
    csrf_token = get_token(request)
    return HttpResponse(csrf_token)

def robots(request):
    robots = RootSettings.get_settings().robots
    if not robots:
        robots = 'User-agent: *\nDisallow: /'
    return HttpResponse(robots, content_type="text/plain")