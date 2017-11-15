const helpers = require('../helpers');
const QuestionPage = require('../pages/surveys/question.page');
const PipingAddressPage = require('../pages/surveys/piping/what-is-your-address.page');
const PipingPersonPage = require('../pages/surveys/piping/household-composition.page');
const MultiplePipingPage = require('../pages/surveys/piping/term-time-location.page');
const PipingSummaryPage = require('../pages/surveys/piping/summary.page');

describe('Multiple piping into question and answer', function() {

    var piping_schema = 'test_multiple_piping.json';

  it('Given I enter values into multiple address fields, when i navigate to term-time-location question, I should see all values separated  by commas and spaces', function() {
    return helpers.openQuestionnaire(piping_schema).then(() => {
      return browser
        .setValue(PipingAddressPage.addressLine1(), '1 The ONS')
        .setValue(PipingAddressPage.townCity(), 'Newport')
        .setValue(PipingAddressPage.postcode(), 'NP10 8XG')
        .setValue(PipingAddressPage.country(), 'Wales')
        .click(PipingAddressPage.submit())
        .setValue(PipingPersonPage.firstName(), 'Fireman')
        .setValue(PipingPersonPage.lastName(), 'Sam')
        .click(PipingPersonPage.submit())
        .getText(MultiplePipingPage.atYourAddress()).should.eventually.contain('1 The ONS, Newport, NP10 8XG, Wales');
    });
  });

  it('Given I enter a value into address line 1 and enter a person on the next page, when i navigate to term-time-location question, both the name and address line 1 in the question', function() {
    return helpers.openQuestionnaire(piping_schema).then(() => {
      return browser
        .setValue(PipingAddressPage.addressLine1(), '1 The ONS')
        .click(PipingAddressPage.submit())
        .setValue(PipingPersonPage.firstName(), 'Fireman')
        .setValue(PipingPersonPage.lastName(), 'Sam')
        .click(PipingPersonPage.submit())
        .getText(MultiplePipingPage.questionText()).should.eventually.contain('During term time, does Fireman Sam live at 1 The ONS');
    });
  });
});
