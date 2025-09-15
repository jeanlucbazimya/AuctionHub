from .models import Watch

def watch_count(request):
    if request.user.is_authenticated:
        count = Watch.objects.filter(user=request.user, watched="yes").count()
    else:
        count = 0
    return {'watch_count': count}