#!/usr/bin/perl

use Image::Magick;

$im = new Image::Magick;
$im->Read("MandM.gif");

my $x=0;
my $y=0;
for ($x=0; $x<291; $x++) {
	for ($y=0; $y<291; $y++) {
		my @pixel = $im->GetPixel(x=>$x, y=>$y);
		if ($pixel[0] != 1 || $pixel[1] != 1 or $pixel[2] != 1) {
#			print($pixel[0]*255 . "," . $pixel[1]*255 . "," . $pixel[2]*255 . "\r\n");
			
		}
	}
	print("\r\n");
}
