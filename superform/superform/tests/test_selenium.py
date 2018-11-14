from superform.suputils import selenium_utils
from superform.models import Channel
from superform.suputils import keepass
from time import sleep


#Create a channel and add 2 post (moderation and publication have to be done manually)
def test_prepare():
    driver = selenium_utils.get_chrome()
    selenium_utils.login(driver, 'superego', 'superego')
    keepass.set_entry_from_keepass('account_linkedin')
    selenium_utils.create_channel(driver, 'test_linkedin', keepass.KeepassEntry.username, keepass.KeepassEntry.password, 'linkedin')
    keepass.set_entry_from_keepass('account_slack')
    selenium_utils.create_channel(driver, 'test_slack', keepass.KeepassEntry.username, keepass.KeepassEntry.password, 'slack')
    selenium_utils.create_channel(driver, 'test_chan_slack', keepass.KeepassEntry.username, keepass.KeepassEntry.password, 'slack')
    selenium_utils.add_authorization(driver, 'test_linkedin', 'superego', 2)
    selenium_utils.add_authorization(driver, 'test_slack', 'superego', 2)
    selenium_utils.add_authorization(driver, 'test_chan_slack', 'superego', 2)

    selenium_utils.add_new_post(driver, 'test_linkedin', 'test_linkedin title', 'test_linkedin description', '14112018', '14112018')
    selenium_utils.add_new_post(driver, 'test_slack', 'test_slack title', 'test_slack description', '14112018', '14112018')

    assert 1 == 1

