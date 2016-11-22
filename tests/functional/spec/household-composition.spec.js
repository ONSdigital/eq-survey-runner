
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
    HouseholdCompositionPage.setPersonName(0, 'Person One').submit()

    // Then
    expect(HouseholdCompositionSummary.isNameDisplayed('Person One')).to.be.true
  })

  it('Given no people added, when I enter another name, then there should be two input fields displayed.', function() {
    //Given
    startQuestionnaire(household_composition_schema)

    //When
    HouseholdCompositionPage.setPersonName(0, 'Person One').addPerson()

    // Then
    expect(HouseholdCompositionPage.isInputVisible(0)).to.be.true
    expect(HouseholdCompositionPage.isInputVisible(1)).to.be.true
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
    var names = HouseholdCompositionSummary.getHouseholdNames()
    assert.include(names, 'Person One')
    assert.include(names, 'Person Two')
    assert.include(names, 'Person Three')
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
    var names = HouseholdCompositionSummary.getHouseholdNames()
    assert.include(names, 'Person One')
    assert.include(names, 'Person Two')

    // When
    HouseholdCompositionSummary.clickEdit()
    HouseholdCompositionPage.removePerson(1).submit()

    // Then
    names = HouseholdCompositionSummary.getHouseholdNames()
    assert.include(names, 'Person One')
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
    var names = HouseholdCompositionSummary.getHouseholdNames()
    assert.include(names, 'Person One')
    assert.include(names, 'Person Two')
    assert.include(names, 'Person Three')

    // When
    HouseholdCompositionSummary.clickEdit()
    HouseholdCompositionPage.removePerson(1).submit()

    // Then
    names = HouseholdCompositionSummary.getHouseholdNames()
    assert.include(names, 'Person One')
    assert.include(names, 'Person Three')
  })

})
