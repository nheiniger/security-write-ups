23 - Lovely Vase
----------------
In this challenge we are given what looks like 3 ciphertexts. I noticed in a previous challenge that PS seems to know the site dcode.fr that provides lots of tools to encode/decode messages using known ciphers. I tried some of the most well-known on the ciphertexts. After some tries I found out that the second ciphertext is not encoded, it is only transposed using Railfence. The plaintext for the second part is then `the second part is susannabob`.

Seeing the form of the plaintext we can now try to find other transposition scheme to attack the first and third parts. For the third part, we start with the text `hacektpsrnediiahrtartirlf`.

Write the text in 5 columns starting top left and going down first:

| 1 | 2 | 3 | 4 | 5 |
| - | - | - | - | - |
| h | t | e | h | t |
| a | p | d | r | i |
| c | s | i | t | r |
| e | r | i | a | l |
| k | n | a | r | f |

Reorder the columns in the opposite order:

| 5 | 4 | 3 | 2 | 1 |
| - | - | - | - | - |
| t | h | e | t | h |
| i | r | d | p | a |
| r | t | i | s | c |
| l | a | i | r | e |
| f | r | a | n | k |

Read then from left to right and from top to bottom to have `the third part is clairefrank`.

For the first part, we start with the ciphertext `trickhesitenadrfairairstp`.

Write it in 5 lines as follows:

| 5 | 4 | 3 | 2 | 1 |
| - | - | - | - | - |
| t | r | i | c | k |
| h | e | s | i | t |
| e | n | a | d | r |
| f | a | i | r | a |
| i | r | s | t | p |

And then read it as the pattern shown on top of the vase (kind of a spiral) to have the plaintext `the first part is adrianerick`.

When entering those 3 parts in the right order and without any typo we are given the egg:  
![](./23/egg23.png)
