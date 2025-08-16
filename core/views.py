import requests
from django.shortcuts import render
from .models import UserMetadata

def home(request):
    suggestion = None
    weather = None

    if request.method == 'POST':
        name = request.POST.get('name')
        interests = request.POST.get('interests')
        drives = request.POST.get('drives') == 'on'
        lat = request.POST.get('lat')
        lon = request.POST.get('lon')

        # Save user metadata (optional)
        user, created = UserMetadata.objects.get_or_create(
            name=name,
            defaults={'interests': interests, 'drives': drives}
        )

        # Fetch weather from Open-Meteo
        weather_resp = requests.get(
            f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        )
        if weather_resp.status_code == 200:
            weather_data = weather_resp.json()
            weather = weather_data.get('current_weather', {})

        # Simple AI-based suggestion (replace with real AI call)
        if weather:
            temp = weather.get('temperature', 20)
            suggestion = "Go for a walk" if temp > 15 else "Watch a movie"

    return render(request, 'core/home.html', {'suggestion': suggestion, 'weather': weather})
