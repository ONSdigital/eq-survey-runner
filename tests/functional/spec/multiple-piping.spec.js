const helpers = require('../helpers');
const AddressPage = require('../generated_pages/multiple_piping/what-is-your-address.page');
const TextfieldPage = require('../generated_pages/multiple_piping/textfield.page');
const MultiplePipingPage = require('../generated_pages/multiple_piping/piping-question.page');

describe('Piping', function() {

  var piping_schema = 'test_multiple_piping.json';

  describe('Multiple piping into question and answer', function() {
    beforeEach('load the survey', function() {
      return helpers.openQuestionnaire(piping_schema);
    });

    it('Given I enter multiple fields in one question, When I navigate to the multiple piping answer, Then I should see all values piped into an answer', function() {
      return browser
        .setValue(AddressPage.addressLine1(), '1 The ONS')
        .setValue(AddressPage.townCity(), 'Newport')
        .setValue(AddressPage.postcode(), 'NP10 8XG')
        .setValue(AddressPage.country(), 'Wales')
        .click(AddressPage.submit())
        .setValue(TextfieldPage.firstText(), 'Fireman')
        .setValue(TextfieldPage.secondText(), 'Sam')
        .click(TextfieldPage.submit())
        .getText(MultiplePipingPage.atYourAddressLabel()).should.eventually.contain('1 The ONS, Newport, NP10 8XG, Wales');
    });

    it('Given I enter values in multiple questions, When I navigate to the multiple piping question, Then I should see both values piped into the question', function() {
      return browser
        .setValue(AddressPage.addressLine1(), '1 The ONS')
        .click(AddressPage.submit())
        .setValue(TextfieldPage.firstText(), 'Fireman')
        .setValue(TextfieldPage.secondText(), 'Sam')
        .click(TextfieldPage.submit())
        .getText(MultiplePipingPage.questionText()).should.eventually.contain('Does Fireman Sam live at 1 The ONS');
    });
  });

});
