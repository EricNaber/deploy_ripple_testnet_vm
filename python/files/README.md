This directory was created by a project from: https://github.com/EricNaber/deploy_rippled_docker_testnet


Angriff	auf Common Prefix: 

1. Hochfahren der Docker-Container (docker-compose up -d)
2. Deployen der Network	Delays (network_delay.py)
3. Transaction 1: Genesis -> Source 
4. Gleichzeitiges submitten von transaction_dest1.sh und transaction_dest2.sh
   -> Source -> rG1eMis	bzw. Source -> rnkP5Ti
   -> common_prefix_attack.py (nutzt Threads und Semaphoren, um Gleichzeitigkeit bestmöglich umzusetzen)
5. Im Monitoring sieht man einen Fork des Netzwerkes
