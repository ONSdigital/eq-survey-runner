
import chai from 'chai'
import {startQuestionnaire} from '../helpers'
import HouseholdCompositionPage from '../pages/surveys/household_composition/household-composition.page'
import HouseholdCompositionSummary from '../pages/surveys/household_composition/summary.page'

const expect = chai.expect
const assert = chai.assert

describe('Household composition question for census test.', function() {

  var household_composition_schema = 'test_household_question.json';

  it('Given no people added, when enter a name and submit, then name should be displayed on summary.', function() {
    //Given
    startQuestionnaire(household_composition_schema)

    //When
    HouseholdCompositionPage.setPersonName(0, 'Alpha', '', 'One').submit()

    // Then
    HouseholdCompositionSummary.isNameDisplayed('Alpha One')
  })

  it('Given no people added, when I enter another name, then there should be two input fields displayed.', function() {
    //Given
    startQuestionnaire(household_composition_schema)

    //When
    HouseholdCompositionPage.setPersonName(0, 'Alpha', '', 'One').addPerson()

    // Then
    expect(HouseholdCompositionPage.isInputVisible(0, 'first-name')).to.be.true
    expect(HouseholdCompositionPage.isInputVisible(1, 'first-name')).to.be.true
  })

  it('Given three people added, when submitted, all three names should appear on summary.', function() {
    //Given
    startQuestionnaire(household_composition_schema)

    //When
    HouseholdCompositionPage
        .setPersonName(0, 'Alpha', '', 'One')
        .addPerson()
        .setPersonName(1, 'Bravo', '', 'Two')
        .addPerson()
        .setPersonName(2, 'Charlie', '', 'Three')
        .submit()

    // Then
    HouseholdCompositionSummary.isNameDisplayed('Alpha One')
    HouseholdCompositionSummary.isNameDisplayed('Bravo Two')
    HouseholdCompositionSummary.isNameDisplayed('Charlie Three')
  })

 it('Given two people added, when I remove second person, only first person should appear on summary.', function() {
    //Given
    startQuestionnaire(household_composition_schema)

    //When
    HouseholdCompositionPage
        .setPersonName(0, 'Alpha', '', 'One')
        .addPerson()
        .setPersonName(1, 'Bravo', '', 'Two')
        .submit()

    // Then
    HouseholdCompositionSummary.isNameDisplayed('Alpha')
    HouseholdCompositionSummary.isNameDisplayed('Bravo')

    // When
    HouseholdCompositionSummary.clickAddAnother().submit()
    HouseholdCompositionPage.removePerson(1).submit()

    // Then

    HouseholdCompositionSummary.isNameDisplayed('Alpha')
    HouseholdCompositionSummary.isNameDisplayed('Bravo')
  })

 it('Given three people added, when I remove second person, first and third person should appear on summary.', function() {
    //Given
    startQuestionnaire(household_composition_schema)

    //When
    HouseholdCompositionPage
        .setPersonName(0, 'Alpha', '', 'One')
        .addPerson()
        .setPersonName(1, 'Bravo', '', 'Two')
        .addPerson()
        .setPersonName(2, 'Charlie', '', 'Three')
        .submit()

    // Then
    HouseholdCompositionSummary.isNameDisplayed('Alpha One')
    HouseholdCompositionSummary.isNameDisplayed('Bravo Two')
    HouseholdCompositionSummary.isNameDisplayed('Charlie Three')

    // When
    HouseholdCompositionSummary.clickAddAnother().submit()
    HouseholdCompositionPage.removePerson(1).submit()

    // Then
    HouseholdCompositionSummary.isNameDisplayed('Alpha One')
    HouseholdCompositionSummary.isNameDisplayed('Charlie Three')
  })

  it('Given first, middle and last names entered, then each part of name should appear on summary.', function() {
    //Given
    startQuestionnaire(household_composition_schema)

    //When
    HouseholdCompositionPage
        .setPersonName(0, 'Alpha', 'Bravo', 'Charlie')
        .addPerson()
        .setPersonName(1, 'Delta', 'Echo', 'Foxtrot')
        .submit()

    // Then
    HouseholdCompositionSummary.isNameDisplayed('Alpha Bravo Charlie')
    HouseholdCompositionSummary.isNameDisplayed('Delta Echo Foxtrot')
  })

})
