const helpers = require('../../helpers');

const MandatoryCheckboxPage = require('../../pages/components/checkbox/mutually-exclusive/mandatory-checkbox.page');
const SummaryPage = require('../../pages/components/checkbox/mutually-exclusive/summary.page');

describe('Component: Mutually Exclusive Checkbox', function() {

  beforeEach(function() {
    return helpers.openQuestionnaire('test_checkbox_mutually_exclusive.json');
  });

  describe('Given the user has clicked multiple non-exclusive options', function() {
    it('When then user clicks the mutually exclusive option, Then only the mutually exclusive option should be checked.', function() {

      return browser
        // Given
        .click(MandatoryCheckboxPage.cheese())
        .click(MandatoryCheckboxPage.ham())
        .click(MandatoryCheckboxPage.pineapple())

        .isSelected(MandatoryCheckboxPage.ham()).should.eventually.be.true
        .isSelected(MandatoryCheckboxPage.cheese()).should.eventually.be.true
        .isSelected(MandatoryCheckboxPage.pineapple()).should.eventually.be.true

        // When
        .click(MandatoryCheckboxPage.none())
        .isSelected(MandatoryCheckboxPage.none()).should.eventually.be.true

        // Then
        .isSelected(MandatoryCheckboxPage.cheese()).should.eventually.be.false
        .isSelected(MandatoryCheckboxPage.ham()).should.eventually.be.false
        .isSelected(MandatoryCheckboxPage.pineapple()).should.eventually.be.false

        .click(MandatoryCheckboxPage.submit())

        .getUrl().should.eventually.contain(SummaryPage.pageName)
        .getText(SummaryPage.answer()).should.eventually.have.string('No extra toppings')
        .getText(SummaryPage.answer()).should.not.eventually.have.string('Cheese\nHam\nPineapple');

    });
  });

  describe('Given the user has clicked the mutually exclusive option', function() {
    it('When the user clicks the non-exclusive options, Then only the non-exclusive options should be checked.', function() {

      return browser
        // Given
        .click(MandatoryCheckboxPage.none())
        .isSelected(MandatoryCheckboxPage.none()).should.eventually.be.true

        // When
        .click(MandatoryCheckboxPage.cheese())
        .click(MandatoryCheckboxPage.ham())
        .click(MandatoryCheckboxPage.pineapple())

        // Then
        .isSelected(MandatoryCheckboxPage.none()).should.eventually.be.false
        .isSelected(MandatoryCheckboxPage.cheese()).should.eventually.be.true
        .isSelected(MandatoryCheckboxPage.ham()).should.eventually.be.true
        .isSelected(MandatoryCheckboxPage.pineapple()).should.eventually.be.true

        .click(MandatoryCheckboxPage.submit())

        .getUrl().should.eventually.contain(SummaryPage.pageName)
        .getText(SummaryPage.answer()).should.eventually.have.string('Cheese\nHam\nPineapple')
        .getText(SummaryPage.answer()).should.not.eventually.have.string('No extra toppings');

    });
  });

  describe('Given the user has not clicked the mutually exclusive option', function() {
    it('When the user clicks multiple non-exclusive options, Then only the non-exclusive options should be checked.', function() {

      return browser
        // When
        .click(MandatoryCheckboxPage.cheese())
        .click(MandatoryCheckboxPage.ham())
        .click(MandatoryCheckboxPage.pineapple())

        // Then
        .isSelected(MandatoryCheckboxPage.cheese()).should.eventually.be.true
        .isSelected(MandatoryCheckboxPage.ham()).should.eventually.be.true
        .isSelected(MandatoryCheckboxPage.pineapple()).should.eventually.be.true

        .click(MandatoryCheckboxPage.submit())

        .getUrl().should.eventually.contain(SummaryPage.pageName)
        .getText(SummaryPage.answer()).should.eventually.have.string('Cheese\nHam\nPineapple')
        .getText(SummaryPage.answer()).should.not.eventually.have.string('No extra toppings');

    });
  });

  describe('Given the user has not clicked any of the non-exclusive options', function() {
    it('When the user clicks the mutually exclusive option, Then only the exclusive option should be checked.', function() {

      return browser
        // When
        .click(MandatoryCheckboxPage.none())
        .isSelected(MandatoryCheckboxPage.none()).should.eventually.be.true
        .click(MandatoryCheckboxPage.submit())

        // Then
        .getUrl().should.eventually.contain(SummaryPage.pageName)
        .getText(SummaryPage.answer()).should.eventually.have.string('No extra toppings')
        .getText(SummaryPage.answer()).should.not.eventually.have.string('Cheese\nHam\nPineapple');

    });
  });

});
