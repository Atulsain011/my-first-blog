from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required  
from .forms import SignUpForm
from .forms import ProfileForm 
# from .models import Profile  
from django.contrib.auth.decorators import login_required
from blog.models import Post

def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("login")

    else:
        form = SignUpForm()

    return render(
        request,
        "registration/signup.html",
        {"form": form}
    )


@login_required

def profile(request):

    my_posts = Post.objects.filter(
        author=request.user
    )

    return render(
        request,
        "registration/profile.html",
        {
            "my_posts": my_posts
        }
    )

@login_required
def profile_edit(request):

    profile = request.user
    
    if request.method == "POST":  
        
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        
        if form.is_valid():
            form.save()
            return redirect("profile")  
    else:
        form = ProfileForm(instance=profile)
        
    return render(
        request, 
        "registration/profile_edit.html", 
        {"form": form}
    )


# def profile(request):
#     return render(request, "registration/profile.html")

def delete_profile_image(request):

    profile = request.user

    if profile.image and profile.image.name != "default.jpg":
        profile.image.delete(save=False)
        profile.image = "default.jpg"
        profile.save()

    return redirect("profile_edit")