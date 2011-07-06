#!/bin/sh
HOST=ax-k.de
USERNAME=marvin
PASSWORD=1.andreas.1

cd /home/marvin/Dropbox/Projektmaterial/Friedländer/lections
ftp -n $HOST <<EOD
quote USER $USERNAME
quote PASS $PASSWORD
cd /httpdocs/friedlaender/fileadmin/templates/tmailform
put *.tmpl
quit
EOD
exit 0