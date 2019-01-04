import {openQuestionnaire} from '../../../helpers/helpers.js';

const HouseholdCompositionPage =  require('../../../../generated_pages/routing_answer_count/household-composition.page.js');
const GroupLessThan2 =            require('../../../../generated_pages/routing_answer_count/group-less-than-2-block.page.js');
const GroupEqual2 =               require('../../../../generated_pages/routing_answer_count/group-equal-2-block.page.js');
const GroupGreaterThan2 =         require('../../../../generated_pages/routing_answer_count/group-greater-than-2-block.page.js');

const test_questionnaire_name = 'test_routing_answer_count.json';

describe('Feature: Routing on answer count', function() {

  it('Given I have a household with two members, When I enter both household members, Then I am routed to the Equals 2 Group page', function() {
    openQuestionnaire(test_questionnaire_name)
      .get(HouseholdCompositionPage.firstName()).type('Alpha')
      .get(HouseholdCompositionPage.lastName()).type('One')
      .get(HouseholdCompositionPage.addPerson()).click()
      .get(HouseholdCompositionPage.firstName('_1')).type('Bravo')
      .get(HouseholdCompositionPage.lastName('_1')).type('Two')
      .get(HouseholdCompositionPage.submit()).click()
      .url().should('contain', GroupEqual2.pageName);
  });

  it('Given I have a household with three members, When I enter three household members, Then I am routed to the greater than 2 Group page', function() {
    openQuestionnaire(test_questionnaire_name)
      .get(HouseholdCompositionPage.firstName()).type('Alpha')
      .get(HouseholdCompositionPage.lastName()).type('One')
      .get(HouseholdCompositionPage.addPerson()).click()
      .get(HouseholdCompositionPage.firstName('_1')).type('Bravo')
      .get(HouseholdCompositionPage.lastName('_1')).type('Two')
      .get(HouseholdCompositionPage.addPerson()).click()
      .get(HouseholdCompositionPage.firstName('_1')).type('Charlie')
      .get(HouseholdCompositionPage.lastName('_1')).type('Three')
      .get(HouseholdCompositionPage.submit()).click()
      .url().should('contain', GroupGreaterThan2.pageName);
  });

  it('Given I have a household with one member, When I enter a single household member, Then i am routed to the Less than 2 Group page', function() {
    openQuestionnaire(test_questionnaire_name)
      .get(HouseholdCompositionPage.firstName()).type('Alpha')
      .get(HouseholdCompositionPage.lastName()).type('One')
      .get(HouseholdCompositionPage.submit()).click()
      .url().should('contain', GroupLessThan2.pageName);
  });

});
