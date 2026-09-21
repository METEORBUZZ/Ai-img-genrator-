import mimetypes
from pathlib import Path
import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.conf import settings
from .models import ImageGeneration
from .forms import ImageGenerationForm
from .services import generate_image


def home_view(request):
    """
    Renders the AI Image Generator homepage.
    Displays the hero, prompt form with style and aspect ratio options,
    and the empty state before generations.
    """
    form = ImageGenerationForm()
    recent_generations = ImageGeneration.objects.all()[:4]
    return render(request, 'generator/home.html', {
        'form': form,
        'recent_generations': recent_generations,
    })


def generate_view(request):
    """
    Handles generation form submission via standard HTTP POST.
    Validates form data, executes AI service generation, saves record to PostgreSQL/ORM,
    and displays the result page.
    """
    if request.method != 'POST':
        return redirect('home')

    form = ImageGenerationForm(request.POST)
    if not form.is_valid():
        return render(request, 'generator/home.html', {
            'form': form,
            'recent_generations': ImageGeneration.objects.all()[:4],
        }, status=400)

    prompt = form.cleaned_data['prompt']
    style = form.cleaned_data['style']
    aspect_ratio = form.cleaned_data['aspect_ratio']

    try:
        image_url = generate_image(prompt, style, aspect_ratio)
        generation = ImageGeneration.objects.create(
            prompt=prompt,
            style=style,
            aspect_ratio=aspect_ratio,
            image_url=image_url
        )
        return render(request, 'generator/result.html', {
            'generation': generation,
            'success_message': 'Image generated successfully!',
        })
    except Exception as exc:
        error_message = str(exc)
        if not error_message or 'Error' in error_message:
            error_message = 'Image generation failed. Please try again with a different prompt.'
        return render(request, 'generator/home.html', {
            'form': form,
            'api_error': error_message,
            'recent_generations': ImageGeneration.objects.all()[:4],
        }, status=502)


def history_view(request):
    """
    Displays the generation history loaded from the persistent database.
    Shows image cards with creation dates, styles, aspect ratios, and action links.
    """
    generations = ImageGeneration.objects.all()
    return render(request, 'generator/history.html', {
        'generations': generations,
        'count': generations.count(),
    })


def detail_view(request, pk):
    """
    Displays a single generation's detail view with large image, full prompt,
    metadata, and action buttons (download, delete, back to history).
    """
    generation = get_object_or_404(ImageGeneration, pk=pk)
    return render(request, 'generator/detail.html', {
        'generation': generation,
    })


def delete_view(request, pk):
    """
    Handles generation deletion via standard HTTP POST with CSRF protection.
    If requested via GET, shows a confirmation card.
    After deletion, redirects cleanly to history.
    """
    generation = get_object_or_404(ImageGeneration, pk=pk)
    if request.method == 'POST':
        generation.delete()
        return redirect('history')

    return render(request, 'generator/detail.html', {
        'generation': generation,
        'confirm_delete': True,
    })


def download_view(request, pk):
    """
    Streams the generated image as a downloadable attachment file.
    Ensures safe, direct browser download without JavaScript.
    """
    generation = get_object_or_404(ImageGeneration, pk=pk)
    image_url = generation.image_url
    filename = f"ai_generation_{generation.id}_{generation.style.lower()}.jpg"

    # If it's a local media file
    if image_url.startswith(settings.MEDIA_URL):
        rel_path = image_url[len(settings.MEDIA_URL):]
        file_path = Path(settings.MEDIA_ROOT) / rel_path
        if file_path.exists():
            with open(file_path, 'rb') as f:
                content = f.read()
            response = HttpResponse(content, content_type='image/jpeg')
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response

    # If it's an external URL, fetch and stream it
    if image_url.startswith('http://') or image_url.startswith('https://'):
        try:
            res = requests.get(image_url, timeout=5)
            if res.status_code == 200:
                content_type = res.headers.get('Content-Type', 'image/jpeg')
                response = HttpResponse(res.content, content_type=content_type)
                response['Content-Disposition'] = f'attachment; filename="{filename}"'
                return response
        except Exception:
            pass

    # Fallback to direct redirect
    return redirect(image_url)
