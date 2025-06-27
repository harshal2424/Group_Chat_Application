# from django.shortcuts import render
from django.shortcuts import render, redirect
from .models import Message,Profile
from .forms import MessageForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.views import LogoutView
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse
from .forms import ProfileForm
from .forms import UserCreationFormWithProfile
from django.apps import apps
from .forms import CustomSignupForm



@login_required
def chat_view(request):
    # Handle form submission
    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)  # Handle file uploads
        if form.is_valid():
            message = form.save(commit=False)  # Do not immediately save the instance
            message.user = request.user  # Assign the logged-in user to the message
            message.save()  # Save the message with the user and file (if provided)
            return redirect('chat')  # Redirect to clear the form
    
    # Display the last 20 messages (most recent first)
    messages = Message.objects.order_by('-timestamp')[:20]
    form = MessageForm()

    # Render the template with messages, the form, and the logged-in user
    return render(request, 'chat.html', {
        'messages': messages,
        'form': form,
        'user': request.user
    })




# Create your views here.

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationFormWithProfile(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            # Create or update the Profile instance with the uploaded avatar
            profile, created = Profile.objects.get_or_create(user=user)
            profile.avatar = form.cleaned_data.get('avatar')
            profile.save()
            login(request, user)
            return redirect('chat')  # Redirect to chat or any other page
    else:
        form = UserCreationFormWithProfile()
    return render(request, 'signup.html', {'form': form})








class CustomLogoutView(LogoutView):
    def get(self, request, *args, **kwargs):
        # Log out the user and redirect to the desired page
        self.logout(request)
        return HttpResponseRedirect(self.next_page)
    
    
@login_required
def clear_chat(request):
    if not request.user.is_superuser:  # Check if user is an admin (superuser)
        return HttpResponse("You do not have authority", status=403)  # 403 Forbidden status
    if request.method == "POST":
        # Delete all messages
        Message.objects.all().delete()
        return redirect('chat')  # Redirect back to the chat page after clearing

    return render(request, 'clear_chat_confirm.html')  # Optional: Show a confirmation page if needed


@login_required
def edit_profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('chat')  # Redirect to the chat page
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'edit_profile.html', {'form': form})


@login_required
def profile_view(request):
    # Dynamically resolve the Profile model
    Profile = apps.get_model('myapp', 'Profile')
    
    # Ensure the Profile exists for the logged-in user
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        nickname = request.POST.get('nickname', profile.nickname)  # Default to existing nickname
        avatar = request.FILES.get('avatar', None)  # Get the uploaded file, if any

        # Update profile fields
        profile.nickname = nickname
        if avatar:  # Update avatar only if a new one is provided
            profile.avatar = avatar
        profile.save()  # Save changes to the database

        return redirect('profile_view')  # Redirect to the same page after saving

    # Pass the profile object and user information to the template
    context = {
        'profile': profile,
        'username': request.user.username,
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'email': request.user.email,
    }
    return render(request, 'profile.html', context)
