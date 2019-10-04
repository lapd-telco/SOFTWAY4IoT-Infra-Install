import sys


class ClientsManager:
    def __init__(self, client):
        self.client = client

    def run_container(self, container):
        """
        Receive information about the container and run
        :param name:
        :return:
        """

        print('Running container:\t' + container['image'])

        if 'container_name' in container:
            string_container_name = container['container_name']

        else:
            string_container_name = ""

        if 'ports' in container:

            container_ports_list = container['ports']

            for item in container_ports_list:
                string_container_ports = item

            string_ports = string_container_ports.split(':', 1)

            dict_ports = {string_ports[0] + '/tcp': string_ports[1]}

        else:
            dict_ports = {}

        if 'extra_hosts' in container:

            for item in container_ports_list:
                string_container_extra_hosts = item

            string_extra_hosts = string_container_extra_hosts.split(':', 1)

            dict_extra_hosts = {string_extra_hosts[0]: string_extra_hosts[1]}

            dict_extra_hosts = {}

        else:
            dict_extra_hosts = {}

        if 'command' in container:
            string_command = container['command']

        else:
            string_command = ""

        if 'volumes' in container:

            list_container_volumes = container['volumes']

        else:
            list_container_volumes = []

        if 'healthcheck' in container:

            healthcheck = container['healthcheck']

            healthcheck['test']

            dict_healthcheck = {'test': healthcheck['test']}

        else:
            dict_healthcheck = {}

        if 'environment' in container:
            dict_environment = container['environment']

        else:
            dict_environment = []

        if 'network_mode' in container:
            string_network_mode = container['network_mode']

        else:
            string_network_mode = "none"

        if 'privileged' in container:
            privileged_bool = container['privileged']

        else:
            privileged_bool = False

        if 'labels' in container:
            dict_labels = container['labels']

        else:
            dict_labels = {}

        if 'shm_size' in container:
            string_shm_size = container['shm_size']

        else:
            string_shm_size = ""

        if 'cap_add' in container:
            list_cap_add = container['cap_add']

        else:
            list_cap_add = []

        if 'cap_drop' in container:
            list_cap_drop = container['cap_drop']

        else:
            list_cap_drop = []

        if 'cgroup_parent' in container:
            string_cgroup_parent = container['cgroup_parent']

        else:
            string_cgroup_parent = ""

        if 'restart_policy' in container:
            dict_restart_policy = container['restart_policy']

        else:
            dict_restart_policy = {}

        if 'devices' in container:
            list_devices = container['devices']

        else:
            list_devices = []

        if 'init' in container:
            bool_init = True

        else:
            bool_init = False

        if 'isolation' in container:
            string_isolation = container['isolation']

        else:
            string_isolation = ""

        if 'pid_mode' in container:
            string_pid_mode = container['pid_mode']

        else:
            string_pid_mode = ""

        if 'security_opt' in container:
            list_security_opt = container['security_opt']

        else:
            list_security_opt = []

        if 'stop_signal' in container:
            string_stop_signal = container['stop_signal']

        else:
            string_stop_signal = ""

        if 'sysctls' in container:
            dict_sysctls = container['sysctls']

        else:
            dict_sysctls = {}

        if 'tmpfs' in container:
            dict_tmpfs = container['tmpfs']

        else:
            dict_tmpfs = {}

        if 'ulimits' in container:
            list_ulimits = container['ulimits']

        else:
            list_ulimits = []

        if 'user' in container:
            string_user = container['user']

        else:
            string_user = ""

        if 'userns_mode' in container:
            string_userns_mode = container['userns_mode']

        else:
            string_userns_mode = ""

        if 'volume_driver' in container:
            string_volume_driver = container['volume_driver']

        else:
            string_volume_driver = ""

        container_id = self.client.containers.run(image=container['image'], detach=True, name=string_container_name,
                                                  network_mode=string_network_mode, ports=dict_ports,
                                                  command=string_command, volumes=list_container_volumes,
                                                  extra_hosts=dict_extra_hosts, healthcheck=dict_healthcheck,
                                                  environment=dict_environment, privileged=privileged_bool,
                                                  labels=dict_labels, shm_size=string_shm_size, cap_add=list_cap_add,
                                                  cap_drop=list_cap_drop, cgroup_parent=string_cgroup_parent,
                                                  restart_policy=dict_restart_policy, devices=list_devices,
                                                  init=bool_init, isolation=string_isolation,
                                                  pid_mode=string_pid_mode, security_opt=list_security_opt,
                                                  stop_signal=string_stop_signal, sysctls=dict_sysctls,
                                                  tmpfs=dict_tmpfs, ulimits=list_ulimits, user=string_user,
                                                  userns_mode=string_userns_mode, volume_driver=string_volume_driver)

        container_id = str(container_id)

        print(container_id)

        container_id = container_id.split(':', 1)

        container_id = container_id[1][:11].replace(" ", "")

        print("container ID: \t" + str(container_id))
        print("OK")

        return str(container_id)

    def running_container_list(self):
        """
        Return a list with all running containers
        :param id: id of container to stop
        :return:
        """

        print("Container List:")

        for container in self.client.containers.list():
            sys.stdout.write(container.name + '\t')

        print(" ")

    def start_container(self, name):
        """
        Return True if the container was started again, or False if not.

        :param name: container name to start
        :return: True or False
        """

        for container in self.client.containers.list(all=True):
            if container.name == name:
                if container.status == 'exited':
                    print("Starting container: \t" + name)
                    container.start()

                return True

        return False

    def remove_container(self, id):
        """

        :param name:
        :return:
        """

        container = self.client.containers.get(id)
        print("Remove container: \t" + id)
        container.remove()

        return True

    def stop_container(self, id):
        """
        Receive the information about the container and stop this container
        :param id: container id or name to stop
        :return: True if everything is okay or false if not
        """

        container = self.client.containers.get(id)

        print("Stopping container: " + id)
        container.stop()

        for container in self.client.containers.list():
            if container.id == id:
                return False

        return True

    def stop_all_containers(self):
        """
        Stop all running containers
        :param client:
        :return: True if everything is okay or false if not
        """

        for container in self.client.containers.list():
            print(container.name + " stoped")
            container.stop()

        if not self.client.containers.list():
            return True

        else:
            return False

    def container_prune(self):
        """
        Remove all stopped containers
        :param
        :return:
        """

        self.client.containers.prune()

