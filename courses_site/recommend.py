import math

def build_dicts(likes):
    user_to_courses = dict()
    course_to_count = dict()
    for like in likes:
        user = like.user_id
        course = like.course_id
        if user in user_to_courses:
            user_to_courses[user].add(course)
        else:
            user_to_courses[user] = set([course])

        if course in course_to_count:
            course_to_count[course]+=1
        else:
            course_to_count[course]=1
    ordered_courses = sort_dict_dec(course_to_count)
    return user_to_courses, ordered_courses

def course_to_count(likes):
    ctc=dict()
    for like in likes:
        course=like.course_id
        if course in ctc:
            ctc[course]+=1
        else:
            ctc[course]=1
    return ctc

def user_to_courses(likes):
    utc=dict()
    for like in likes:
        user = like.user_id
        course = like.course_id
        if user in utc:
            utc[user].add(course)
        else:
            utc[user]=set([course])
    return utc

def user_to_count(if_str):
    utc=dict()
    with open(if_str,"r") as f:
        for line in f:
            user,_,_=line.strip().split('\t')
            if user in utc:
                utc[user]+=1
            else:
                utc[user]=1
    return utc

def sort_dict_dec(d):
    return sorted(d.keys(),key=lambda s:d[s],reverse=True)

def User_Score(user_songs, u2c, q=1, a=0):
   s_scores = {}
   for u_tr in u2c:
       if not u_tr in u2c:
           continue
       w = float(len(u2c[u_tr] & user_songs))
       if w > 0:
           l1 = len(user_songs)
           l2 = len(u2c[u_tr])
           w /= (math.pow(l1, a) * (math.pow(l2, (1.0 - a))))
           w = math.pow(w, q)
       for s in u2c[u_tr]:
           if s in s_scores:
               s_scores[s] += w
           else:
               s_scores[s] = w
   return s_scores

def RecommendToUser(user, u2c, ord_courses, fav, num):
    songs_sorted = []
    cleaned_songs = []
    ssongs = []
    if user in u2c:
        ssongs = sort_dict_dec(User_Score(u2c[user], u2c))
    else:
        ssongs = list(ord_courses)
        for x in ssongs:
            if len(cleaned_songs) >= num:
                break
            if x not in fav:
                cleaned_songs.append(x)
        return cleaned_songs
    print(ssongs)
    for x in ssongs:
        if len(cleaned_songs) >= num:
            break
        if (x not in u2c[user]) and (x not in fav):
            cleaned_songs.append(x)

    #songs_sorted += [cleaned_songs]
    return cleaned_songs