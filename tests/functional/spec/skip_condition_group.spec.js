const WantToSkipPage = require('../generated_pages/skip_condition_group/do-you-want-to-skip.page');
const LastGroupPage = require('../generated_pages/skip_condition_group/last-group-block.page');

describe('Skip Condition Group', function() {
  it('Given I am not skipping, When I complete all questions, Then I should see the summary page', function() {
    browser.openQuestionnaire('test_skip_condition_group.json');
    $(WantToSkipPage.yes()).click();
    $(WantToSkipPage.submit()).click();
    expect(browser.getUrl()).to.contain(LastGroupPage.pageName);
  });
});
