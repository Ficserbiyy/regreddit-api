
from exceptions import ValidationError


def validate_query_pagination(
    filters,
):
    if filters.page < 1:
        raise ValidationError("page must be at least 1.")
    if not 1 <= filters.limit <= 100:
        raise ValidationError("limit must be between 1 and 100.")