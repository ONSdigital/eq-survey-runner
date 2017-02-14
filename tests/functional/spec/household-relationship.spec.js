import chai from 'chai'
import {startQuestionnaire} from '../helpers'
import HouseholdCompositionPage from '../pages/surveys/household_composition/household-composition.page'
import HouseholdRelationshipPage from '../pages/surveys/relationship/household-relationship.page'
import SummaryPage from '../pages/summary.page'

const expect = chai.expect

describe('Household relationship', function() {

  var schema = 'test_relationship_household.json'


  it('Given I am on the household page when I enter Joe Bloggs then I should not have to enter relationship details', function() {
    // Given
    startQuestionnaire(schema)
    HouseholdCompositionPage.setPersonName(0, 'Joe Bloggs')

    // When
    HouseholdCompositionPage.submit()

    // Then
    expect(SummaryPage.isOpen()).to.be.true
  })

  it('Given I answer the relationship questions for Joe Bloggs when answer the relationship questions for Jane Doe then I should not have to enter relationship details for John Doe', function() {
    // Given
    startQuestionnaire(schema)
    HouseholdCompositionPage.setPersonName(0, 'Joe Bloggs')
      .addPerson()
      .setPersonName(1, 'Jane Doe')
      .addPerson()
      .setPersonName(2, 'John Doe')
      .submit()
    HouseholdRelationshipPage.setHusbandOrWifeRelationship(0)
      .setSonOrDaughterRelationship(1)
      .submit()

    // When
    HouseholdRelationshipPage.setHusbandOrWifeRelationship(0)
      .submit()

    // Then
    expect(SummaryPage.isOpen()).to.be.true
  })

})
