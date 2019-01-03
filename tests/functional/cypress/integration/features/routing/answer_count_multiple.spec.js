import {openQuestionnaire} from '../../../helpers/helpers.js'

const PrimaryNamePage =   require('../../../../generated_pages/routing_answer_count_multiple/primary-name-block.page.js');
const AnyoneElsePage =    require('../../../../generated_pages/routing_answer_count_multiple/repeating-anyone-else-block.page.js');
const RepeatingNamePage = require('../../../../generated_pages/routing_answer_count_multiple/repeating-name-block.page.js');
const GroupLessThan2 =    require('../../../../generated_pages/routing_answer_count_multiple/group-less-than-2-block.page.js');
const GroupEqual2 =       require('../../../../generated_pages/routing_answer_count_multiple/group-equal-2-block.page.js');
const GroupGreaterThan2 = require('../../../../generated_pages/routing_answer_count_multiple/group-greater-than-2-block.page.js');

const test_questionnaire_name = 'test_routing_answer_count_multiple.json';

describe('Feature: Routing on answer count', function() {

  it('Given I have a household with one member, When I enter the household member, Then I am routed to the less than 2 Group page', function () {
    openQuestionnaire(test_questionnaire_name)
      .get(PrimaryNamePage.primaryName()).type('Alpha')
      .get(PrimaryNamePage.submit()).click()
      .get(AnyoneElsePage.no()).click()
      .get(AnyoneElsePage.submit()).click()
      .url().should('contain', GroupLessThan2.pageName);
  });

  it('Given I have a household with two members, When I enter the household members, Then I am routed to the equals 2 Group page', function () {
    openQuestionnaire(test_questionnaire_name)
      .get(PrimaryNamePage.primaryName()).type('Alpha')
      .get(PrimaryNamePage.submit()).click()
      .get(AnyoneElsePage.yes()).click()
      .get(AnyoneElsePage.submit()).click()
      .get(RepeatingNamePage.repeatingName()).type('Beta')
      .get(RepeatingNamePage.submit()).click()
      .get(AnyoneElsePage.no()).click()
      .get(AnyoneElsePage.submit()).click()
      .url().should('contain', GroupEqual2.pageName);
  });

  it('Given I have a household with three members, When I enter the household members, Then I am routed to the greater than 2 Group page', function () {
    openQuestionnaire(test_questionnaire_name)
      .get(PrimaryNamePage.primaryName()).type('Alpha')
      .get(PrimaryNamePage.submit()).click()
      .get(AnyoneElsePage.yes()).click()
      .get(AnyoneElsePage.submit()).click()
      .get(RepeatingNamePage.repeatingName()).type('Beta')
      .get(RepeatingNamePage.submit()).click()
      .get(AnyoneElsePage.yes()).click()
      .get(AnyoneElsePage.submit()).click()
      .get(RepeatingNamePage.repeatingName()).type('Charlie')
      .get(RepeatingNamePage.submit()).click()
      .get(AnyoneElsePage.no()).click()
      .get(AnyoneElsePage.submit()).click()
      .url().should('contain', GroupGreaterThan2.pageName);
  });
});
