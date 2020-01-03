09 - Microscope
---------------
In this mobile challenge, the displayed picture is too small to read the QR-code of the egg. Even when using Android accessibility tools (magnifier) it remains unreadable. However, when proxying the application Internet connection through Burp we directly see the HTTP request made to get the file `https://hackyeaster.hacking-lab.com/hackyeaster/images/challenge/egg09_fs0sYle2SN.png` downloading this file in a browser gives the egg:  
![](./09/egg09.png)
