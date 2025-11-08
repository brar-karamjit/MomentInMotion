from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import requests
import json
import os
from .forms import *
from django.contrib.auth.models import User
from django.contrib.auth import login
from core.models import UserMetadata     




GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")  # stored in environment variable


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = SignUpForm()
    return render(request, "core/signup.html", {"form": form})


def get_suggestion(user, metadata, weather, latitude, longitude):
    user_name = f"{user.first_name} {user.last_name}" or "none"
    interests = metadata.interests or "no specific interest"
    drives = metadata.drives

    prompt_text = f"""
    User: {user_name}
    Interests: {interests}
    Drives: {drives}
    Latitude: {latitude}
    Longitude: {longitude}
    Weather: {weather['temperature']}°C, {weather.get('weathercode', 'unknown')}
    Calculate the rough city name from given latitute longitude.
    Important: Keep your answer very brief. For example, "Visit the local museum" or "Go for a walk in the park (park name)". 
    You can also suggest acitivies outside user interest, take various factors into account like weather, time of day, events happening in city.
    Suggest activities this user can do right now.
    """

    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
    headers = {"Content-Type": "application/json", "X-goog-api-key": GEMINI_API_KEY}
    data = {"contents": [{"parts": [{"text": prompt_text}]}]}

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()

        candidates = result.get("candidates", [])
        suggestion_text = ""
        if candidates:
            parts = candidates[0].get("content", {}).get("parts", [])
            if parts:
                suggestion_text = parts[0].get("text", "").strip()

        return {"response": suggestion_text or "No suggestion available."}

    except Exception as e:
        return {"response": f"Error generating suggestion: {e}"}


@login_required
def home(request):
    user = request.user
    try:
        metadata = UserMetadata.objects.get(user=user)
    except UserMetadata.DoesNotExist:
        metadata = None

    suggestion_data = None
    city = "N/A"

    if request.method == "POST" and request.POST.get("action") == "get_suggestion":
        lat = request.POST.get("lat")
        lon = request.POST.get("lon")
        temperature = request.POST.get("temperature")
        weathercode = request.POST.get("weathercode")

        weather = {"temperature": temperature, "weathercode": weathercode}

        suggestion_data = get_suggestion(user, metadata, weather, lat, lon)

    return render(request, "core/home.html", {
        "user": user,
        "suggestion_data": suggestion_data,
    })


@login_required
def profile(request):
    user = request.user
    try:
        metadata = UserMetadata.objects.get(user=user)
    except UserMetadata.DoesNotExist:
        metadata = UserMetadata(user=user)  # create blank metadata if missing

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=metadata)
        if form.is_valid():
            form.save()
            return redirect('profile')  # reload page after saving
    else:
        form = UserProfileForm(instance=metadata)

    return render(request, 'core/profile.html', {'form': form, 'user': user})