
import docker


if __name__ == '__main__':
    print('| testanto conexão VMs docker Vagrant...')
    print('| ')
    print('| ')
    client = docker.DockerClient(base_url='tcp://192.168.50.11:2375');
    print('| status conexão 192.168.50.11:')
    if client.ping():
        print('|      CONECTADO!!');
    print('| ')
    client = docker.DockerClient(base_url='tcp://192.168.50.10:2375');
    print('| status conexão 192.168.50.10:')
    if client.ping():
        print('|      CONECTADO!!');
    print('| ')