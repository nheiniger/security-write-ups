Day 12: Crypt-o-Math
--------------------
The file we get is a list of integers and looking at the second line we see that each line must be a tuple like `(m,b,p)` With the two last lines we see that we need to find 'a' such that the equation `m = a * 0x1337 * b % p` is satisfied. Since there are 29 tuples concatenating the values of a should give our flag.

If the flag is really constructed like this, then we should find it easily by looping over the integers from 0 to 255 (we could do less of course but I was lazy). So with this python script we can get the flag. In `data.txt` are only the lines with the tuples `(m,b,p)`.
```python
#!/usr/bin/python3

f = open('data.txt', 'r')
flag = ""

for line in f:
        (n1, n2, n3) = line.split(',')
        m = int(n1)
        b = int(n2)
        p = int(n3)
        for a in range(255):
                if m == a * 0x1337 * b % p:
                        flag = flag + chr(a)

print(flag)
```

And the flag is:

> HV16-laWz-D5yT-0Uzb-DFj0-FIsL
