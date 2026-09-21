from unittest.mock import patch
from django.test import TestCase, Client
from django.urls import reverse
from generator.models import ImageGeneration
from generator.forms import ImageGenerationForm


class GeneratorTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.sample_gen = ImageGeneration.objects.create(
            prompt="A futuristic city floating above the clouds during sunset",
            style="Realistic",
            aspect_ratio="1:1",
            image_url="/media/generations/test_sample.jpg"
        )

    def test_home_page_status_and_template(self):
        """Test home page renders successfully with empty state."""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'generator/home.html')
        self.assertContains(response, 'Create anything with AI')
        self.assertContains(response, 'Describe your image')
        self.assertContains(response, 'Your creation will appear here')

    def test_form_valid_data(self):
        """Test ImageGenerationForm with valid prompt, style and aspect ratio."""
        form = ImageGenerationForm(data={
            'prompt': 'A cyberpunk samurai standing in neon rain',
            'style': 'Cinematic',
            'aspect_ratio': '16:9',
        })
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['prompt'], 'A cyberpunk samurai standing in neon rain')

    def test_form_empty_prompt(self):
        """Test ImageGenerationForm rejects empty or whitespace-only prompt."""
        form = ImageGenerationForm(data={
            'prompt': '   ',
            'style': 'Anime',
            'aspect_ratio': '1:1',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('prompt', form.errors)
        self.assertIn('Please enter an image description.', form.errors['prompt'])

    def test_form_prompt_too_long(self):
        """Test ImageGenerationForm rejects prompts exceeding 1000 characters."""
        long_prompt = 'A' * 1005
        form = ImageGenerationForm(data={
            'prompt': long_prompt,
            'style': 'Realistic',
            'aspect_ratio': '1:1',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('prompt', form.errors)

    def test_form_invalid_style(self):
        """Test ImageGenerationForm rejects unknown style choice."""
        form = ImageGenerationForm(data={
            'prompt': 'A mystical forest',
            'style': 'InvalidStyle',
            'aspect_ratio': '1:1',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('style', form.errors)

    def test_form_invalid_aspect_ratio(self):
        """Test ImageGenerationForm rejects unknown aspect ratio."""
        form = ImageGenerationForm(data={
            'prompt': 'A mystical forest',
            'style': 'Fantasy',
            'aspect_ratio': '99:99',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('aspect_ratio', form.errors)

    @patch('generator.views.generate_image')
    def test_generate_post_success(self, mock_generate):
        """Test successful generation creates record and renders result page."""
        mock_generate.return_value = "/media/generations/test_created.jpg"

        response = self.client.post(reverse('generate'), {
            'prompt': 'A magical dragon soaring over mountain peaks',
            'style': 'Fantasy',
            'aspect_ratio': '16:9',
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'generator/result.html')
        self.assertContains(response, 'Your Creation')
        self.assertContains(response, 'A magical dragon soaring over mountain peaks')
        self.assertContains(response, 'Fantasy')

        # Verify database insertion
        created = ImageGeneration.objects.filter(prompt='A magical dragon soaring over mountain peaks').first()
        self.assertIsNotNone(created)
        self.assertEqual(created.image_url, "/media/generations/test_created.jpg")

    @patch('generator.views.generate_image')
    def test_generate_post_ai_service_failure(self, mock_generate):
        """Test graceful error handling when external AI service fails."""
        mock_generate.side_effect = RuntimeError("The AI image service is temporarily unavailable. Please try again.")

        response = self.client.post(reverse('generate'), {
            'prompt': 'A peaceful zen garden in autumn',
            'style': 'Realistic',
            'aspect_ratio': '1:1',
        })

        self.assertEqual(response.status_code, 502)
        self.assertTemplateUsed(response, 'generator/home.html')
        self.assertContains(response, 'The AI image service is temporarily unavailable.', status_code=502)

    def test_history_page(self):
        """Test history page lists saved generations with metadata."""
        response = self.client.get(reverse('history'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'generator/history.html')
        self.assertContains(response, 'Your Generations')
        self.assertContains(response, self.sample_gen.prompt)
        self.assertContains(response, self.sample_gen.style)

    def test_detail_page(self):
        """Test generation detail page displays full details."""
        response = self.client.get(reverse('detail', args=[self.sample_gen.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'generator/detail.html')
        self.assertContains(response, self.sample_gen.prompt)
        self.assertContains(response, self.sample_gen.style)
        self.assertContains(response, self.sample_gen.aspect_ratio)

    def test_detail_page_404(self):
        """Test generation detail page returns 404 for non-existent ID."""
        response = self.client.get(reverse('detail', args=[99999]))
        self.assertEqual(response.status_code, 404)

    def test_delete_generation(self):
        """Test generation deletion redirects to history and deletes record from database."""
        gen_id = self.sample_gen.id
        response = self.client.post(reverse('delete', args=[gen_id]))
        self.assertRedirects(response, reverse('history'))

        # Verify deletion from database
        self.assertFalse(ImageGeneration.objects.filter(id=gen_id).exists())
