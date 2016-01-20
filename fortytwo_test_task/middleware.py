from apps.hello.models import StorageRequests


class ProcessMiddleware:
    '''
      This is class save in model request store in model
    '''
    def process_request(self, request):
        '''
           Object for HttpRequest
        '''
        rqst = StorageRequests()
        rqst.host = request.get_host()
        rqst.path = request.get_full_path()
        rqst.method = request.method
        rqst.save()
