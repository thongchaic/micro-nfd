#!/bin/bash

IP=192.168.0.101

#FILES=('./src/nfd.py' './src/main.py' './src/misc/ping.py' './src/fw/routes.py' './src/config/config.py' './src/fw/fw.py' './src/core/ndn.py' './src/core/sx127x.py' './src/faces/face_table.py' './src/faces/lora.py' './src/faces/mqtt.py' './src/utils/pit.py'  './src/misc/experiments.py')
#FILES=('./src/main.py' './src/faces/mqtt.py' './src/core/ndn.py' './src/config/config.py')
FILES=('./src/main.py' './src/faces/mqtt.py')

kill_proc(){
    exit
}

trap kill_proc SIGINT

for f in "${FILES[@]}"
do

 echo uploading ${f##*/} .......
 ./webrepl/webrepl_cli.py $f $IP:/${f##*/} -p good2cu
 #./webrepl/webrepl_cli.py $IP:${f##*/} ${f##*/} -p good2cu
 echo -e "\033[0;32m success... \033[0m"
done

# ./webrepl/webrepl_cli.py ./src/misc/wifi.py $IP:main.py -p good2cu
