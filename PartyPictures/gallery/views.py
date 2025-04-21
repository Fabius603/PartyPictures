from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import UploadedImage, AppConfig
from .forms import ImageUploadForm
from django.http import JsonResponse
import time
import random

def upload_view(request):
    config = AppConfig.objects.first() or AppConfig(slideshow_speed=10, upload_cooldown=30)
    cooldown = config.upload_cooldown
    upload_enabled = config.upload_enabled

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
        'upload_enabled': upload_enabled,
        'remaining': max(0, cooldown - int(time.time() - request.session.get("last_upload_ts", 0))),
    })

def slideshow_view(request):
    config = AppConfig.objects.first()
    images = UploadedImage.objects.filter(approved=True)

    if config and config.slideshow_random:
        images = list(images)
        random.shuffle(images)
    else:
        images = images.order_by('uploaded_at')

    return render(request, 'gallery/slideshow.html', {
        'images': images,
        'speed': config.slideshow_speed if config else 10,
        'cooldown': config.upload_cooldown if config else 30,
    })

def slideshow_data(request):
    config = AppConfig.objects.first()
    qs = UploadedImage.objects.filter(approved=True)

    if config and config.slideshow_random:
        qs = list(qs)
        random.shuffle(qs)
    else:
        qs = qs.order_by('uploaded_at')

    urls = [request.build_absolute_uri(img.image.url) for img in qs]
    return JsonResponse({
        'urls': urls,
        'speed': config.slideshow_speed if config else 10,
        'cooldown': config.upload_cooldown if config else 30
    })


@login_required
def settings_view(request):
    config, _ = AppConfig.objects.get_or_create(id=1)

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

        elif request.POST.get('action') == 'save_config':
            try:
                config.slideshow_speed = int(request.POST.get('speed', config.slideshow_speed))
                config.upload_cooldown = int(request.POST.get('cooldown', config.upload_cooldown))
                config.camera_cooldown = int(request.POST.get('camera_cooldown', config.camera_cooldown))
                config.upload_enabled = 'upload_enabled' in request.POST
                config.slideshow_random = 'slideshow_random' in request.POST
                config.save()
                messages.success(request, "Einstellungen gespeichert.")
            except (ValueError, TypeError):
                messages.error(request, "Ungültige Eingaben.")
            return redirect('settings')

    return render(request, 'gallery/settings.html', {
        'images': UploadedImage.objects.all().order_by('uploaded_at'),
        'speed': config.slideshow_speed,
        'cooldown': config.upload_cooldown,
        'camera_cooldown': config.camera_cooldown,
        'upload_enabled': config.upload_enabled,
        'slideshow_random': config.slideshow_random,
    })


def menu_view(request):
    return render(request, 'gallery/menu.html')