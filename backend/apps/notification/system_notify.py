def notify_create_book(book, users=None):
    from .models import Notification
    Notification.create_notification(
        title='Новая книга в библиотеке',
        text=f'<p>Появилась новая книга "{book.title}". Посмотреть ее можно в <a href="/library">библиотеке</a></p>',
        users=users,
    )