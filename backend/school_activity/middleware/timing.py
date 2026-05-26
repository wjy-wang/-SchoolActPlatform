import time
import logging
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger('school_activity')

class ResponseTimeMiddleware(MiddlewareMixin):
    """记录API响应时间的中间件"""
    
    def process_request(self, request):
        request.start_time = time.time()
    
    def process_response(self, request, response):
        if hasattr(request, 'start_time'):
            duration = time.time() - request.start_time
            duration_ms = int(duration * 1000)
            
            log_level = logging.WARNING if duration_ms > 2000 else logging.INFO
            
            logger.log(
                log_level,
                f"API响应时间 | {request.method} {request.path} | {duration_ms}ms | {response.status_code}",
                extra={
                    'method': request.method,
                    'path': request.path,
                    'duration_ms': duration_ms,
                    'status_code': response.status_code,
                    'query_params': dict(request.GET),
                }
            )
            
            response['X-Response-Time'] = f"{duration_ms}ms"
        
        return response