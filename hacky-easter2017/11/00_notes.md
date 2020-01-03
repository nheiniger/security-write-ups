11 - Tweaked Tweet
------------------
In this mobile activity we can click on a button and a the twitter application is opened to tweet something. When looking at the application code we see that this is done by opening the following URL:
```
https://twitter.com/intent/tweet?text=%23%EF%BC%A8a%EF%BD%83%EF%BD%8By%CE%95\
%EF%BD%81ste%EF%BD%92%E2%80%A9201%EF%BC%97%E2%80%A9%E2%85%B0%EF%BD%93%E2%80%80\
a%E2%80%84l%EF%BD%8F%EF%BD%94%E2%80%80%CE%BFf%E2%80%89%EF%BD%86un%EF%BC%81%E2\
%80%A8%23%D1%81tf%E2%80%88%23%EF%BD%88%EF%BD%81%CF%B2king-lab
```

After looking during hours for ways to reveal hidden information inside the URL I googled "twitter steganography" and solved the challenge in 30 seconds using [1]. Entering the tweet in the tool you get the password `st3g4isfunyo`.

When entering this in the egg-o-matic the egg is shown:  
![](./11/egg11.png)

\[1\]: Twitter Secret Messages, <http://holloway.co.nz/steg/>
