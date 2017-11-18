from json import JSONDecodeError
from japronto import Application


GET = 'GET'
POST = 'POST'
PUT = 'PUT'
DELETE = 'DELETE'

BAD_REQUEST = 400
INTERNAL_ERROR = 500


class ServiceLayer(object):

    def __init__(self, host, port):
        self.__host = host or '0.0.0.0'
        self.__port = port or 5000
        self.__application = Application()
        self.map_business_error(TypeError, 402)

    def map_business_error(self, error, code):
        def handle(request, exception):
            return request.Response(code=code, text=str(exception))
        self.__application.add_error_handler(error, handle)

    def map_business_process(self, method, url, business_process):
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
        self.__application.run(host=self.__host, port=self.__port)
