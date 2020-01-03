Day 16: Try to escape ...
=========================
> *... from the snake cage*
> 
> Santa programmed a secure jail to give his elves access from remote. Sadly the jail is not as secure as expected.

We get a ncat command to connect to a port on a server, `nc challenges.hackvent.hacking-lab.com 1034`. When run we are greeted with a python-like shell:
```
~/D/c/16 ❯❯❯ nc challenges.hackvent.hacking-lab.com 1034
                        _____
                    .-'`     '.
                 __/  __       \\
                /  \ /  \       |    ___
               | /`\| /`\|      | .-'  /^\/^\\
               | \(/| \(/|      |/     |) |)|
              .-\__/ \__/       |      \_/\_/__..._
      _...---'-.                /   _              '.
     /,      ,             \   '|  `\                \\
    | ))     ))           /`|   \    `.       /)  /) |
    | `      `          .'       |     `-._         /
    \                 .'         |     ,_  `--....-'
     `.           __.' ,         |     / /`'''`
       `'-.____.-' /  /,         |    / /
           `. `-.-` .'  \        /   / |
             `-.__.'|    \      |   |  |-.
                _.._|     |     /   |  |  `'.
          .-''``    |     |     |   /  |     `-.
       .'`         /      /     /  |   |        '.
     /`           /      /     |   /   |\         \\
    /            |      |      |   |   /\          |
   ||            |      /      |   /     '.        |
   |\            \      |      /   |       '.      /
   \ `.           '.    /      |    \        '---'/
    \  '.           `-./        \    '.          /
     '.  `'.            `-._     '.__  '-._____.'--'''''--.
       '-.  `'--._          `.__     `';----`              \\
          `-.     `-.          `."'```                     ;
             `'-..,_ `-.         `'-.                     /
                    '.  '.           '.                 .'

Challenge by pyth0n33. Have fun!



The flag is stored super secure in the function SANTA!
>>> a =
```

When providing inputs, we quickly notice that some characters are forbidden and when included return a `Denied`. I compiled a list of authorized characters:
```
a, c, d, e, i, l, n, o, p, r, s, t, v, (, ), +, [, ], ., _
```

Using those I found that the functions `eval`, `print` and `str` are available. We also notice that the string that we input are put in lower case before being interpreted. So no way to call the `SANTA` function directly. Since we can use `eval` we should be able to call this function nonetheless if we cant find a way to "generate" the uppercase letters from our restricted set of possibilities.

Once more I lost a lot of time to search for these SANT letters in every location I thought of. I was at this point:
```
S = str.center.__doc__[0]
N = repr(eval("print(1)"))[0]
T = repr(a.__class__)[12]
```

When I finally understood that I could simply use:
```
A = "a".title()
```

Then it was possible to call the `SANTA` function as follows:
```
>>> a = eval('print(eval("s".title()+"a".title()+"n".title()+"t".title()+"a".title())())')
No flag for you!
```

But no flag for me yet... it was time for some googling and I found a useful article here: <https://lbarman.ch/blog/pyjail/> I thought of disassembling the bytecode we can get using `SANTA.__code__.co_code` but could not find a way to do that. Then I started to put some arguments in the function and had:
```
>>> a = eval('print(eval("s".title()+"a".title()+"n".title()+"t".title()+"a".title())("11111111111111111111111111111"))')
HT31-H67l/guc6/v3gf+w6x|-1cuy
```

The result is similar to a flag and if we fiddle around we get to:
```
>>> a = eval('print(eval("s".title()+"a".title()+"n".title()+"t".title()+"a".title())("1337"))')
HV17
```

And trying to go on I finally found how to generate the flag:
```
>>> a = eval('print(eval("s".title()+"a".title()+"n".title()+"t".title()+"a".title())("13371337133713371337133713371"))')
HV17-J41l-esc4-p3ed-w4zz-3asy
```
