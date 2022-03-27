---
layout: post
title:  "Insomni'hack 2022 - Can't C"
date:   2022-03-27 12:00:00 +0000
categories: [ Security ]
tags: [ ctf, write-up, insomnihack, en ]
---
In this challenge we are given several files:
- `train.txt`, a text file with a specific text
- `train.raw`, a raw audio file containing the recording of someone typing the text of `train.txt`
- `password.raw`, a raw audio file containing the recording of someone typing his password
- `english.txt`, a dictionary with english words
We knew that the password and the training text were typed on the same keyboard and that the password consist of 8 lowecase words separated by a space.

To solve this challenge, we use a tool named Skype&Type, and more precisely, a fork of the original tool allowing for python3: <https://github.com/yossigor/Skype-Type>. As a first step, the readme specifies that the audio files must be *.wav (Microsoft), 32bit float PCM*. We can convert the raw audio in that format easily with Audacity. We also take the opportunity to remove the mouse clicks at the end of the password file, just to avoid any issue there. Then, again from the readme, the text file must have exactly ine character per line and contain no space (replaced here by '-').
```bash
$cat ~/Desktop/cantc/text.txt | sed 's/ /-/g' | sed -r 's/(.)/\1\n/g' > cantc-train/train.txt
```

Then, we need to train the tool (generate a model). This is done as follows (where `cantc-train` is a folder containing the text and audio files):
```bash
$ python3 generate_model.py cantc-train model
Found 1 files already mined
Found 0 files to mine
Learning...
Learning task completed!
Writing model to disk
Estimating accuracy...
0.7272727272727274
```

Then, we can run the model against the password recording:
```bash
$ python3 main.py --opmode from_file --target cantc-password/password.wav --pipeline model
```

The tool then lists the predictions for each character:
```
PREDICTIONS
0 - ['r', 'n', 'g', 'h', 'e', 't', 'v', '-', 'y', 'm']
1 - ['l', 'o', 'd', 'm', 'a', 'h', 'e', 'p', 'n', 'x']
2 - ['a', 't', 'd', 'u', 'x', 's', 'v', 'm', 'e', 'q']
3 - ['b', 'e', 'n', 'u', 'l', 'h', 'm', 'k', '-', 'o']
4 - ['c', 'v', 'm', 'e', 'j', 'z', 'h', 't', 'x', 'b']
5 - ['e', 't', 'f', 'w', 'q', 'o', 'u', 'g', 'y', 'x']
6 - ['-', 'h', 'r', 'b', 'g', 'm', 'v', 'd', 'p', 'y']
7 - ['f', 'd', 'a', 's', 'g', 'e', 't', 'j', 'z', 'v']
8 - ['o', 'u', 'l', 'e', 't', 'r', 'i', '-', 'h', 'p']
9 - ['v', 'h', 'm', '-', 'd', 't', 'n', 'g', 'f', 'b']
10 - ['-', 'm', 'z', 'v', 'o', 'c', 't', 's', 'p', 'g']
11 - ['d', 'h', 's', 'f', 'e', 'z', 'x', 'v', 'a', 't']
12 - ['e', 't', 'w', 'y', 'v', 'n', 'h', 'r', '-', 'm']
13 - ['h', 'o', 'l', 'n', 'e', 'c', 'u', 'p', '-', 'm']
14 - ['u', 'y', 'o', 'h', 't', 'i', 'n', 'b', 'r', 'k']
15 - ['-', 'q', 'r', 'p', 'h', 'n', 'b', 'y', 'w', 'm']
16 - ['s', 'd', 'z', 'a', 'f', 'x', 'w', 'h', 'e', 'v']
17 - ['t', 'f', 'e', 'w', 's', 'j', 'o', 'g', 'b', 'r']
18 - ['e', 'r', 'o', 't', 'v', 'a', '-', 'n', 'g', 'w']
19 - ['o', 'i', 'u', 't', 'h', 'r', 'j', 'p', 'm', 'l']
20 - ['v', 'm', 'h', '-', 't', 'u', 'n', 'b', 'g', 'e']
21 - ['g', 'f', 't', 'b', 'd', 'j', 'e', 'h', 'v', 'n']
22 - ['-', 't', 'v', 'z', 'h', 'j', 'b', 'o', 'a', 'f']
23 - ['l', 'k', 'm', 'h', 'e', 'p', 'a', 'o', 'q', '-']
24 - ['e', 'w', 'f', 'o', 'v', 'z', 'g', 'x', 't', 'r']
25 - ['m', 'b', 'h', 'v', 'n', '-', 'u', 'g', 'k', 'i']
26 - ['d', 's', 'z', 'f', 'x', 'a', 'v', 'h', 'e', 't']
27 - ['-', 'e', 'r', 'b', 'n', 'h', 'v', 'q', 'y', 'w']
28 - ['-', 'e', 'r', 'h', 'n', 'a', 'u', 'g', 'z', 'y']
29 - ['p', 'o', 'k', 'l', 'a', 'h', 'u', 'q', 'r', 'i']
30 - ['r', 'e', 't', 'a', 'b', 'u', 'y', 'o', 'g', 'n']
31 - ['i', 'o', 'h', 'u', 'y', 'p', 'g', 't', 'n', 'l']
32 - ['m', 'v', '-', 'u', 'e', 'j', 'x', 'h', 'c', 'n']
33 - ['s', 'a', 'w', 'd', 'o', 'z', 't', 'f', 'u', 'g']
34 - ['t', 'e', 'g', 'r', 'd', 'w', 'f', 'a', 'j', 'p']
35 - ['e', 't', 'o', 'u', 'y', 'v', 'h', 'r', 'w', 'x']
36 - ['-', 'h', 'm', 'y', 'b', 'i', 'p', 'k', 'r', 'n']
37 - ['f', 'd', 'e', 's', 'w', 'z', 't', 'a', 'b', 'g']
38 - ['e', 't', 'r', 'o', 'n', '-', 'w', 'v', 'g', 'h']
39 - ['o', 'i', '-', 'y', 't', 'h', 'u', 'e', 'k', 'r']
40 - ['n', 'b', 'm', 'h', 'k', 'p', 'u', 'e', 'l', 't']
41 - ['e', 'r', 'g', 'h', 'n', 'o', 'u', 'y', 't', 'v']
42 - ['e', 't', 'w', 'f', 'x', 'z', 'd', 'q', 'v', 'g']
43 - ['-', 't', 'm', 'v', 'z', 'x', 'f', 'g', 'c', 'b']
44 - ['t', 'e', 'v', 'j', 'n', 'o', 'h', 'u', 'w', 'x']
45 - ['o', 'e', 'u', 'i', 'h', 'n', 't', 'r', '-', 'k']
46 - ['m', 'n', 'h', 'k', 'p', 'b', 'l', '-', 'q', 'u']
47 - ['a', 'd', 'z', 'h', 's', 'w', 'e', 'v', 'q', 'x']
48 - ['t', 'r', 'n', 'e', 'h', 'g', 'y', 'a', 'z', 'o']
49 - ['o', 'p', 'e', 't', 'r', 'l', 'h', 'n', 'x', 'v']
50 - ['-', 'e', 'w', 't', 'q', 'v', 'b', 'm', 'y', 'r']
51 - ['-', 'e', 'w', 'm', 't', 'g', 'b', 'q', 'r', 'v']
52 - ['-', 'e', 'w', 't', 'n', 'm', 'k', 'v', 'b', 'c']
```

For some reason there are more characters than can be heard in the audio file... but we can already see some words, tomato at the end for example . The tool continues and asks some questions. We can specify which character separates the words ('-' in our case) and then the position of the spaces. They are detected correctly in the first column:
```bash
ARE THESE WORDS? [Y/n] Y
Which are the word separators? (separated with spaces): -
Hint me the correct word segmentation (Suggested spaces in [6, 9, 10, 15, 20, 22, 27, 28, 32, 36, 39, 43, 50, 51, 52]): 6 10 15 22 27 28 36 43 50 51 52 53
Available dictionaries:
0 - /home/jsmith/tools/Skype-Type/dictionaries/cantc-english.txt
1 - /home/jsmith/tools/Skype-Type/dictionaries/README.md
Select dictionary number ([0]): 0
```

After this, we get a list of possible words for each "slot":
```bash
WORD FROM CHARACTER 0 to 6
[('glance', 4), ('reduce', 11), ('notice', 13), ('bounce', 16), ('planet', 16), ('reject', 18), ('detect', 19), ('nature', 19), ('rotate', 19), ('enable', 22), ('gadget', 22), ('rocket', 22), ('volume', 22), ('rather', 23), ('remove', 23
), ('double', 24), ('source', 24), ('toilet', 24), ('addict', 25), ('expect', 25), ('gather', 25), ('insect', 25), ('plunge', 25), ('rabbit', 25), ('result', 25), ('robust', 25), ('lounge', 26), ('viable', 26), ('change', 27), ('retire',
 27)]

WORD FROM CHARACTER 7 to 10
[('fog', 7), ('fun', 7), ('dog', 8), ('arm', 9), ('aim', 10), ('fox', 10), ('sun', 10), ('fit', 11), ('gun', 11), ('art', 12), ('fly', 12), ('mom', 12), ('fee', 13), ('few', 13), ('all', 14), ('dad', 15), ('fat', 15), ('ten', 15), ('add'
, 16), ('dry', 16), ('fan', 16), ('fix', 16), ('gym', 16), ('job', 16), ('nut', 16), ('old', 16), ('put', 16), ('sea', 16), ('toe', 16), ('top', 16)]

WORD FROM CHARACTER 11 to 15
[('deny', 4), ('defy', 11), ('deer', 12), ('help', 13), ('hero', 13), ('menu', 13), ('rely', 13), ('sell', 14), ('stay', 14), ('seek', 15), ('belt', 16), ('echo', 16), ('melt', 16), ('seat', 16), ('seed', 16), ('tent', 16), ('feed', 17),
 ('feel', 17), ('rent', 17), ('slot', 17), ('spot', 17), ('stem', 17), ('step', 17), ('zero', 17), ('diet', 18), ('drop', 18), ('foot', 18), ('hint', 18), ('hunt', 18), ('only', 18)]

WORD FROM CHARACTER 16 to 22
[('strong', 7), ('derive', 11), ('devote', 17), ('spring', 18), ('strike', 18), ('daring', 19), ('during', 19), ('arrive', 20), ('second', 22), ('street', 22), ('series', 23), ('shrimp', 23), ('smooth', 23), ('boring', 24), ('device', 24
), ('script', 24), ('settle', 24), ('stereo', 24), ('amount', 25), ('asthma', 25), ('around', 26), ('assume', 26), ('attend', 26), ('define', 26), ('stairs', 26), ('afford', 28), ('artist', 28), ('autumn', 28), ('detect', 28), ('remove',
 28)]

WORD FROM CHARACTER 23 to 27
[('lend', 4), ('lens', 5), ('loud', 9), ('pond', 12), ('head', 13), ('leaf', 13), ('load', 13), ('home', 14), ('love', 14), ('kind', 15), ('hold', 16), ('hood', 16), ('menu', 16), ('mind', 16), ('move', 16), ('hand', 17), ('long', 17), (
'lava', 18), ('left', 19), ('mesh', 19), ('feed', 20), ('lamp', 20), ('limb', 20), ('need', 20), ('seed', 20), ('come', 21), ('keen', 21), ('keep', 21), ('live', 21), ('maid', 21)]

WORD FROM CHARACTER 29 to 36
[('private', 2), ('promote', 5), ('primary', 8), ('provide', 16), ('prepare', 24), ('leisure', 25), ('trumpet', 25), ('luggage', 27), ('project', 27), ('athlete', 28), ('laundry', 28), ('payment', 28), ('leopard', 29), ('produce', 29), (
'prosper', 29), ('sausage', 29), ('avocado', 30), ('cricket', 30), ('imitate', 30), ('stomach', 30), ('isolate', 31), ('situate', 31), ('ability', 32), ('educate', 32), ('mandate', 32), ('orchard', 32), ('prevent', 32), ('problem', 32), 
('protect', 32), ('utility', 32)]

WORD FROM CHARACTER 37 to 43
[('fringe', 5), ('toilet', 19), ('bronze', 20), ('desert', 20), ('friend', 20), ('degree', 21), ('double', 21), ('entire', 21), ('future', 21), ('lounge', 21), ('street', 21), ('frozen', 22), ('bridge', 23), ('depart', 23), ('detect', 23
), ('ensure', 23), ('forget', 23), ('helmet', 23), ('broken', 24), ('enough', 24), ('orange', 24), ('secret', 24), ('around', 25), ('bright', 25), ('define', 25), ('flight', 25), ('height', 25), ('nephew', 25), ('orient', 25), ('people',
 25)]

WORD FROM CHARACTER 44 to 50
[('tomato', 0), ('tenant', 7), ('donate', 13), ('inmate', 17), ('wonder', 17), ('debate', 18), ('vendor', 18), ('depart', 19), ('voyage', 19), ('potato', 20), ('render', 20), ('timber', 20), ('moment', 21), ('toward', 21), ('tunnel', 21)
, ('cement', 22), ('rotate', 22), ('velvet', 22), ('demand', 23), ('engage', 23), ('estate', 23), ('female', 23), ('number', 23), ('sunset', 23), ('tongue', 23), ('either', 24), ('tumble', 24), ('behave', 25), ('nephew', 25), ('vessel', 
25)]
```

And as we can see, the words are presented with a number representing the confidence that the word is correct (actually this is probably the minimal distance with the provided dictionary words). We had to do mmultiple runs and try several different combinations before getting the correct flag but in the end it worked. The final flag was `INS{glance fun deny strong lend primary fringe tomato}`. If you want to test it for yourself, here are [the original files](2022-03-27_insomnihack-cantc-files.zip).

Last note, I reproduced the challenge today on my machine for this write-up, but originally it was made by [@sploutchy](https://twitter.com/sploutchy). I only gave some suggestions and offered psychologic support while watching over his shoulder.
