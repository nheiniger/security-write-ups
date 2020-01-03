Day 07: TrivialKRYPTO 1.42
--------------------------
In this challenge we are presented with a code that looks like some crypto mechanism using CRC32 function. When looking closely we see that everything happens client-side in JavaScript. We can assume that the result, if we can find the correct password, will be the flag being displayed.

Here is the interesting script excerpt:
```javascript
s3cr3t=[2155568001, 3847164610, 2684356740, 2908571526, 2557362074, 2853440707, 3849194977, 3171764887];
document.getElementById('decrypt').onclick = function() {
    var pass = document.getElementById('pass').value;
    
    var s="";
    for(var i=0;i<s3cr3t.length;i++) {
        var pp="";
        for(var p = (s3cr3t[i] ^ crc32(pass)); p>0; p>>=8) {
            pp = String.fromCharCode(p&0xFF)+pp;
        }
    s+=pp;
}
```

From there on, we know that the string "s" that is being generated must be the flag and thus it starts with HV16. We can do a known-plaintext attack against the system and try to guess what the crc32(pass) value will be. Since this value does not change we only need to find it once and it will be our key, we don't need the password :)

For the first iteration s3cr3t[0] is used so we need to find a guess such that:
```
s3cr3t[0] ^ guess = 'HV16'
=> s3cr3t[0] ^ 'HV16' = guess
=> guess = 0b10000000011110110101101110000001 ^ 0b01001000010101100011000100110110
=> guess = 0xc82d6ab7
```

When modifying the page to input this value instead of crc32(pass) we see in the browser's debugger that 'HV16' is correctly generated. And if we let the script run through the end the whole flag is generated:

> HV16-bxuh-b3ep-1PCU-b9ft-CgVu
