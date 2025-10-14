from django.db import models
from apps.library.models import Book


class BookWishlist(models.Model):

    user = models.ForeignKey(
        'users.User', verbose_name='Пользователь', related_name='wishlist', on_delete=models.CASCADE)
    books = models.ManyToManyField(
        'library.Book', verbose_name='Книги', blank=True)

    class Meta:

        verbose_name = 'Список понравившихся книг'
        verbose_name_plural = 'Списоки понравившихся книг'

    def __str__(self):
        return f'Список понравившихся книг {self.user.email}'
    
    def toggle_book(self, book_id):
        if self.books.filter(id=book_id).exists():
            self.books.set(self.books.exclude(pk=book_id))
            return False
        else:
            self.books.add(Book.objects.get(pk=book_id))
            return True
    
    def get_book_ids(self):
        return self.books.values_list('id', flat=True)