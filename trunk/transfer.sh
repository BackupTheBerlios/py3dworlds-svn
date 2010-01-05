#! /bin/sh
rsync  -avz  --numeric-ids -e 'ssh -p 22'  ./ root@cdonner.de://Py3D-Worlds 

#scp -r /opt/Projekte/PyLife/* root@cdonner.de://PyLife
