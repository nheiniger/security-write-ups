10 - Level Two
==============
> So you managed to beat the boss in the teaser game? This one won't be that easy!
> 
> You'll need RPG Maker Run Time Packages to run the game.
> 
> Hints: there are several parts to be found. Combine them, and enter the final flag in the egg-o-matic below, without spaces! Saving the game from time to time certainly helps.

Here we get the follow-up of the teaser challenge. The solution is not fundamentally different. I used 2 tools, first one to edit the game save files called RPGMakerSaveEdit and available from <http://www.ulmf.org/bbs/showthread.php?t=28936> and one tool to search and edit the memory of the game process in real time called Cheat Engine <http://www.cheatengine.org>.

I started by editing the save file to level up to level 99 and get every items (including the final egg and the key). This already gave me one part of the flag, namely:
```
7034353577307264355f3472335f6330306c
```

Then I used Cheat Engine to make easy movements even where it was not allowed to due to game mechanics. This allowed me to pass through the levels easily. Along the way I found a seond flag on a sign just after escaping the prison:
```
7034353577307264355f052d066b15035433
```

One more was one level 1 (green level with rain):
```
70343535773072105d6c6b05032d0f546f4c
```

And the last one was on level 3, after a barred door:
```
7034353577307264355f3406033b5749114c
```

The challenge description says that we need to combine the parts so I XORed each 3 "level" flags with the egg flag to get the following:
```
1_54v3d_
t0d4y!
th3_w0rld_
```

Which is combined to `1_54v3d_th3_w0rld_t0d4y!`. When entering this as password, the egg is revealed:
![](./10_egg.png)
