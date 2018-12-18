import {openQuestionnaire} from ../../../helpers/helpers.js
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
              .get(NameEntryPage.name()).type('Peter')
        .get(NameEntryPage.submit()).click()
        .get(CheckBoxPage.questionText()).stripText().should('contain', 'Did Peter make changes to this business?');
    });

    it('When I enter an unknown name and go to the checkbox page', function() {
              .get(NameEntryPage.name()).type('Fred')
        .get(NameEntryPage.submit()).click()
        .get(CheckBoxPage.questionText()).stripText().should('contain', 'Did this business make major changes in the following areas')
        .get(CheckBoxPage.implementationOfChangesToMarketingConceptsOrStrategies()).click()
        .get(RadioButtonsPage.questionText()).stripText().should('contain', 'Did this business make major changes in the following areas');
    });

    it('When I enter another known name page title should include selected title', function() {
              .get(NameEntryPage.name()).type('Mary')
        .get(NameEntryPage.submit()).click()
        .getTitle().should.eventually.contain('Did Mary make changes to this business? - Test Survey - Checkbox and Radio titles');
    });

    it('When I enter another known name and go to the summary', function() {
              .get(NameEntryPage.name()).type('Mary')
        .get(NameEntryPage.submit()).click()
        .get(CheckBoxPage.questionText()).stripText().should('contain', 'Did Mary make changes to this business')
        .get(CheckBoxPage.implementationOfChangesToMarketingConceptsOrStrategies()).click()
        .get(CheckBoxPage.submit()).click()
        .get(RadioButtonsPage.questionText()).stripText().should('contain', 'Is Mary the boss?')
        .get(RadioButtonsPage.maybe()).click()
        .get(RadioButtonsPage.submit()).click()
        .get(SummaryPage.nameAnswer()).stripText().should('contain', 'Mary')
        .get(SummaryPage.summaryQuestionText()).stripText().should('contain', 'Did Mary make changes to this business?');
    });
  });
});
