15 - P Cap
----------
We were given a traffic dump. When analyzing it with Wireshark we can see a big chunk of data due to SMB communication. Wireshark has a nice tool to extract data from SMB exchanges "File -> Export Objects -> SMB...". Using this we can extract a picture, `R05h4L.jpg`.

This picture shows a stickman with "challenge denied" text. However when looking at the file data we see at the end of the file more data that is not part of the picture. It contains the string "imnothere.txt" and the data chunk starts with the bytes `50 4b` or `PK` which are the magic bytes for zip archives. Knowing that we can unzip the file as follows:
```
$ unzip R05h4L.jpg
Archive:  R05h4L.jpg
warning [R05h4L.jpg]:  100447 extra bytes at beginning or within zipfile
  (attempting to process anyway)
  inflating: imnothere.txt
```

Then we look at `imnothere.txt` and see that it is actually not a text file but a picture: ![](./15/imnothere.jpg)

The picture gives a PHP page that we can access on the hacky easter server at `https://hackyeaster.hacking-lab.com/hackyeaster/7061n.php` and get the egg:
![](./15/egg15.png)
