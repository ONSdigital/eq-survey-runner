import {startQuestionnaire} from '../helpers/helpers.js'

const HouseholdCompositionPage = require('../../generated_pages/household_question/household-composition.page.js');
const HouseholdSummaryPage = require('../../generated_pages/household_question/household-summary.page.js');

describe('Household Composition', function() {

  beforeEach(() => {
    startQuestionnaire('test_household_question.json')
  });

  it('Given no people added, when enter a name and submit, then name should be displayed on summary.', function() {
    cy
          .get(HouseholdCompositionPage.firstName()).type('Alpha')
          .get(HouseholdCompositionPage.lastName()).type('One')
          .get(HouseholdCompositionPage.submit()).click()
          .get(HouseholdSummaryPage.householdSummaryDescription()).stripText().should('contain', 'Alpha One');
  });

  it('Given no people added, when I add another person, then there should be two sets of input fields displayed.', function() {
    cy
          .get(HouseholdCompositionPage.addPerson()).click()
          .get(HouseholdCompositionPage.firstName()).should('exist')
          .get(HouseholdCompositionPage.firstName('_1')).should('exist')
  });


  it('Given three people added, when submitted, all three names should appear on summary.', function() {
    cy
          .get(HouseholdCompositionPage.firstName()).type('Alpha')
          .get(HouseholdCompositionPage.lastName()).type('One')
          .get(HouseholdCompositionPage.addPerson()).click()
          .get(HouseholdCompositionPage.firstName('_1')).type('Bravo')
          .get(HouseholdCompositionPage.middleNames('_1')).type('Two')
          .get(HouseholdCompositionPage.lastName('_1')).type('Zero')
          .get(HouseholdCompositionPage.addPerson()).click()
          .get(HouseholdCompositionPage.firstName('_2')).type('Charlie')
          .get(HouseholdCompositionPage.lastName('_2')).type('Three')
          .get(HouseholdCompositionPage.submit()).click()
          .get(HouseholdSummaryPage.householdSummaryDescription()).stripText().should('contain', 'Alpha One')
          .get(HouseholdSummaryPage.householdSummaryDescription()).stripText().should('contain', 'Bravo Two Zero')
          .get(HouseholdSummaryPage.householdSummaryDescription()).stripText().should('contain', 'Charlie Three');
  });

  it('Given two people added, when I remove second person, only first person should appear on summary.', function() {
    cy
          .get(HouseholdCompositionPage.firstName()).type('Alpha')
          .get(HouseholdCompositionPage.lastName()).type('One')
          .get(HouseholdCompositionPage.addPerson()).click()
          .get(HouseholdCompositionPage.firstName('_1')).type('Bravo')
          .get(HouseholdCompositionPage.lastName('_1')).type('Two')
          .get(HouseholdCompositionPage.removePerson(1)).click()
          .get(HouseholdCompositionPage.removePerson(1), {timeout: 2000}).should('not.exist' )
          .get(HouseholdCompositionPage.submit()).click()
          .get(HouseholdSummaryPage.householdSummaryDescription()).stripText().should('contain', 'Alpha One')
          .get(HouseholdSummaryPage.householdSummaryDescription()).should('not.contain', 'Bravo Two');
  });

  it('Given three people added, when I remove second person, first and third person should appear on summary.', function() {
    cy
          .get(HouseholdCompositionPage.firstName()).type('Alpha')
          .get(HouseholdCompositionPage.lastName()).type('One')
          .get(HouseholdCompositionPage.addPerson()).click()
          .get(HouseholdCompositionPage.firstName('_1')).type('Bravo')
          .get(HouseholdCompositionPage.lastName('_1')).type('Two')
          .get(HouseholdCompositionPage.addPerson()).click()
          .get(HouseholdCompositionPage.firstName('_2')).type('Charlie')
          .get(HouseholdCompositionPage.lastName('_2')).type('Three')
          .get(HouseholdCompositionPage.removePerson(1)).click()
          .get(HouseholdCompositionPage.removePerson(2), {timeout: 2000}).should('not.exist')
          .get(HouseholdCompositionPage.submit()).click()
          .get(HouseholdSummaryPage.householdSummaryDescription()).stripText().should('contain', 'Alpha One')
          .get(HouseholdSummaryPage.householdSummaryDescription()).stripText().should('contain', 'Charlie Three')
          .get(HouseholdSummaryPage.householdSummaryDescription()).should('not.contain', 'Bravo Two');
  });

  it('Given first name entered, when second name entered and RETURN pressed, should navigate to next question.', function() {
    cy
          .get(HouseholdCompositionPage.firstName()).type('Alpha')
          .get(HouseholdCompositionPage.lastName()).type('One')
          .get(HouseholdCompositionPage.addPerson()).click()
          .get(HouseholdCompositionPage.firstName('_1')).type('Bravo')
          .get(HouseholdCompositionPage.middleNames('_1')).type('Two')
          .get(HouseholdCompositionPage.lastName('_1')).type('Zero')
          .keys('\uE006')
          .get(HouseholdSummaryPage.householdSummaryDescription()).stripText().should('contain', 'Alpha One')
          .get(HouseholdSummaryPage.householdSummaryDescription()).stripText().should('contain', 'Bravo Two Zero');
  });

  it('Given first name entered, when second name entered and ENTER pressed, should navigate to next question.', function() {
    cy
          .get(HouseholdCompositionPage.firstName()).type('Alpha')
          .get(HouseholdCompositionPage.lastName()).type('One')
          .get(HouseholdCompositionPage.addPerson()).click()
          .get(HouseholdCompositionPage.firstName('_1')).type('Bravo')
          .get(HouseholdCompositionPage.middleNames('_1')).type('Two')
          .get(HouseholdCompositionPage.lastName('_1')).type('Zero')
          .keys('\uE007')
          .get(HouseholdSummaryPage.householdSummaryDescription()).stripText().should('contain', 'Alpha One')
          .get(HouseholdSummaryPage.householdSummaryDescription()).stripText().should('contain', 'Bravo Two Zero');
  });

  it('Given no name entered, when ENTER/RETURN pressed, form should submit and validation should fire.', function() {
    cy
          .get(HouseholdCompositionPage.firstName()).type('')
          .get(HouseholdCompositionPage.lastName()).type('')
          .keys('\uE006')
          .get(HouseholdCompositionPage.alert()).should('exist')
          .keys('\uE007')
          .get(HouseholdCompositionPage.alert()).should('exist');
  });

  it('Given named entered, and we come back into the page and press ENTER, should navigate to next question', function() {
    cy
          .get(HouseholdCompositionPage.firstName()).type('Bravo')
          .get(HouseholdCompositionPage.middleNames()).type('Two')
          .keys('\uE006')
          .get(HouseholdSummaryPage.previous()).click()
          .get(HouseholdCompositionPage.lastName()).type('Zero')
          .keys('\uE007')
          .get(HouseholdSummaryPage.householdSummaryDescription()).stripText().should('contain', 'Bravo Two Zero');
  });

  it('Given a census household survey, when a user adds a new person, the "Person x" count should increment in the hidden legend', function() {
    cy
          .get(HouseholdCompositionPage.personLegend(1)).should('exist')
          .get(HouseholdCompositionPage.personLegend(2)).should('not.exist')
          .get(HouseholdCompositionPage.addPerson()).click()
          .get(HouseholdCompositionPage.personLegend(2)).should('exist')
          .get(HouseholdCompositionPage.personLegend(3)).should('not.exist')
          .get(HouseholdCompositionPage.addPerson()).click()
          .get(HouseholdCompositionPage.personLegend(3)).should('exist')
          .get(HouseholdCompositionPage.personLegend(4)).should('not.exist')
          .get(HouseholdCompositionPage.addPerson()).click()
          .get(HouseholdCompositionPage.personLegend(4)).should('exist');
  });


  it('Given first name entered, when second name entered and ENTER pressed, should navigate to next question.', function() {
    cy
          .get(HouseholdCompositionPage.addPerson()).click()
          .get(HouseholdCompositionPage.addPerson()).click()
          .keys('\uE007')
          .get(HouseholdCompositionPage.errorNumber()).should('exist')
          .get(HouseholdCompositionPage.errorNumber(2)).should('exist')
          .get(HouseholdCompositionPage.errorNumber(3)).should('exist');
  });

});

