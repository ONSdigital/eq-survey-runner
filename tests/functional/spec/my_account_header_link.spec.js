const helpers = require('../helpers');

const IntroductionPage = require('../generated_pages/introduction/introduction.page');

describe('My Account header link', function() {

  it('Given I start a survey, When I visit a page then I should not see the My account button', function() {
    return helpers.openQuestionnaire('test_introduction.json').then(() => {
      return browser
        .getUrl().should.eventually.contain('introduction')
        .isExisting(IntroductionPage.myAccountLink()).should.eventually.be.false;
   });
 });
});
