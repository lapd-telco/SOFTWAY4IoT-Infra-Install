import logging
import json
from sw4iotdatabase import database
from sw4iotdatabase.schemas import SecuritySchema
from sw4iotdatabase.models import data_converter, JsonSerializable, Model, VlanModel, SliceNetModel
from marshmallow import Schema, fields
from datetime import datetime
db = database.Sw4IotDatabase()
logger = logging.getLogger('OrchSW4IoT')


def config_slices_net():
    """
    Configure slice network, creating the network on Contiv plugin
    """
    for slice in db.get_slices():
        logger.info('slice {}'.format(slice))

        # create net info
        net = db.get_slice_net(slice.id)
        logger.info('Slice {} with network: {}'.format(slice.id, net))

        slice_net = SliceNetModel(tenant="s{}".format(slice.id), network='s{}-net'.format(slice.id),
                                  group='s{}-group'.format(slice.id), nat_policy='s{}-nat-policy'.format(slice.id),
                                  subnet='10.1.0.0/16', gateway='10.1.1.1', netmask='255.255.0.0', dns='8.8.8.8')

        vlan = db.get_slice_vlan(slice.id)

        if vlan and not net:
            net_created = True
            if net_created:
                db.save_slice_security(slice.id, 'nat', SecuritySchema().load({"enabled": False}))
                db.save_slice_net(slice.id, slice_net)  # TODO: Update contiv_sdk library


def config_slices_vlan():
    """
    Configure slice vlan
    """
    for slice in db.get_slices():
        # create vlan of slice
        vlan = db.get_slice_vlan(slice.id)
        logger.info('Slice {} with vlan: {}'.format(slice.id, vlan))
        if not vlan:
            logger.info('Create a vlan to slice {}'.format(slice.id))
            # get last vlan and create the next
            last_vlan_id = db.get_last_vlan()
            next_vlan_id = last_vlan_id + 1 if last_vlan_id else 100
            logger.info('Vlan {} seleted to be used by slice {}'.format(next_vlan_id, slice.id))
            # verify if this next vlan is not being used
            if not db.get_vlan(next_vlan_id):
                # save vlan
                db.save_last_vlan(next_vlan_id)
                db.save_vlan(VlanModel(slice.id, next_vlan_id))
                db.save_slice_vlan(slice.id, next_vlan_id)
            else:
                vlan_used = db.get_vlan(next_vlan_id)
                logger.warn('The vlan {} already being used by slice {}'.format(next_vlan_id, vlan_used.slice))


def config_slices_enabled():
    """
    With network and vlan configured the slice can be enabled
    """
    for slice in db.get_slices():
        net = 10
        vlan = 11

        # with network and vlan configured the slice can be enabled
        if net and vlan:
            db.save_slice_enabled(slice.id, enabled=True)
            logger.info('Slice {} enabled: {}'.format(slice.id, True))