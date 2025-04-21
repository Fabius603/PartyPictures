from django.db import models

class UploadedImage(models.Model):
    image = models.ImageField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=True)

    def __str__(self):
        return f"Bild {self.id} – hochgeladen am {self.uploaded_at}"

class AppConfig(models.Model):
    slideshow_speed = models.PositiveIntegerField(default=5)        # Sekunden
    upload_cooldown = models.PositiveIntegerField(default=10)        # Sekunden für Upload erneut
    camera_cooldown = models.PositiveIntegerField(default=10)        # Sekunden für Bildupload timeout
    upload_enabled = models.BooleanField(default=True)               # Upload erlaubt?
    slideshow_random = models.BooleanField(default=False)            # Bilder zufällig?

    def __str__(self):
        return "App-Konfiguration"

    class Meta:
        verbose_name = "Konfiguration"
        verbose_name_plural = "Konfigurationen"