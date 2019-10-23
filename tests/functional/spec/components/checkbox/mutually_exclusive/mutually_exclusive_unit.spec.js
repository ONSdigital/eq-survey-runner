const helpers = require('../../../../helpers');

const UnitPage = require('../../../../generated_pages/mutually_exclusive/mutually-exclusive-unit.page');
const SummaryPage = require('../../../../generated_pages/mutually_exclusive/optional-unit-section-summary.page');

describe('Component: Mutually Exclusive Unit With Single Checkbox Override', function() {
  let browser;

  beforeEach(function() {
    browser = helpers.openQuestionnaire('test_mutually_exclusive.json')
    .then(openBrowser => browser = openBrowser)
    .then(function() {
        browser.url('/questionnaire/mutually-exclusive-unit');
    });
  });

  describe('Given the user has entered a value for the non-exclusive unit answer', function() {
    it('When then user clicks the mutually exclusive checkbox answer, Then only the mutually exclusive checkbox should be answered.', function() {

        // Given
        $(UnitPage.unit()).setValue('10');
        $(UnitPage.unit()).getValue();

        // When
        $(UnitPage.unitExclusiveIPreferNotToSay()).click();

        // Then
        expect($(UnitPage.unitExclusiveIPreferNotToSay()).isSelected()).to.be.true;
        $(UnitPage.unit()).getValue();

        $(UnitPage.submit()).click();

        expect($(SummaryPage.unitExclusiveAnswer()).getText()).to.have.string('I prefer not to say');
        expect($(SummaryPage.unitExclusiveAnswer()).getText()).to.not.have.string('10');

    });
  });

  describe('Given the user has clicked the mutually exclusive checkbox answer', function() {
    it('When the user enters a value for the non-exclusive unit answer and removes focus, Then only the non-exclusive unit answer should be answered.', function() {

        // Given
        $(UnitPage.unitExclusiveIPreferNotToSay()).click();
        expect($(UnitPage.unitExclusiveIPreferNotToSay()).isSelected()).to.be.true;

        // When
        $(UnitPage.unit()).setValue('10');

        // Then
        $(UnitPage.unit()).getValue();
        expect($(UnitPage.unitExclusiveIPreferNotToSay()).isSelected()).to.be.false;

        $(UnitPage.submit()).click();

        expect($(SummaryPage.unitAnswer()).getText()).to.have.string('10');
        expect($(SummaryPage.unitAnswer()).getText()).to.not.have.string('I prefer not to say');

    });
  });

  describe('Given the user has not clicked the mutually exclusive checkbox answer', function() {
    it('When the user enters a value for the non-exclusive unit answer, Then only the non-exclusive unit answer should be answered.', function() {

        // Given
        expect($(UnitPage.unitExclusiveIPreferNotToSay()).isSelected()).to.be.false;

        // When
        $(UnitPage.unit()).setValue('10');

        // Then
        $(UnitPage.unit()).getValue();
        expect($(UnitPage.unitExclusiveIPreferNotToSay()).isSelected()).to.be.false;

        $(UnitPage.submit()).click();

        expect($(SummaryPage.unitAnswer()).getText()).to.have.string('10');
        expect($(SummaryPage.unitAnswer()).getText()).to.not.have.string('I prefer not to say');

    });
  });

  describe('Given the user has not answered the non-exclusive unit answer', function() {
    it('When the user clicks the mutually exclusive checkbox answer, Then only the exclusive checkbox should be answered.', function() {

        // Given
        $(UnitPage.unit()).getValue();

        // When
        $(UnitPage.unitExclusiveIPreferNotToSay()).click();
        expect($(UnitPage.unitExclusiveIPreferNotToSay()).isSelected()).to.be.true;

        // Then
        $(UnitPage.submit()).click();

        expect($(SummaryPage.unitExclusiveAnswer()).getText()).to.have.string('I prefer not to say');
        expect($(SummaryPage.unitExclusiveAnswer()).getText()).to.not.have.string('10');

    });
  });

  describe('Given the user has not answered the question and the question is optional', function() {
    it('When the user clicks the Continue button, Then it should display `No answer provided`', function() {

        // Given
        $(UnitPage.unit()).getValue();
        expect($(UnitPage.unitExclusiveIPreferNotToSay()).isSelected()).to.be.false;

        // When
        $(UnitPage.submit()).click();

        // Then
        expect($(SummaryPage.unitAnswer()).getText()).to.contain('No answer provided');

    });
  });

});
