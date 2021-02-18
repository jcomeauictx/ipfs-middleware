#!/usr/bin/python3
'''
Implement simple IPFS server
'''
import sys, os, subprocess, logging, posixpath, http.server
from http import HTTPStatus
from io import BytesIO

logging.basicConfig(level=logging.DEBUG if __debug__ else logging.INFO)

CACHE = os.path.expanduser('~/.ipfsserver/cache')

class IPFSRequestHandler(http.server.SimpleHTTPRequestHandler):
    '''
    Extend request handler to fetch IPFS documents
    '''
    def __init__(self, *args, **kwargs):
        '''
        Initialize class
        '''
        os.makedirs(CACHE, exist_ok=True)
        kwargs['directory'] = CACHE
        super().__init__(*args, **kwargs)

    def do_GET(self, head_only=False):
        '''
        Fetch file before continuing
        '''
        path = self.path.lstrip(posixpath.sep)
        fullpath = os.path.join(CACHE, path)
        dirname, filename = posixpath.split(fullpath)
        if not os.path.exists(path):
            os.makedirs(dirname, exist_ok=True)
            logging.info('fetching %s', path)
            subprocess.run([
                'ipfs',
                'get',
                '--output={dirname}'.format(dirname=dirname),
                path,
            ])
        if head_only:
            super().do_HEAD()
        else:
            super().do_GET()

    def do_HEAD(self):
        '''
        Handle HEAD request
        '''
        do_GET(self, head_only=True)

if __name__ == '__main__':
    http.server.test(
        HandlerClass=IPFSRequestHandler,
        port=8088)
