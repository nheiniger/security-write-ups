#!/usr/bin/env python3

from OpenSSL import crypto, SSL
import sys
import requests

TYPE_RSA = crypto.TYPE_RSA
TYPE_DSA = crypto.TYPE_DSA

# adapted from https://github.com/pyca/pyopenssl/blob/master/examples/certgen.py
def create_CSR(pkey, payload, digest="sha256"):
    req = crypto.X509Req()
    subj = req.get_subject()

    setattr(subj, 'ST', payload)

    req.set_pubkey(pkey)
    req.sign(pkey, digest)
    return req

# statically defined key
key_str = """-----BEGIN RSA PRIVATE KEY-----
MIIEpQIBAAKCAQEAzqKQ7C8t5aZwprcsWvazHINq3v/pCXkXMyOs5uc9It8xBXu9
50yh2/hLfvPoi6ZLwFD690i3HOX+0hJzZfEkf+tEbYvgrkwJzefL5wVtCdaaAwq3
iArWZs3eWoSCxgKHnysu1s+OVozE/FxSqkfEQY74EHdtZtv8hdfJ6h+WtJmdTqFI
r3UuJaiz4r7CDge4mMOX36AjzptkUu2etoGsQgwScqNixSAkHAwKHlaQnI51nAVV
Mj0X+4Zsb+dn/xtT9yBsaDFweBfHWFL0WkBr8naYUUqw4T42xZ5Mi4rlUFHuwVYr
GZOC7OOtZRcupGesWsy0EEMWGxxiGKeUOIaEgQIDAQABAoIBAQC1imnct06Rlvsd
3YxglqGiCWuZZChvJC3Xxh4f90TlIEXHVYHwdok14x0g+lVya7XdzsfO/dmyz/Zi
xccQ5x10LVS/EcdiGnf6qQ2heEjl/d7tkTrRkQPw6inSSN1D7fENTDkojM23CJIA
TXRrGgY4us0CWoqJdfiT9pP016/mFgO6xM9wwz1jS/xIYSf9I2Oz9qhxRdMseX5m
eG2WRmW+lyAa+uVgVgM6ZGXxqq5NHieJiEtSEOkI4fhKFF9Gca+RT2MW9dSRCuV2
ltNBJbFiXle3WA7r2ST+R+yzlDd8OycJJFDIMRQuPG74KbkW6GF4JRx8awM0Oc6F
ZAinAmrJAoGBAOtJLHfDD8CohFcujqoeIklXjygJXYRNkWPFf4piHImp6TYl1Ls5
0/cQ5XJ9IGjA7rCXsvyiXuXgCmo9mNoA6uOs3BU7G/AAOAKTLDWKgbGm3xPdN7nt
qyUcNft2qm0S//zB5J4iYh30oyagUj9y5YL1BtYU/C3UNXMboMkppjsLAoGBAODT
qn92jXgPM1s8KYwRrAEk+GBmdxp007X7XtsGT91dCwawZ8BZHwFM9JAUc+mqiWKC
cRLqf0G9rNuKoYgMm7TKtjaeslZQoD1p/si8REdRWKzcgY6MLLlUDiUDery51f++
dizLFDVRq465faOrHOB8xAqYoxhnyAC7aGvhHJYjAoGBAIdCApE6jpS3i5S+y/7Z
4eX9sutWLu9+1ATiJYa9DiDJj6q0Js4W2Vaf3PdrHTV7K/xSyO9YvGsz12jpzjQM
8Ps/hSmjWFUpGwnH51NEM3iYMIev1XhKO+fShunvdtvLX2PDZxTNOVB1MVFkOsQE
3hHhoDNzzuDdrHhmupDKI6ivAoGAdAcIsKtgKxu9J1KPJohgOl74B9gZk3/DWuGV
fHdvdBB2hkc35B6aT7OFa24CvA6UxFAJRvfaIPVgZhTPdET9fno3O0z/QGhvqgIv
ySzQF/Y1S1CpVAWndyWX/yYii49kj42ds1RC45l4bjnwSy0dxATfr5BCa2/z2dzd
8P7GH/0CgYEAvcSBlUTv4XI54FMOCZmktEnUTC3OqysAyEdc/HxZAU0+AJMAgo+5
7CAE/MTjguo+1s60lGxWiW4JVYqzY+08RXU0G2nWB/pnLOvwF8g/55j/w5+2Xm/P
rE7pBtRFBCae44LIqXj2dly48J8q6QrceIc5VzL/l8TH0yDnOCqy9ow=
-----END RSA PRIVATE KEY-----
"""
key = crypto.load_privatekey(crypto.FILETYPE_PEM, key_str)

csr = create_CSR(key, sys.argv[1])
csr_str = crypto.dump_certificate_request(crypto.FILETYPE_PEM, csr).decode()

r = requests.post('http://challenges.hackvent.hacking-lab.com:1088/php/api.php?function=csr&argument=&key=E7g24fPcZgL5dg78', data = {'csr':csr_str})
print('=== {} ==='.format(r.status_code))
print(r.text)
