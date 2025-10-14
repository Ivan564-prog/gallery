from django.core.management import BaseCommand
from apps.content.models import SeoText, Content
from apps.page.models import Page


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        heading = Page.objects.get(title='Новости')
        post_name = 'Мой пост'
        text = '<h1>Текст</h1>'
        post = Page.objects.get_or_create(title=post_name, parent=heading)
        content = Content.objects.get_or_create(title=post_name)
        block = SeoText.objects.create(text=text)
        content.stream.add(block)
        content.save()
        post.content = content
        post.save()