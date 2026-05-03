from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegistrationForm, UserUpdateForm
from blog.models import Post
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required



def register(request):
    
    form = UserRegistrationForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
      
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

     
        activation_link = request.build_absolute_uri(
            f"/activate/{uid}/{token}/"
        )

        
        send_mail(
            subject='Confirm your account',
            message=f'Click this link to activate your account: {activation_link}',
            from_email='noreply@inkwell.com',
            recipient_list=[user.email],
            fail_silently=False,
        )

        messages.success(
            request,
            "Account created successfully. Check your email to activate your account."
        )

        return redirect('login')

    return render(request, 'users/register.html', {'form': form})
        



def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('login')
    else:
        return HttpResponse("Invalid activation link")
    

@login_required
def edit_user(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully")
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)

    return render(request, 'users/edit_user.html', {'form': form})
@login_required
def delete_user(request):
    if request.method == 'POST':
        user = request.user
        logout(request)   # logout first
        user.delete()     # then delete
        return redirect('home')

    return render(request, 'users/delete_user.html')


