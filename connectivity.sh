#!/bin/sh

case "$(curl -s --max-time 2 -I http://google.com | sed 's/^[^ ]*  *\([0-9]\).*/\1/; 1q')" in
	  [23])  echo "HTTP connectivity is up "
		/path/to/launcher.sh;; #Edit to your path
	      5) echo "The web proxy won't let us through";;
	      *) echo "The network is down or very slow";;
esac
