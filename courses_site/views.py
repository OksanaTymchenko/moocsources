from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from rest_framework.generics import ListCreateAPIView

from serializers import *
from rest_framework import viewsets, generics

import random
from .recommend import *

from .models import *


def index(request):
    return HttpResponse(render(request, 'index.html'))

def user_account(request):
    usr = User.objects.get(id=request.user.id)
    total_likes = Like.objects.filter(user=usr).count()
    total_favorites = Favorite.objects.filter(user=usr).count()
    return HttpResponse(render(request, 'user_account.html', context={'user': usr, 'likes': total_likes, 'fav': total_favorites}))




def allcourses(request):
    sort = False

    categories = ''
    providers = ''
    sources = ''
    language = ''
    duration = ''
    if request.GET.get('c'):
        categories = request.GET.get('c')
    if request.GET.get('p'):
        providers = request.GET.get('p')
    if request.GET.get('s'):
        sources = request.GET.get('s')
    if request.GET.get('l'):
        language = request.GET.get('l')
    if request.GET.get('d'):
        duration = request.GET.get('d')
    if request.GET.get('sorted'):
        sort = True

    courses_list = Course.objects.all()
    if categories:
        courses_list = courses_list.filter(category__in=categories.split('_'))
    if providers:
        courses_list = courses_list.filter(provider__in=providers.split('_'))
    if sources:
        courses_list = courses_list.filter(source__in=sources.split('_'))
    if language:
        courses_list = courses_list.filter(language__in=language.split('_'))
    if duration:
        courses_list = courses_list.filter(duration_filter__in=duration.split('_'))



    if sort:
        print("sort")
        sorted_courses = []
        for c in courses_list:
            likes = Like.objects.filter(course__id=c.id).count()
            sorted_courses.append([c, likes])
        sorted_courses = sorted(sorted_courses, key=lambda item: -item[1])
        courses_list = [c[0] for c in sorted_courses]


    # filter_category = Course.objects.order_by('category').values_list('category', flat=True).distinct().annotate(cc=Count('category'))
    filter_category = Course.objects.exclude(category__isnull=True).order_by('category').values('category').distinct().annotate(count = Count('category'))
    f_c = {}
    for item in filter_category:
        f_c[item['category']] = item['count']
    # filter_category = {value : filter_category.get(key, None) for key, value in firstDictionary.items()}
    # for each in filter_category:
    #     print(each.category, each.count)
    filter_provider = Course.objects.exclude(provider__isnull=True).order_by('provider').values('provider').distinct().annotate(count = Count('provider'))
    f_p = {}
    for item in filter_provider:
        f_p[item['provider']] = item['count']

    filter_source = Course.objects.order_by('source').values('source').distinct().annotate(count = Count('source'))
    f_s = {}
    for item in filter_source:
        f_s[item['source']] = item['count']

    filter_lang = Course.objects.order_by('language').values('language').distinct().annotate(count = Count('language'))
    f_l = {}
    for item in filter_lang:
        f_l[item['language']] = item['count']

    filter_duration = Course.objects.exclude(duration_filter__isnull=True).order_by('duration_filter').values(
        'duration_filter').distinct().annotate(count = Count('duration_filter'))

    f_d = {}
    for item in filter_duration:
        f_d[item['duration_filter']] = item['count']

    paginator = Paginator(courses_list, 10)
    page = request.GET.get('page')
    try:
        courses = paginator.page(page)
    except PageNotAnInteger:
        courses = paginator.page(1)
    except EmptyPage:
        courses = paginator.page(paginator.num_pages)

    index = courses.number - 1
    max_index = len(paginator.page_range)
    start_index = index - 10 if index >= 10 else 0
    end_index = index + 10 if index <= max_index - 10 else max_index
    page_range = paginator.page_range[start_index:end_index]

    new_path = request.get_full_path()
    print(new_path)
    # print (new_path.find('page='))
    if new_path != '/courses/' and new_path.find('page=')!=-1:
        new_path = new_path[:new_path.find('page=')][:-1]
        # pass
    elif new_path == '/courses/':
        new_path+='?'
    print(new_path)
    context = {'courses_list': courses, 'filter_category': sorted(f_c.items()), 'filter_provider': sorted(f_p.items()),
               'filter_source': sorted(f_s.items()), 'filter_lang': sorted(f_l.items()), 'filter_duration': sorted(f_d.items()),
               'page_range': page_range, 'new_path': new_path, 'categories': categories.split('_'),
               'providers': providers.split('_'), 'sources': sources.split('_'), 'language': language.split('_'),
               'duration': duration.split('_'), 'list_len': len(courses_list)}
    return render(request, 'allcourses.html', context)


def detail(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    video = ''
    if course.video:
        video = course.video.replace("watch?v=", "embed/")
        print('video ', video)
    instructors = Instructor.objects.filter(course=course_id)
    likes = Like.objects.filter(course=course).count()
    fav = Favorite.objects.filter(course=course).count()
    return render(request, 'detail.html', {'course': course, 'instructors': instructors,'video': video, 'likes': likes, 'favorites': fav})

def signup(request):
    if request.method == 'POST':
        users = User.objects.filter(email=request.POST['email'])
        if len(users) == 0:
            user = User.objects.create_user(email=request.POST['email'], username=request.POST['login'], password=request.POST['password'])
            user.save()
            q = Questionnaire.objects.create()
            q.save()
            account = Account.objects.create(is_admin=0, user_id=user.id, questionaire_id = q.id)
            account.save()
            usr = authenticate(username=request.POST['login'], password=request.POST['password'])
            if user is not None:
                login(request, usr)
            return loadInfo(request)
        else:
            return HttpResponse(render(request, 'signup.html', context={'message': 'Таких email вже зареєстрований'}))
    else:
        if not request.user.id is None:
            return HttpResponse(render(request, 'index.html'))
        return HttpResponse(render(request, 'signup.html'))

def home(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST['login'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            return HttpResponse(render(request, 'index.html'))
        else:
            return HttpResponse(render(request, 'login.html', context={'message': 'Невдача'}))
    else:
        if not request.user.id is None:
            return HttpResponse(render(request, 'index.html'))
        return HttpResponse(render(request, 'login.html'))

def out(request):
    logout(request)
    return HttpResponse(render(request, 'login.html'))

def loadInfo(request):
    cat = Course.objects.order_by('category').values_list('category', flat=True).distinct()
    lang = Course.objects.order_by('language').values_list('language', flat=True).distinct()
    return HttpResponse(render(request,'questionnaire.html', context={'category': cat, 'language': lang}))

def saveq(request):
    q = Account.objects.filter(user_id=request.user.id)[0].questionaire
    category = request.POST.getlist('category')
    language = request.POST.getlist('language')
    duration = request.POST['duration']
    free = request.POST['free']
    rate = request.POST['rate']
    q.preferences = ";".join(category)
    q.rate = rate
    q.duration = duration
    q.is_free = len(free) > 0
    q.language = ";".join(language)
    q.save()

    return HttpResponse(render(request, "index.html"))

def like(request, course_id):
    c = get_object_or_404(Course, pk=course_id)
    if Like.objects.filter(user=User.objects.get(id=request.user.id), course=c).count() < 1:
        like = Like.objects.create(user=User.objects.get(id=request.user.id), course=c)
        like.save()
    else:
        Like.objects.filter(user = User.objects.get(id=request.user.id), course=c).delete()
    return detail(request, course_id)

def favorite(request, course_id):
    c = get_object_or_404(Course, pk=course_id)
    if Favorite.objects.filter(user=User.objects.get(id=request.user.id), course=c).count() < 1:
        fav = Favorite.objects.create(user=User.objects.get(id=request.user.id), course=c)
        fav.save()
    else:
        Favorite.objects.filter(user=User.objects.get(id=request.user.id), course=c).delete()
    return detail(request, course_id)

def favlist(request):
    fav = Favorite.objects.filter(user=User.objects.get(id=request.user.id))
    courses = []
    for f in fav:
        c = Course.objects.get(id=f.course.id)
        courses.append(c)

    paginator = Paginator(courses, 10)
    page = request.GET.get('page')
    try:
        courses = paginator.page(page)
    except PageNotAnInteger:
        courses = paginator.page(1)
    except EmptyPage:
        courses = paginator.page(paginator.num_pages)

    index = courses.number - 1
    max_index = len(paginator.page_range)
    start_index = index - 10 if index >= 10 else 0
    end_index = index + 10 if index <= max_index - 10 else max_index
    page_range = paginator.page_range[start_index:end_index]
    return HttpResponse(render(request,'favorites.html', context={'courses_list': courses, 'page_range': page_range}))

def adminProfile(request):
    usr = User.objects.all()
    users = []
    for u in usr:
        users.append(u.username)
    return HttpResponse(render(request, 'profile.html', context={'users': users}))

def search(request):
    courses = Course.objects.filter(name__icontains=request.GET['search'])

    paginator = Paginator(courses, 10)
    page = request.GET.get('page')
    try:
        courses = paginator.page(page)
    except PageNotAnInteger:
        courses = paginator.page(1)
    except EmptyPage:
        courses = paginator.page(paginator.num_pages)

    index = courses.number - 1
    max_index = len(paginator.page_range)
    start_index = index - 10 if index >= 10 else 0
    end_index = index + 10 if index <= max_index - 10 else max_index
    page_range = paginator.page_range[start_index:end_index]

    return HttpResponse(render(request, 'searchcourses.html', context={'courses_list': courses, 'page_range': page_range, 'search': request.GET['search']}))

def emailing(request):
    emails = [u.email for u in User.objects.all() if len(u.email) > 0]
    subject, from_email, to = 'New courses are added', 'lucyuk.a.v@gmail.com', emails
    text_content = 'New courses are added'
    f = open('/Volumes/MemoryCard/4c2s/courses/static/letter.html')
    html_content = ''.join(f.readlines())
    print(len(html_content))
    courses = Course.objects.all()[:3]
    for c in courses:
        print(c.name)
        print(c.link)
    print(courses[0].name)
    print(courses[0].link)
    print(courses[1].name)
    html_content = html_content.replace("#href1#",courses[0].link).replace("#href2#", courses[1].link).replace("#href3#",courses[2].link)
    html_content = html_content.replace("#Name1", courses[0].name).replace("#Name2", courses[1].name).replace("#Name3", courses[2].name)
    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    return HttpResponse(render(request, 'profile.html'))


def generate_recommendations(request):
    #user = int(user)
    courses = []
    liked = True
    fav = Favorite.objects.filter(user=User.objects.get(id=request.user.id)).values_list('course_id', flat=True)
    #print(fav[0])
    num = 10
    # print(len(res_rec))
    likes = Like.objects.all()
    user2courses, ordered_courses = build_dicts(likes)
    if not (request.user.id in user2courses):
        liked = False
    if liked and (len(likes) >= 100):
        prediction = RecommendToUser(request.user.id, user2courses, ordered_courses, fav, num)
        print(prediction)
        course_ids = ";".join(prediction)
        for p in prediction:
            c = Course.objects.get(id=p)
            courses.append(c)
    else:
        preference = Questionnaire.objects.get(id=((Account.objects.get(user_id=request.user.id)).questionaire_id))
        categories = preference.preferences.split(';')
        languages = preference.language.split(';')
        rec1 = []
        for c in categories:
            rec1 += Course.objects.filter(category=c)
        rec2 = []
        for r in rec1:
            try:
                dur = r.duration.split()[0]
                if int(dur) <= preference.duration:
                    print(dur)
                    rec2.append(r)
            except:
                continue

        res_rec = []
        for r in rec2:
            for l in languages:
                if r.language == l:
                    res_rec.append(r)
                    break
        random.shuffle(res_rec)
        ids = []
        for x in res_rec:
            if len(courses) >= num:
                break
            if (x not in fav) and ((not liked) or (liked and (x not in user2courses[request.user.id]))):
                ids.append(x.id)
                courses.append(x)
        print(ids)
        course_ids = ";".join(str(i) for i in ids)
        print(course_ids)
    return courses, course_ids

def recommendations(request):
    courses = []
    user_rec = Recommendation.objects.filter(user_id=request.user.id)
    if len(user_rec)!=0:
        ids = user_rec[0].courses.split(';')
        for i in ids:
            c = Course.objects.get(id=i)
            courses.append(c)
        return HttpResponse(render(request, 'recommendations.html', context={'courses_list': courses}))
    else:
        courses, course_ids = generate_recommendations(request)
        recommendation = Recommendation.objects.create(user=User.objects.get(id=request.user.id), courses=course_ids)
        recommendation.save()
        return HttpResponse(render(request, 'recommendations.html', context={'courses_list': courses}))

def regenerate(request):
    user_rec = Recommendation.objects.get(user_id=request.user.id)
    courses, course_ids = generate_recommendations(request)
    user_rec.courses = course_ids
    user_rec.save()
    return HttpResponse(render(request, 'recommendations.html', context={'courses_list': courses}))


#

#SERIALIZERS REST

class AccountList(generics.ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

class AccountDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class CourseList(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class CourseDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class QuestionnaireList(generics.ListCreateAPIView):
    queryset = Questionnaire.objects.all()
    serializer_class = QuestionnaireSerializer

class QuestionnaireDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Questionnaire.objects.all()
    serializer_class = QuestionnaireSerializer







