import logging
import ast
import docker
import requests
import yaml
import json
import uuid
from datetime import datetime
from src.docker_comm.clients_manager import ClientsManager
from sw4iotdatabase import database
from sw4iotdatabase.utils import get_yaml_content
from sw4iotdatabase.schemas import ActionSchema
from sw4iotdatabase.models import ActionModel, data_converter, JsonSerializable, AppStatusModel, \
    Model, ActionEnum, TokenGatewayInstallModel
db = database.Sw4IotDatabase()
logger = logging.getLogger(__name__)


def yaml_validate(yaml_file):

    services = yaml_file["services"]

    for item in services:
        container = services[item]

        if 'gateway' in container:
            if 'image' in container:
                continue

        else:
            return False

    return True


def apps_create():
    slices = db.get_slices()
    for slice in slices:
        slice.enabled = db.get_slice_enabled(slice.id)
        if slice.enabled:
            apps = db.get_slice_apps(slice.id)
            for app in apps:
                action_app = db.get_slice_app_action(slice.id, app.id)
                if action_app and action_app.action != ActionEnum.INSTALL:
                    continue
                app_status = db.get_slice_app_status(slice.id, app.id)
                if app_status is not None:
                    continue
                json_file = json.loads(str(app))

                yaml_file = get_yaml_content(json_file["url"])
                id = 0
                if yaml_validate(yaml_file):
                    hosts_dict = {}
                    container_dict = {}
                    services = yaml_file["services"]
                    for item in services:
                        container = services[item]
                        gateway = container["gateway"]
                        hosts_dict[id] = gateway
                        if gateway == 'host':
                            dockerClient = docker.from_env()
                        else:
                            certs_path = '/opt/softway4iot/docker_certs'
                            tls_config = docker.tls.TLSConfig(
                                client_cert=(certs_path + '/client-softway4iot-gatweway-cert.pem',
                                             certs_path + '/client-softway4iot-gatweway-key.pem'))
                            gateway_id = container["gateway"]
                            print(db.get_slice_gws(slice.id))
                            for gateway in db.get_slice_gws(slice.id):
                                if str(gateway.id) == str(gateway_id):
                                    gateway_ip = str(gateway.info.ip)+":2375"
                            dockerClient = docker.DockerClient(base_url='tcp://' + str(gateway_ip), tls=tls_config)
                        docker_requisition = ClientsManager(dockerClient)
                        container_id = docker_requisition.run_container(container)
                        container_dict[id] = container_id
                        id = id + 1
                    app_status = AppStatusModel('10.16.0.130', str(container_dict), 'Waiting', str(hosts_dict), None, None,
                                                None, None, None, None)
                    db.save_slice_app_status(slice.id, app.id, app_status)
                else:
                    app_status = AppStatusModel('10.16.0.130', None, 'Error', None, None, None, None, None, None,
                                                None)
                    db.save_slice_app_status(slice.id, app.id, app_status)


def apps_status():
    slices = db.get_slices()
    for slice in slices:
        slice.enabled = db.get_slice_enabled(slice.id)
        apps = db.get_slice_apps(slice.id)
        if slice.enabled:
            for app in apps:
                status = db.get_slice_app_status(slice.id, app.id)
                print(status)


def apps_delete():
    slices = db.get_slices()
    for slice in slices:
        apps = db.get_all_slice_apps(slice.id)
        for app in apps:
            action_app = db.get_slice_app_action(slice.id, app.id)
            if not action_app or action_app.action != ActionEnum.DELETE:
                continue

            status = db.get_slice_app_status(slice.id, app.id)

            if status.phase == 'Terminated':
                continue

            container_list = status.message

            container_list = ast.literal_eval(container_list)

            hosts_ip = status.pod_ip

            hosts_ip = ast.literal_eval(hosts_ip)

            for item in container_list:
                container = container_list[item]
                gateway = hosts_ip[item]

                if gateway == 'host':
                    dockerClient = docker.from_env()

                else:
                    certs_path = '/opt/softway4iot/docker_certs'
                    tls_config = docker.tls.TLSConfig(
                        client_cert=(certs_path + '/client-softway4iot-gatweway-cert.pem',
                                     certs_path + '/client-softway4iot-gatweway-key.pem'))
                    gateway_id = str(gateway)
                    gateway = db.get_slice_gw(slice.id, gateway_id)
                    gateway_ip = str(gateway.info.ip) + ":2375"
                    dockerClient = docker.DockerClient(base_url='tcp://' + gateway_ip, tls=tls_config)

                docker_requisition = ClientsManager(dockerClient)
                docker_requisition.stop_container(container)
                docker_requisition.remove_container(container)

            db.save_slice_app_action(slice.id, app.id, ActionSchema().load(ActionModel(action='terminated').to_dict()))


def token_create():
    now = datetime.now()
    token = TokenGatewayInstallModel(str(uuid.uuid1()), str(now))
    print(token)
    db.save_token_gateway_install(token)
