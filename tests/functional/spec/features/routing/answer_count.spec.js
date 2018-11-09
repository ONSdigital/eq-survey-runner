const helpers = require('../../../helpers');

const HouseholdCompositionPage =  require('../../../generated_pages/routing_answer_count/household-composition.page.js');
const GroupLessThan2 =            require('../../../generated_pages/routing_answer_count/group-less-than-2-block.page.js');
const GroupEqual2 =               require('../../../generated_pages/routing_answer_count/group-equal-2-block.page.js');
const GroupGreaterThan2 =         require('../../../generated_pages/routing_answer_count/group-greater-than-2-block.page.js');

const test_questionnaire_name = 'test_routing_answer_count.json';

describe('Feature: Routing on answer count', function() {

  it('Given I have a household with two members, When I enter both household members, Then I am routed to the Equals 2 Group page', function () {
    return helpers.openQuestionnaire(test_questionnaire_name).then(() => {
      return browser
        .setValue(HouseholdCompositionPage.firstName(), 'Alpha')
        .setValue(HouseholdCompositionPage.lastName(), 'One')
        .click(HouseholdCompositionPage.addPerson())
        .setValue(HouseholdCompositionPage.firstName('_1'), 'Bravo')
        .setValue(HouseholdCompositionPage.lastName('_1'), 'Two')
        .click(HouseholdCompositionPage.submit())
        .getUrl().should.eventually.contain(GroupEqual2.pageName);
    });
  });

  it('Given I have a household with three members, When I enter three household members, Then I am routed to the greater than 2 Group page', function () {
    return helpers.openQuestionnaire(test_questionnaire_name).then(() => {
      return browser
        .setValue(HouseholdCompositionPage.firstName(), 'Alpha')
        .setValue(HouseholdCompositionPage.lastName(), 'One')
        .click(HouseholdCompositionPage.addPerson())
        .setValue(HouseholdCompositionPage.firstName('_1'), 'Bravo')
        .setValue(HouseholdCompositionPage.lastName('_1'), 'Two')
        .click(HouseholdCompositionPage.addPerson())
        .setValue(HouseholdCompositionPage.firstName('_1'), 'Charlie')
        .setValue(HouseholdCompositionPage.lastName('_1'), 'Three')
        .click(HouseholdCompositionPage.submit())
        .getUrl().should.eventually.contain(GroupGreaterThan2.pageName);
    });
  });

  it('Given I have a household with one member, When I enter a single household member, Then i am routed to the Less than 2 Group page', function () {
    return helpers.openQuestionnaire(test_questionnaire_name).then(() => {
      return browser
        .setValue(HouseholdCompositionPage.firstName(), 'Alpha')
        .setValue(HouseholdCompositionPage.lastName(), 'One')
        .click(HouseholdCompositionPage.submit())
        .getUrl().should.eventually.contain(GroupLessThan2.pageName);
    });
  });

});
