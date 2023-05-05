import math

class Paginator:
    def __init__(self, queryset, request, page_ranged=True):
        self.queryset = queryset
        self.request = request
        self.page_ranged = page_ranged

    def paginate(self, page=1, limit=10, span=2, serializer=None):
        request = self.request
        request_data = None
        if request.method == 'GET':
            request_data = request.GET
        else:
            request_data = request.data
    
        page = int(request_data.get('pageNumber', 1))
        limit = int(request_data.get('pageSize', 10))
        span = int(span)

        offset = (page - 1) * limit

        count = len(self.queryset)

        try:
            page_count = math.ceil(count / limit)
        except:
            page_count = 1

        has_next = page < page_count
        has_prev = page > 1

        record_from = offset + 1
        record_to = offset + limit if offset + limit <= count else count

        if self.page_ranged:
            max_range = page + span if page + span <= page_count else page_count
            min_range = page - span if page - span >= 1 else 1

            pages = range(min_range, max_range + 1)

        else:
            pages = range(1, page_count + 1)

        data_list = self.queryset[offset:offset + limit]
        if serializer:
            data_list = serializer(data_list, many=True).data
        return {
            "limit": limit,
            "recordCount": count,
            "pageCount": page_count,
            "recordFrom": record_from,
            "recordTo": record_to,
            "pages": list(pages),
            "page": page,
            "hasNext": has_next,
            "hasPrev": has_prev,
            "dataList": data_list
        }