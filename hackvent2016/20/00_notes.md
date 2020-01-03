Day 20: MitT
------------
On this challenge when running the VM image we can press "Enter" key several times in the "fireplace" screen to get a CLI. In retrospect we could also have run the script on every port in sequence until we found the one to connect to if we did not had access to this CLI. Using the CLI we can use the commands `ifconfig` to show the current IP and `netstat -l` to show the listening ports. When connecting on the IP:port combination using netcat we get this:
```bash
$ nc 192.168.43.61 26139
port 36862 in 8 seconds
```

So we should connect to this port after waiting this number of seconds. Lets automate this with a script:
```python
#!/usr/bin/python2

import argparse
import time
from pwn import *

parser = argparse.ArgumentParser()
parser.add_argument("ip", help="The IP to connect to.")
parser.add_argument("port", help="The first port that should be knocked.", type=int)
args = parser.parse_args()

delay = 0
new_port = args.port
for i in range(10):
        time.sleep(delay)
        conn = remote(args.ip, new_port)
        answer = conn.recvline()
        conn.close()
        print(answer)
        split_answer = answer.split(" ")
        new_port = int(split_answer[1])
        delay = int(split_answer[3])
        print(str(new_port) + " " + str(delay))
```

The run of the script is as follows:
```bash
$ ./exploitKnocker.py 192.168.43.61 26308                                                                 ⏎
[+] Opening connection to 192.168.43.61 on port 26308: Done
[*] Closed connection to 192.168.43.61 port 26308
port 31168 in 10 seconds

31168 10
[+] Opening connection to 192.168.43.61 on port 31168: Done
[*] Closed connection to 192.168.43.61 port 31168
port 48392 in 8 seconds

48392 8
[+] Opening connection to 192.168.43.61 on port 48392: Done
[*] Closed connection to 192.168.43.61 port 48392
port 44492 in 2 seconds

44492 2
[+] Opening connection to 192.168.43.61 on port 44492: Done
[*] Closed connection to 192.168.43.61 port 44492
port 34422 in 1 seconds

34422 1
[+] Opening connection to 192.168.43.61 on port 34422: Done
[*] Closed connection to 192.168.43.61 port 34422
port 30539 in 7 seconds

30539 7
[+] Opening connection to 192.168.43.61 on port 30539: Done
[*] Closed connection to 192.168.43.61 port 30539
port 25904 in 10 seconds

25904 10
[+] Opening connection to 192.168.43.61 on port 25904: Done
[*] Closed connection to 192.168.43.61 port 25904
port 53736 in 7 seconds

53736 7
[+] Opening connection to 192.168.43.61 on port 53736: Done
[*] Closed connection to 192.168.43.61 port 53736
the flag is HV16-aBB9-Gis5-RMu2-parP-ckoj

Traceback (most recent call last):
  File "./exploitKnocker.py", line 21, in <module>
    new_port = int(split_answer[1])
ValueError: invalid literal for int() with base 10: 'flag'
```

And in the end, although we have errors in the script we can see the flag:

> HV16-aBB9-Gis5-RMu2-parP-ckoj
