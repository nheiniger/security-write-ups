14 - Same same...
=================
> *...but different!*
> 
> Upload the right files and make the server return an Easter egg!
> 
> `http://whale.hacking-lab.com:4444`

Here we get this description and the code of the web page:
```php
<?php
require __DIR__ . "/vendor/autoload.php"; // QR decoder library from https://github.com/khanamiryan/php-qrcode-detector-decoder

try {
    $qrcode1 = new QrReader($_FILES["file1"]["tmp_name"]);
    $answer1 = $qrcode1->text();
} catch(Exception $e) {
    exit("Error while reading the first QR.");
}

try {
    $qrcode2 = new QrReader($_FILES["file2"]["tmp_name"]);
    $answer2 = $qrcode2->text(); 
} catch(Exception $e) {
    exit("Error while reading the second QR.");
}

if(($answer1 == "Hackvent" && $answer2 == "Hacky Easter" or $answer1 == "Hacky Easter" && $answer2 == "Hackvent") && sha1_file($_FILES["file1"]["tmp_name"]) == sha1_file($_FILES["file2"]["tmp_name"])) {
    [SURPRISE]
}
else {
    echo ":-(";
}
?>
```

So it seems that we need to upload two files with the same SHA1 hash but that decode (as QR-code) to a different result. Thankfully SHA1 has been broken last year andit is now easy to generate collisions (at least for PDF files). Since this library supports PDF we can directly use any online service to generate QR-codes that decode to the expected strings, "Hackvent" and "Hacky Easter". Then send those to another online service that helps creating PDFs that have the same SHA1 hash but a different content, I used <https://alf.nu/SHA1>. This generates two files with the same hash and when uploading those files to the website we get the egg:
![](./14_egg.png)
