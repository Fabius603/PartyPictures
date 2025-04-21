from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import UploadedImage, AppConfig
from .forms import ImageUploadForm
from django.http import JsonResponse
import time

def upload_view(request):
    config = AppConfig.objects.first() or AppConfig(slideshow_speed=10, upload_cooldown=30)
    cooldown = config.upload_cooldown

    if request.method == 'POST':
        last_upload = request.session.get("last_upload_ts", 0)
        if time.time() - last_upload < cooldown:
            wait = cooldown - int(time.time() - last_upload)
            messages.error(request, f"Wart noch {wait}s, bevor du noch ein Bild hochlädst.")
            return redirect('upload')

        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            request.session["last_upload_ts"] = int(time.time())
            return redirect('upload')  # leitet weiter zur GET-Anfrage
    else:
        form = ImageUploadForm()

    return render(request, 'gallery/upload.html', {
        'form': form,
        'cooldown': cooldown,
        'remaining': max(0, cooldown - int(time.time() - request.session.get("last_upload_ts", 0))),
    })

def slideshow_view(request):
    config = AppConfig.objects.first() or AppConfig(slideshow_speed=10, upload_cooldown=30)
    cooldown = config.upload_cooldown
    speed = config.slideshow_speed
    
    # Alle freigegebenen Bilder ältestes → neuestes
    return render(request, 'gallery/slideshow.html', {
        'images': UploadedImage.objects.filter(approved=True).order_by('uploaded_at'),
        'speed': speed,
        'cooldown': cooldown,
    })

def slideshow_data(request):
    qs = UploadedImage.objects.filter(approved=True).order_by('uploaded_at')
    urls = [request.build_absolute_uri(img.image.url) for img in qs]
    speed = request.session.get('slideshow_speed', 10)  # Sekunden
    cooldown = request.session.get('upload_cooldown', 30)  # Sekunden

    return JsonResponse({
        'urls': urls,
        'speed': speed,
        'cooldown': cooldown
    })


@login_required
def settings_view(request):
    config, created = AppConfig.objects.get_or_create(id=1)

    if request.method == 'POST':
        if 'disable_all' in request.POST:
            UploadedImage.objects.update(approved=False)
            messages.success(request, "Alle Bilder wurden deaktiviert.")
            return redirect('settings')

        elif 'disable_image' in request.POST:
            image_id = request.POST.get('disable_image')
            try:
                UploadedImage.objects.get(id=image_id).approved = False
                UploadedImage.objects.filter(id=image_id).update(approved=False)
                messages.success(request, "Bild wurde deaktiviert.")
            except UploadedImage.DoesNotExist:
                messages.error(request, "Bild nicht gefunden.")
            return redirect('settings')

        elif 'enable_image' in request.POST:
            image_id = request.POST.get('enable_image')
            try:
                UploadedImage.objects.get(id=image_id).approved = True
                UploadedImage.objects.filter(id=image_id).update(approved=True)
                messages.success(request, "Bild wurde reaktiviert.")
            except UploadedImage.DoesNotExist:
                messages.error(request, "Bild nicht gefunden.")
            return redirect('settings')

        elif 'speed' in request.POST and 'cooldown' in request.POST:
            try:
                config.slideshow_speed = int(request.POST['speed'])
                config.upload_cooldown = int(request.POST['cooldown'])
                config.save()
                messages.success(request, "Einstellungen gespeichert.")
            except (ValueError, TypeError):
                messages.error(request, "Ungültige Eingaben.")
            return redirect('settings')

    return render(request, 'gallery/settings.html', {
        'images': UploadedImage.objects.all().order_by('uploaded_at'),
        'speed': config.slideshow_speed,
        'cooldown': config.upload_cooldown,
    })

def menu_view(request):
    return render(request, 'gallery/menu.html')