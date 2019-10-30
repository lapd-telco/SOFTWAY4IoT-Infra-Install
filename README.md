# SOFTWAY4IoT

The importance of IoT is virtually unquestionable, in part due to the huge number of applications available and under 
development. Although the deployment and use of a large number of IoT devices already become a reality, the theme is still 
considered extremely important for both industry and academia. Among IoT applications, intelligent environments, such as smart 
city and campus, are highlighted. 

In this context, the [SOFTware-defined gateWAY and fog computing for IoT](https://softway4iot.labora.inf.ufg.br)  project aims to address four basic problems: 

1. Need to support multiple wireless technologies for IoT, e.g., BLE, ZigBee, Z-Wave, LoRa/LoRaWAN, 2G/3G, NB-IoT.
2. Need to minimize the impact of choosing a wireless technology for IoT not yet consolidated.
3. Public exposure of IoT devices on the Internet, i.e., potential risks related to the network security of the devices.
4. Device connectivity to the infrastructure for data collection and processing, typically a cloud computing infrastructure.

## Installation Guide

The whole installation process is based on using [Ansilble](https://www.ansible.com/). You must first deploy a gateway manager. 
To deploy a gateway manager you must edit the `hosts` file adding:

```
  [sw4iot-manager]
  <gateway-manager-IP-address> physical_network_interface=<manager-machine-interface-name> user_name=<username-of-the-manager-machine>
```

After entering the connection parameters, just run the gateway manager deployment playbook with ansible:
```
  ansible-playbook -v  manager.yml -i hosts
```

The previous command will deploy the gateway manager using default parameters, for example, the [fireware infrastructure](https://www.fiware.org/) will not be deployed, the `etcd database` from any previous Softway version will be preserved  and the `WebSM` access port will be 8080.
```
    ansible-playbook -v  manager.yml -i hosts -e "fiware_deploy=true  remove_etcd_data=true websm_external_acess_port=8080"
```

