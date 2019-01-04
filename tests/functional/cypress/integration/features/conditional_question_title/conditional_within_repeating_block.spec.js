import {openQuestionnaire} from '../../../helpers/helpers.js';
const EveryoneAtAddressConfirmationPage = require('../../../../generated_pages/titles_conditional_within_repeating_block/everyone-at-address-confirmation.page');
const HouseholdCompositionPage = require('../../../../generated_pages/titles_conditional_within_repeating_block/household-composition.page');
const ProxyCheckPage = require('../../../../generated_pages/titles_conditional_within_repeating_block/proxy-check.page');
const ReligionPage = require('../../../../generated_pages/titles_conditional_within_repeating_block/religion.page');
const WhoLivesHereCompletedPage = require('../../../../generated_pages/titles_conditional_within_repeating_block/who-lives-here-completed.page');
const HouseholdMemberCompletedPage = require('../../../../generated_pages/titles_conditional_within_repeating_block/household-member-completed.page');
const ConfirmationPage = require('../../../../generated_pages/titles_conditional_within_repeating_block/confirmation.page');

describe('Feature: Use of conditional Titles in Repeating blocks with condition dependant on answer changing within block', function() {

  beforeEach(function() {
    openQuestionnaire('test_titles_conditional_within_repeating_block.json');
  });

  describe('Given I start the survey with a repeating block to gather a list of names', function() {
    it('When I enter another repeating block with conditional title based on the answer I should see those names in the title of a subsequent question and can get to confirm page', function() {
      cy
        .get(HouseholdCompositionPage.firstName()).type('Fred')
        .get(HouseholdCompositionPage.addPerson()).click()
        .get(HouseholdCompositionPage.firstName('_1')).type('Mary')
        .get(HouseholdCompositionPage.addPerson()).click()
        .get(HouseholdCompositionPage.firstName('_2')).type('Barney')
        .get(HouseholdCompositionPage.submit()).click()
        .get(EveryoneAtAddressConfirmationPage.yes()).click()
        .get(EveryoneAtAddressConfirmationPage.submit()).click()
        .get(WhoLivesHereCompletedPage.submit()).click()
        .get(ProxyCheckPage.proxy()).click()
        .get(ProxyCheckPage.submit()).click()
        .get(ReligionPage.questionText()).stripText().should('contain', 'What is Fred’s religion?')
        .get(ReligionPage.noReligion()).click()
        .get(ReligionPage.submit()).click()
        .get(HouseholdMemberCompletedPage.submit()).click()
        .get(ProxyCheckPage.proxy()).click()
        .get(ProxyCheckPage.submit()).click()
        .get(ReligionPage.questionText()).stripText().should('contain', 'What is Mary’s religion?')
        .get(ReligionPage.jedi()).click()
        .get(ReligionPage.submit()).click()
        .get(HouseholdMemberCompletedPage.submit()).click()
        .get(ProxyCheckPage.noProxy()).click()
        .get(ProxyCheckPage.submit()).click()
        .get(ReligionPage.questionText()).stripText().should('contain', 'What is your religion?')
        .get(ReligionPage.jedi()).click()
        .get(ReligionPage.submit()).click()
        .get(HouseholdMemberCompletedPage.submit()).click()
        .url().should('contain', ConfirmationPage.pageName);
    });
  });
});
