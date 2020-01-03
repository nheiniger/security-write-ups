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