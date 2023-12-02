This directory was created by a project by: https://github.com/EricNaber/deploy_rippled_docker_testnet


Attack on Common Prefix: 
1. docker-compose up -d
2. python network_delay.py
3. python common_prefix_attack.py
4. the monitoring

Angriff auf Liveness:
1. docker-compose up -d
2. python network_delay.py
3. docker exec -it validator_XY bash
4. rippled submit snoPBrXtMeMyMHUVTgbuqAfg1SUTb '{"Account":"rHb9CJAWyB4rj91VRWn96DkukG4bwdtyTh","Amount": "1500000000","Destination":"rfhWbXmBpxqjUWfqVv34t4pHJHs6YDFKCN","TransactionType": "Payment","Fee": "10" }'
5. rippled attack
6. rippled unfreeze
