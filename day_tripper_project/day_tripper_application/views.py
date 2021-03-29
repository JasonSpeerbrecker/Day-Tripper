from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages
import bcrypt

###########################################  Display Methods  ###########################################
def index(request):
    if 'user_id' in request.session:
        return redirect('/success')
    return render(request, "index.html")

def success(request):
    if 'user_id' not in request.session:
        return redirect('/')
    context = {
        'this_user': User.objects.get(id=request.session['user_id'])
    }
    return render(request, "success.html", context)

###########################################  Action Methods  ###########################################
def register(request):
    # Validations
    errors = User.objects.reg_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    
    # Password Hashing
    password = request.POST['password']
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    # Create New User
    new_user = User.objects.create(
        first_name = request.POST['fName'],
        last_name = request.POST['lName'],
        email_address= request.POST['email'],
        password = pw_hash
    )
    # Start User's session by saving their id to request.session['user_id']
    request.session['user_id'] = new_user.id
    return redirect('/success')

def login(request):
    # create variable user_matching_email to save the instance of User that matches the entered email
    user_matching_email = User.objects.filter(email_address=request.POST['email']).first()

    # if the email entered in login DOES exist in our database then
    if user_matching_email is not None:
        # hash the entered password and check if matches the hashed password saved in database
        if bcrypt.checkpw(request.POST['password'].encode(), user_matching_email.password.encode()):
            #if email and password match start users session
            request.session['user_id'] = user_matching_email.id
            return redirect('/success')
        else:
            #this else is if password does not match
            messages.add_message(request, messages.ERROR, 'Invalid Credentials')
            return redirect('/')
    #this else is if email does not exist in our database
    else:
        messages.add_message(request, messages.ERROR, 'Invalid Credentials')
        return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/')