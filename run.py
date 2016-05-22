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
import argparse
import datetime
import os
import random
import subprocess

our_dir = os.path.dirname(os.path.realpath(__file__))
priv_dir = '/home/private'
encr_dir = os.path.join(priv_dir, 'letsencrypt.sh')
cert_dir = os.path.join(encr_dir, 'certs', '{domain}')

def init_tls(domain):
    #print({'our': our_dir, 'priv': priv_dir, 'encr': encr_dir, 'cert': cert_dir.format(domain=domain)})
    os.chdir(priv_dir)
    success = subprocess.call(['git', 'clone', 'https://github.com/lukas2511/letsencrypt.sh'])
    if success != 0:
        exit('Unable to clone letsencrypt. Nothing has been done yet. Aborting.')
    os.chdir(encr_dir)
    rand = random.randrange(100000, 1000000)
    os.makedirs('/home/public/.well-known/acme-challenge/{}/'.format(rand))
    with open('config.sh', 'w') as f:
        f.write('WELLKNOWN="/home/public/.well-known/acme-challenge/{}/"\n'.format(rand))
    with open('domains.txt', 'w') as f:
        f.write('{domain} www.{domain}\n'.format(domain=domain))
    print('\n\n\nINFO:\nTLS has been initialized.\n')

def update_tls(domain):
    os.chdir(encr_dir)
    success = subprocess.call(['./letsencrypt.sh', '--cron'])
    if success != 0:
        exit('Unable to run letsencrypt.sh. TLS has not been updated. Aborting.')
    os.chdir(cert_dir.format(domain))
    success = subprocess.call(['bash', '-c', 'cat privkey.pem cert.pem chain.pem | nfsn -i set-tls'])
    if success != 0:
        exit('''Unable to import the certificates.
        After investing the problem, please run these commands:

        cd {}
        cat privkey.pem cert.pem chain.pem | nfsn -i set-tls
        '''.format(os.path.realpath(os.curdir)))
    with open(os.path.join(our_dir, 'certificate_expiration.txt'), 'w') as f:
        f.write(str(cert_expires('cert', domain).timestamp()))
    print('\n\n\nINFO:\nTLS has been updated.\n')

def cert_expires(from_, domain=None):
    if from_ == 'cert':
        if not domain:
            raise ValueError('When from_ is "cert", you MUST set domain')
        try:
            raw = subprocess.check_output(
                ['openssl', 'x509', '-noout', '-in',
                    os.path.join(cert_dir.format(domain)), 'cert.pem', '-enddate'],
                universal_newlines=True).strip()
        except subprocess.CalledProcessError:
            exit('Unable to determine the certificate expiration date. Please investigate. Aborting')
        # Example return from openssl: notAfter='Aug 20 00:24:00 2016 GMT'
        junk, when = raw.split('=', maxsplit=1)
        return datetime.datetime.strptime(when.replace('GMT', '+0000'), '%b %d %H:%M:%S %Y %Z')
    elif from_ == 'file':
        with open(os.path.join(our_dir, 'certificate_expiration.txt')) as f:
            return datetime.datetime.fromtimestamp(float(f.read().strip()), tz=datetime.timezone.utc)
    else:
        raise ValueError('Bad value for from_')

def is_installed():
    return os.path.isdir(encr_dir)

def parse_args():
    desc="Automatically enable and/or update TLS on NearlyFreeSpeech.net sites using Let's Encrypt"
    parser = argparse.ArgumentParser(description=desc)
    group = parser.add_mutually_exclusive_group(required=True)
    padd = parser.add_argument
    gadd = group.add_argument
    padd('domain', metavar='DOMAIN',
        help='Your bare domain name (example.com, not www.example.com). IMPORTANT NOTE: This script DOES NOT work with NFSN default names, such as example.nfshost.com.')
    gadd('--install', action='store_true',
        help="Enable Let's Encrypt for the first time")
    gadd('--update', action='store_true',
        help="Update your certificate, if necessary. Will not update certificates which are valid for at least two more weeks unless -f/--force is given.")
    padd('-f', '--force', action="store_true",
        help='With --update, force certificate update even if it is not necessary')
    padd('-q', '--quiet', action='store_true',
        help='With --update, exit silently if no update is carried out. Useful to avoid useless messages from cron.')
    return parser.parse_args()

def main():
    args = parse_args()
    if args.install:
        if args.domain.endswith('.nfshost.com'):
            exit("This script doesn't work with domains ending with '.nfshost.com'. If your site has its own domain name, please use that. If not, you can't use this script.")
        if is_installed():
            exit("Let's Encrypt is already installed. Perhaps you meant to give --update instead of --install.")
        else:
            init_tls(args.domain)
            update_tls(args.domain)
    elif args.update:
        if not is_installed():
            exit("You have to install Let's Encrypt first using the --install option.")
        now = datetime.datetime.now(datetime.timezone.utc)
        expires = cert_expires('file')
        if expires - now <= datetime.datetime.timedelta(weeks=2):
            update_tls(args.domain)
        else:
            if args.force:
                update_tls(domain)
            elif not args.quiet:
                print("The certificate doesn't expire until {}. Not updating.".format(expires.isoformat()))

if __name__ == '__main__':
    main()
