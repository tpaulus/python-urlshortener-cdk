import json
import logging

from shortner import AbstractShortener, Shortener2

LOG = logging.getLogger()
LOG.setLevel(logging.INFO)


def main(event, context):
    LOG.info("EVENT: " + json.dumps(event))

    query_string_params = event["queryStringParameters"]
    if query_string_params is not None:
        target_url = query_string_params['targetUrl']
        if target_url is not None:
            return create_short_url(event)

    path_parameters = event['pathParameters']
    if path_parameters is not None:
        if path_parameters['proxy'] is not None:
            return read_short_url(event)

    return {
        'statusCode': 200,
        'body': 'usage: ?targetUrl=URL'
    }


def create_short_url(event):
    shortener: AbstractShortener = Shortener2()

    # Parse targetUrl
    target_url = event["queryStringParameters"]['targetUrl']

    slug = shortener.shorten(target_url)

    # Create the redirect URL
    url = "https://" \
          + event["requestContext"]["domainName"] \
          + event["requestContext"]["path"] \
          + slug

    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'text/plain'},
        'body': f"Created URL: {url}"
    }


def read_short_url(event):
    shortener: AbstractShortener = Shortener2()

    # Parse redirect ID from path
    slug = event['pathParameters']['proxy']

    # noinspection PyBroadException
    try:
        long_url = shortener.expand(slug)

        if not long_url.startswith("http"):
            long_url = "https://" + long_url

        return {
            'statusCode': 301,
            'headers': {
                'Location': long_url
            }
        }
    except KeyError:
        return {
            'statusCode': 400,
            'headers': {'Content-Type': 'text/plain'},
            'body': f'No redirect found for {slug}'
        }
    except Exception:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'text/plain'},
            'body': 'Something went wrong!'
        }
