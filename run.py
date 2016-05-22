#!/usr/bin/env python3
'''Commands:

cd /home/private
git clone https://github.com/lukas2511/letsencrypt.sh 
cd letsencrypt
mkdir -p /home/public/.well-known/acme-challenge/ 
echo 'WELLKNOWN="/home/public/.well-known/acme-challenge/"' > config.sh 
echo '{domain} www.{domain}' > domains.txt

## Below is also for renewal
./letsencrypt.sh --cron
cd certs/{domain}
cat privkey.pem cert.pem chain.pem | nfsn -i set-tls

Check expiration date:
openssl x509 -noout -in cert.pem -enddate
# notAfter=Aug 20 00:24:00 2016 GMT


'''

def init_tls(domain):
    pass

def update_tls():
    pass

def cert_expires():
    pass

def parse_args():
    pass

def main():
    pass

if __name__ == '__main__':
    main()
