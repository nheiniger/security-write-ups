26 - Hidden Egg #2
==================
> This egg is hidden in a very subtile manner. Perhaps you need to browse on the edge.

Here we need some Windows knowledge. Someone had to give me a tip to look out of the browser until I finally found that the egg is hidden in the Windows Start menu. In IE11 and edge you can pin websites to the start menu as a tile. The egg is hidden there, some documentation from Microsoft is available here <https://docs.microsoft.com/en-us/previous-versions/windows/internet-explorer/ie-developer/platform-apis/dn320426(v=vs.85)>

To find out what image to use for the tile, Windows looks for the config file `browserconfig.xml` at the root of the website. The one for hackyeaster.hacking-lab.com is as follows:
```xml
<browserconfig>
	<msapplication>
		<tile>
			<square70x70logo src="https://hackyeaster.hacking-lab.com/hackyeaster/images/tiles/mstile-70x70.png"/>
			<square150x150logo src="https://hackyeaster.hacking-lab.com/hackyeaster/images/tiles/mstile-270x270.png"/>
			<square310x310logo src="https://hackyeaster.hacking-lab.com/hackyeaster/images/tiles/mstile-310x310.png"/>
			<wide310x150logo src="https://hackyeaster.hacking-lab.com/hackyeaster/images/tiles/mstile-310x150.png"/>
			<TileColor>#4923a0</TileColor>
		</tile>
	</msapplication>
</browserconfig>
```

Now we only need to get the biggest image to get our egg <https://hackyeaster.hacking-lab.com/hackyeaster/images/tiles/mstile-310x310.png>:
![](./26_egg.png)
