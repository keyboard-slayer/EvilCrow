# EvilCrow
A little virus for stealing Bulrezo's credential

## How does it works ?
According to Bulrezo's documentation, teacher, director, etc ... Have to go to a link like http://pythomium/bul/<schoolCode>.html. You notice that the website only use HTTP, that were is the vulnerability.

The first stage of the virus disable UAC and check if the website is correctly spoof in the HOSTS file (in C:\Windows\System32\drivers\etc\hosts). 

in the second stage the virus create a http server that spoof only the link template you can see above. and put a simple XSS payload that create a very convincing form that ask to the victim it information and give it to an attacker (:warning: this phase is not completed at a 100% :warning:)

The only fix that the virus need is a way to fix the image and the title