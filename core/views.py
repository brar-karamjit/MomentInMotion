from django.shortcuts import render
from .models import UserMetadata
import requests

def get_weather(city):
    # Replace with your weather API key
    api_key = "YOUR_API_KEY"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={api_key}"
    response = requests.get(url)
    data = response.json()
    if data.get("main"):
        temp = data["main"]["temp"]
        condition = data["weather"][0]["description"]
        return f"{condition}, {temp}°C"
    return "Weather unavailable"

def suggest_activity(request):
    user = request.user
    profile = UserMetadata.objects.get(user=user)
    
    # Fetch city (for MVP, you can hardcode or ask user in profile)
    city = profile.name  # replace with profile.location if added
    
    weather = get_weather(city)
    
    # Generate prompt for AI
    prompt = f"""
    User: {profile.name}
    Interests: {profile.interests}
    Drives: {'Yes' if profile.drives else 'No'}
    Location: {city}
    Weather: {weather}

    Suggest one fun activity for today.
    """
    
    # Call AI model (pseudo-code)
    ai_response = call_chat_model(prompt)  # implement this with OpenAI or your chosen API

    return render(request, "core/suggest.html", {"activity": ai_response})
