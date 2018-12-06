import datetime
import pytest

from superform.suputils import selenium_utils
from superform.suputils import keepass


@pytest.fixture(scope='session', autouse=True)
def prepare():
    pytest.driver = selenium_utils.get_chrome()
    pytest.now = datetime.datetime.now().strftime("%d%m%Y")

    #pytest.linkedin_title_max = 200
    #pytest.linkedin_description_max = 256
    #pytest.slack_title_max = 40000
    #pytest.slack_description_max = 40000

    #keepass.set_entry_from_keepass('account_superform')
    selenium_utils.login(pytest.driver, "superego", "superego")

    #keepass.set_entry_from_keepass('account_twitter')
    selenium_utils.create_channel(pytest.driver, 'test_twitter', 'twitter')

    #keepass.set_entry_from_keepass('account_ictv')
    selenium_utils.create_channel(pytest.driver, 'test_ictv', 'ICTV')



    selenium_utils.add_authorization(pytest.driver, 'test_twitter', 'superego', 2)
    selenium_utils.add_authorization(pytest.driver, 'test_ictv', 'superego', 2)

    yield

    pytest.driver.close()

#I create a post here so be careful
def test_edit_post_7():
    title = 'test_edit titre'
    description = 'test_edit description'
    selenium_utils.add_new_post(pytest.driver, ['test_twitter'], title, description, pytest.now, pytest.now)

    selenium_utils.edit_post(pytest.driver, )
