from django.shortcuts import render, redirect
from .models import User, Trail, Trip
from django.contrib import messages
import bcrypt

###########################################  Display Methods  ###########################################

# Login/Reg Page
def index(request):
    if 'user_id' in request.session:
        return redirect('/dashboard')
    return render(request, "index.html")

# table listing all TRAILS
def display_dashboard(request):
    if 'user_id' not in request.session:
        return redirect('/')
    context = {
        'this_user': User.objects.get(id=request.session['user_id']),
        'all_trails': Trail.objects.all()
    }
    return render(request, "dashboard_placeholder.html", context)

# displays a single trail details
def display_trail_details(request, id):
    if 'user_id' not in request.session:
        return redirect('/')
    context = {
      'this_user': User.objects.get(id=request.session['user_id']),
      'this_trail': Trail.objects.get(id=id)
    }
    return render(request, "trail_details_placeholder.html", context)

# table listing all "my trips"
# still need to add this page and have it separate created trips and joined trips
def display_my_trips(request):
    if 'user_id' not in request.session:
        return redirect('/')
    context = {
        'this_user': User.objects.get(id=request.session['user_id'])
    }
    return render(request, "my_trips_placeholder.html", context)

# form page to create a trip itinerary
def display_make_new_trip(request):
    if 'user_id' not in request.session:
        return redirect('/')
    context = {
        'this_user': User.objects.get(id=request.session['user_id']),
        'all_trails': Trail.objects.all()
    }
    return render(request, "create_trip.html", context)

# form page to edit a trip
def display_update_trip(request, id):
    if 'user_id' not in request.session:
        return redirect('/')
    context = {
        'this_user': User.objects.get(id=request.session['user_id']),
        'this_trip': Trip.objects.get(id=id)
    }
    return render(request, "update_trip.html", context)

# single trip details
def display_trip_details(request, id):
    if 'user_id' not in request.session:
        return redirect('/')
    context = {
      'this_user': User.objects.get(id=request.session['user_id']),
      'this_trip': Trip.objects.get(id=id)
    }
    return render(request, "trip_details_placeholder.html", context)
###########################################  Action Methods  ###########################################

# Logic to create trip
def create(request):
    user = User.objects.get(id=request.session['user_id'])
    add_trail = Trail.objects.get(id=request.POST['trail'])
    # errors = Trip.objects.trip_validator(request.POST)
    # if len(errors) > 0:
    #     for key, value in errors.items():
    #         messages.error(request, value)
    #     return redirect('/trip/new')
    new_trip = Trip.objects.create(
        trip_name = request.POST['trip_name'],
        trip_date = request.POST['trip_date'],
        food_list = request.POST['food_list'],
        gear_check = request.POST['gear_check'],
        creator = user,
    )
    new_trip.trails.add(add_trail)
    return redirect('/trip/my_trips')

# Logic to update trip
def update_trip(request, id):
    # errors = Trip.objects.trip_validator(request.POST)
    # if len(errors) > 0:
    #     for key, value in errors.items():
    #         messages.error(request, value)
    #     return redirect(f'/trip/edit/{id}')
    this_trip = Trip.objects.get(id=id)
    this_trail = Trail.objects.get(id=request.POST['trail'])
    if request.POST['trip_name'] != this_trip.trip_name:
        this_trip.trip_name=request.POST['trip_name']
        this_trip.save()
    if this_trail != this_trip.trail:
        this_trip.trail=this_trail
        this_trip.save()
    if request.POST['trip_date'] != this_trip.trip_date:
        this_trip.trip_date=request.POST['trip_date']
        this_trip.save()
    if request.POST['food_list'] != this_trip.food_list:
        this_trip.food_list=request.POST['food_list']
        this_trip.save()
    if request.POST['gear_check'] != this_trip.gear_check:
        this_trip.gear_check=request.POST['gear_check']
        this_trip.save()
    return redirect('/trip/my_trips')
# 
# Logic to cancel(un-join) someone elses trip (does not delete the trip)
# def cancel(request, id):
#     remove_trip = Trip.objects.get(id=id)
#     remove_user = request.session['user_id']
#     remove_trip.joined.remove(remove_user)
#     return redirect('/trip/my_trips')

# Logic to join someone elses trip
# def join(request, id):
#     join_trip = Trip.objects.get(id=id)
#     join_user = request.session['user_id']
#     join_trip.joined.add(join_user)
#     return redirect('/trip/my_trips')

# Logic to delete a trip (can only delete trips you created)
# def remove(request, id):
#     trip_delete = Trip.objects.get(id=id).delete()
#     return redirect('/trip/my_trips')
# 
# 
# 
# 
# 
#       #need a hidden input on form for this so we can get id for the page this is from
# def post_comment(request, id):
#     post_user = User.objects.get(id=request.session['user_id'])
#     new_comment = Comment.objects.create(
#         user = post_user,
#         comment = request.POST['comment']
#     )
#     return redirect(f'/trail/detail/{id}')

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
    return redirect('/dashboard')

def login(request):
    # create variable user_matching_email to save the instance of User that matches the entered email
    user_matching_email = User.objects.filter(email_address=request.POST['email']).first()

    # if the email entered in login DOES exist in our database then
    if user_matching_email is not None:
        # hash the entered password and check if matches the hashed password saved in database
        if bcrypt.checkpw(request.POST['password'].encode(), user_matching_email.password.encode()):
            #if email and password match start users session
            request.session['user_id'] = user_matching_email.id
            return redirect('/dashboard')
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


#################### admin methods ###############################
def display_make_new_trail(request):
    if 'user_id' not in request.session:
        return redirect('/')
    context = {
        'this_user': User.objects.get(id=request.session['user_id'])
    }
    return render(request, "admin_create_trail.html", context)

def create_trail(request):
    user = User.objects.get(id=request.session['user_id'])
    # errors = Trip.objects.trip_validator(request.POST)
    # if len(errors) > 0:
    #     for key, value in errors.items():
    #         messages.error(request, value)
    #     return redirect('/new')
    new_trail = Trail.objects.create(
        name = request.POST['name'],
        location = request.POST['location'],
        difficulty = request.POST['difficulty'],
        distance = request.POST['distance'],
        elevation_change = request.POST['elevation_change'],
        route_type = request.POST['route_type'],
        rating = request.POST['rating'],
        description = request.POST['description']
    )
    return redirect('/dashboard')

def display_update_trail(request):
    pass

def update_trail(request):
    pass

def delete_trail(request):
    pass