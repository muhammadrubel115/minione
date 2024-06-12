from django.shortcuts import render
#all import of views are here

from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

#import Models here
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy


# urls.py

from minigen.models import Response

# Create your views here.
@login_required(login_url=reverse_lazy('signin'))
def Mini(request):
    
    responses = Response.objects.filter(is_correct=True).order_by('-created_at')
    
    context = {
        'responses': responses,
        
    }

    return render(request, 'minigen/mini.html', context)






from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from minigen.models import MCQPost, Response
from miniaccounts.models import ProfileInfo


from django.http import JsonResponse

@login_required(login_url=reverse_lazy('signin'))
def Home(request):

    users = User.objects.all()
    
    userinfo = request.user.profileinfo

    current_user = request.user

    # Fetch the profile info of the current user
    current_user_profile = get_object_or_404(ProfileInfo, user=current_user)
    
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        mcq_post_id = request.POST.get('mcq_post_id')
        selected_option = request.POST.get('option')

        mcq_post = get_object_or_404(MCQPost, id=mcq_post_id)
        
        if selected_option:
            # Save the response
            Response.objects.create(
                user=current_user,
                mcq_post=mcq_post,
                selected_option=selected_option,
                is_correct=(selected_option == mcq_post.answer)
            )
            
            if selected_option == mcq_post.answer:
                response_message = 'Correct answer!'
            else:
                response_message = 'Incorrect answer.'
        else:
            response_message = 'No option selected.'

        return JsonResponse({'message': response_message})

    form_data = MCQPost.objects.select_related('user').prefetch_related('responses').all()

    context = {
        'users': users,
        'userinfo': userinfo,
        'current_user': current_user,
        'current_user_profile': current_user_profile,
        'form_data': form_data,
    }
    
    return render(request, 'minigen/home.html', context)


from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from minigen.models import MCQPost





from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import MCQPost

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from minigen.models import MCQPost, Notification

from django.contrib import messages
from django.shortcuts import render, redirect
from .models import MCQPost

@login_required(login_url=reverse_lazy('signin'))
def Postmcqview(request):
    if request.method == 'POST':
        question = request.POST.get('question')
        reference = request.POST.get('reference')
        option1 = request.POST.get('option1')
        option2 = request.POST.get('option2')
        option3 = request.POST.get('option3')
        option4 = request.POST.get('option4')
        answer = request.POST.get('answer')
        description = request.POST.get('description', '')  # Set default value if not provided

        # Ensure all fields are provided
        if not (question and reference and option1 and option2 and option3 and option4 and answer):
            messages.error(request, 'All fields are required.')
            return render(request, 'minigen/postmcq.html')

        # Ensure the answer matches one of the options
        if answer not in ['option1', 'option2', 'option3', 'option4']:
            messages.error(request, 'The answer must match one of the options.')
            return render(request, 'minigen/postmcq.html')

        # Create the MCQ post
        MCQPost.objects.create(
            user=request.user,
            question=question,
            reference=reference,
            option1=option1,
            option2=option2,
            option3=option3,
            option4=option4,
            answer=answer,
            description=description
        )

        messages.success(request, 'MCQ posted successfully!')
        return redirect('home')

    # Render the form for GET requests
    return render(request, 'minigen/postmcq.html')




@login_required(login_url=reverse_lazy('signin'))
def Notification(request):
    
    notifications = request.user.notifications.all().select_related('follower').order_by('-created_at')
    
    notifications.update(is_read=True)  # Mark all notifications as read
    context = {
        'notifications': notifications,
    }

    return render(request, 'minigen/notification.html', context)


from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import ProfileInfo

@login_required(login_url=reverse_lazy('signin'))
def Search(request):
    query = request.POST.get('question', '')  # Get the search query from the form
    result1 = result2 = None  # Initialize results as None
    
    if query:  # Perform search only if the query is not empty
        result1 = ProfileInfo.objects.filter(user__username__icontains=query)
        result2 = ProfileInfo.objects.filter(bio__icontains=query)

    context = {
        'query': query,  # Pass the query back to the template for displaying in the form
        'result1': result1,
        'result2': result2,
    }

    return render(request, 'minigen/search.html', context)



from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render
from django.core.paginator import Paginator
from miniaccounts.models import ProfileInfo

@login_required(login_url=reverse_lazy('signin'))
def Profile(request):
    
    try:
        userinfo = request.user.profileinfo
    except ProfileInfo.DoesNotExist:
        userinfo = None  # Handle the case where the profile info does not exist
    
    # Get users who follow the current user
    followers = request.user.profileinfo.followers.select_related('profileinfo').all()

    # Paginate the followers list
    paginator = Paginator(followers, 10)  # Show 10 followers per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'users': page_obj,
        'userinfo': userinfo,
        
    }

    return render(request, 'minigen/profile.html', context)


@login_required(login_url=reverse_lazy('signin'))
def Settings(request):
    
    try:
        userinfo = request.user.profileinfo
    except ProfileInfo.DoesNotExist:
        userinfo = None  # Handle the case where the profile info does not exist
    
    # Get users who follow the current user
    followers = request.user.profileinfo.followers.select_related('profileinfo').all()

    # Paginate the followers list
    paginator = Paginator(followers, 10)  # Show 10 followers per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'users': page_obj,
        'userinfo': userinfo,
        
    }

    return render(request, 'minigen/settings.html', context)

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from miniaccounts.models import ProfileInfo
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

@login_required(login_url=reverse_lazy('signin'))
def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    users = User.objects.all()
    userinfo = request.user.profileinfo
    # Retrieve the user object
    profile_user = get_object_or_404(User, username=username)

    # Retrieve MCQPost objects associated with the user
    user_posts = MCQPost.objects.filter(user=profile_user)
    current_user = request.user
    
    following = request.user.profileinfo.following.select_related('profileinfo').all()
    paginator = Paginator(following, 10)  # Show 10 followers per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    try:
        following_users = paginator.page(page_obj)
    except PageNotAnInteger:
        following_users = paginator.page(1)
    except EmptyPage:
        following_users = paginator.page(paginator.num_pages)

    # Fetch the profile info of the current user
    current_user_profile = get_object_or_404(ProfileInfo, user=current_user)
    
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        mcq_post_id = request.POST.get('mcq_post_id')
        selected_option = request.POST.get('option')

        mcq_post = get_object_or_404(MCQPost, id=mcq_post_id)
        
        if selected_option:
            # Save the response
            Response.objects.create(
                user=current_user,
                mcq_post=mcq_post,
                selected_option=selected_option,
                is_correct=(selected_option == mcq_post.answer)
            )
            
            if selected_option == mcq_post.answer:
                response_message = 'Correct answer!'
            else:
                response_message = 'Incorrect answer.'
        else:
            response_message = 'No option selected.'

        return JsonResponse({'message': response_message})

    form_data = MCQPost.objects.select_related('user').prefetch_related('responses').all()
    context = {
        'profile_user': user,
        'users': users,
        'userinfo': userinfo,
        'current_user': current_user,
        'current_user_profile': current_user_profile,
        'form_data': form_data,
        'following_users': following_users,
        'user_posts': user_posts
    }
    return render(request, 'minigen/profile_view.html', context)


from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.models import User

@login_required(login_url=reverse_lazy('signin'))
def follow(request, username):
    user_to_follow = get_object_or_404(User, username=username)
    request.user.profileinfo.following.add(user_to_follow)
    user_to_follow.profileinfo.followers.add(request.user)
    return redirect('profile_view', username=username)

@login_required(login_url=reverse_lazy('signin'))
def unfollow(request, username):
    user_to_unfollow = get_object_or_404(User, username=username)
    request.user.profileinfo.following.remove(user_to_unfollow)
    user_to_unfollow.profileinfo.followers.remove(request.user)
    return redirect('profile_view', username=username)




from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from miniaccounts.models import ProfileInfo
from miniaccounts.forms import ProfileInfoForm




from django.contrib.auth import logout
from django.shortcuts import redirect

@login_required(login_url=reverse_lazy('signin'))
def logout_view(request):
    """
    Logs out the current user and redirects to the homepage.
    """
    logout(request)
    # Redirect to the homepage or any other desired page
    return redirect('signin')


@login_required(login_url=reverse_lazy('signin'))
def Change_username(request):
    if request.method == 'POST':
        new_username = request.POST['new_username']

        # Check if the new username is different from the current one
        if new_username != request.user.username:
            # Check if the new username is already taken
            if User.objects.filter(username=new_username).exists():
                messages.error(request, "Username already exists. Please choose a different one.")
            else:
                # Update the username
                request.user.username = new_username
                request.user.save()
                messages.success(request, "Username changed successfully.")
                return redirect('profile')  # Redirect to the profile page or any other page
        else:
            messages.warning(request, "New username is the same as the current one.")

    return render(request, 'minigen/change_username.html')

@login_required(login_url=reverse_lazy('signin'))
def Change_acc_name(request):
    if request.method == 'POST':
        acc_name = request.POST['acc_name']

        # Check if the new username is different from the current one
        if acc_name != request.user.username:
            # Check if the new username is already taken
                request.user.profileinfo.acc_name = acc_name
                request.user.profileinfo.save()
                messages.success(request, "Username changed successfully.")
                return redirect('profile')  # Redirect to the profile page or any other page
        else:
            messages.warning(request, "New username is the same as the current one.")

    return render(request, 'minigen/change_accname.html')

@login_required(login_url=reverse_lazy('signin'))
def Change_email(request):
    if request.method == 'POST':
        new_email = request.POST['new_email']

        # Check if the new email is different from the current one
        if new_email != request.user.email:
            # Check if the new email is already registered by another user
            if User.objects.filter(email=new_email).exists():
                messages.error(request, "Email address already exists. Please choose a different one.")
            else:
                # Update the email address
                request.user.email = new_email
                request.user.save()
                messages.success(request, "Email address changed successfully.")
                return redirect('profile')  # Redirect to the profile page or any other page
        else:
            messages.warning(request, "New email address is the same as the current one.")

    return render(request, 'minigen/change_email.html')

@login_required(login_url=reverse_lazy('signin'))
def Change_remail(request):
    if request.method == 'POST':
        remail = request.POST.get('remail')

        # Check if the new email is different from the current one
        if remail != request.user.email:
            # Check if the new email is already registered by another user
            if User.objects.filter(email=remail).exists():
                messages.error(request, "Email address already exists. Please choose a different one.")
            else:
                # Update the email address
                request.user.profileinfo.remail = remail
                request.user.profileinfo.save()
                messages.success(request, "Email address changed successfully.")
                return redirect('profile')  # Redirect to the profile page or any other page
        else:
            messages.warning(request, "New email address is the same as the current one.")

    return render(request, 'minigen/change_remail.html')

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required

@login_required(login_url=reverse_lazy('signin'))
def Change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important to keep the user logged in
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile')  # Redirect to the profile page or any other page after password change
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'minigen/change_password.html', {'form': form})




from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from miniaccounts.models import ProfileInfo
from miniaccounts.forms import ProfileInfoForm

@login_required(login_url=reverse_lazy('signin'))
def ChangeProfilePicture(request):
    if request.method == 'POST':
        profile = request.user.profileinfo
        profile.image = request.FILES['image']
        profile.save()
        messages.success(request, 'Your profile picture has been updated successfully!')
        return redirect('profile')
    return render(request, 'minigen/change_profile_picture.html')

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from miniaccounts.models import ProfileInfo

@login_required(login_url=reverse_lazy('signin'))
def ChangeBio(request):
    if request.method == 'POST':
        new_bio = request.POST.get('bio', '').strip()
        
        if new_bio:
            request.user.profileinfo.bio = new_bio
            request.user.profileinfo.save()
            messages.success(request, 'Your bio has been updated successfully!')
            return redirect('profile')
        else:
            messages.error(request, 'Bio cannot be empty.')

    return render(request, 'minigen/change_bio.html')



from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from miniaccounts.models import ProfileInfo

@login_required(login_url=reverse_lazy('signin'))
def ChangeAccountCategory(request):
    if request.method == 'POST':
        new_account_category = request.POST.get('account_category', '').strip()
        
        if new_account_category:
            request.user.profileinfo.acc_type = new_account_category
            request.user.profileinfo.save()
            messages.success(request, 'Your account category has been updated successfully!')
            return redirect('profile')
        else:
            messages.error(request, 'Account category cannot be empty.')

    return render(request, 'minigen/change_account_category.html')


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from miniaccounts.models import ProfileInfo

@login_required(login_url=reverse_lazy('signin'))
def UpdateCountry(request):
    if request.method == 'POST':
        new_country = request.POST.get('country', '').strip()
        
        if new_country:
            request.user.profileinfo.country = new_country
            request.user.profileinfo.save()
            messages.success(request, 'Your country has been updated successfully!')
            return redirect('profile')
        else:
            messages.error(request, 'Country cannot be empty.')

    return render(request, 'minigen/update_country.html')

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from miniaccounts.models import ProfileInfo

@login_required(login_url=reverse_lazy('signin'))
def ChangeGender(request):
    if request.method == 'POST':
        new_gender = request.POST.get('gender', '').strip()
        
        if new_gender:
            request.user.profileinfo.gender = new_gender
            request.user.profileinfo.save()
            messages.success(request, 'Your gender has been updated successfully!')
            return redirect('profile')
        else:
            messages.error(request, 'Gender cannot be empty.')

    return render(request, 'minigen/change_gender.html')

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from miniaccounts.models import ProfileInfo

@login_required(login_url=reverse_lazy('signin'))
def ChangeDOB(request):
    if request.method == 'POST':
        new_dob = request.POST.get('dob', '').strip()
        
        if new_dob:
            request.user.profileinfo.dob = new_dob
            request.user.profileinfo.save()
            messages.success(request, 'Your date of birth has been updated successfully!')
            return redirect('profile')
        else:
            messages.error(request, 'Date of birth cannot be empty.')

    return render(request, 'minigen/change_dob.html')


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from miniaccounts.models import ProfileInfo

@login_required(login_url=reverse_lazy('signin'))
def ChangePhoneNumber(request):
    if request.method == 'POST':
        new_phone_number = request.POST.get('phone_number', '').strip()
        
        if new_phone_number:
            request.user.profileinfo.phone = new_phone_number
            request.user.profileinfo.save()
            messages.success(request, 'Your phone number has been updated successfully!')
            return redirect('profile')
        else:
            messages.error(request, 'Phone number cannot be empty.')

    return render(request, 'minigen/change_phone_number.html')


@login_required(login_url=reverse_lazy('signin'))
def Support(request):
    
    return render(request, 'minigen/support.html')

@login_required(login_url=reverse_lazy('signin'))
def Edit_Profile(request):
    
    return render(request, 'minigen/edit_profile.html')