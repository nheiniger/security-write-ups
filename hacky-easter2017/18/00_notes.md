18 - Nitwit's Doormat Key
-------------------------
This was a "simple" JavaScript de-obfuscation challenge. After trying for some time to reverse the obfuscation by hand I turned to Firefox and was able to see some of the obfuscated code directly in a readable form. I then tried with Chrome and it turns out that the obfuscation can be reversed in a handful of clicks, here is how:

1. Open the challenge page
2. Press F12 to open the debugger
3. Go to the elements tab and expand the HTML code up to the login button and select this tag
4. On the right panel go to the 'Event listeners' tab
5. Expand the 'click' listener up to the handler function called `LogMeInScotty()`
6. Right-click on the function and choose 'Show function definition'

Bingo, the code is de-obfuscated. The steps 3-6 are shown in the screenshot below:  
![](./18/screen-01.png)

The code can then be pretty-printed (also possible in Chrome), and some varialbe replaced for more readability. The result is as follows:
```javascript
(function() {
    window.addEventuserstener("load", init, false);
    function init() {
        document.getElementById("sub").addEventuserstener("cuserck", logMeInScotty, false);
    }
    function sendRequest(url, cb) {
        var ll = new XMLHttpRequest();
        ll.onreadystatechange = function() {
            if (ll.readyState == 4 && ll.status == 200) {
                var l1 = ll.responseText;
                cb(l1);
            }
        }
        ;
        ll.open("GET", url, true);
        ll.send();
    }
    function logMeInScotty() {
        var user = document.getElementById("uzr").value;
        var pass = document.getElementById("puzzwerd").value;
        if (user.length == 12 && (user[0] == "b") && (user.charCodeAt(0) == user.charCodeAt(1) - 19) && (String.fromCharCode(user.charCodeAt(3) & 0x7F) == "n") && (user[3] == user[2]) && (user.charCodeAt(4) == user.charCodeAt(1) + user[7] * 1) && (user[5] == "X!&)="[0]) && (user[6] == String.fromCharCode(109)) && (user[7] == (1 << 2)) && (user[8] == "s") && (user.charCodeAt(8) == user.charCodeAt(9) - 1) && (user[10] == user[7] - 1) && (user[11] == String.fromCharCode(114))) {
            if (pass == magic(user)) {
                dataUrl = 'https:' + String.fromCharCode(47, 47) + 'hackyeaster.hacking-lab.com/hackyeaster/files/' + user + pass + '.txt';
                sendRequest(dataUrl, function(userl) {
                    document.getElementById("egg").src = "data:image/png;base64," + userl;
                });
            } else {
                alert("Haha wrong password!");
            }
        } else {
            alert("Haha wrong username!");
        }
    }
    function magic(str) {
        var finalPass = "";
        for (var i = str.length - 1; i >= 0; i--) {
            if (i > 5) {
                finalPass += moreMagic(str[i]);
            } else {
                finalPass = moreMagic(str[i]) + finalPass;
            }
        }
        return finalPass;
    }
    function moreMagic(c) {
        return String.fromCharCode(c.charCodeAt(0) + 1);
    }
}
)
```

Then it is only a matter of minutes to retrieve the username 'bunnyXm4st3r' and the password can be found by calling the `magic()` function with the username as argument to find 'cvoozYs4ut5n'.

When entering thes two values in the login page, the egg is displayed:  
![](./18/egg18.png)
