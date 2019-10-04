from config import config_slices_enabled
from app_orch import apps_create
from app_orch import apps_status
from app_orch import apps_delete
from app_orch import token_create

import logging

from apscheduler.schedulers.blocking import BlockingScheduler

# logging
logging.getLogger('apscheduler').setLevel(logging.ERROR)
logging.getLogger('sw4iot').setLevel(logging.INFO)
logging.getLogger('sw4iot_net_man').setLevel(logging.DEBUG)

FORMAT = '%(asctime)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s'  # by default funcName is removed
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('NetManSW4IoT')
logger.setLevel(logging.INFO)


if __name__ == '__main__':
    scheduler = BlockingScheduler(timezone="UTC")

    # slice enable
    scheduler.add_job(config_slices_enabled, 'interval', seconds=5, id=config_slices_enabled.__name__,
                      replace_existing=True)

    #first toker create
    token_create()

    #apps
    scheduler.add_job(apps_create, 'interval', seconds=5, id=apps_create.__name__, replace_existing=True)
    scheduler.add_job(apps_status, 'interval', seconds=5, id=apps_status.__name__, replace_existing=True)
    scheduler.add_job(apps_delete, 'interval', seconds=5, id=apps_delete.__name__, replace_existing=True)

    #token create for new gateways
    scheduler.add_job(token_create, 'interval', hours=12, id=token_create.__name__, replace_existing=True)

    try:
        logger.info("Starting OrchSW4IoT scheduler jobs")
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logger.error("Exit OrchSW4IoT scheduler jobs")
        scheduler.remove_all_jobs()  # TODO remove this
        logger.info("All jobs have been removed")
