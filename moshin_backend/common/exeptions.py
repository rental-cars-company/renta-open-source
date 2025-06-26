from rest_framework.serializers import ReturnDict
from rest_framework.views import exception_handler


def detailed_exception_handler(exc: Exception, context):
    """message: str
    title: str
    code: str
    traceback: str | None.
    """
    response = exception_handler(exc, context)

    if response is not None and response.data is not None:
        if isinstance(response.data, ReturnDict):
            message = []
            for key, value in response.data.items():
                if isinstance(value, list):
                    items = []
                    for item in value:
                        if isinstance(item, dict):
                            # если словарь — преобразуем в строку ключ:значение
                            items.append(
                                ", ".join(f"{k}: {v}" for k, v in item.items())
                            )
                        else:
                            items.append(str(item))
                    message.append(f"{key} : {', '.join(items)}")
                else:
                    message.append(f"{key} : {str(value)}")
            message = "; ".join(message)
        else:
            message = "; ".join(map(str, response.data))

        response.data = {
            "code": response.status_code,
            "title": exc.__class__.__name__,
            "message": message,
            "traceback": None,
        }
        return response
    return None

    # Если ошибка не была поймана. Internal Server Error
    # return Response(
    #     status=500,
    #     data={
    #         "code": 500,
    #         "title": exc.__class__.__name__,
    #         "message": exc.args[0],
    #         "traceback": "".join(traceback.format_tb(exc.__traceback__)),
    #     },
    # )
