import {openQuestionnaire} from '../helpers/helpers.js'
const AddressPage = require('../../generated_pages/multiple_piping/what-is-your-address.page');
const TextfieldPage = require('../../generated_pages/multiple_piping/textfield.page');
const MultiplePipingPage = require('../../generated_pages/multiple_piping/piping-question.page');

describe('Piping', function() {

  const piping_schema = 'test_multiple_piping.json';

  describe('Multiple piping into question and answer', function() {
    beforeEach('load the survey', function() {
      openQuestionnaire(piping_schema);
    });

    it('Given I enter multiple fields in one question, When I navigate to the multiple piping answer, Then I should see all values piped into an answer', function() {
      cy
        .get(AddressPage.addressLine1()).type('1 The ONS')
        .get(AddressPage.townCity()).type('Newport')
        .get(AddressPage.postcode()).type('NP10 8XG')
        .get(AddressPage.country()).type('Wales')
        .get(AddressPage.submit()).click()
        .get(TextfieldPage.firstText()).type('Fireman')
        .get(TextfieldPage.secondText()).type('Sam')
        .get(TextfieldPage.submit()).click()
        .get(MultiplePipingPage.atYourAddressLabel()).stripText().should('contain', '1 The ONS, Newport, NP10 8XG, Wales');
    });

    it('Given I enter values in multiple questions, When I navigate to the multiple piping question, Then I should see both values piped into the question', function() {
      cy
        .get(AddressPage.addressLine1()).type('1 The ONS')
        .get(AddressPage.submit()).click()
        .get(TextfieldPage.firstText()).type('Fireman')
        .get(TextfieldPage.secondText()).type('Sam')
        .get(TextfieldPage.submit()).click()
        .get(MultiplePipingPage.questionText()).stripText().should('contain', 'Does Fireman Sam live at 1 The ONS');
    });
  });

});
