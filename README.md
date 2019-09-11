# Docker Compose Validator
## Idea
When we are using docker-compose, we may make silly mistakes. This tool helps you avoid making such mistakes!
<br />For example:
``` yaml
version: '3'

services:
    app:
        build: .
        image: takacsmark/flask-redis:1.0
        environment:
          - FLASK_ENV=development
        ports:
          - "4999-5005:4999-5005"
    redis:
        image: redis:4.0.11-alpine
```
This is a docker-compose that works correctly!
But imagine that you need more services. More services means complicated our docker-compose template! And at this point, human mistakes will probably show up! Say, we add more services, and at this point, we forgot that two of them share the same name, but <b>THEY ARE NOT THE SAME SERVICE!</b>
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
<br />
<br />
<br />


Another example:
Imagine you are new to docker-compose, and your template looks like this:
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