# apps/produccion/pagination.py
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class CustomPagination(PageNumberPagination):
    page_size_query_param = 'pageSize'

    def get_paginated_response(self, data):
        return Response({
            "data": {
                "results": data,
                "pageNumber": self.page.number,
                "pageSize": self.get_page_size(self.request),
                "totalCount": self.page.paginator.count,
                "totalPages": self.page.paginator.num_pages
            }
        })
