Day 06: Santa's journey
=======================
> *Make sure Santa visits every country*
> 
> Follow Santa Claus as he makes his journey around the world.

In this one we're given a URL: <http://challenges.hackvent.hacking-lab.com:4200>. When calling the URL a QR code is returned as a PNG file. When decoded we get a country name. Trying it several times shows different countries. And iwth the hint we can assume that we have to get all countries.

I did it using bash and a QR code reader called zbarimg. It goes as follows:
```bash
# download 500 times the picture
$ for i in {1..500}; do; wget -q -O qr$i.png 'http://challenges.hackvent.hacking-lab.com:4200'; done;

# decode all QR codes and send result to a file
$ touch countries.txt
$ for f in `ls -1 *.png`;do;zbarimg -q --raw $f >> countries.txt;done;

# search for the flag among the countries
$ grep HV17 countries.txt
HV17-eCFw-J4xX-buy3-8pzG-kd3M
```
