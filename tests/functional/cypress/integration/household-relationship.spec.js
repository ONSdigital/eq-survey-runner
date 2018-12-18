import {openQuestionnaire} from '../helpers/helpers.js'

const HouseholdCompositionPage = require('../../generated_pages/relationship_household/household-composition.page.js');
const RelationshipsPage = require('../../generated_pages/relationship_household/household-relationships.page.js');
const VisitorsPage = require('../../generated_pages/relationship_household/overnight-visitors.page.js');
const SummaryPage = require('../../generated_pages/relationship_household/summary.page.js');

describe('Household Relationship', function() {

  beforeEach(() => {
    openQuestionnaire('test_relationship_household.json')
  });

  it('Given I am on the household page when I enter one name then I should not have to enter relationship details', function() {
    cy
      .get(HouseholdCompositionPage.firstName()).type('Alpha')
      .get(HouseholdCompositionPage.lastName()).type('One')
      .get(HouseholdCompositionPage.submit()).click()
      .get(VisitorsPage.answer()).type('0')
      .get(VisitorsPage.submit()).click()
      .url().should('contain', SummaryPage.pageName);
  });

  it('Given I answer the relationship questions for the first person when answer the relationship questions for second person then I should not have to enter relationship details for third person', function() {
    cy
      .get(HouseholdCompositionPage.firstName()).type('Alpha')
      .get(HouseholdCompositionPage.lastName()).type('One')
      .get(HouseholdCompositionPage.addPerson()).click()
      .get(HouseholdCompositionPage.firstName('_1')).type('Bravo')
      .get(HouseholdCompositionPage.lastName('_1')).type('Two')
      .get(HouseholdCompositionPage.addPerson()).click()
      .get(HouseholdCompositionPage.firstName('_2')).type('Charlie')
      .get(HouseholdCompositionPage.lastName('_2')).type('Three')
      .get(HouseholdCompositionPage.submit()).click()
      .get(VisitorsPage.answer()).type('0')
      .get(VisitorsPage.submit()).click()
      .get('#who-is-related-0').select('Husband or wife')
      .get('#who-is-related-1').select('Son or daughter')
      .url().should('contain', SummaryPage.pageName)

  });

  it('Given I answer the relationship questions when I go back from the summary page then my answers should still be selected', function() {
    cy
      .get(HouseholdCompositionPage.firstName()).type('Alpha')
      .get(HouseholdCompositionPage.lastName()).type('One')
      .get(HouseholdCompositionPage.addPerson()).click()
      .get(HouseholdCompositionPage.firstName('_1')).type('Bravo')
      .get(HouseholdCompositionPage.lastName('_1')).type('Two')
      .get(HouseholdCompositionPage.addPerson()).click()
      .get(HouseholdCompositionPage.firstName('_2')).type('Charlie')
      .get(HouseholdCompositionPage.lastName('_2')).type('Three')
      .get(HouseholdCompositionPage.submit()).click()
      .get(VisitorsPage.answer()).type('0')
      .get(VisitorsPage.submit()).click()
      .get(RelationshipsPage.relationship(0, 'Partner')).click()
      .get(RelationshipsPage.relationship(1, 'Brother or sister')).click()
      .get(RelationshipsPage.submit()).click()
      .back()
      .getValue(RelationshipsPage.whoIsRelated(0)).should.eventually.equal("Partner")
      .getValue(RelationshipsPage.whoIsRelated(1)).should.eventually.equal("Brother or sister");
  });

});

