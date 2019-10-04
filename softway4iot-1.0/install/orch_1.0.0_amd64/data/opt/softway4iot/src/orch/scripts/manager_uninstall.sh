 sudo ovs-vsctl del-br br-data
 sudo ovs-vsctl del-br br-control

 sudo apt-get purge -y strongswan
 sudo apt-get auto-remove -y --purge strongswan
 sudo apt-get purge -y openvswitch-switch
 sudo apt-get auto-remove -y --purge openvswitch-switch
 
 sudo  apt-get purge -y docker-engine docker docker.io docker-ce  
 sudo apt-get autoremove -y --purge docker-engine docker docker.io docker-ce 
 rm -rf /var/lib/docker /etc/docker
 rm /etc/apparmor.d/docker
 groupdel docker
 rm -rf /var/run/docker.sock

 rm -r /var/lib/etcd/
 rm -r /etc/etcd
 rm /usr/local/bin/etcd
 rm /usr/local/bin/etcdctl
 rm -r /etc/softway4iot
 rm -r /usr/bin/ovs-docker
