
import chai from 'chai'
import {startQuestionnaire} from '../helpers'
import HouseholdCompositionPage from '../pages/surveys/household_composition/household-composition.page'
import HouseholdCompositionSummary from '../pages/surveys/household_composition/summary.page'

const expect = chai.expect

describe('Household composition question for census test.', function() {

  var household_composition_schema = 'test_household_question.json';

  it('Given no people added, when enter a name and submit, then name should be displayed on summary.', function() {
    //Given
    startQuestionnaire(household_composition_schema)

    //When
    HouseholdCompositionPage.setPersonName(0, 'Person One').submit()

    // Then
    expect(HouseholdCompositionSummary.isNameDisplayed('Person One')).to.be.true
  })

  it('Given no people added, when enter a name and add another person, then there should be two input fields displayed.', function() {
    //Given
    startQuestionnaire(household_composition_schema)

    //When
    HouseholdCompositionPage.setPersonName(0, 'Person One').addPerson()

    // Then
    expect(HouseholdCompositionPage.isInputVisible(0)).to.be.true
    expect(HouseholdCompositionPage.isInputVisible(1)).to.be.true
  })

  it('Given two people added, when submitted, both names should appear on summary.', function() {
    //Given
    startQuestionnaire(household_composition_schema)

    //When
    HouseholdCompositionPage
        .setPersonName(0, 'Person One')
        .addPerson()
        .setPersonName(1, 'Person Two')
        .submit()

    // Then
    expect(HouseholdCompositionSummary.areNamesDisplayed(['Person One', 'Person Two'])).to.be.true
  })

  it('Given three people added, when submitted, all three names should appear on summary.', function() {
    //Given
    startQuestionnaire(household_composition_schema)

    //When
    HouseholdCompositionPage
        .setPersonName(0, 'Person One')
        .addPerson()
        .setPersonName(1, 'Person Two')
        .addPerson()
        .setPersonName(2, 'Person Three')
        .submit()

    // Then
    expect(HouseholdCompositionSummary.areNamesDisplayed(['Person One', 'Person Two', 'Person Three'])).to.be.true
  })

 it('Given two people added, when I remove second person, only first person should appear on summary.', function() {
    //Given
    startQuestionnaire(household_composition_schema)

    //When
    HouseholdCompositionPage
        .setPersonName(0, 'Person One')
        .addPerson()
        .setPersonName(1, 'Person Two')
        .submit()

    // Then
    expect(HouseholdCompositionSummary.areNamesDisplayed(['Person One', 'Person Two'])).to.be.true

    // When
    HouseholdCompositionSummary.clickEdit()
    HouseholdCompositionPage.removePerson(1).submit()

    // Then
    expect(HouseholdCompositionSummary.areNamesDisplayed(['Person One'])).to.be.true
  })

   it('Given three people added, when I remove second person, first and third person should appear on summary.', function() {
    //Given
    startQuestionnaire(household_composition_schema)

    //When
    HouseholdCompositionPage
        .setPersonName(0, 'Person One')
        .addPerson()
        .setPersonName(1, 'Person Two')
        .addPerson()
        .setPersonName(2, 'Person Three')
        .submit()

    // Then
    expect(HouseholdCompositionSummary.areNamesDisplayed(['Person One', 'Person Two', 'Person Three'])).to.be.true

    // When
    HouseholdCompositionSummary.clickEdit()
    HouseholdCompositionPage.removePerson(1).submit()

    // Then
    expect(HouseholdCompositionSummary.areNamesDisplayed(['Person One', 'Person Three'])).to.be.true
  })

})
