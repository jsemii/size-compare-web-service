import json     # 딕셔너리를 JSON 글자로 바꾸는 도구
import logging  # 로그 찍는 파이썬 기본 도구
import time     # 시간 재는 도구(스톱워치)
import uuid     # 겹치지 않는 번호 만드는 도구

from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger("app")


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        request_id = str(uuid.uuid4())[:8]
        start = time.perf_counter()
        status_code = 500

        try:
            response = await call_next(request)
            status_code = response.status_code
            return response
        finally:
            duration_ms = round((time.perf_counter() - start) * 1000, 2)
            log = {
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "status_code": status_code,
                "duration_ms": duration_ms,
            }
            logger.info(json.dumps(log, ensure_ascii=False))

