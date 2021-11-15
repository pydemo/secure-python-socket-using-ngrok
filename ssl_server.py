# -*- coding: latin-1 -*-
#
# Copyright (C) AB Strakt
# Copyright (C) Jean-Paul Calderone
# See LICENSE for details.

"""
Simple echo server, using nonblocking I/O
"""

from OpenSSL import SSL
import sys, os, select, socket


def verify_cb(conn, cert, errnum, depth, ok):
    # This obviously has to be updated
    print ('Got certificate: %s' % cert.get_subject())
    return ok

if len(sys.argv) < 2:
    print ('Usage: python[2] server.py PORT')
    sys.exit(1)

dir = os.path.dirname(sys.argv[0])
if dir == '':
    dir = os.curdir

# Initialize context
ctx = SSL.Context(SSL.SSLv23_METHOD)
ctx.set_options(SSL.OP_NO_SSLv2)
ctx.set_verify(SSL.VERIFY_PEER|SSL.VERIFY_FAIL_IF_NO_PEER_CERT, verify_cb) # Demand a certificate
ctx.use_privatekey_file (os.path.join(dir, 'simple', 'server.pkey'))
ctx.use_certificate_file(os.path.join(dir, 'simple', 'server.cert'))
ctx.load_verify_locations(os.path.join(dir, 'simple', 'CA.cert'))

# Set up server
server = SSL.Connection(ctx, socket.socket(socket.AF_INET, socket.SOCK_STREAM))
server.bind(('', int(sys.argv[1])))
server.listen(3) 
server.setblocking(0)

clients = {}
writers = {}

def dropClient(cli, errors=None):
    if errors:
        print ('Client %s left unexpectedly:' % (clients[cli],))
        print ('  ', errors)
    else:
        print ('Client %s left politely' % (clients[cli],))
    del clients[cli]
    if cli in writers:
        del writers[cli]
    if not errors:
        cli.shutdown()
    cli.close()
from pyngrok import ngrok
port=6063
public_url = ngrok.connect(port, "tcp").public_url
print(f"ngrok tunnel '{public_url}' -> 'tcp://127.0.0.1:{port}'")

while 1:
    #print(123)
    try:
        r,w,_ = select.select([server]+list(clients.keys()), writers.keys(), [])
    except:
        
        raise

    for cli in r:
        if cli == server:
            cli,addr = server.accept()
            print ('Connection from %s' % (addr,))
            clients[cli] = addr

        else:
            try:
                ret = cli.recv(1024)
                print(555, ret)
            except (SSL.WantReadError, SSL.WantWriteError, SSL.WantX509LookupError):
                pass
            except SSL.ZeroReturnError:
                raise
                dropClient(cli)
            except SSL.Error as errors:
                raise
                dropClient(cli, errors)
            else:
                if not cli in writers:
                    writers[cli] = b''
                writers[cli] = writers[cli] + ret
    if 0:
        for cli in w:
            try:
                ret = cli.send(writers[cli])
            except (SSL.WantReadError, SSL.WantWriteError, SSL.WantX509LookupError):
                pass
            except SSL.ZeroReturnError:
                print(111)
                raise
                dropClient(cli)
            except SSL.Error as  errors:
                raise
                dropClient(cli, errors)
            else:
                writers[cli] = writers[cli][ret:]
                if writers[cli] == '':
                    del writers[cli]

for cli in clients.keys():
    cli.close()
server.close()