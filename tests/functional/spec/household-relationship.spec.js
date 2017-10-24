const helpers = require('../helpers');

const HouseholdCompositionPage = require('../pages/surveys/household/household-composition.page.js');
const RelationshipsPage = require('../pages/surveys/household/relationships.page.js');
const SummaryPage = require('../pages/surveys/household/summary.page.js');

describe('Example Test', function() {

  it('Given I am on the household page when I enter one name then I should not have to enter relationship details', function() {
    return helpers.openQuestionnaire('test_relationship_household.json').then(() => {
        return browser
          .setValue(HouseholdCompositionPage.firstName(),'Alpha')
          .setValue(HouseholdCompositionPage.lastName(),'One')
          .click(HouseholdCompositionPage.submit())
          .getUrl().should.eventually.contain(SummaryPage.pageName);
    });
  });

  it('Given I answer the relationship questions for the first person when answer the relationship questions for second person then I should not have to enter relationship details for third person', function() {
    return helpers.openQuestionnaire('test_relationship_household.json').then(() => {
        return browser
          .setValue(HouseholdCompositionPage.firstName(),'Alpha')
          .setValue(HouseholdCompositionPage.lastName(),'One')
          .click(HouseholdCompositionPage.addPerson())
          .setValue(HouseholdCompositionPage.firstName('_1'),'Bravo')
          .setValue(HouseholdCompositionPage.lastName('_1'),'Two')
          .click(HouseholdCompositionPage.addPerson())
          .setValue(HouseholdCompositionPage.firstName('_2'),'Charlie')
          .setValue(HouseholdCompositionPage.lastName('_2'),'Three')
          .click(HouseholdCompositionPage.submit())
          .click(RelationshipsPage.relationship(0, 'Husband or wife'))
          .click(RelationshipsPage.relationship(1, 'Son or daughter'));
    });
  });

  it('Given I answer the relationship questions when I go back from the summary page then my answers should still be selected', function() {
    return helpers.openQuestionnaire('test_relationship_household.json').then(() => {
        return browser
          .setValue(HouseholdCompositionPage.firstName(),'Alpha')
          .setValue(HouseholdCompositionPage.lastName(),'One')
          .click(HouseholdCompositionPage.addPerson())
          .setValue(HouseholdCompositionPage.firstName('_1'),'Bravo')
          .setValue(HouseholdCompositionPage.lastName('_1'),'Two')
          .click(HouseholdCompositionPage.addPerson())
          .setValue(HouseholdCompositionPage.firstName('_2'),'Charlie')
          .setValue(HouseholdCompositionPage.lastName('_2'),'Three')
          .click(HouseholdCompositionPage.submit())
          .click(RelationshipsPage.relationship(0, 'Partner'))
          .click(RelationshipsPage.relationship(1, 'Brother or sister'))
          .click(RelationshipsPage.submit())
          .back()
          .getValue(RelationshipsPage.answer(0)).should.eventually.equal("Partner")
          .getValue(RelationshipsPage.answer(1)).should.eventually.equal("Brother or sister");
    });
  });

});

