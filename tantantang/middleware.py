import logging

from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

from tantantang.exceptions import (
    BusinessException
)
from tantantang.models import HttpResult

logger = logging.getLogger(__name__)


class GlobalExceptionMiddleware(MiddlewareMixin):
    """
    全局异常处理中间件
    """

    def process_exception(self, request, exception):
        """
        处理未捕获的异常
        """
        # 记录异常日志
        logger.error(f"全局异常处理: {str(exception)}", exc_info=True)
        # 根据不同异常类型返回不同的错误信息
        if isinstance(exception, BusinessException):
            return JsonResponse(
                HttpResult.error(str(exception)).to_dict(),
                status=500
            )
        else:
            # 默认的服务器内部错误
            return JsonResponse(
                HttpResult.error("服务器内部错误").to_dict(),
                status=500
            )