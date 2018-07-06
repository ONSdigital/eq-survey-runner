const helpers = require('../../../helpers');

describe('Feature: Use of conditional Titles in Repeating blocks with condition dependant on answer changing within block', function() {
  var EveryoneAtAddressConfirmationPage = require('../../../pages/features/conditional_question_title/conditional_within_repeating_block/everyone-at-address-confirmation.page');
  var HouseholdCompositionPage = require('../../../pages/features/conditional_question_title/conditional_within_repeating_block/household-composition.page');
  var ProxyCheckPage = require('../../../pages/features/conditional_question_title/conditional_within_repeating_block/proxy-check.page');
  var ReligionPage = require('../../../pages/features/conditional_question_title/conditional_within_repeating_block/religion.page');
  var WhoLivesHereCompletedPage = require('../../../pages/features/conditional_question_title/conditional_within_repeating_block/who-lives-here-completed.page');
  var HouseholdMemberCompletedPage = require('../../../pages/features/conditional_question_title/conditional_within_repeating_block/household-member-completed.page');
  var ConfirmationPage = require('../../../pages/features/conditional_question_title/conditional_within_repeating_block/confirmation.page');

  beforeEach(function() {
      return helpers.openQuestionnaire('test_titles_conditional_within_repeating_block.json');
  });

  describe('Given I start the survey with a repeating block to gather a list of names', function() {
    it('When I enter another repeating block with conditional title based on the answer I should see those names in the title of a subsequent question and can get to confirm page', function() {
      return browser
        .setValue(HouseholdCompositionPage.answer(),'Fred')
        .click(HouseholdCompositionPage.addPerson())
        .setValue(HouseholdCompositionPage.answer('_1'),'Mary')
        .click(HouseholdCompositionPage.addPerson())
        .setValue(HouseholdCompositionPage.answer('_2'),'Barney')
        .click(HouseholdCompositionPage.submit())
        .click(EveryoneAtAddressConfirmationPage.yes())
        .click(EveryoneAtAddressConfirmationPage.submit())
        .click(WhoLivesHereCompletedPage.submit())
        .click(ProxyCheckPage.proxy())
        .click(ProxyCheckPage.submit())
        .getText(ReligionPage.questionText()).should.eventually.contain("What is Fred’s religion?")
        .click(ReligionPage.noReligion())
        .click(ReligionPage.submit())
        .click(HouseholdMemberCompletedPage.submit())
        .click(ProxyCheckPage.proxy())
        .click(ProxyCheckPage.submit())
        .getText(ReligionPage.questionText()).should.eventually.contain("What is Mary’s religion?")
        .click(ReligionPage.jedi())
        .click(ReligionPage.submit())
        .click(HouseholdMemberCompletedPage.submit())
        .click(ProxyCheckPage.noProxy())
        .click(ProxyCheckPage.submit())
        .getText(ReligionPage.questionText()).should.eventually.contain("What is your religion?")
        .click(ReligionPage.jedi())
        .click(ReligionPage.submit())
        .click(HouseholdMemberCompletedPage.submit())
        .getUrl().should.eventually.contain(ConfirmationPage.pageName);
    });
  });
});
