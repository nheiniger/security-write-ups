27 - Hidden Egg #3
==================
> *Got appetite? What about an egg for launch?*

This hint leads to the application launch screen and indeed when launching the application it looks like there is an egg hidden at the bottom of the screen. When looking at the source code of the application that we previously decoimpiled with jadx we see a class `ps.hacking.hackyeaster.android.SplashActivity` and a `splash.xml` file.

In `splash.xml` we see the following line:
```xml
<ImageView android:id="@+id/imageView" android:layout_width="240dp" android:layout_height="240dp" android:layout_marginBottom="-230dp" android:src="@drawable/jc_launcher" android:scaleType="centerCrop" android:layout_alignParentBottom="true" android:layout_centerHorizontal="true"/>
```

And we sse that the file to be displayed is `drawable/jc_launcher` this can be easily retrieved in jadx and is actually our egg already:
![](./27_egg.png)
