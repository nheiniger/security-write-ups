Bonus flag 01
=============
When accessing the daily challenges, the URL looks like <https://hackvent.hacking-lab.com/challenge.php?day=01>. The `day` parameter being suspicious we can try to play with it. Depending on the number we put inside, the answer is interesting:
```
day=-1:
This exception ()schould not happen ... what are you doing?

day=02:
nice try, hobo!
The resource (#1) you are trying to access, is not (yet) for your eyes.

day=25:
nice try, geek!
The resource (#1959) you are trying to access, is not (yet) for your eyes.

day=26:
nice try, geek!
The resource (#1958) you are trying to access, is not (yet) for your eyes.

day=27:
nice try, geek!
The resource (#1957) you are trying to access, is not (yet) for your eyes.
```

Seeing this, we can try to get this counter to #0, and this would be:
```
day=1984:
nice try, geek!
The resource you are trying to access, is hidden in the header.
```

Now looking at the HTTP header of the response we see the flag:
```
HTTP/1.1 200 OK
Date: Fri, 01 Dec 2017 07:21:51 GMT
Server: Merry Christmas & Hacky New Year
Strict-Transport-Security: max-age=15768000
Flag: HV17-4llw-aysL-00ki-nTh3-H34d
Connection: close
Content-Type: text/html; charset=UTF-8
Content-Length: 16042
```
