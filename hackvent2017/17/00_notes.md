Day 17: Portable NotExecutable
==============================
> here is your flag.
> 
> but wait - its not running, because it uses the new Portable NotExecutable Format. this runs only on Santas PC. can you fix that?

Here we get an executable that is actually not executable, when trying to run it, it fails. We first need to fix the file format to make it executable. To get an idea of how it should look like I compared with existing valid executables and had a look at the very valuable binary posters of Ange Albertini at <https://github.com/corkami/pics/tree/master/binary>.

I had to fiddle with the executable a lot but in the end, the following changes were required:

- Magic number at offset 0x0: 4D 5A (MZ)
- Field e_lfanew at offset 0x3c: 40 00 00 00 (pointer to start of PE header, 0x40)
- PE header signature at offset 0x40: 50 45 00 00 (PE/0/0)
- Number of section at offset 0x46: 04 00 (4 sections)
- Windows subsystem at 0x9c : 02 00 (Windows GUI)

Here is a diff of the start of both executables:
```diff
~/D/c/17 ❯❯❯ diff orig.txt final.txt
diff --git a/orig.txt b/final.txt
index d0284c1..07dbd41 100644
--- a/orig.txt
+++ b/final.txt
@@ -1,10 +1,10 @@
-00000000: 4d53 4000 0100 0000 0200 0400 ffff 0200  MS@.............
+00000000: 4d5a 4000 0100 0000 0200 0400 ffff 0200  MZ@.............
 00000010: 4000 0000 0e00 0000 1c00 0000 0000 0000  @...............
 00000020: 5769 6e33 3220 6f6e 6c79 210d 0a24 0eb4  Win32 only!..$..
-00000030: 09ba 0000 1fcd 21b8 014c cd21 2000 0000  ......!..L.! ...
-00000040: 504e 4500 4c01 0600 624b e4a0 4841 434b  PNE.L...bK..HACK
+00000030: 09ba 0000 1fcd 21b8 014c cd21 4000 0000  ......!..L.!@...
+00000040: 5045 0000 4c01 0400 624b e4a0 4841 434b  PE..L...bK..HACK
 00000050: 7665 6e74 e000 8e81 0b01 0219 0016 0000  vent............
 00000060: 0096 0000 0000 0000 721f 0000 0010 0000  ........r.......
 00000070: 0030 0000 0000 4000 0010 0000 0002 0000  .0....@.........
 00000080: 0100 0000 0000 0000 0400 0000 0000 0000  ................
-00000090: 00f0 0000 0002 0000 0000 0000 0300 0000  ................
+00000090: 00f0 0000 0002 0000 0000 0000 0200 0000  ................
```

Then, when running the program and clicking on the "Flag" button we get the following valid flag:
```
HV17-VIQn-oHcL-hVd9-KdAP-txiK
```
