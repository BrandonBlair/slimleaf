import requests

from slimleaf.exceptions import SlimleafException


FAILED_RQST_MSG = """Expected a response of {exp}, got {act}\n
                    While trying to: {desc}\n
                    Req URL: {url}\n
                    Req Headers: {hdrs}\n
                    Req Body: {body}\n
                    Response: {resp}"""


def validated_request(method, url, expect, desc='', session=None, timeout=30, *args, **kwargs):
    """Performs HTTP request and validates the response against an expected status code. Shrinks
    test code and provides actionable, readable Exceptions when things do not go as
    expected.

    Args:
        session (requests.Session): A session, presumably headers are already in desired state
        method (str): GET, POST, PUT, DELETE, etc.
        url (str): Request URL
        expect (int): Expected status code
        desc (str): Description of what request is attempting to accomplish, e.g. 'Retrieve some data'
        args: Passed through to Request
        kwargs: Passed through to Request

    Returns:
        resp (requests.Response)

    """
    session = session or requests.Session()
    try:
        resp = session.request(method, url, *args, timeout=timeout, verify=False, **kwargs)

    except ConnectTimeout as conn_tout:
        raise SlimleafException(f'Connection to {url} timed out. Exception: {conn_tout}')

    except ConnectionError as conn_err:
        raise SlimleafException(
            f'Connection to {url} was refused. Is it available? Exception: {conn_err}'
        )

    if resp.status_code != expect:
        raise SlimleafException(
            FAILED_RQST_MSG.format(
                exp=expect,
                act=resp.status_code,
                desc=desc,
                url=url,
                hdrs=session.headers,
                body=resp.request.body,
                resp=resp.text[:500]
            )
        )
    return resp
