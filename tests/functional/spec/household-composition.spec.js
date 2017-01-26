
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

  it('Given first name entered, when second name entered and RETURN pressed, should navigate to next question.', function() {
    // Given
    startQuestionnaire(household_composition_schema)

    // When
    HouseholdCompositionPage
        .setPersonName(0, 'Homer', 'J', 'Simpson')
        .addPerson()
        .setPersonName(1, 'Marge', '', 'Simpson')
        .returnKey()

    // Then
    HouseholdCompositionSummary.isNameDisplayed('Homer J Simpson')
    HouseholdCompositionSummary.isNameDisplayed('Marge Simpson')
  })

  it('Given first name entered, when second name entered and ENTER pressed, should navigate to next question.', function() {
    // Given
    startQuestionnaire(household_composition_schema)

    // When
    HouseholdCompositionPage
        .setPersonName(0, 'Homer', 'J', 'Simpson')
        .addPerson()
        .setPersonName(1, 'Marge', '', 'Simpson')
        .enterKey()

    // Then
    HouseholdCompositionSummary.isNameDisplayed('Homer J Simpson')
    HouseholdCompositionSummary.isNameDisplayed('Marge Simpson')
  })

  it('Given no name entered, when ENTER pressed, form should submit and validation should fire.', function() {
    // Given
    startQuestionnaire(household_composition_schema)

    // When
    HouseholdCompositionPage
        .setPersonName(0, '', '', '')
        .enterKey()

    // Then
    expect(HouseholdCompositionPage.errorExists()).to.be.true
  })

  it('Given more than two names entered, when ENTER pressed, form should submit navigate to next page.', function() {
    // Given
    startQuestionnaire(household_composition_schema)

    // When
    HouseholdCompositionPage
        .setPersonName(0, 'Homer', 'J', 'Simpson')
        .addPerson()
        .setPersonName(1, 'Marge', '', 'Simpson')
        .addPerson()
        .setPersonName(2, 'Lisa', '', 'Simpson')
        .addPerson()
        .setPersonName(3, 'Bart', '', 'Simpson')
        .addPerson()
        .setPersonName(4, 'Maggie', '', 'Simpson')
        .enterKey()

    // Then
    HouseholdCompositionSummary.isNameDisplayed('Homer J Simpson')
    HouseholdCompositionSummary.isNameDisplayed('Marge Simpson')
    HouseholdCompositionSummary.isNameDisplayed('Lisa Simpson')
    HouseholdCompositionSummary.isNameDisplayed('Bart Simpson')
    HouseholdCompositionSummary.isNameDisplayed('Maggie Simpson')
  })

  it('Given named entered, and we come back into the page and press ENTER, should navigate to next question.', function() {
    // Given
    startQuestionnaire(household_composition_schema)

    // When
    HouseholdCompositionPage
        .setPersonName(0, 'Homer', 'J', 'Simpson')
        .addPerson()
        .setPersonName(1, 'Marge', '', 'Simpson')
        .enterKey()
        .previous()

    // Focus on input field and press enter.
    HouseholdCompositionPage.setMiddleNames(1, '').enterKey()

    // Then
    HouseholdCompositionSummary.isNameDisplayed('Homer J Simpson')
    HouseholdCompositionSummary.isNameDisplayed('Marge Simpson')
  })

})
