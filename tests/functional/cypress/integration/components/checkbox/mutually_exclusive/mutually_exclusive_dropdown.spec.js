import {openQuestionnaire} from ../../../../helpers/helpers.js

const DropdownPage = require('../../../../../generated_pages/mutually_exclusive/mutually-exclusive-dropdown.page');
const SummaryPage = require('../../../../../generated_pages/mutually_exclusive/optional-dropdown-section-summary.page');

describe('Component: Mutually Exclusive Dropdown With Single Checkbox Override', function() {

  beforeEach(function() {
    openQuestionnaire('test_mutually_exclusive.json')
          return browser.get(helpers.navigationLink('Dropdown')).click();
        });
  });

  describe('Given the user has entered a value for the non-exclusive dropdown answer', function() {
    it('When then user clicks the mutually exclusive checkbox answer, Then only the mutually exclusive checkbox should be answered.', function() {

              // Given
        .get(DropdownPage.dropdown()).select('Liverpool')
        .get(DropdownPage.dropdown()).stripText().should('contain', 'Liverpool')

        // When
        .get(DropdownPage.dropdownExclusiveIPreferNotToSay()).click()

        // Then
        .isSelected(DropdownPage.dropdownExclusiveIPreferNotToSay()).should('be.true')
        .getValue(DropdownPage.dropdown()).should.eventually.contain('')


        .get(DropdownPage.submit()).click()

        .get(SummaryPage.dropdownExclusiveAnswer()).stripText().should('have.string', 'I prefer not to say')
        .get(SummaryPage.dropdownExclusiveAnswer()).should('not.have.string', 'Liverpool');

    });
  });

  describe.skip('Given the user has clicked the mutually exclusive checkbox answer', function() {
    it('When the user enters a value for the non-exclusive dropdown answer and removes focus, Then only the non-exclusive dropdown answer should be answered.', function() {

              // Given
        .get(DropdownPage.dropdownExclusiveIPreferNotToSay()).click()
        .isSelected(DropdownPage.dropdownExclusiveIPreferNotToSay()).should('be.true')

        // When
        .get(DropdownPage.dropdown()).select('Liverpool')

        // Then
        .get(DropdownPage.dropdown()).stripText().should('contain', 'Liverpool')
        .isSelected(DropdownPage.dropdownExclusiveIPreferNotToSay()).should('be.false')

        .get(DropdownPage.submit()).click()

        .get(SummaryPage.dropdownAnswer()).stripText().should('have.string', 'Liverpool')
        .get(SummaryPage.dropdownAnswer()).should('not.have.string', 'I prefer not to say');

    });
  });

  describe('Given the user has not clicked the mutually exclusive checkbox answer', function() {
    it('When the user enters a value for the non-exclusive dropdown answer, Then only the non-exclusive dropdown answer should be answered.', function() {

              // Given
        .isSelected(DropdownPage.dropdownExclusiveIPreferNotToSay()).should('be.false')

        // When
        .get(DropdownPage.dropdown()).select('Liverpool')

        // Then
        .get(DropdownPage.dropdown()).stripText().should('contain', 'Liverpool')
        .isSelected(DropdownPage.dropdownExclusiveIPreferNotToSay()).should('be.false')

        .get(DropdownPage.submit()).click()

        .get(SummaryPage.dropdownAnswer()).stripText().should('have.string', 'Liverpool')
        .get(SummaryPage.dropdownAnswer()).should('not.have.string', 'I prefer not to say');

    });
  });

  describe('Given the user has not answered the non-exclusive dropdown answer', function() {
    it('When the user clicks the mutually exclusive checkbox answer, Then only the exclusive checkbox should be answered.', function() {

              // Given
        .getValue(DropdownPage.dropdown()).should.eventually.contain('')

        // When
        .get(DropdownPage.dropdownExclusiveIPreferNotToSay()).click()
        .isSelected(DropdownPage.dropdownExclusiveIPreferNotToSay()).should('be.true')

        // Then
        .get(DropdownPage.submit()).click()

        .get(SummaryPage.dropdownExclusiveAnswer()).stripText().should('have.string', 'I prefer not to say')
        .get(SummaryPage.dropdownExclusiveAnswer()).should('not.have.string', 'Liverpool');

    });
  });

  describe('Given the user has not answered the question and the question is optional', function() {
    it('When the user clicks the Continue button, Then it should display `No answer provided`', function() {

              // Given
        .getValue(DropdownPage.dropdown()).should.eventually.contain('')

        .isSelected(DropdownPage.dropdownExclusiveIPreferNotToSay()).should('be.false')

        // When
        .get(DropdownPage.submit()).click()

        // Then
        .get(SummaryPage.dropdownAnswer()).stripText().should('contain', 'No answer provided');

    });
  });

});
