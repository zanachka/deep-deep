# -*- coding: utf-8 -*-
import logging

from formasaurus.utils import get_domain
from scrapy.exceptions import IgnoreRequest

logger = logging.getLogger(__name__)


offdomain_request_dropped = object()


class OffsiteDownloaderMiddleware:
    """
    This middleware filters out requests if they are not to the same domain
    as specified in request.meta['domain'].
    """
    def __init__(self, signals):
        self.signals = signals

    def process_request(self, request, spider):
        if not request.meta.get('domain'):
            return

        domain = request.meta['domain']
        if get_domain(request.url) != domain:
            logger.info("Dropped request {}: it doesn't belong to {}".format(
                request, domain
            ))
            self.signals.send_catch_log(offdomain_request_dropped,
                                        request=request)
            raise IgnoreRequest()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.signals)