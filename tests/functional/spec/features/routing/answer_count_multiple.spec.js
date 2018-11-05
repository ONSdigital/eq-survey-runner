const helpers = require('../../../helpers');

const PrimaryNamePage =   require('../../../generated_pages/routing_answer_count_multiple/primary-name-block.page.js');
const AnyoneElsePage =    require('../../../generated_pages/routing_answer_count_multiple/repeating-anyone-else-block.page.js');
const RepeatingNamePage = require('../../../generated_pages/routing_answer_count_multiple/repeating-name-block.page.js');
const GroupLessThan2 =    require('../../../generated_pages/routing_answer_count_multiple/group-less-than-2-block.page.js');
const GroupEqual2 =       require('../../../generated_pages/routing_answer_count_multiple/group-equal-2-block.page.js');
const GroupGreaterThan2 = require('../../../generated_pages/routing_answer_count_multiple/group-greater-than-2-block.page.js');

const test_questionnaire_name = 'test_routing_answer_count_multiple.json';

describe('Feature: Routing on answer count', function() {

  it('Given I have a household with one member, When I enter the household member, Then I am routed to the less than 2 Group page', function () {
    return helpers.openQuestionnaire(test_questionnaire_name).then(() => {
      return browser
        .setValue(PrimaryNamePage.primaryName(), 'Alpha')
        .click(PrimaryNamePage.submit())
        .click(AnyoneElsePage.no())
        .click(AnyoneElsePage.submit())
        .getUrl().should.eventually.contain(GroupLessThan2.pageName);
    });
  });

  it('Given I have a household with two members, When I enter the household members, Then I am routed to the equals 2 Group page', function () {
    return helpers.openQuestionnaire(test_questionnaire_name).then(() => {
      return browser
        .setValue(PrimaryNamePage.primaryName(), 'Alpha')
        .click(PrimaryNamePage.submit())
        .click(AnyoneElsePage.yes())
        .click(AnyoneElsePage.submit())
        .setValue(RepeatingNamePage.repeatingName(), 'Beta')
        .click(RepeatingNamePage.submit())
        .click(AnyoneElsePage.no())
        .click(AnyoneElsePage.submit())
        .getUrl().should.eventually.contain(GroupEqual2.pageName);
    });
  });

  it('Given I have a household with three members, When I enter the household members, Then I am routed to the greater than 2 Group page', function () {
    return helpers.openQuestionnaire(test_questionnaire_name).then(() => {
      return browser
        .setValue(PrimaryNamePage.primaryName(), 'Alpha')
        .click(PrimaryNamePage.submit())
        .click(AnyoneElsePage.yes())
        .click(AnyoneElsePage.submit())
        .setValue(RepeatingNamePage.repeatingName(), 'Beta')
        .click(RepeatingNamePage.submit())
        .click(AnyoneElsePage.yes())
        .click(AnyoneElsePage.submit())
        .setValue(RepeatingNamePage.repeatingName(), 'Charlie')
        .click(RepeatingNamePage.submit())
        .click(AnyoneElsePage.no())
        .click(AnyoneElsePage.submit())
        .getUrl().should.eventually.contain(GroupGreaterThan2.pageName);
    });
  });
});
