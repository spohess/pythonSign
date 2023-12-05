import sys
from datetime import datetime

from erpbrasil.assinatura.assinatura import Assinatura
from erpbrasil.assinatura.certificado import Certificado

##################################################
## author: Sergio Hess
## date: 04/12/2023
## version: 1.0.0
## description: Sign file with one or two A1 certs
##################################################
## dependencies:
##    erpbrasil/erpbrasil.assinatura: https://github.com/erpbrasil/erpbrasil.assinatura
##    m32/endesive: https://github.com/m32/endesive
##################################################
## command: sign.py
## parameters:
##     original_file
##         - required
##         - type: .pdf
##         - with path (example: /var/www/path/file.pdf)
##     output_file
##         - required
##         - type: .pdf
##         - with path (example: /var/www/path/file)
##     cert_file
##         - required
##         - extension: .pfx
##         - with path (example: /var/www/path/cert.pfx)
##     cert_password
##         - required
##         - type: string
##     second_cert_file
##         - optional
##         - extension: .pfx
##         - with path (example: /var/www/path/cert.pfx)
##     second_cert_password
##         - optional
##         - type: string
## examples:
##     python sign.py storage/tmp/original.pdf storage/files/sign_20230101.pdf storage/certs/user_876564.pfx SECRET_PASSWORD
##     python sign.py storage/tmp/original.pdf storage/files/sign_20230101.pdf storage/certs/user_876564.pfx SECRET_PASSWORD storage/certs/user_065875.pfx OTHER_SECRET_PASSWORD
##################################################

if len(sys.argv) < 5:
    with open('options', 'r') as f:
        print(f.read())

    exit(400)

##################################################
## First sign
##################################################
cert = Certificado(sys.argv[3], sys.argv[4], raise_expirado=False)
entity_cert = Assinatura(cert)

data_sign = {
    'sigflags': 3,
    'contact': cert.proprietario,
    'location': 'BR',
    'signingdate': "%s+02'00'" % datetime.now().strftime("%Y%m%d%H%M%S"),
    'reason': 'Document Authenticity',
}

original_file = sys.argv[1]
open_file = open(original_file, 'rb').read()

sign_content = entity_cert.assina_pdf(arquivo=open_file, dados_assinatura=data_sign)

with open(sys.argv[2], 'wb') as fp:
    fp.write(open_file)
    fp.write(sign_content)

if len(sys.argv) == 5:
    print('file signed successfully')
    exit()

##################################################
## Second sign
##################################################
sign_file = open(sys.argv[2], 'rb').read()

second_cert = Certificado(sys.argv[5], sys.argv[6], raise_expirado=False)
second_entity_cert = Assinatura(second_cert)

data_sign = {
    'sigflags': 3,
    'contact': second_cert.proprietario,
    'location': 'BR',
    'signingdate': "%s+02'00'" % datetime.now().strftime("%Y%m%d%H%M%S"),
    'reason': 'Document Authenticity',
}

new_sign_content = second_entity_cert.assina_pdf(arquivo=sign_file, dados_assinatura=data_sign)

with open(sys.argv[2], 'wb') as fp:
    fp.write(sign_file)
    fp.write(new_sign_content)

print('file signed successfully')
exit()
