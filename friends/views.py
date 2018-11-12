from friends.models import FriendRequest
from users.models import SiteUser
from django.shortcuts import redirect
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods


def send_friend_request(request, id):
    to_user = SiteUser.objects.get(id=id)
    frequest, created = FriendRequest.objects.get_or_create(from_user=request.user, to_user=to_user)
    return redirect('profile')


def cancel_friend_request(request, id):
    to_user = SiteUser.objects.get(id=id)
    frequest = FriendRequest.objects.filter(from_user=request.user,to_user=to_user).first()
    frequest.delete()
    return redirect('profile')


def accept_friend_request(request, id):
    from_user = SiteUser.objects.get(id=id)
    frequest = FriendRequest.objects.filter(from_user=from_user, to_user=request.user).first()
    u1 = frequest.to_user
    u2 = from_user
    u1.friends.add(u2)
    u2.friends.add(u1)
    frequest.delete()
    return redirect('profile')


def delete_friend_request(request, id):
    from_user = SiteUser.objects.get(id=id)
    frequest = FriendRequest.objects.filter(from_user=from_user, to_user=request.user).first()
    frequest.delete()
    return redirect('profile')


@login_required
@require_http_methods(["GET"])
def search_friend(request):
    query = request.GET.get('query')
    if len(query) < 3:
        return HttpResponseBadRequest('Search query too short')
    search_friends = request.user.friends.filter(first_name__startswith=query)[:10]
    response = []
    for friend in search_friends:
        response.append({
            'name': friend.name(),
            'profile_picture': friend.profile_picture.url,
            'id': friend.id
        })
    return JsonResponse({'data': response})

