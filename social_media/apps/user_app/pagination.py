from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination

class CustomPageNumberPagination(PageNumberPagination):
    page_size = 10  # Default number of items per page
    page_size_query_param = 'page_size'  # Allow clients to specify page size via query parameter
    # max_page_size = 100  # Maximum number of items per page


class LOPagination(LimitOffsetPagination):
    default_limit = 10