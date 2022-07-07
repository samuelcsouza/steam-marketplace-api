from fastapi import HTTPException


def raise_error_response(error, detail=None) -> Exception:
    """
    Throws an HTTPException with appropriate status code and detail.
    """

    error_body = dict(error.error)

    if detail is not None:
        error_body["detail"] = detail

    raise HTTPException(
        status_code=error.status_code,
        detail=error_body
    )


class BusinessException(Exception):
    pass


class ErrorResourceInvalid(BusinessException):

    status_code = 400

    error = {
        "type": "Resource Invalid!",
        "detail": "The requested resource is invalid."
    }


class ErrorResourceNotFound(BusinessException):

    status_code = 404

    error = {
        "type": "Resource not found!",
        "detail": "The requested resource does not exists."
    }


class ErrorInvalidParameters(BusinessException):

    status_code = 400

    error = {
        "type": "Invalid parameters!",
        "detail": "The parameters provided are invalid."
    }


class ErrorRouteNotFound(BusinessException):
    status_code = 404

    error = {
        "type": "Route not found!",
        "description": "The requested route does not exist.",
    }


class ErrorMethodNotAllowed(BusinessException):
    status_code = 405

    error = {
        "type": "Method not allowed!",
        "description": "The requested resource does not allow this action.",
    }


class ErrorInternal(BusinessException):
    status_code = 500

    error = {
        "type": "Interal error!",
        "description": "An internal API error has occurred."
    }
