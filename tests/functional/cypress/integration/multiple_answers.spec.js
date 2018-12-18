import {openQuestionnaire} from '../helpers/helpers.js'
const PersonalDetailPage = require('../../generated_pages/multiple_answers/personal-details-block.page.js');
const SummaryPage = require('../../generated_pages/multiple_answers/summary.page.js');

describe('Multiple Answers', function() {
  beforeEach(() => {
    openQuestionnaire('test_multiple_answers.json')
  })

  it('Given I complete a survey that has multiple answers for a question when I edit an answer then I appear on the page to edit my answer', function() {
    cy
      .get(PersonalDetailPage.firstName()).type('HAN')
      .get(PersonalDetailPage.surname()).type('SOLO')
      .get(PersonalDetailPage.submit()).click()
      .get(SummaryPage.firstNameAnswerEdit()).click()
      .focused().should('match', PersonalDetailPage.firstName())
      .url().should('contain', PersonalDetailPage.pageName)
  });

  it('Given a survey has multiple answers for a question when I save the survey then the summary shows all the answers', function() {
    cy
      .get(PersonalDetailPage.firstName()).type('HAN')
      .get(PersonalDetailPage.surname()).type('SOLO')
      .get(PersonalDetailPage.submit()).click()
      .get(SummaryPage.firstNameAnswer()).stripText().should('contain', 'HAN')
      .get(SummaryPage.surnameAnswer()).stripText().should('contain', 'SOLO');
  });
});
