from django.db import models

class ImageGeneration(models.Model):
    prompt = models.CharField(max_length=1000)
    style = models.CharField(max_length=50)
    aspect_ratio = models.CharField(max_length=20)
    image_url = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Image Generation'
        verbose_name_plural = 'Image Generations'

    def __str__(self):
        return f"{self.prompt[:35]}... ({self.style}, {self.aspect_ratio})"
