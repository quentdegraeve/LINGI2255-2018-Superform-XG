from superform.suputils import selenium_utils
from superform.models import Channel
from superform.suputils import keepass
from time import sleep


#Create a channel and add 2 post (moderation and publication have to be done manually)
def test_complete_linkedin():
    driver = selenium_utils.get_chrome()
    selenium_utils.login(driver, 'superego', 'superego')
    keepass.set_entry_from_keepass('account_linkedin')
    selenium_utils.create_channel(driver, 'test_linkedin', keepass.KeepassEntry.username, keepass.KeepassEntry.password, 'linkedin')
    sleep(1)
    selenium_utils.create_channel(driver, 'test_slack', 'raphael.hacha@student.uclouvain.be', keepass.KeepassEntry.password, 'slack')
    sleep(1)
    selenium_utils.create_channel(driver, 'test_chan_slack', 'raphael.hacha@student.uclouvain.be', keepass.KeepassEntry.password, 'slack')
    sleep(1)
    selenium_utils.add_authorization(driver, 'test_linkedin', 'superego', 2)
    sleep(1)
    selenium_utils.add_authorization(driver, 'test_slack', 'superego', 2)
    sleep(1)
    selenium_utils.add_authorization(driver, 'test_chan_slack', 'superego', 2)
    assert 1 == 1
