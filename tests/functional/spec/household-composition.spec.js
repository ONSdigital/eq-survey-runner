const helpers = require('../helpers');

const HouseholdCompositionPage = require('../generated_pages/household_question/household-composition.page.js');
const HouseholdSummaryPage = require('../generated_pages/household_question/household-summary.page.js');

describe('Household Composition', function() {

  it('Given no people added, when enter a name and submit, then name should be displayed on summary.', function() {
    return helpers.startQuestionnaire('test_household_question.json').then(() => {
        return browser
          .setValue(HouseholdCompositionPage.firstName(),'Alpha')
          .setValue(HouseholdCompositionPage.lastName(),'One')
          .click(HouseholdCompositionPage.submit())
          .getText(HouseholdSummaryPage.householdSummaryDescription()).should.eventually.contain('Alpha One');
    });
  });

  it('Given no people added, when I add another person, then there should be two sets of input fields displayed.', function() {
    return helpers.startQuestionnaire('test_household_question.json').then(() => {
        return browser
          .click(HouseholdCompositionPage.addPerson())
          .isExisting(HouseholdCompositionPage.firstName()).should.eventually.be.true
          .isExisting(HouseholdCompositionPage.firstName('_1')).should.eventually.be.true;
    });
  });


  it('Given three people added, when submitted, all three names should appear on summary.', function() {
    return helpers.startQuestionnaire('test_household_question.json').then(() => {
        return browser
          .setValue(HouseholdCompositionPage.firstName(),'Alpha')
          .setValue(HouseholdCompositionPage.lastName(),'One')
          .click(HouseholdCompositionPage.addPerson())
          .setValue(HouseholdCompositionPage.firstName('_1'),'Bravo')
          .setValue(HouseholdCompositionPage.middleNames('_1'),'Two')
          .setValue(HouseholdCompositionPage.lastName('_1'),'Zero')
          .click(HouseholdCompositionPage.addPerson())
          .setValue(HouseholdCompositionPage.firstName('_2'),'Charlie')
          .setValue(HouseholdCompositionPage.lastName('_2'),'Three')
          .click(HouseholdCompositionPage.submit())
          .getText(HouseholdSummaryPage.householdSummaryDescription()).should.eventually.contain('Alpha One')
          .getText(HouseholdSummaryPage.householdSummaryDescription()).should.eventually.contain('Bravo Two Zero')
          .getText(HouseholdSummaryPage.householdSummaryDescription()).should.eventually.contain('Charlie Three');
    });
  });

  it('Given two people added, when I remove second person, only first person should appear on summary.', function() {
    return helpers.startQuestionnaire('test_household_question.json').then(() => {
        return browser
          .setValue(HouseholdCompositionPage.firstName(),'Alpha')
          .setValue(HouseholdCompositionPage.lastName(),'One')
          .click(HouseholdCompositionPage.addPerson())
          .setValue(HouseholdCompositionPage.firstName('_1'),'Bravo')
          .setValue(HouseholdCompositionPage.lastName('_1'),'Two')
          .click(HouseholdCompositionPage.removePerson(1))
          .waitForExist(HouseholdCompositionPage.removePerson(1), 2000, true)
          .click(HouseholdCompositionPage.submit())
          .getText(HouseholdSummaryPage.householdSummaryDescription()).should.eventually.contain('Alpha One')
          .getText(HouseholdSummaryPage.householdSummaryDescription()).should.not.eventually.contain('Bravo Two');
    });
  });

  it('Given three people added, when I remove second person, first and third person should appear on summary.', function() {
    return helpers.startQuestionnaire('test_household_question.json').then(() => {
        return browser
          .setValue(HouseholdCompositionPage.firstName(),'Alpha')
          .setValue(HouseholdCompositionPage.lastName(),'One')
          .click(HouseholdCompositionPage.addPerson())
          .setValue(HouseholdCompositionPage.firstName('_1'),'Bravo')
          .setValue(HouseholdCompositionPage.lastName('_1'),'Two')
          .click(HouseholdCompositionPage.addPerson())
          .setValue(HouseholdCompositionPage.firstName('_2'),'Charlie')
          .setValue(HouseholdCompositionPage.lastName('_2'),'Three')
          .click(HouseholdCompositionPage.removePerson(1))
          .waitForExist(HouseholdCompositionPage.removePerson(2), 2000, true)
          .click(HouseholdCompositionPage.submit())
          .getText(HouseholdSummaryPage.householdSummaryDescription()).should.eventually.contain('Alpha One')
          .getText(HouseholdSummaryPage.householdSummaryDescription()).should.eventually.contain('Charlie Three')
          .getText(HouseholdSummaryPage.householdSummaryDescription()).should.not.eventually.contain('Bravo Two');
    });
  });

  it('Given first name entered, when second name entered and RETURN pressed, should navigate to next question.', function() {
    return helpers.startQuestionnaire('test_household_question.json').then(() => {
        return browser
          .setValue(HouseholdCompositionPage.firstName(),'Alpha')
          .setValue(HouseholdCompositionPage.lastName(),'One')
          .click(HouseholdCompositionPage.addPerson())
          .setValue(HouseholdCompositionPage.firstName('_1'),'Bravo')
          .setValue(HouseholdCompositionPage.middleNames('_1'),'Two')
          .setValue(HouseholdCompositionPage.lastName('_1'),'Zero')
          .keys('\uE006')
          .getText(HouseholdSummaryPage.householdSummaryDescription()).should.eventually.contain('Alpha One')
          .getText(HouseholdSummaryPage.householdSummaryDescription()).should.eventually.contain('Bravo Two Zero');
    });
  });

  it('Given first name entered, when second name entered and ENTER pressed, should navigate to next question.', function() {
    return helpers.startQuestionnaire('test_household_question.json').then(() => {
        return browser
          .setValue(HouseholdCompositionPage.firstName(),'Alpha')
          .setValue(HouseholdCompositionPage.lastName(),'One')
          .click(HouseholdCompositionPage.addPerson())
          .setValue(HouseholdCompositionPage.firstName('_1'),'Bravo')
          .setValue(HouseholdCompositionPage.middleNames('_1'),'Two')
          .setValue(HouseholdCompositionPage.lastName('_1'),'Zero')
          .keys('\uE007')
          .getText(HouseholdSummaryPage.householdSummaryDescription()).should.eventually.contain('Alpha One')
          .getText(HouseholdSummaryPage.householdSummaryDescription()).should.eventually.contain('Bravo Two Zero');
    });
  });

  it('Given no name entered, when ENTER/RETURN pressed, form should submit and validation should fire.', function() {
    return helpers.startQuestionnaire('test_household_question.json').then(() => {
        return browser
          .setValue(HouseholdCompositionPage.firstName(),'')
          .setValue(HouseholdCompositionPage.lastName(),'')
          .keys('\uE006')
          .isExisting(HouseholdCompositionPage.alert()).should.eventually.be.true
          .keys('\uE007')
          .isExisting(HouseholdCompositionPage.alert()).should.eventually.be.true;
    });
  });

  it('Given named entered, and we come back into the page and press ENTER, should navigate to next question', function() {
    return helpers.startQuestionnaire('test_household_question.json').then(() => {
        return browser
          .setValue(HouseholdCompositionPage.firstName(),'Bravo')
          .setValue(HouseholdCompositionPage.middleNames(),'Two')
          .keys('\uE006')
          .click(HouseholdSummaryPage.previous())
          .setValue(HouseholdCompositionPage.lastName(),'Zero')
          .keys('\uE007')
          .getText(HouseholdSummaryPage.householdSummaryDescription()).should.eventually.contain('Bravo Two Zero');
    });
  });

  it('Given a census household survey, when a user adds a new person, the "Person x" count should increment in the hidden legend', function() {
    return helpers.startQuestionnaire('test_household_question.json').then(() => {
        return browser
          .isExisting(HouseholdCompositionPage.personLegend(1)).should.eventually.be.true
          .isExisting(HouseholdCompositionPage.personLegend(2)).should.eventually.be.false
          .click(HouseholdCompositionPage.addPerson())
          .isExisting(HouseholdCompositionPage.personLegend(2)).should.eventually.be.true
          .isExisting(HouseholdCompositionPage.personLegend(3)).should.eventually.be.false
          .click(HouseholdCompositionPage.addPerson())
          .isExisting(HouseholdCompositionPage.personLegend(3)).should.eventually.be.true
          .isExisting(HouseholdCompositionPage.personLegend(4)).should.eventually.be.false
          .click(HouseholdCompositionPage.addPerson())
          .isExisting(HouseholdCompositionPage.personLegend(4)).should.eventually.be.true;
    });
  });


  it('Given first name entered, when second name entered and ENTER pressed, should navigate to next question.', function() {
    return helpers.startQuestionnaire('test_household_question.json').then(() => {
        return browser
          .click(HouseholdCompositionPage.addPerson())
          .click(HouseholdCompositionPage.addPerson())
          .keys('\uE007')
          .isExisting(HouseholdCompositionPage.errorNumber()).should.eventually.be.true
          .isExisting(HouseholdCompositionPage.errorNumber(2)).should.eventually.be.true
          .isExisting(HouseholdCompositionPage.errorNumber(3)).should.eventually.be.true;
    });
  });

});

