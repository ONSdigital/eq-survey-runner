const helpers = require('../../helpers');

const MandatoryCheckboxPage = require('../../pages/components/checkbox/mutually-exclusive/mandatory-checkbox.page');
const SummaryPage = require('../../pages/components/checkbox/mutually-exclusive/summary.page');

describe('Component: Mutually Exclusive Checkbox', function() {

  beforeEach(function() {
    return helpers.openQuestionnaire('test_checkbox_mutually_exclusive.json').then(() => {
      return browser
        .getUrl().should.eventually.contain(MandatoryCheckboxPage.pageName);
    });
  });

  describe('Given a mutually exclusive option is available', function() {
    it('When the user clicks a range of options and the mutually exclusive option then an error should be visible.', function() {
      return browser
        .click(MandatoryCheckboxPage.cheese())
        .click(MandatoryCheckboxPage.ham())
        .click(MandatoryCheckboxPage.pineapple())
        .click(MandatoryCheckboxPage.none())
        .click(MandatoryCheckboxPage.submit())
        .isExisting(SummaryPage.errorNumber()).should.eventually.be.true
        .getText(MandatoryCheckboxPage.errorNumber()).should.eventually.contain('Uncheck "Cheese", "Ham" and "Pineapple" or "No extra toppings" to continue');
    });
  });

  describe('Given a mutually exclusive option is available', function() {
    it('When the user clicks a range of options but not the mutually exclusive option then it should go to summary.', function() {
      return browser
        .click(MandatoryCheckboxPage.cheese())
        .click(MandatoryCheckboxPage.ham())
        .click(MandatoryCheckboxPage.pineapple())
        .click(MandatoryCheckboxPage.submit())
        .getUrl().should.eventually.contain(SummaryPage.pageName)
        .getText(SummaryPage.answer()).should.eventually.have.string('Cheese\nHam\nPineapple');
    });
  });

    describe('Given a mutually exclusive option is available', function() {
    it('When the user clicks only the mutually exclusive option then it should go to summary.', function() {
      return browser
        .click(MandatoryCheckboxPage.none())
        .click(MandatoryCheckboxPage.submit())
        .getUrl().should.eventually.contain(SummaryPage.pageName)
        .getText(SummaryPage.answer()).should.eventually.have.string('No extra toppings');
    });
  });

  describe('Given an "other" option is available', function() {
    it('When the user clicks the "other" option the other input should be visible and usable.', function() {
      return browser
        .getText(MandatoryCheckboxPage.otherLabel()).should.eventually.have.string('Choose any other topping')
        .click(MandatoryCheckboxPage.other())
        .isVisible(MandatoryCheckboxPage.otherText()).should.eventually.be.true
        .setValue(MandatoryCheckboxPage.otherText(), 'Chicken')
        .click(MandatoryCheckboxPage.submit())
        .getUrl().should.eventually.contain(SummaryPage.pageName)
        .getText(SummaryPage.answer()).should.eventually.have.string('Other\nChicken');
    });
  });

});
