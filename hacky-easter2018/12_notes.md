12 - Patience
=============
> All you need is a little patience...
> 
> Countdown:
> 100000

Here we could simply wait for much too long or bypass this wait :) When looking at the code of the challenge in the decompiled sources of the mobile application we see the following script managing the countdown:
```javascript
hash = 'genesis';
count = 100000;
setTimeout( function() { document.location.href = 'ps://count?h=' + hash + '&c=' + count; } , 1000);
function countFeedback(jsonString) {
    var json = JSON.parse(jsonString);
      if (json) {
        hash = json.h;
        count = json.c;
        $('#count').text(count);
        if (count == 0) {
   	        document.getElementById('flag').setAttribute('src', 'https://hackyeaster.hacking-lab.com/hackyeaster/images/eggs/'+hash+'.png');
        } else if (count > 0) {
            setTimeout( function() { document.location.href = 'ps://count?h=' + hash + '&c=' + count; } , 3000);
        }
      }
  }
```

Looking at the URL handler for the `ps://` we see the following:
```java
if (url.startsWith(Activity.URL_COUNT)) {
    uri = Uri.parse(url);
    final String h = uri.getQueryParameter("h");
    final String c = uri.getQueryParameter("c");
    final WebView fView = view;
    new Handler().postDelayed(new Runnable() {
        public void run() {
            String json = Activity.this.handleCount(h, c);
            if (json != null) {
                fView.loadUrl("javascript:countFeedback('" + json + "');");
            }
        }
    }, 7000);
    return true;
}
```

The `h` and `c` parameter are passed to the `handleCount` function:
```java
private String handleCount(String h, String c) {
    if (!(c == null || h == null)) {
        try {
            Integer count = Integer.valueOf(Integer.parseInt(c));
            String hash = sha1(h + c);
            if (count.intValue() >= 0) {
                return "{ \"h\":\"" + hash + "\", \"c\":\"" + (count.intValue() - 1) + "\" }";
            }
        } catch (Exception e) {
        }
    }
    return null;
}
```

Basically, a sha1 hash of the previous hash concatenated with the current counter is done. Then this new hash is returned with the decremented counter. When the counter reach 0 a URL is fetched with the last hash on the hacky easter website. To get the egg we need to fetch this URL and, thus, first compute the hash. This can be done using the following python script:
```python
!/usr/bin/python3

import hashlib
value = 'genesis'

for i in range(100000, 0, -1):
    concat = (value + str(i)).encode()
    value = hashlib.sha1(concat).hexdigest()

print(value)
```

Running the script:
```bash
$ python 12_hash.py
dd6f1596ab39b463ebecc2158e3a0a2ceed76ec8
```

Then we get the egg at the corresponding URL <https://hackyeaster.hacking-lab.com/hackyeaster/images/eggs/dd6f1596ab39b463ebecc2158e3a0a2ceed76ec8.png>:
![](./12_egg.png)
