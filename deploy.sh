#!/bin/bash

IP=192.168.6.108
#FILES=('./src/micro-nfd.py' './src/faces/routes.py' './src/config/config.py' './src/fw/fw.py' './src/fw/ndn.py' './src/faces/udp.py' './src/faces/face_table.py' './src/faces/lora.py' './src/core/sx127x.py')
FILES=('./src/fw/fw.py' './src/faces/lora.py')

kill_proc(){
    exit
}
trap kill_proc SIGINT

for f in "${FILES[@]}"
do
 echo uploading ${f##*/} from $f .......
 ./webrepl/webrepl_cli.py $f $IP:/${f##*/} -p good2cu
 echo -e "\033[0;32m success... \033[0m"
done
