const helpers = require('../helpers');
const AddressPage = require('../generated_pages/multiple_piping/what-is-your-address.page');
const TextfieldPage = require('../generated_pages/multiple_piping/textfield.page');
const MultiplePipingPage = require('../generated_pages/multiple_piping/piping-question.page');

describe('Piping', function() {
  const piping_schema = 'test_multiple_piping.json';

  describe('Multiple piping into question and answer', function() {
    beforeEach('load the survey', function() {
      helpers.openQuestionnaire(piping_schema);
    });

    it('Given I enter multiple fields in one question, When I navigate to the multiple piping answer, Then I should see all values piped into an answer', function() {
        $(AddressPage.addressLine1()).setValue('1 The ONS');
        $(AddressPage.townCity()).setValue('Newport');
        $(AddressPage.postcode()).setValue('NP10 8XG');
        $(AddressPage.country()).setValue('Wales');
        $(AddressPage.submit()).click();
        $(TextfieldPage.firstText()).setValue('Fireman');
        $(TextfieldPage.secondText()).setValue('Sam');
        $(TextfieldPage.submit()).click();
        expect($(MultiplePipingPage.atYourAddressLabel()).getText()).to.contain('1 The ONS, Newport, NP10 8XG, Wales');
    });

    it('Given I enter values in multiple questions, When I navigate to the multiple piping question, Then I should see both values piped into the question', function() {
        $(AddressPage.addressLine1()).setValue('1 The ONS');
        $(AddressPage.submit()).click();
        $(TextfieldPage.firstText()).setValue('Fireman');
        $(TextfieldPage.secondText()).setValue('Sam');
        $(TextfieldPage.submit()).click();
        expect($(MultiplePipingPage.questionText()).getText()).to.contain('Does Fireman Sam live at 1 The ONS');
    });
  });
});
