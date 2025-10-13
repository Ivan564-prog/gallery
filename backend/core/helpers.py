from django.core.paginator import Paginator
from django.utils.html import strip_tags
from django.core import mail
from apps.task_manager.decorators import task


@task
def send_mail(subject, to, message):
    plain_message = strip_tags(message)
    from_email = None
    mail.send_mail(
        subject, plain_message, from_email,
        to, html_message=message)


def get_host(request):
    return f"{request.scheme}://{request.META['HTTP_HOST']}"


def get_pagination_page(request, queryset, serializer_class, paginate_by=15):
    page = int(request.GET.get('page', '1'))
    pagin = int(request.GET.get('pagin', paginate_by))
    paginator = Paginator(queryset, pagin)
    page_obj = paginator.get_page(page)

    return {
        'items': serializer_class(page_obj, many=True, context={'request': request}).data,
        'item_count': queryset.count(),
        'num_pages': paginator.num_pages,
        'page': page,
        'has_next': page_obj.has_next(),
        'has_prev': page_obj.has_previous(),
    }