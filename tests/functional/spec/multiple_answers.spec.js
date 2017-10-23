const helpers = require('../helpers');
const PersonalDetailPage = require('../pages/surveys/multiple_answers/personal-details-block.page.js');
const SummaryPage = require('../pages/surveys/multiple_answers/summary.page.js');

describe('Error messages', function() {

  it('Given a survey has multiple answers for a question when I save the survey then the summary shows all the answers', function() {
    return helpers.openQuestionnaire('multiple_answers.json').then(() => {
      return browser
        .setValue(PersonalDetailPage.firstName(), 'HAN')
        .setValue(PersonalDetailPage.surname(), 'SOLO')
        .click(PersonalDetailPage.submit())
        .getText(SummaryPage.answer()).should.eventually.contain('HAN')
        .getText(SummaryPage.otherAnswer()).should.eventually.contain('SOLO');
      });
    });

  it('Given I complete a survey that has multiple answers for a question when I edit an answer then I appear on the page to edit my answer', function() {
    return helpers.openQuestionnaire('multiple_answers.json').then(() => {
      return browser
        .setValue(PersonalDetailPage.firstName(), 'HAN')
        .setValue(PersonalDetailPage.surname(), 'SOLO')
        .click(PersonalDetailPage.submit())
        // When
        .click(SummaryPage.editFirstName())
        // Then
        .getUrl().should.eventually.contain(PersonalDetailPage.pageName)
        .hasFocus(PersonalDetailPage.firstName());
    });
  });
});
