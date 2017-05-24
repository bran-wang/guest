from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from sign.models import Event, Guest
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.

def index(request):
#    return HttpResponse("Hello Django!")
    return render(request, "index.html")

def login_action(request):
    if request.method == "POST":
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            request.session['user'] = username
            response =  HttpResponseRedirect('/event_manage/')
            return response
        else:
            return render(request, 'index.html', {'error': 'username or password error!'})

@login_required
def event_manage(request):
    event_list = Event.objects.all()
    username = request.session.get('user', '')
    return render(request, "event_manage.html", {"user":username, "events":event_list})

@login_required
def search_name(request):
    username = request.session.get('user', '')
    search_name = request.GET.get('name', '')
    event_list = Event.objects.filter(name__contains=search_name)
    return render(request, "event_manage.html", {"user":username, "events":event_list})

@login_required
def search_phone(request):
    username = request.session.get('user', '')
    phone = request.GET.get('phone', '')
    guest_list = Guest.objects.filter(phone__contains=phone)
    return render(request, "guest_manage.html", {"user":username, "guests":guest_list})

@login_required
def guest_manage(request):
    username = request.session.get('user', '')
    guest_list = Guest.objects.all()
    paginator = Paginator(guest_list, 5)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    return render(request, "guest_manage.html", {"user":username, "guests":contacts})


@login_required
def sign_index(request, eid):
    event = get_object_or_404(Event, id=eid)
    guest_count = Guest.objects.filter(event_id=eid).count()
    sign_count = Guest.objects.filter(event_id=eid, sign=1).count()
    return render(request, 'sign_index.html', {'event':event, 'guest':guest_count, 'sign':sign_count})

@login_required
def sign_index_action(request, eid):
    event = get_object_or_404(Event, id=eid)
    phone = request.POST.get('phone', '')
    print phone
    result = Guest.objects.filter(phone=phone)
    sign_count = Guest.objects.filter(event_id=eid, sign=1).count()
    guest_count = Guest.objects.filter(event_id=eid).count()
    if not result:
        return render(request, 'sign_index.html', {'event':event, 'hint':'phone error.', 'guest':guest_count, 'sign':sign_count})

    result = Guest.objects.filter(phone=phone, event_id=eid)
    if not result:
        return render(request, 'sign_index.html', {'event':event, 'hint':'event id or phone error.', 'guest':guest_count,  'sign':sign_count})

    result = Guest.objects.get(phone=phone, event_id=eid)
    if result.sign:
        return render(request, 'sign_index.html', {'event':event, 'hint':'user has sign in.', 'guest':guest_count, 'sign':sign_count})
    else:
        return render(request, 'sign_index.html', {'event':event, 'hint':'sign in success', 'guest':guest_count, 'sign':sign_count})
