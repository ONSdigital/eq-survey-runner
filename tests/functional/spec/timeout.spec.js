const TimeoutBlockPage = require('../generated_pages/timeout/timeout-block.page.js');

describe('Timeout', function() {
  before('Open Survey', function(){
    browser.openQuestionnaire('test_timeout.json');
  });

  it('Given I am completing an electronic questionnaire, when I have been inactive for the timeout period and attempt to submit data, then I will be redirected to a page confirming my session has timed out', function() {
    browser.pause(4000);
    $(TimeoutBlockPage.submit()).click();

    expect($('body').getHTML()).to.contain('Your session has expired');
  });
});
