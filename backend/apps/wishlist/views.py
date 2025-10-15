from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from apps.library.serializers import BookListSerializer
from .models import BookWishlist, DiaryWishlist


class BookWishlist(ViewSet):
    queryset = BookWishlist.objects.all()
    permissions = [IsAuthenticated,]

    # def list(self, request):
    #     return Response(BookListSerializer(
    #         request.user.get_book_wishlist().books.exclude(status='deleted'), many=True, context={'request': request}).data)
    
    def create(self, request):
        book_id = request.data.get('book_id')
        return Response(
            request.user.get_book_wishlist().toggle_book(int(book_id)), status=HTTP_200_OK)
    
    # @action(detail=False)
    # def get_ids(self, request):
    #     return Response(request.user.get_book_wishlist().get_book_ids())


class DiaryWishlist(ViewSet):
    queryset = DiaryWishlist.objects.all()
    permissions = [IsAuthenticated,]
    
    def create(self, request):
        diary_id = request.data.get('diary_id')
        return Response(
            request.user.get_diary_wishlist().toggle_diary(int(diary_id)), status=HTTP_200_OK)