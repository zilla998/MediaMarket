from products.models import Favorite


def favorite_count(request):
    count = 0
    if request.user.is_authenticated:
        count = Favorite.objects.filter(user=request.user).count()
    return {'favorite_count': count}
