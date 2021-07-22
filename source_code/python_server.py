# -*- coding: utf-8 -*-
"""
Created on Thu May 21 17:42:33 2020
@author: Nommie, James
"""

# Note: This server is set to localhost (see demo). 

from http.server import HTTPServer, BaseHTTPRequestHandler
from io import BytesIO
from urllib.parse import urlparse, parse_qs
import os
import random


ip = "localhost"
port = 8000
random.seed(123456)


class responses(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Hello, world!')

    def do_POST(self):
        if "/uploadresponse" in self.path:
                params = parse_qs(urlparse(self.path).query)
                response = BytesIO()

                if len(params) == 3:
                    content_length = int(self.headers['Content-Length'])
                    body = self.rfile.read(content_length)
                    self.send_response(200)
                    self.end_headers()
                    
                    print(params)
                    # Getting the data info
                    title = params['title'][0]
                    path = params['path'][0]
                    filetype = params['filetype'][0]
                    client_ip = self.client_address[0]
                    
                    # try to create the nested directory
                    try:
                        os.makedirs(path + "_" + str(client_ip))
                        if filetype == 'psydat' or filetype == 'csv':
                            f = open(path + "_" + str(client_ip) + "/" + title + "." + filetype, "wb")
                            f.write(body)
                        else: 
                            f = open(path + "_" + str(client_ip) + "/" + title + "." + filetype, "w")
                            f.write(body.decode('utf-8'))
                        
                        response.write(b'Received post. Successfully written file')
                        self.wfile.write(response.getvalue())
                    except OSError: # if the directory already exists
                        try: # try to write to the existing directory
                            if filetype == 'psydat' or filetype == 'csv':
                                f = open(path + "_" + str(client_ip) + "/" + title + "." + filetype, "wb")
                                f.write(body)
                            else: 
                                f = open(path + "_" + str(client_ip) + "/" + title + "." + filetype, "w")
                                f.write(body.decode('utf-8'))
                        
                            response.write(b'Received post. Successfully written file')
                            self.wfile.write(response.getvalue())
                        except OSError:
                            response.write(b'Unable to write file.')
                            self.wfile.write(response.getvalue())
                            pass
                else: 
                    response.write(b'Invalid POST')
                    self.wfile.write(response.getvalue())  
        else:
            self.send_response(200)
            self.end_headers()


httpd = HTTPServer((ip, port), responses)
print("Server server at port " + str(port))
httpd.serve_forever()