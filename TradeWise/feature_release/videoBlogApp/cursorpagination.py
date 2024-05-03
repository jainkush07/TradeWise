from rest_framework.pagination import CursorPagination

class MyCursorPagination(CursorPagination):
    page_size = 1
    ordering = '-id'