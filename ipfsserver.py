#!/usr/bin/python3
'''
Implement simple IPFS server
'''
import sys, os, http.server
from http import HTTPStatus
from io import BytesIO

class IPFSRequestHandler(http.server.SimpleHTTPRequestHandler):
    '''
    Extend request handler to fetch IPFS documents
    '''
    def __init__(self, *args, **kwargs):
        '''
        Initialize class
        '''
        super(IPFSRequestHandler, self).__init__(*args, **kwargs)

    def do_GET(self, head_only=False):
        '''
        Fetch file before continuing
        '''
        path = self.translate_path(self.path)
        self.send_response(HTTPStatus.OK)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        if not head_only:
            outfile = BytesIO(path.encode())
            try:
                self.copyfile(outfile, self.wfile)
            finally:
                outfile.close()

    def do_HEAD(self):
        '''
        Handle HEAD request
        '''
        return do_GET(self, head_only=True)

if __name__ == '__main__':
    http.server.test(HandlerClass=IPFSRequestHandler, port=8088)
