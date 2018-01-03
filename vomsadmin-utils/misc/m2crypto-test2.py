import socket, M2Crypto
from M2Crypto import SSL

class SSLSocketClient(object):
    # setting socket types
    address_family = socket.AF_INET
    socket_type = socket.SOCK_STREAM
 
    def __init__(self, server_address, cert, certkey, ca):
        self.server_address = server_address
        self.connected = False
        self.cert = cert
        self.certkey = certkey
        self.ca = ca
        
    def connect(self):
        global ca
        cert = self.cert
        certkey = self.certkey
        ca = self.ca
        
        def verify_cb(ok, store) :
            global ca
            cert = store.get_current_cert()
            mecert = M2Crypto.X509.load_cert(ca)
            if mecert.get_fingerprint(md="sha1") == cert.get_fingerprint(md="sha1"):
                return 1
            else:
                return ok
        # setup an SSL context.
        context = SSL.Context("sslv23")
        context.load_verify_locations(ca, "./")
        # setting verifying level
        context.set_verify(SSL.verify_peer | SSL.verify_fail_if_no_peer_cert, 1,verify_cb )
        # load up certificate stuff.
        context.load_cert(cert, certkey)
        # setting callback so we can monitor our SSL
        context.set_info_callback()
        # create real socket
        real_sock = socket.socket(self.address_family, self.socket_type)
        connection = SSL.Connection(context, real_sock)
        self.socket = connection
        self.socket.connect(self.server_address)
        self.connected = True
        
    
        