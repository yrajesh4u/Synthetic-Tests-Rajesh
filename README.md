body_update_service Synthetic 
== 

This is a synthetic tests suite created to showcase the usage of pytest in the framework.

* build the docker image
```
make
```
* run the docker image locally
```
PROBE=(probe) TARGET=(target) make run
```
* push the docker image to TiVO artifactory
```
make deploy
```
