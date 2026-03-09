"""Custom Scrapy middlewares."""
import logging

logger = logging.getLogger(__name__)


class RetryOnRateLimitMiddleware:
    """Retry requests that receive HTTP 429 (rate limit) responses."""

    def process_response(self, request, response, spider):
        if response.status == 429:
            logger.warning(f"Rate limited on {request.url}, will retry")
            from scrapy.downloadermiddlewares.retry import get_retry_request

            retried = get_retry_request(request, spider=spider, reason="rate_limit")
            if retried:
                return retried
        return response
