# Build Docker Images for this project

This directory contains different Dockerfiles to create images based on rippled. It can be distinguished between versions (1.4.3 - latest) and type of attack (standard, liveness, common_prefix). The names of the folders are as follows: 
```
folder-name: build_<attack_type>_<version>
```

## Build
```
- cd <foldername>
- docker-build -t rippled_<attack_type>_<version> .
- docker run -it rippled_<attack_type>_<version> "rippled --version"
    -> to verify a correct installation process
```
