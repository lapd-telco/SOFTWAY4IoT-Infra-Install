# SOFTWAY4IoT-Orch

Exemplo de comando para atribuir a chave requisição no etcd do softway

	etcdctl mk /softway/requisition "{\"command\": \"containerStop\", \"containerName\": \"db-mongo\", \"host\": \"yes\", \"yamlName\": \"docker-compose.yml\", \"ipPort\": \"10.16.0.130:2375\"}"

Significado de cada variável do JSON passado por parâmetro:

	host = (yes/no) caso o gateway a realizar uma ação é o host do cli, ou outro gateway configurado pelo docker daemon comm.
	ipPort = o ip:porta do gateway a ser acessado remotamente pelo docker daemon comm.
	command = "runYaml", "containerStop", "stopAllContainers", "containerPrune", "containerList".
	containerName = nome do container a executar alguma ação.
	yamlName = nome do arquivo yaml ou yml que deseja ser executado (por enquanto arquivo na pasta raiz sempre).

Iniciar servidor etcd para acesso remoto:

	etcd --name infra1 --data-dir infra1   --auto-tls --peer-auto-tls   --initial-advertise-peer-urls=http://10.16.0.118:2380 --listen-peer-urls=http://10.16.0.118:2380 --listen-client-urls http://10.16.0.119:2379 --advertise-client-urls http://10.16.0.119:2379

### Implantação do GatewayManager
Abaixo, segue um exemplo de execução do playbook de implantação do Gateway Manager:

```
ansible-playbook -v  manager.yml -i hosts -e "fiware_deploy=true"
```
onde:

`-v` representa o nível de verbosidade de log durante o processo de implantação. Pode-se utilizar *-v*, *-vv*, *-vvv* e *-vvvv*. Quanto maior a quantidade de *v* mais **verboso** será o log. `manager.yml` representa o playbook
    