import gevent
import gevent.monkey
gevent.monkey.patch_socket()
import requests
import urllib
import urllib.parse

import pprint as pp
import pandas as pd
import time

# GLOBALS


def fetch(url, verbose=False):
    """Simple function to return response from requests.get(url), as json if valid"""

    resp = requests.get(url)
    if verbose:
        print(resp.json())
    if resp.status_code == 200:

        resp=resp.json()
        return resp
    else:
        return None



def asynchronous(urls, batch_size, delay=0, verbose=False):
    """wrapper to make async calls using gevent, concurrent not parallel"""
    try:
        count=1
        threads=[]
        print(urls.strip(' ').split(","))
        for url in urls.strip(" '").split(","):
            print('On batch {}'.format(count))
            threads.append(gevent.spawn(fetch, url, verbose))
        responses = gevent.joinall(threads)
        time.sleep(delay)
        return responses
    except Exception as e:
        print(e)
        return None

        
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("URL_STRINGS", help="comma separated set of urls to pass into: requests.get(). i.e. -> 'google.com, yahoo.com' ")
    parser.add_argument("BATCH_SIZE", help="batch size for async cals made to url", type=int)
    parser.add_argument("DELAY", help="delay between batches, defaults to 0 seconds", type=int)
    parser.add_argument("OUTPUT_FILE", help="output to filename (returns newline separated text file)")
    parser.add_argument("-v", "--verbose", action="store_true",
                    help="increase output verbosity, print responses as they are called")
    args = parser.parse_args()
    verbose=False
    if args.verbose:
        print('Verbose mode on')
        verbose = True
    responses = asynchronous(args.URL_STRINGS, args.BATCH_SIZE, args.DELAY, args.verbose)
    if responses:
        fn = str(args.OUTPUT_FILE) + '.txt'
        print(fn)
        with open(fn.strip("'"), 'w') as f:
            _ = [f.write(str(resp.value) + '\n') for resp in responses]
            print('File Outputted to {}'.format(fn))
    else:
        print("Nothing returned")
