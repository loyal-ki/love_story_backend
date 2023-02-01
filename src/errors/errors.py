
# Base app error extend Exeption
class AppError(Exception):

    # HTTP response status codes
    status_code = 500

    # HTTP type error
    error_type = "AppError"

    # app error
    error_code = 0

    # error message
    message: str = ""

    # error description (custom = str | dict | None)
    description: str | dict | None = None

    # init
    def __init__(
        self,
        description: str | None = None
    ):
        self.description = description


# Bad request (400)
class InvalidParameterError(AppError):
    """
    400 ERROR: Invalid Parameter (Bad request)
    """
    status_code = 400
    error_type = "InvalidParameterError"
    error_code = 400
    message = "Sending requests with malformed request syntax, invalid request message framing, or deceptive request routing"


# Bad request (401)
class UnauthorizedError(AppError):
    """
    401 ERROR: UnauthorizedError
    """
    status_code = 401
    error_type = "UnauthorizedError"
    error_code = 401
    message = "Access token data is invalid"


# OTP blocked with user_id (403)
class OTPBlockedWithUserId(AppError):
    """
    401 ERROR: This OTP is blocked in a few minutes.
    """
    status_code = 403
    error_type = "OTPBlockedWithUserId"
    error_code = 403
    message = "This OTP is blocked in 5 minutes."


# OTP blocked with user_id (403)
class OTPCodeHasExpired(AppError):
    """
    401 ERROR: This OTP code has expired.
    """
    status_code = 403
    error_type = "OTPCodeHasExpired"
    error_code = 403
    message = "This OTP code has expired, please request otp again!"

# OTP blocked with user_id (403)
class OTPCodeIsAlreadyUsed(AppError):
    """
    401 ERROR: This OTP code is already used.
    """
    status_code = 403
    error_type = "OTPCodeIsAlreadyUsed"
    error_code = 403
    message = "This OTP code is already used, please request otp again!"


# Not found (404)
class NotSupportedError(AppError):
    """
    404 ERROR: Unsupported Request
    """
    status_code = 404
    error_type = "NotSupportedError"
    error_code = 404
    message = "Server cannot find the requested resource"

    def __init__(self, method: str | None = None, url: str | None = None):
        description = None
        if method and url:
            description = 'method: %s, url: %s' % (method, url)
        super().__init__(description=description)


# Data conflict (409)
class DataConflictError(AppError):
    """
    409 ERROR: Data is conflicted
    """
    status_code = 409
    error_type = "DataConflictError"
    error_code = 409
    message = "Uploading a file that is older than the existing one on the server, resulting in a version control conflict."


# Data conflict (409)
class UserDataConflict(AppError):
    """
    409 ERROR: User data is conflicted
    """
    status_code = 409
    error_type = "UserDataConflict"
    error_code = 409
    message = "User is registered on the server."


# Service unavailable (500)
class InternalServerError(AppError):
    """
    503 ERROR: Internal server error
    """
    status_code = 500
    error_type = "InternalServerError"
    error_code = 500
    message = "Server encountered an unexpected condition that prevented it from fulfilling the request."


# Service unavailable (503)
class ServiceUnavailable(AppError):
    """
    503 ERROR: Service is temporarily unavailable
    """
    status_code = 503
    error_type = "ServiceUnavailable"
    error_code = 503
    message = "Service Unavailable"
