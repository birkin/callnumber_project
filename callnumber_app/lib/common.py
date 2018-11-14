import logging, pprint


log = logging.getLogger(__name__)


def make_request_url( request ):
    """ Returns requesting url.
        Called by lib.view_info_helper.make_context() and lib.mapper_helper.prep_code_response() and prep_dump_response() """
    # log.debug( 'request.__dict__, ```%s```' % pprint.pformat(request.__dict__) )
    request_url = '%s://%s%s' % ( request.scheme,
        request.META.get( 'HTTP_HOST', '127.0.0.1' ),  # HTTP_HOST doesn't exist for client-tests
        request.META.get( 'REQUEST_URI', request.META['PATH_INFO'] )
    )
    querystring = request.META.get( 'QUERY_STRING', None )
    if querystring:
        request_url = '%s?%s' % ( request_url, querystring )
    log.debug( 'request_url, ```%s```' % request_url )
    return request_url
