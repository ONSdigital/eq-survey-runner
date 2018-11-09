const helpers = require('../helpers');
const PersonalDetailPage = require('../generated_pages/multiple_answers/personal-details-block.page.js');
const SummaryPage = require('../generated_pages/multiple_answers/summary.page.js');

describe('Multiple Answers', function() {

  it('Given I complete a survey that has multiple answers for a question when I edit an answer then I appear on the page to edit my answer', function() {
    return helpers.openQuestionnaire('test_multiple_answers.json').then(() => {
      return browser
        .setValue(PersonalDetailPage.firstName(), 'HAN')
        .setValue(PersonalDetailPage.surname(), 'SOLO')
        .click(PersonalDetailPage.submit())
        .click(SummaryPage.firstNameAnswerEdit())
        .getUrl().should.eventually.contain(PersonalDetailPage.pageName)
        .hasFocus(PersonalDetailPage.firstName());
    });
  });

  it('Given a survey has multiple answers for a question when I save the survey then the summary shows all the answers', function() {
    return helpers.openQuestionnaire('test_multiple_answers.json').then(() => {
      return browser
        .setValue(PersonalDetailPage.firstName(), 'HAN')
        .setValue(PersonalDetailPage.surname(), 'SOLO')
        .click(PersonalDetailPage.submit())
        .getText(SummaryPage.firstNameAnswer()).should.eventually.contain('HAN')
        .getText(SummaryPage.surnameAnswer()).should.eventually.contain('SOLO');
    });
  });
});
