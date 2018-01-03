import commands, re

class X509Helper:
    def __init__(self,filename, openssl_cmd=None):    
        self.filename= filename
        self.openssl_cmd = openssl_cmd
        self.parse()
    
    def parse(self):        
        if self.openssl_cmd:
            openssl = self.openssl_cmd
        else:
            openssl = 'openssl'
        
        base_cmd = openssl+' x509 -in %s -noout ' % self.filename
        
        status,subject = commands.getstatusoutput(base_cmd+'-subject')
        if status:
            raise RuntimeError, "Error invoking openssl: "+ subject
        
        status,issuer = commands.getstatusoutput(base_cmd+'-issuer')
        if status:
            raise RuntimeError, "Error invoking openssl: "+ issuer
        
        
        status,email = commands.getstatusoutput(base_cmd+'-email')
        if status:
            raise RuntimeError, "Error invoking openssl: "+ email
        
        self.subject = re.sub(r'^subject= ','',subject.strip())
        self.issuer = re.sub(r'^issuer= ','',issuer.strip())
        self.subject = re.sub(r'/(E|e|((E|e|)(mail|mailAddress|mailaddress|MAIL|MAILADDRESS)))=','/Email=',self.subject)
        
        self.email = email.strip()
    
    def __repr__(self):
        return 'Subject:%s\nIssuer:%s\nEmail:%s' % (self.subject, self.issuer, self.email)