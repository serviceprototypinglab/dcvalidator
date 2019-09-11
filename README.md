# Docker Compose Validator
## Idea
When we are using docker-compose, we may make some silly mistake. This tool has this responsibility to remind you of these mistakes.
<br />For example:
``` yaml
version: '3'

services:
         eim:
                image: elastest/eim:latest
                depends_on:
                        - edm-mysql  
                stdin_open: true
                tty: true
                environment:
                        - ET_EDM_ALLUXIO_API=http://edm-alluxio-master:19999/
                        - ET_EDM_MYSQL_HOST=edm-mysql
                        - ET_EDM_MYSQL_PORT=3306
                        - ET_EDM_ELASTICSEARCH_API=http://edm-elasticsearch:9200/
                        - ET_EDM_API=http://edm:37003/
                        - ET_EPM_API=http://epm:37002/
                        - ET_ETM_API=http://etm:37006/
                        - ET_ESM_API=http://esm:37005/
                        - ET_EIM_API=http://eim:37004/
                        - ET_ETM_LSBEATS_HOST=etm-beats
                        - ET_ETM_LSBEATS_PORT=5044
                        - ET_ETM_LSHTTP_API=http://etm-logstash:5002/
                        - ET_ETM_RABBIT_HOST=etm-rabbitmq
                        - ET_ETM_RABBIT_PORT=5672
                        - ET_EMP_API=http://eim:37001/
                        - ET_EMP_INFLUXDB_API=http://emp-influxdb:8086/
                        - ET_EMP_INFLUXDB_HOST=emp-influxdb
                        - ET_EMP_INFLUXDB_GRAPHITE_PORT=2003
                expose:
                        - 8080
                ports:
                        - "37004:8080" 
                networks:
                        - elastest
                labels:
                        - io.elastest.type=core
networks:
        elastest:
                driver: bridge
```
This is a docker-compose that works correctly!
But imagine that you need more services. More services mean that docker-compose should be more complicated! And at this point, human mistakes showing up! I'll add more services, and at this point, I forgot that two of them have the same name, but <b>THEY ARE NOT THE SAME SERVICE!</b>
<br />Simply I'll lose one of my services!

``` yaml
version: '3'

services:

  service1:
    /* Some stuff */

  service2:
    /* Some other stuff */
    
    
    ************ OTHER SERVICES ************
    
    service-n:
        /* Some stuff */
    
    service2:   <---------------- DUPLICATE SERVICE! ----------------
        /* Some stuff */    
    
```




Another example:
Imagine you are new to docker-compose
``` yaml
version: '3'

services:

  service1:
    /* Some stuff */

  service2:
    /* Some other stuff */
    
volumes:   <---------------- NOT IN A GOOD PLACE! ----------------
  db-data:


networks:
  something:
    external: true
    
```
Well this might happened to every newcomer with docker-compose!<br />
<br />
### This tool can analyze your docker-compose file with Github link or uploading the file.
<br />
<br />
<br />
<br />
**********************************************************************************************************

## How to use it
Just go [HERE](http://160.85.252.231:3000/) and enjoy!

## How to make it better
Make sure you have node.JS, npm, yarn, python 3, pip on your machine.
<br />Then follow these steps:
<br />
<b>
1. Download it as a zip file or clone it!
2. Change your directory to the project directory   
3. `yarn`
4. `yarn install-client`
5. `yarn install-server`
6. `yarn dev`
</b>
You are ready to go!

## Can I contribute?
<b>YES!</b> <br />
Feel free to add some features!