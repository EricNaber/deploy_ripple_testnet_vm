# Validator-Servers Key Material

1. docker run -it --entrypoint /bin/bash xrpllabsofficial/xrpld:latest
2. cd /opt/ripple/bin &&
    ./validator-keys create_keys --keyfile /PATH/TO/YOUR/validator-<NUMBER>-keys.json
3. cat /PATH/TO/YOUR/validator-<NUMBER>-keys.json
4. copy public_key from json-files
5. create validator token:
	./validator-keys create_token --keyfile /PATH/TO/YOUR/validator-<NUMBER>-keys.json

## Source
https://xrpl.org/private-network-with-docker.html
