const helpers = require('../../../../helpers');

const DropdownPage = require('../../../../generated_pages/mutually_exclusive/mutually-exclusive-dropdown.page');
const SummaryPage = require('../../../../generated_pages/mutually_exclusive/optional-dropdown-section-summary.page');

describe('Component: Mutually Exclusive Dropdown With Single Checkbox Override', function() {

  beforeEach(function() {
    return helpers.openQuestionnaire('test_mutually_exclusive.json').then(() => {
          return browser.url('/questionnaire/mutually-exclusive-dropdown');
        });
  });

  describe('Given the user has entered a value for the non-exclusive dropdown answer', function() {
    it('When then user clicks the mutually exclusive checkbox answer, Then only the mutually exclusive checkbox should be answered.', function() {

      return browser
        // Given
        .selectByValue(DropdownPage.dropdown(), 'Liverpool')
        .getText(DropdownPage.dropdown()).should.eventually.contain('Liverpool')

        // When
        .click(DropdownPage.dropdownExclusiveIPreferNotToSay())

        // Then
        .isSelected(DropdownPage.dropdownExclusiveIPreferNotToSay()).should.eventually.be.true
        .getValue(DropdownPage.dropdown()).should.eventually.contain('')


        .click(DropdownPage.submit())

        .getText(SummaryPage.dropdownExclusiveAnswer()).should.eventually.have.string('I prefer not to say')
        .getText(SummaryPage.dropdownExclusiveAnswer()).should.not.eventually.have.string('Liverpool');

    });
  });

  describe.skip('Given the user has clicked the mutually exclusive checkbox answer', function() {
    it('When the user enters a value for the non-exclusive dropdown answer and removes focus, Then only the non-exclusive dropdown answer should be answered.', function() {

      return browser
        // Given
        .click(DropdownPage.dropdownExclusiveIPreferNotToSay())
        .isSelected(DropdownPage.dropdownExclusiveIPreferNotToSay()).should.eventually.be.true

        // When
        .selectByValue(DropdownPage.dropdown(), 'Liverpool')

        // Then
        .getText(DropdownPage.dropdown()).should.eventually.contain('Liverpool')
        .isSelected(DropdownPage.dropdownExclusiveIPreferNotToSay()).should.eventually.be.false

        .click(DropdownPage.submit())

        .getText(SummaryPage.dropdownAnswer()).should.eventually.have.string('Liverpool')
        .getText(SummaryPage.dropdownAnswer()).should.not.eventually.have.string('I prefer not to say');

    });
  });

  describe('Given the user has not clicked the mutually exclusive checkbox answer', function() {
    it('When the user enters a value for the non-exclusive dropdown answer, Then only the non-exclusive dropdown answer should be answered.', function() {

      return browser
        // Given
        .isSelected(DropdownPage.dropdownExclusiveIPreferNotToSay()).should.eventually.be.false

        // When
        .selectByValue(DropdownPage.dropdown(), 'Liverpool')

        // Then
        .getText(DropdownPage.dropdown()).should.eventually.contain('Liverpool')
        .isSelected(DropdownPage.dropdownExclusiveIPreferNotToSay()).should.eventually.be.false

        .click(DropdownPage.submit())

        .getText(SummaryPage.dropdownAnswer()).should.eventually.have.string('Liverpool')
        .getText(SummaryPage.dropdownAnswer()).should.not.eventually.have.string('I prefer not to say');

    });
  });

  describe('Given the user has not answered the non-exclusive dropdown answer', function() {
    it('When the user clicks the mutually exclusive checkbox answer, Then only the exclusive checkbox should be answered.', function() {

      return browser
        // Given
        .getValue(DropdownPage.dropdown()).should.eventually.contain('')

        // When
        .click(DropdownPage.dropdownExclusiveIPreferNotToSay())
        .isSelected(DropdownPage.dropdownExclusiveIPreferNotToSay()).should.eventually.be.true

        // Then
        .click(DropdownPage.submit())

        .getText(SummaryPage.dropdownExclusiveAnswer()).should.eventually.have.string('I prefer not to say')
        .getText(SummaryPage.dropdownExclusiveAnswer()).should.not.eventually.have.string('Liverpool');

    });
  });

  describe('Given the user has not answered the question and the question is optional', function() {
    it('When the user clicks the Continue button, Then it should display `No answer provided`', function() {

      return browser
        // Given
        .getValue(DropdownPage.dropdown()).should.eventually.contain('')

        .isSelected(DropdownPage.dropdownExclusiveIPreferNotToSay()).should.eventually.be.false

        // When
        .click(DropdownPage.submit())

        // Then
        .getText(SummaryPage.dropdownAnswer()).should.eventually.contain('No answer provided');

    });
  });

});
