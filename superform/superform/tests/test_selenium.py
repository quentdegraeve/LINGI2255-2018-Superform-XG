from superform.suputils import selenium_utils
from superform.models import Channel
from superform.suputils import keepass


#Create a channel and add 2 post (moderation and publication have to be done manually)
def test_complete_linkedin():
    driver = selenium_utils.get_chrome()
    selenium_utils.login(driver, 'superego', 'superego')
    keepass.set_entry_from_keepass('account_linkedin')
    selenium_utils.create_channel(driver, 'test_linkedin', keepass.KeepassEntry.username, keepass.KeepassEntry.password, 'linkedin')
    selenium_utils.add_authorization(driver, 'test_linkedin', 'superego', 2)
    selenium_utils.add_new_post(driver, 'test_linkedin', 'test title1', 'test description1', '', '', '08112018', '09112018')
    selenium_utils.add_new_post(driver, 'test_linkedin', 'test title2', 'test description2', '', '', '08112018', '09112018')
    assert 1 == 1
