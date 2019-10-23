const helpers = require('../../../helpers');
const CheckBoxPage = require('../../../generated_pages/titles_radio_and_checkbox/checkbox-block.page');
const NameEntryPage = require('../../../generated_pages/titles_radio_and_checkbox/preamble-block.page');
const RadioButtonsPage = require('../../../generated_pages/titles_radio_and_checkbox/radio-block.page');
const SummaryPage = require('../../../generated_pages/titles_radio_and_checkbox/summary.page');


describe('Feature: Conditional checkbox and radio question titles', function() {
  let browser;

  beforeEach(function() {
      browser = helpers.openQuestionnaire('test_titles_radio_and_checkbox.json')
        .then(openBrowser => browser = openBrowser);;
  });

  describe('Given I start the test_titles_radio_and_checkbox survey', function() {
    it('When I enter an expected name and submit', function() {
        $(NameEntryPage.name()).setValue('Peter');
        $(NameEntryPage.submit()).click();
        expect($(CheckBoxPage.questionText()).getText()).to.contain('Did Peter make changes to this business?');
    });

    it('When I enter an unknown name and go to the checkbox page', function() {
        $(NameEntryPage.name()).setValue('Fred');
        $(NameEntryPage.submit()).click();
        expect($(CheckBoxPage.questionText()).getText()).to.contain('Did this business make major changes in the following areas');
        $(CheckBoxPage.checkboxImplementationOfChangesToMarketingConceptsOrStrategies()).click();
        expect($(RadioButtonsPage.questionText()).getText()).to.contain('Did this business make major changes in the following areas');
    });

    it('When I enter another known name page title should include selected title', function() {
        $(NameEntryPage.name()).setValue('Mary');
        $(NameEntryPage.submit()).click();

        expect(browser.getTitle()).to.contain('Did Mary make changes to this business? - Test Survey - Checkbox and Radio titles');
    });

    it('When I enter another known name and go to the summary', function() {
        $(NameEntryPage.name()).setValue('Mary');
        $(NameEntryPage.submit()).click();
        expect($(CheckBoxPage.questionText()).getText()).to.contain('Did Mary make changes to this business');
        $(CheckBoxPage.checkboxImplementationOfChangesToMarketingConceptsOrStrategiesLabel()).click();
        $(CheckBoxPage.submit()).click();
        expect($(RadioButtonsPage.questionText()).getText()).to.contain('Is Mary the boss?');
        $(RadioButtonsPage.radioMaybe()).click();
        $(RadioButtonsPage.submit()).click();
        expect($(SummaryPage.nameAnswer()).getText()).to.contain('Mary');
        expect($(SummaryPage.checkboxQuestion()).getText()).to.contain('Did Mary make changes to this business?');
    });
  });
});
