Day 15: SAP - Santas Admin Panel
--------------------------------
The challenge description immediately hints at bit flipping so let's log in with the valid account and try to modify the cookie named cmlnaHRz. I started by modifying each character to see when the resulting page would change. My original cookie was: `cmlnaHRz=5WT4yVGAfS/n0z5MzSbbZd0K3vpWLmhfxuFo85apE+o=`

I first found a value that changes the user role to none: `cmlnaHRz=5WT4yVGAfS+n0z5MzSbbZd0K3vpWLmhfxuFo85apE+o=`

If you look closely, you will see that the '/' is now a '+'.

OK, so bit flipping it is, now we need to find the value that will give us admin access. Burp has a very handy tool called Intruder that allows us to do bit flipping automatically on the chosen payload. We send the request to the Intruder and configure it as shown in the screenshots.

First we show the request as it is fed in the Intruder. The payload will be derived from the initial cookie (marked in orange):
![](./15/15_screen01.png)

Then we have the options for the payload. We use the bit flipper tool with default configuration:
![](./15/15_screen02.png)

We also add a "Grep - Extract" option to display the role returned by the request:
![](./15/15_screen03.png)

Finally we start the attack and the results are displayed. Highlighted is the request with the successful payload and the Admin role that results:
![](./15/15_screen04.png)

Then we only have to fetch the image in the browser and scan the QR-code to get the flag:

> HV16-R41n-d33r-8yt3-Fl1p-H4ck
