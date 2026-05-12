from typing import Any, TypeAlias

ResponseDict: TypeAlias = dict[int | str, dict[str, Any]]

COMMON_200_401_RESPONSES: ResponseDict = {
    200: {"description": "Success"},
    401: {"description": "Unauthorized"},
}

COMMON_201_401_RESPONSES: ResponseDict = {
    201: {"description": "Created"},
    401: {"description": "Unauthorized"},
}

COMMON_204_401_RESPONSES: ResponseDict = {
    204: {"description": "No Content"},
    401: {"description": "Unauthorized"},
}

COMMON_200_401_404_RESPONSES: ResponseDict = {
    **COMMON_200_401_RESPONSES,
    404: {"description": "Not Found"},
}

COMMON_204_401_404_RESPONSES: ResponseDict = {
    **COMMON_204_401_RESPONSES,
    404: {"description": "Not Found"},
}

COMMON_422_RESPONSES: ResponseDict = {
    422: {"description": "Validation Error"},
}