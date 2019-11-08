const ageQuestionBlock = require('../generated_pages/variants_content/age-question-block.page.js');

describe('QuestionVariants', function() {

  beforeEach(function() {
    browser.openQuestionnaire('test_variants_content.json');
  });

  it('Given I am completing the survey, then the correct content is shown based on my previous answers when i am under 16', function () {
      $(ageQuestionBlock.age()).setValue(12);
      $(ageQuestionBlock.submit()).click();
      expect($('main.page__main h1').getText()).to.contain('You are 16 or younger');
  });

  it('Given I am completing the survey, then the correct content is shown based on my previous answers when i am under 16', function () {
      $(ageQuestionBlock.age()).setValue(22);
      $(ageQuestionBlock.submit()).click();
      expect($('main.page__main h1').getText()).to.contain('You are 16 or older');
  });
});
