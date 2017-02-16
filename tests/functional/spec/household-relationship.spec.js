import chai from 'chai'
import {openQuestionnaire} from '../helpers'
import HouseholdCompositionPage from '../pages/surveys/household_composition/household-composition.page'
import HouseholdRelationshipPage from '../pages/surveys/relationship/relationships.page'
import SummaryPage from '../pages/summary.page'

const expect = chai.expect

describe('Household relationship', function() {

  var schema = 'test_relationship_household.json'


  it('Given I am on the household page when I enter Joe Bloggs then I should not have to enter relationship details', function() {
    // Given
    openQuestionnaire(schema)
    HouseholdCompositionPage.setPersonName(0, 'Joe Bloggs')

    // When
    HouseholdCompositionPage.submit()

    // Then
    expect(SummaryPage.isOpen()).to.be.true
  })

  it('Given I answer the relationship questions for Joe Bloggs when answer the relationship questions for Jane Doe then I should not have to enter relationship details for John Doe', function() {
    // Given
    openQuestionnaire(schema)
    HouseholdCompositionPage.setPersonName(0, 'Joe Bloggs')
      .addPerson()
      .setPersonName(1, 'Jane Doe')
      .addPerson()
      .setPersonName(2, 'John Doe')
      .submit()
    HouseholdRelationshipPage.clickWhoIsRelatedHusbandOrWife(0)
      .clickWhoIsRelatedSonOrDaughter(1)
      .submit()

    // When
    HouseholdRelationshipPage.clickWhoIsRelatedHusbandOrWife(0)
      .submit()

    // Then
    expect(SummaryPage.isOpen()).to.be.true
  })

})
