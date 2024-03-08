from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import *
import bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

def index(request):
    return render(request, "index.html")

def login_page(request):
    return render(request, 'login.html')

def register_page(request):
    return render(request, 'register.html')

def dashboard(request):
    context = {
        'user_data' : User.objects.all()
    }
    return render(request, 'dashboard.html', context)

def register(request):
    print(request)
    error = False
    if len(request.POST['first_name']) < 2:
        error = True
        messages.error(request, "First name must be a minimum length of three characters!")
    if request.POST['first_name'].isalpha() == False:
        error = True
        messages.error(request, "First name cannot have a number in it or be blank!")
    if len(request.POST['last_name']) < 2:
        error = True
        messages.error(request, "Last name must be a minimum length of three characters!")
    if request.POST['last_name'].isalpha() == False:
        error = True
        messages.error(request, "Last name cannot have a number in it or be blank!")
    if len(request.POST['email']) < 7:
        error = True
        messages.error(request, "Last name must be a minimum length of three characters!")
    if not EMAIL_REGEX.match(request.POST['email']):
        error = True
        messages.error(request, "Email must be a valid email address!")
    if len(request.POST['password']) < 8:
        error = True
        messages.error(request, "Password must be a minimum length of eight characters!")
    if request.POST['password'] != request.POST['confirm_password']:
        error = True
        messages.error(request, "Passwords must match!")
    if User.objects.filter(email=request.POST['email']):
        error = True
        messages.error(request, "User already exists!")
    if error:
        return redirect('/register_page')
    
    hashed = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
    decoded_hash = hashed.decode('utf-8')
    
    user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=decoded_hash)
    print(user)
    request.session['u_id'] = user.id
    user.profile = user.id
    if user.id == 1:
        user.user_level = 1
    return redirect('/dashboard')

def login(request):
    # print(request)
    user_list = User.objects.filter(email=request.POST['email'])
    if not user_list:
        messages.error(request, "Invalid credentials!")
        return redirect('/login')
    user = user_list[0]
    if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
        request.session['u_id'] = user.id
        request.session['u_fname'] = user.first_name
        request.session['user_level'] = user.user_level
        if request.session['user_level'] == 1:
            return redirect('/dashboard/admin')
        if request.session['user_level'] == 2:
            return redirect('/dashboard')
    else:
        messages.error(request, "Invalid credentials!")
        return redirect('/')


def users_homepage(request, id):
    context = {
        "user" : User.objects.filter(id = id),
        "message" : Message.objects.filter(profile=id)
    }
    return render(request, 'profile.html', context)

def edit_users(request,id):
    user = User.objects.get(id = request.POST['u_id'])
    if request.POST['submit'] == 'Save':
        for i in request.POST:
            setattr(user,i,request.POST[i])
        user.save()
        return redirect('/dashboard')
    if request.POST['submit'] == 'Update Password':
        error = False
        if len(request.POST['password']) < 8:
            error = True
            messages.error(request, "Password must be a minimum length of eight characters!")
        if request.POST['password'] != request.POST['confirm_password']:
            error = True
            messages.error(request, "Passwords must match!")
        if error == True:
            return redirect('/users/edit/'+str(user.id))
        password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        user.password = password
        user.save()
    if request.POST['submit'] == 'Change Description!':
        user.description = request.POST['description']
        return redirect('/dashboard')

def edit(request, id):
    context = {
        'user_data': User.objects.filter(id = id)
    }
    return render(request, 'edit.html', context)

def adminedit(request, id):
    context = {
        'user_data': User.objects.filter(id = id)
    }
    return render(request, 'adminedit.html', context)

    
def wall(request, id):
    context = {
        'message' : Message.objects.all(),
    }
    return render(request, 'wall.html', context)

def post(request, id):
    request.session["prof_id"] = id
    Message.objects.create(message=request.POST['message'],message_author=User.objects.get(id=request.session['u_id']),profile=request.session["prof_id"])
    return redirect('/users/show/' + str(id))
    print(request.POST['message'])
    
    #try to assign messages using foriegn keys
def comment(request):
    Comment.objects.create(comment=request.POST['comment'], comment_author=User.objects.get(id=request.session['u_id']), comment_message=Message.objects.get(id=request.POST['comment_message_id']))
    return redirect('/users/show/' + str(id))
    print(request.POST['comment'])

def logout(request):
    del request.session['u_id']
    del request.session['user_level']
    return redirect ('/login')

def delete(request, id):
    User.objects.get(id=id).delete()
    return redirect ('/dashboard')
