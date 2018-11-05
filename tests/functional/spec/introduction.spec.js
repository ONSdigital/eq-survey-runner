const helpers = require('../helpers');

const IntroductionPage = require('../base_pages/introduction.page');

describe('Introduction page', function() {

  const introduction_schema = 'test_introduction.json';

  it('Given I start a survey, When I view the introduction page then I should be able to see introduction information', function() {
    return helpers.openQuestionnaire(introduction_schema).then(() => {
      return browser
        .getText(IntroductionPage.useOfData()).should.eventually.contain('How we use your data')
        .getText(IntroductionPage.useOfInformation()).should.eventually.contain('What you need to do next')
        .getText(IntroductionPage.legalResponse()).should.eventually.contain('Your response is legally required')
        .getText(IntroductionPage.legalBasis()).should.eventually.contain('Notice is given under section 999 of the Test Act 2000')
        .getText(IntroductionPage.introDescription()).should.eventually.contain('To take part, all you need to do is check that you have the information you need to answer the survey questions.')
        .getText(IntroductionPage.introTitleDescription()).should.eventually.contain('If the company details or structure have changed contact us on 0300 1234 931 or email surveys@ons.gov.uk');
    });
  });
});
