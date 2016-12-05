import chai from 'chai'
import {startQuestionnaire} from '../helpers'
import HouseholdCompositionPage from '../pages/surveys/household_composition/household-composition.page'
import HouseholdRelationshipPage from '../pages/surveys/relationship/household-relationship.page'
import SummaryPage from '../pages/summary.page'

const expect = chai.expect

describe('Household relationship', function() {

  var schema = 'test_relationship_household.json'

  it('Given I have added Joe Bloggs, Jane Doe and John Doe to my household when I set Joe Bloggs relationships then I should see the questions `Joe Bloggs is the husband or wife of Jane Doe` and `Joe Bloggs is the son or daughter of John Doe`', function() {
    // Given
    startQuestionnaire(schema)
    HouseholdCompositionPage.setPersonName(0, 'Joe Bloggs')
      .addPerson()
      .setPersonName(1, 'Jane Doe')
      .addPerson()
      .setPersonName(2, 'John Doe')
      .submit()

    // When
    HouseholdRelationshipPage.setHusbandOrWifeRelationship(0)
      .setSonOrDaughterRelationship(1)

    // Then
    expect(HouseholdRelationshipPage.getRelationshipLabelAt(0)).to.have.string('Joe Bloggs is the husband or wife of Jane Doe')
    expect(HouseholdRelationshipPage.getRelationshipLabelAt(1)).to.have.string('Joe Bloggs is the son or daughter of John Doe');
  })

  it('Given I have answered how Joe Bloggs is related Jane Doe and John Doe when I go to the next relationship question then I should see the questions `Jane Doe is the … of John Doe`', function() {
    // Given
    startQuestionnaire(schema)
    HouseholdCompositionPage.setPersonName(0, 'Joe Bloggs')
      .addPerson()
      .setPersonName(1, 'Jane Doe')
      .addPerson()
      .setPersonName(2, 'John Doe')
      .submit()

    // When
    HouseholdRelationshipPage.setHusbandOrWifeRelationship(0)
      .setSonOrDaughterRelationship(1)
      .submit()

    // Then
    expect(HouseholdRelationshipPage.getRelationshipLabelAt(0)).to.have.string('Jane Doe is the   …   of John Doe')
  })

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
