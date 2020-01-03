Day 14: Happy Cryptmas
======================
> todays gift was encrypted with the attached program. try to unbox your xmas present.
> 
>     Flag: 7A9FDCA5BB061D0D638BE1442586F3488B536399BA05A14FCAE3F0A2E5F268F2F3142D1956769497AE677A12E4D44EC727E255B391005B9ADCF53B4A74FFC34C

A file including an executable was linked. Unzipping the file revealed a `hackvent` Mac OS 64 bit binary file that I could translate the `main` function to pseudo-code using hopper:
```
int _main(int arg0, int arg1) {
    var_8 = **___stack_chk_guard;
    var_70 = arg1;
    if (arg0 != 0x1) goto loc_100000cfd;

loc_100000e32:
    var_B0 = 0x0;
    if (**___stack_chk_guard == var_8) {
            rax = var_B0;
    }
    else {
            rax = __stack_chk_fail();
    }
    return rax;

loc_100000cfd:
    __gmpz_init(&var_50);
    __gmpz_init(&var_60);
    __gmpz_init_set_str(&var_20, "F66EB887F2B8A620FD03C7D0633791CB4804739CE7FE001C81E6E02783737CA21DB2A0D8AF2D10B200006D10737A0872C667AD142F90407132EFABF8E5D6BD51", 0x10);
    __gmpz_init_set_str(&var_40, "65537", 0xa);
    __gmpz_import(&var_50, strlen(*(var_70 + 0x8)), 0x1, 0x1, 0x0, 0x0, *(var_70 + 0x8));
    if (__gmpz_cmp(&var_50, &var_20) <= 0x0) goto loc_100000de4;

loc_100000ddf:
    rax = abort();
    return rax;

loc_100000de4:
    __gmpz_powm(&var_60, &var_50, &var_40, &var_20);
    __gmp_printf("Crypted: %ZX\n", &var_60);
    __gmpz_clears(&var_50, &var_60, &var_20, &var_40, 0x0);
    goto loc_100000e32;
}
```

To get a better understanding of the process I tried to re-implement the encryption operation in python. To be as close to the pseudo code as possible I came to:
```python
#!/usr/bin/python3

import sys
import binascii

# assign argument to var70
var70 = sys.argv[1]

# initialize variables (one from hex and one from decimal)
var20 = 0xF66EB887F2B8A620FD03C7D0633791CB4804739CE7FE001C81E6E02783737CA21DB2A0D8AF2D10B200006D10737A0872C667AD142F90407132EFABF8E5D6BD51
var40 = 65537

# import argument into var50
var50 = int.from_bytes(var70.encode(), byteorder='big')

# compare values and fail if argument is bigger
if var50 > var20:
        print('fail, arg is too long')
        exit()

# modular exponentiation
var60 = pow(var50, var40, var20)

print('Crypted: ' + hex(var60)[2:].upper())
```

This is actually RSA encryption:
```
c = m^e % n
```

Where we have:
```
n = 0xF66EB887F2B8A620FD03C7D0633791CB4804739CE7FE001C81E6E02783737CA21DB2A0D8AF2D10B200006D10737A0872C667AD142F90407132EFABF8E5D6BD51
c = 0x7A9FDCA5BB061D0D638BE1442586F3488B536399BA05A14FCAE3F0A2E5F268F2F3142D1956769497AE677A12E4D44EC727E255B391005B9ADCF53B4A74FFC34C
e = 0x10001
```

To break it we need to factor n, this is possible using <https://www.alpertron.com.ar/ECM.HTM> and it gives:
```
n = p * q
p = 0xfba54e792d79c98b
q = 0xfab2525ba803f8c8c46dc3daea399a4c2b83c83577803eff349abef1f0ee3cee304d3d1bf07886aa7c269a2bace77dfcfd7281faf82f5813
phi(n) = 0xf66eb887f2b8a62002517574bb3399028396afc1fdc465d0566317f20bf33da2e917e1e6be3ed3c3cfb32ff4830181c84a4112e882a8c27339d7db84c02d9bb4
```

To decrypt, we compute the private key d as the inverse of e modulo phi(n) :
```
d = e^-1 % phi(n) = 0xe3463615db7b046b5cf7f79592d90172da1d6d37426d9160d56b4ab846e12ca544c86be53cec00ae04ae43ba03e0adeb24e06329e0e6f77f0187dcc2cfe2c049
```

And then apply the decryption:
```
m = c^d % n = 0x485631372d35424d752d6d6744302d473753752d455973702d4d673062
```

Converting this to a string (in python) gives the flag:
```
>>> binascii.unhexlify(hex(m)[2:])
b'HV17-5BMu-mgD0-G7Su-EYsp-Mg0b'
```
