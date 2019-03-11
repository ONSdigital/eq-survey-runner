const helpers = require('../helpers');
const ageQuestionBlock = require('../generated_pages/variants_content/age-question-block.page.js');

describe('QuestionVariants', function() {

  beforeEach(function() {
    return helpers.openQuestionnaire('test_variants_content.json');
  });

  it('Given I am completing the survey, then the correct content is shown based on my previous answers when i am under 16', function () {
    return browser
      .setValue(ageQuestionBlock.age(), 12)
      .click(ageQuestionBlock.submit())
      .getText('main.page__main h3').should.eventually.contain('You are 16 or younger');
  });

  it('Given I am completing the survey, then the correct content is shown based on my previous answers when i am under 16', function () {
    return browser
      .setValue(ageQuestionBlock.age(), 22)
      .click(ageQuestionBlock.submit())
      .getText('main.page__main h3').should.eventually.contain('You are 16 or older');
  });
});
