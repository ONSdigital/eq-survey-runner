import {startQuestionnaire} from '../helpers'
import HouseholdCompositionPage from '../pages/surveys/household_composition/household-composition.page'
import HouseholdCompositionSummary from '../pages/surveys/household_composition/summary.page'

describe('Household composition question for census test.', function() {

  const household_composition_schema = 'test_household_question.json';

  it('Given no people added, when enter a name and submit, then name should be displayed on summary.', function() {
    //Given
    startQuestionnaire(household_composition_schema)

    //When
    HouseholdCompositionPage.setPersonName(0, 'Alpha', '', 'One').submit()

    // Then
    expect(HouseholdCompositionSummary.isNameDisplayed(0, 'Alpha One')).to.be.true
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
    expect(HouseholdCompositionSummary.isNameDisplayed(0, 'Alpha One')).to.be.true
    expect(HouseholdCompositionSummary.isNameDisplayed(1, 'Bravo Two')).to.be.true
    expect(HouseholdCompositionSummary.isNameDisplayed(2, 'Charlie Three')).to.be.true
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
    expect(HouseholdCompositionSummary.isNameDisplayed(0, 'Alpha One')).to.be.true
    expect(HouseholdCompositionSummary.isNameDisplayed(1, 'Bravo Two')).to.be.true

    // When
    HouseholdCompositionSummary.clickAddAnother().submit()
    HouseholdCompositionPage.removePerson(1).submit()

    // Then

    expect(HouseholdCompositionSummary.isNameDisplayed(0, 'Alpha One')).to.be.true
    expect(HouseholdCompositionSummary.isNameDisplayed(1, 'Bravo Two')).to.be.false
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
    expect(HouseholdCompositionSummary.isNameDisplayed(0, 'Alpha One')).to.be.true
    expect(HouseholdCompositionSummary.isNameDisplayed(1, 'Bravo Two')).to.be.true
    expect(HouseholdCompositionSummary.isNameDisplayed(2, 'Charlie Three')).to.be.true

    // When
    HouseholdCompositionSummary.clickAddAnother().submit()
    HouseholdCompositionPage.removePerson(1).submit()

    // Then
    expect(HouseholdCompositionSummary.isNameDisplayed(0, 'Alpha One')).to.be.true
    expect(HouseholdCompositionSummary.isNameDisplayed(1, 'Charlie Three')).to.be.true
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
    expect(HouseholdCompositionSummary.isNameDisplayed(0, 'Alpha Bravo Charlie')).to.be.true
    expect(HouseholdCompositionSummary.isNameDisplayed(1, 'Delta Echo Foxtrot')).to.be.true
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
    expect(HouseholdCompositionSummary.isNameDisplayed(0, 'Homer J Simpson')).to.be.true
    expect(HouseholdCompositionSummary.isNameDisplayed(1, 'Marge Simpson')).to.be.true
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
    expect(HouseholdCompositionSummary.isNameDisplayed(0, 'Homer J Simpson')).to.be.true
    expect(HouseholdCompositionSummary.isNameDisplayed(1, 'Marge Simpson')).to.be.true
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
    expect(HouseholdCompositionSummary.isNameDisplayed(0, 'Homer J Simpson')).to.be.true
    expect(HouseholdCompositionSummary.isNameDisplayed(1, 'Marge Simpson')).to.be.true
    expect(HouseholdCompositionSummary.isNameDisplayed(2, 'Lisa Simpson')).to.be.true
    expect(HouseholdCompositionSummary.isNameDisplayed(3, 'Bart Simpson')).to.be.true
    expect(HouseholdCompositionSummary.isNameDisplayed(4, 'Maggie Simpson')).to.be.true
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
    expect(HouseholdCompositionSummary.isNameDisplayed(0, 'Homer J Simpson')).to.be.true
    expect(HouseholdCompositionSummary.isNameDisplayed(1, 'Marge Simpson')).to.be.true
  })

  it('Given a census household survey, when a user adds a new person, the "Person x" count should increment in the hidden legend', function() {
    const numPeople = 4
    startQuestionnaire(household_composition_schema)

    for (let i = 1; i < numPeople; i++) {
      HouseholdCompositionPage.addPerson()
    }

    expect(browser.getHTML('legend .js-household-loopindex', false)[numPeople - 1]).to.equal(numPeople.toString())
  })

  it('Given two more people are added, no names are added and submitted, errors should exist for all three individuals', function() {
    startQuestionnaire(household_composition_schema)

    HouseholdCompositionPage
      .addPerson()
      .addPerson()
      .submit()

      expect(browser.elements('.answer.js-has-errors').value.length).to.equal(3)

  });

})
