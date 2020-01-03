12 - Once Upon a File
---------------------
In this challenge a weird file is provided that looks like a disk image. I tried to mount it and found nothing interesting in the NTFS partition. I tried to find data inside using TestDisk and Autopsy without success. Finally I tried with binwalk and this worked like a charm. The process is as follows, first, extract the original zip:
```
$ unzip onceupon.zip
Archive:  onceupon.zip
  inflating: file
```

Then binwalk on the "file" extracted with automatic extraction of known files:
```
$ binwalk -e file

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
36447         0x8E5F          Unix path: /0/1/2/3/4/5/6/7/8/9/:/;/</=/>/?/@/A/B/C/D/E/F/G/H/I/J/K/L/M/N/O/P/Q/R/S/T/U/V/W/X/Y/Z/[/\/]/^/_/`/a/b/c/d/e/f/g/h/i/j/k/l/m/n/o
184320        0x2D000         Zip archive data, at least v2.0 to extract, compressed size: 439156, uncompressed size: 5242880, name: file
623596        0x983EC         End of Zip archive
```

So it extracted a zip file out of which another "file" was extracted. Let's run binwalk again on this new "file":
```
$ binwalk -e file

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
36447         0x8E5F          Unix path: /0/1/2/3/4/5/6/7/8/9/:/;/</=/>/?/@/A/B/C/D/E/F/G/H/I/J/K/L/M/N/O/P/Q/R/S/T/U/V/W/X/Y/Z/[/\/]/^/_/`/a/b/c/d/e/f/g/h/i/j/k/l/m/n/o
1093632       0x10B000        Microsoft Cabinet archive data, 17834 bytes, 1 file
2832320       0x2B37C0        Microsoft Cabinet archive data, 17834 bytes, 1 file
3116030       0x2F8BFE        Microsoft executable, MS-DOS
3788479       0x39CEBF        mcrypt 2.2 encrypted data, algorithm: blowfish-448, mode: CBC, keymode: 8bit
3793983       0x39E43F        mcrypt 2.2 encrypted data, algorithm: blowfish-448, mode: CBC, keymode: 8bit
4477995       0x44542B        mcrypt 2.2 encrypted data, algorithm: blowfish-448, mode: CBC, keymode: SHA-1 hash
5073287       0x4D6987        mcrypt 2.2 encrypted data, algorithm: blowfish-448, mode: CBC, keymode: 8bit
5075359       0x4D719F        mcrypt 2.2 encrypted data, algorithm: blowfish-448, mode: CBC, keymode: 8bit
5173248       0x4EF000        PNG image, 480 x 480, 8-bit colormap, non-interlaced
5173767       0x4EF207        Zlib compressed data, best compression
```

As we can see lots of files were extracted but when listing the directory only one looks important, `egg12.png` and indeed, this is the egg:  
![](./12/egg12.png)
