const helpers = require('../../../helpers');
const EveryoneAtAddressConfirmationPage = require('../../../generated_pages/titles_conditional_within_repeating_block/everyone-at-address-confirmation.page');
const HouseholdCompositionPage = require('../../../generated_pages/titles_conditional_within_repeating_block/household-composition.page');
const ProxyCheckPage = require('../../../generated_pages/titles_conditional_within_repeating_block/proxy-check.page');
const ReligionPage = require('../../../generated_pages/titles_conditional_within_repeating_block/religion.page');
const WhoLivesHereCompletedPage = require('../../../generated_pages/titles_conditional_within_repeating_block/who-lives-here-completed.page');
const HouseholdMemberCompletedPage = require('../../../generated_pages/titles_conditional_within_repeating_block/household-member-completed.page');
const ConfirmationPage = require('../../../generated_pages/titles_conditional_within_repeating_block/confirmation.page');

describe('Feature: Use of conditional Titles in Repeating blocks with condition dependant on answer changing within block', function() {

  beforeEach(function() {
      return helpers.openQuestionnaire('test_titles_conditional_within_repeating_block.json');
  });

  describe('Given I start the survey with a repeating block to gather a list of names', function() {
    it('When I enter another repeating block with conditional title based on the answer I should see those names in the title of a subsequent question and can get to confirm page', function() {
      return browser
        .setValue(HouseholdCompositionPage.firstName(),'Fred')
        .click(HouseholdCompositionPage.addPerson())
        .setValue(HouseholdCompositionPage.firstName('_1'),'Mary')
        .click(HouseholdCompositionPage.addPerson())
        .setValue(HouseholdCompositionPage.firstName('_2'),'Barney')
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
