22 - Game, Set and Hash
-----------------------
In this challenge we have only a host and a port to connect to. When doing so we have the following behavior:
```
$ nc hackyeaster.hacking-lab.com 8888
Ready for the game?
y
Let's go!
1c8bfe8f801d79745c4631d09fff36c82aa37fc4cce4fc946683d7b336b63032
foo
Wrong! Point for me.
----------------------
Player > 0 0
Master   0 15
----------------------
61ea0803f8853523b777d414ace3130cd4d3f92de2cd7ff8695c337d79c2eeee
```

We start some tennis game where we have to crack a SHA256 hash in less than 10 seconds otherwise we receive a timeout error. If the hash is correctly cracked we get a point, otherwise the "Master" gets a point. To solve this I used a python script using pwntools to interact with the service and hashcat with rockyou wordlist to crack the hashes. The script is as follows:
```python
#!/usr/bin/python2

import re
from pwn import *

r = remote('hackyeaster.hacking-lab.com', 8888)

r.recvline()
r.sendline('y')
r.recvline()
while True:
        h = r.recvline().strip()
        print('Hash is ' + h)
        print('Starting hashcat')
        try:
                hashcat = process('hashcat --force --potfile-disable --weak=0 -m 1400 ' + h + ' rockyou.txt', shell=True)
                print('Going to sleep for 9.5s')
                sleep(9.5)
                line = hashcat.recvline_regex('[0-9a-f]{64}:(.*)').strip()
                m = re.search(r'[0-9a-f]{64}:(.*)$', line)
                if m:
                        pwd = m.group(1)
                        print('Hash cracked: ' + pwd)
                        r.sendline(pwd)
                else:
                        print('FAIL')
                        r.sendline('fail')
        except EOFError:
                r.sendline('fail')

        print(r.recvline().strip())
        print(r.recvline().strip())
        print(r.recvline().strip())
        print(r.recvline().strip())
        print(r.recvline().strip())
```

The inner working is not so complex:

- start the game
- loop infinitely on
  * get the hash
  * launch hascat
  * wait 9.5 seconds (and leave 500ms for the processing/connection)
  * get the cracked hash and send it or send fail if none found

The run I made went like this:
```
python play.py                                                                                          ⏎
[+] Opening connection to hackyeaster.hacking-lab.com on port 8888: Done
Hash is d7697570462f7562b83e81258de0f1e41832e98072e44c36ec8efec46786e24e
Starting hashcat
[+] Starting local process None: Done
Going to sleep for 9.5s
[*] Process None stopped with exit code 0
Hash cracked: 6666
Correct! Point for you.
----------------------
Player > 0 15
Master   0 0
----------------------
Hash is 4ea5ee68fea05586106890ded5733820bb77d919cda27bc4b8139b7cd33b8889
[CUT BY NICOLAS]
Hash is 57fac8572eeab5fc599c760c659f587e76af9a5fa35b560723772df5f33004bf
Starting hashcat
[+] Starting local process None: Done
Going to sleep for 9.5s
[*] Process None stopped with exit code 0
Hash cracked: firebird
Correct! Point for you.
----------------------
Player   6 6 6
Master > 0 1 2
----------------------
Hash is You win! Solution is: !stan-the_marth0n$m4n
```

Then when entering the solution into egg-o-mati we get the egg:  
![](./22/egg22.png)
