from rest_framework_simplejwt.tokens import RefreshToken
import random
import string
from drf_spectacular.utils import OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from django.db.models import Q
import operator
from functools import partial, reduce, update_wrapper


PAGINATED_PARAMETERS = [
    OpenApiParameter(
        name="pageNumber",
        location=OpenApiParameter.QUERY,
        description="Page number of the list.",
        type=OpenApiTypes.NUMBER,
        default=1,
        required=True,
    ), 
    OpenApiParameter(
        name="pageSize",
        location=OpenApiParameter.QUERY,
        description="Page size of the list.",
        type=OpenApiTypes.NUMBER,
        default=10,
        required=True,
    )
]


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user) 
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


def id_generator(size=25, chars=string.ascii_lowercase + string.digits):
    """
    Generate random string
    """
    return ''.join(random.choice(chars) for _ in range(size))


def search_result(queryset, search, orm_lookups, search_max=10, limit_data=True):
    
    for bit in search.split():
        or_queries = [Q(**{orm_lookup: bit})
                    for orm_lookup in orm_lookups]
        queryset = queryset.filter(reduce(operator.or_, or_queries))
    if limit_data:
        return queryset[0:search_max]
    else:
        return queryset