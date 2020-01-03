Day 10: Just play the game
==========================
> *Haven't you ever been bored at school?*
> 
> Santa is in trouble. He's elves are busy playing TicTacToe. Beat them and help Sata to save christmas!

Tic Tac Toe, simple game to win 100 times before getting the flag. I used pwntools for python3 and made a very idiotic strategy that will start with two identical moves every time and then handle the cases one by one until I can win or get a tie every time. In the end I print the result of each game to get the flag when the 100th win is reached.

The script is here:
```python
#!/usr/bin/python3

from pwn import *
import re

# parse response and returns the current state
def parse_response(resp):
        p = re.compile('([*XO])')
        # find all occurences and keep only the game where the bot played 
        m = p.findall(resp)[-9:]
        return(m)

# establish connection and pass preamble
c = remote('challenges.hackvent.hacking-lab.com', 1037)
c.recvuntil('enter to start the game')

# start to play with a list of moves that wins against the "AI" every time
while True:
        c.sendline('')
        state = parse_response(str(c.recvuntil('Field:')))
        c.sendline('1')
        state = parse_response(str(c.recvuntil('Field:')))
        c.sendline('9')
        state = parse_response(str(c.recvuntil('Field:')))
        if state == ['X', '*', 'O', '*', 'O', '*', '*', '*', 'X']:
                c.sendline('7')
                state = parse_response(str(c.recvuntil('Field:')))
                c.sendline('4')
                print(c.recvuntil('enter to start again'))
        elif state == ['X', 'O', '*', '*', 'O', '*', '*', '*', 'X']:
                c.sendline('8')
                state = parse_response(str(c.recvuntil('Field:')))
                if state == ['X', 'O', '*', '*', 'O', '*', 'O', 'X', 'X']:
                        c.sendline('3')
                        state = parse_response(str(c.recvuntil('Field:')))
                        if state == ['X', 'O', 'X', '*', 'O', 'O', 'O', 'X', 'X']:
                                c.sendline('4')
                                print(c.recvuntil('enter to start again'))
                        elif state == ['X', 'O', 'X', 'O', 'O', '*', 'O', 'X', 'X']:
                                c.sendline('6')
                                print(c.recvuntil('enter to start again'))
                elif state == ['X', 'O', 'O', '*', 'O', '*', '*', 'X', 'X']:
                        c.sendline('7')
                        print(c.recvuntil('enter to start again'))
        elif state == ['X', 'O', 'O', '*', '*', '*', '*', '*', 'X']:
                c.sendline('5')
                print(c.recvuntil('enter to start again'))
        else:
                print('Alternative')
                print(state)
                exit()
```

And in the end, a part of the script output gives the flag:
```
b' \x1b[2J\x1b[H\n ------------- \n | X | * | O | \n ------------- \n ------------- \n | X | O | * | \n ------------- \n ------------- \n | X | O | X | \n ------------- \n\x1b[2J\x1b[H\n ------------- \n | X | O | O | \n ------------- \n ------------- \n | X | O | * | \n ------------- \n ------------- \n | X | O | X | \n ------------- \nCongratulations you won! 100/100\n\nHV17-y0ue-kn0w-7h4t-g4me-sure\nPress enter to start again'
```

And the flag is:
```
HV17-y0ue-kn0w-7h4t-g4me-sure
```
