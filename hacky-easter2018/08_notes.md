08 - Disco Egg
==============
>
>    Make things as simple as possible but no simpler.
>
> -- Albert Einstein

After this quote we are given a link to a web page. On this web page is an egg blinking like a disco ball. This was done in JavaScript using jQuery. To prevent the blinking, one can remove the whole JavaScript from the page after saving it locally.

Then, to get the egg itself, it was sufficient to remove all color classes from the table forming the QR-code except for the black and white and apply the background color accordingly. So now we have a table with cells that are either white or black, i.e.:
```html
<td class="white" style="background-color: rgb(255,255,255);"/>
<td class="black" style="background-color: rgb(0,0,0);"/>
```

One can then simply open the html page in a browser to see the egg displayed:
![(./08_egg.png)
