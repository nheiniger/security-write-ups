Special Flag 2: Perl GIF
------------------------
The hint said to look at the second two elements of the flag for day 11. This flag ended with TMTO-WTDI. So when googling that you find that it's a Perl motto: There is more than one way to do it.

After much fiddling with the file itself I eventually executed the command:
```bash
$ perl MandM.gif
PIN?
> 1234
��Z|"���C���e�f�X��spv
```

It asks for a PIN and return some data afterwards. We guess that this must be the flag and bruteforce the PIN with this (slow) script. It will test PINs in increasing order by spawning new proceses, check if the answer includes 'HV16' and stop if yes:
```python
#!/usr/bin/python

import pexpect
import sys

for i in range(100000, 1000000):
	print(str(i))
	child = pexpect.spawn('perl MandM.gif')
	child.delaybeforesend = None
	child.expect('> ')
	child.sendline(str(i))
	try:
		child.expect('foo')
	except:
		if "HV16" in child.before:
			print(child.before)
			print(str(child))
			exit()
```

And when running it it finds that the PIN is 160417 and the flag is:

> HV16-FWtf-Sh9O-cApF-Q9HQ-qMrp
