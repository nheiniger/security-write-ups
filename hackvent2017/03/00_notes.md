Day 03: Strange Logcat Entry
============================
> *Lost in messages*
> 
> I found those strange entries in my Android logcat, but I don't know what it's all about... I just want to read my messages!

In this challenge, we get a logcat with many lines to look at. One stands out though because it is long and looks like some encoded data:
```
11-13 20:40:24.044      137       137  DEBUG: I 07914400000000F001000B913173317331F300003AC7F79B0C52BEC52190F37D07D1C3EB32888E2E838CECF05907425A63B7161D1D9BB7D2F337BB459E8FD12D188CDD6E85CFE931
```

After some tries at decoding this hexadecimal blob I saw a bit before a line that started in a similar fashion:
```
11-13 20:40:13.542       137   137 I DEBUG       :                      FAILED TO SEND RAW PDU MESSAGE
```

Then googling for `RAW PDU MESSAGE` immediately leads to online services that offers to decode SMS Packet Data Units (PDU). I used the one at <https://www.diafaan.com/sms-tutorials/gsm-modem-tutorial/online-sms-pdu-decoder/> and the result is:
```
Text message
To: +13371337133
Message: Good Job! Now take the Flag: HV17-th1s-isol-dsch-00lm-agic
```
