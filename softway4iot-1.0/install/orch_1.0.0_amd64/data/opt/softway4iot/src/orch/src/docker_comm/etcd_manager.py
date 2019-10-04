import etcd

class EtcdManager:
    def __init__(self, client):
        self.client = client

    def read_key(self, key):
        """
        Read and return a etcd key in the key parameter
        """
        return self.client.read(key)
    
    def set_key(self, path, value):
        """
        Set a etcd key in client, with the parameter value in path parameter
        """

        self.client.write(path, value)