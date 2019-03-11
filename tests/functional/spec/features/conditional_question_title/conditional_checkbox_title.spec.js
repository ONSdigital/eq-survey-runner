const helpers = require('../../../helpers');
const CheckBoxPage = require('../../../generated_pages/titles_radio_and_checkbox/checkbox-block.page');
const NameEntryPage = require('../../../generated_pages/titles_radio_and_checkbox/preamble-block.page');
const RadioButtonsPage = require('../../../generated_pages/titles_radio_and_checkbox/radio-block.page');
const SummaryPage = require('../../../generated_pages/titles_radio_and_checkbox/summary.page');


describe('Feature: Conditional checkbox and radio question titles', function() {

  beforeEach(function() {
      return helpers.openQuestionnaire('test_titles_radio_and_checkbox.json');
  });

  describe('Given I start the test_titles_radio_and_checkbox survey', function() {
    it('When I enter an expected name and submit', function() {
      return browser
        .setValue(NameEntryPage.name(),'Peter')
        .click(NameEntryPage.submit())
        .getText(CheckBoxPage.questionText()).should.eventually.contain('Did Peter make changes to this business?');
    });

    it('When I enter an unknown name and go to the checkbox page', function() {
      return browser
        .setValue(NameEntryPage.name(),'Fred')
        .click(NameEntryPage.submit())
        .getText(CheckBoxPage.questionText()).should.eventually.contain('Did this business make major changes in the following areas')
        .click(CheckBoxPage.checkboxImplementationOfChangesToMarketingConceptsOrStrategies())
        .getText(RadioButtonsPage.questionText()).should.eventually.contain('Did this business make major changes in the following areas');
    });

    it('When I enter another known name page title should include selected title', function() {
      return browser
        .setValue(NameEntryPage.name(),'Mary')
        .click(NameEntryPage.submit())
        .getTitle().should.eventually.contain('Did Mary make changes to this business? - Test Survey - Checkbox and Radio titles');
    });

    it('When I enter another known name and go to the summary', function() {
      return browser
        .setValue(NameEntryPage.name(),'Mary')
        .click(NameEntryPage.submit())
        .getText(CheckBoxPage.questionText()).should.eventually.contain('Did Mary make changes to this business')
        .click(CheckBoxPage.checkboxImplementationOfChangesToMarketingConceptsOrStrategiesLabel())
        .click(CheckBoxPage.submit())
        .getText(RadioButtonsPage.questionText()).should.eventually.contain('Is Mary the boss?')
        .click(RadioButtonsPage.radioMaybe())
        .click(RadioButtonsPage.submit())
        .getText(SummaryPage.nameAnswer()).should.eventually.contain('Mary')
        .getText(SummaryPage.summaryQuestionText()).should.eventually.contain('Did Mary make changes to this business?');
    });
  });
});
