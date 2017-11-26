from json import JSONDecodeError
from japronto import Application


GET = 'GET'
"""HTTP get method name constant."""
POST = 'POST'
"""HTTP post method name constant."""
PUT = 'PUT'
"""HTTP put method name constant."""
DELETE = 'DELETE'
"""HTTP delete method name constant."""

BAD_REQUEST = 400
"""HTTP response code for the 'bad request reason constant.'"""
INTERNAL_ERROR = 500
"""HTTP response code for the 'internal error' reason constant."""


class ServiceLayer(object):
    """A facade of a service layer.

    Runs an HTTP server on a specified address and handles incoming requests.
    When an expected request arrives, it calls a previously specified method.
    If method returns something, ServiceLayer sends it as a response to the request.
    Otherwise, ServiceLayer responds with a plain 200 OK.
    If an expected error occurs during a method call, ServiceLayer responds with a predefined
    response code, that corresponds to the type of error.

    Attributes:
        __host (str): Host to listen to incoming requests to.
        __port (int): Port to listen to incoming requests to.
        __application (Application): HTTP server.

    """
    def __init__(self, host, port):
        """Constructor of the ServiceLayer.

        Args:
            host (str): Host to listen to incoming requests to.
            port (int): Port to listen to incoming requests to.

        """
        self.__host = host or '0.0.0.0'
        self.__port = port or 5000
        self.__application = Application()
        self.map_business_error(TypeError, 402)

    def map_business_error(self, error, code):
        """Respond with the specified error code each time, the specified error occurs while processing a request.

        Args:
            error (type): Type of the error.
            code (int): Response code.

        """
        def handle(request, exception):
            return request.Response(code=code, text=str(exception))
        self.__application.add_error_handler(error, handle)

    def map_business_process(self, method, url, business_process):
        """Call a specified method, each time a request with the specified method and url arrives. Use a return value
        of the method as a response data. If specified method returns None, server will respond with a plain 200 OK.

        Args:
            method (str): HTTP method name.
            url (str): URL of the incoming request.
            business_process (method): Method to call, when request arrives.

        """
        async def handle(request):
            arguments = request.match_dict or {}
            try:
                if request.json is not None:
                    arguments.update(request.json)
            except JSONDecodeError:
                pass
            result = await business_process(**arguments)
            return request.Response(json=result) \
                if result is not None \
                else request.Response()
        self.__application.router.add_route(url, handle, method=method)

    def run(self):
        """Run the HTTP server."""
        self.__application.run(host=self.__host, port=self.__port)
