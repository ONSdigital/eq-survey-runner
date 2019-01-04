import {openQuestionnaire} from '../helpers/helpers.js';

const IntroductionPage = require('../../generated_pages/introduction/introduction.page');

describe('Introduction page', function() {
  const introduction_schema = 'test_introduction.json';

  beforeEach(() => {
    openQuestionnaire(introduction_schema);
  });

  it('Given I start a survey, When I view the introduction page then I should be able to see introduction information', function() {
    cy
      .get(IntroductionPage.useOfData()).stripText().should('contain', 'How we use your data')
      .get(IntroductionPage.useOfInformation()).stripText().should('contain', 'What you need to do next')
      .get(IntroductionPage.legalResponse()).stripText().should('contain', 'Your response is legally required')
      .get(IntroductionPage.legalBasis()).stripText().should('contain', 'Notice is given under section 999 of the Test Act 2000')
      .get(IntroductionPage.introDescription()).stripText().should('contain', 'To take part, all you need to do is check that you have the information you need to answer the survey questions.')
      .get(IntroductionPage.introTitleDescription()).stripText(true).should('contain', 'If the company details or structure have changed contact us on 0300 1234 931 or email surveys@ons.gov.uk');
  });
});
