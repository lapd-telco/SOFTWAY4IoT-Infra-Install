from docker_comm.clients_manager import ClientsManager
from docker_comm.etcd_manager import EtcdManager
import docker
import yaml
import json
import etcd


if __name__ == '__main__':

    etcdClient = etcd.Client(host='127.0.0.1', port=2379)

    etcdClass = EtcdManager(etcdClient)

    while True:

        try:
            etcdClient.read('/softway/requisition')

        except etcd.EtcdKeyNotFound:
            continue

        else:

            result = etcdClass.read_key('/softway/requisition')

            etcdRequisition = json.loads(result.value)
            
            if etcdRequisition["host"] == 'yes':
                dockerClient = docker.from_env()
                
            else:

                certs_path = '/etc/softway4iot/docker_certs'
                tls_config = docker.tls.TLSConfig(client_cert=(certs_path + '/client-softway4iot-gatweway-cert.pem',
                certs_path + '/client-softway4iot-gatweway-key.pem'))
                
                ip_port = etcdRequisition["ipPort"]

                dockerClient = docker.DockerClient(base_url='tcp://' + ip_port, tls=tls_config)
            
            dockerRequisition = ClientsManager(dockerClient)

            if etcdRequisition["command"] == "runYaml":

                i = 0

                yamlFile = etcdRequisition["yamlName"]

                stream = open(yamlFile, 'r')

                container_id = dockerRequisition.run_container(yaml.safe_load(stream), etcdClass)

            if etcdRequisition["command"] == 'containerStop':
                container_name = etcdRequisition["containerName"]

                dockerRequisition.stop_container(container_name)
                
            if etcdRequisition["command"] == 'stopAllContainers':
                dockerRequisition.stop_all_containers()

            if etcdRequisition["command"] == 'containerPrune':
                dockerRequisition.container_prune()

            if etcdRequisition["command"] == 'startContainer':
                dockerRequisition.start_container(etcdRequisition["containerName"])

            if etcdRequisition['command'] == 'removeContainer':
                dockerRequisition.remove_container(etcdRequisition['containerName'])

            etcdClient.delete('/softway/requisition')
