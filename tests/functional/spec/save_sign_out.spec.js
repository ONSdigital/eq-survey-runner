const helpers = require('../helpers');
const SetMinMax = require('../generated_pages/numbers/set-min-max-block.page.js');
const TestMinMax = require('../generated_pages/numbers/test-min-max-block.page.js');
const SummaryPage = require('../generated_pages/numbers/summary.page');

describe('SaveSignOut', function() {

  const collectionId = helpers.getRandomString(10);

  it('Given I am completing a survey, when I select save and complete later, then I am redirected to sign out page and my session is cleared', function() {
    return helpers.openQuestionnaire('test_numbers.json', 'test_user', collectionId)
      .then(() => {
        return browser
          .setValue(SetMinMax.setMinimum(), '10')
          .setValue(SetMinMax.setMaximum(), '1020')
          .click(SetMinMax.submit())
          .click(TestMinMax.saveSignOut())
          .getUrl().should.eventually.contain('signed-out')
          .back()
          .getSource().should.eventually.contain('Your session has expired');
      });
  });

  it('Given i am returning to the questionnaire, then I am returned to the page I was on and can then complete the survey', function() {
    return helpers.openQuestionnaire('test_numbers.json', 'test_user', collectionId)
      .then(() => {
        return browser
          .getUrl().should.eventually.contain(TestMinMax.pageName)
          .setValue(TestMinMax.testRange(), '10')
          .setValue(TestMinMax.testMin(), '123')
          .setValue(TestMinMax.testMax(), '1000')
          .setValue(TestMinMax.testPercent(), '100')
          .click(TestMinMax.submit())
          .getUrl().should.eventually.contain(SummaryPage.pageName)
          .click(SummaryPage.submit())
          .getUrl().should.eventually.contain('thank-you');
      });
  });

});
