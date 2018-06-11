const helpers = require('../../../helpers');


describe('Feature: Conditional checkbox and radio question titles', function() {
  var CheckBoxPage = require('../../../pages/features/conditional_checkbox_titles/checkbox-block.page');
  var NameEntryPage = require('../../../pages/features/conditional_checkbox_titles/preamble-block.page');
  var RadioButtonsPage = require('../../../pages/features/conditional_checkbox_titles/radio-block.page');
  var SummaryPage = require('../../../pages/features/conditional_checkbox_titles/summary.page');

  beforeEach(function() {
      return helpers.openQuestionnaire('test_titles_radio_and_checkbox.json');
  });

  describe('Given I start the test_titles_radio_and_checkbox survey', function() {
    it('When I enter an expected name and submit', function() {
      return browser
        .setValue(NameEntryPage.answer(),'Peter')
        .click(NameEntryPage.submit())
        .getText(CheckBoxPage.questionText()).should.eventually.contain('Did Peter make changes to this business?');
    });

    it('When I enter an unknown name and go to the checkbox page', function() {
      return browser
        .setValue(NameEntryPage.answer(),'Fred')
        .click(NameEntryPage.submit())
        .getText(CheckBoxPage.questionText()).should.eventually.contain('Did this business make major changes in the following areas')
        .click(CheckBoxPage.implementationOfChangesToMarketingConceptsOrStrategies())
        .getText(RadioButtonsPage.questionText()).should.eventually.contain('Did this business make major changes in the following areas');
    });

    it('When I enter another known name page title should include selected title', function() {
      return browser
        .setValue(NameEntryPage.answer(),'Mary')
        .click(NameEntryPage.submit())
        .getTitle().should.eventually.contain('Did Mary make changes to this business? - Test Survey - Checkbox and Radio titles');
    });

    it('When I enter another known name and go to the summary', function() {
      return browser
        .setValue(NameEntryPage.answer(),'Mary')
        .click(NameEntryPage.submit())
        .getText(CheckBoxPage.questionText()).should.eventually.contain('Did Mary make changes to this business')
        .click(CheckBoxPage.implementationOfChangesToMarketingConceptsOrStrategies())
        .click(CheckBoxPage.submit())
        .getText(RadioButtonsPage.questionText()).should.eventually.contain('Is Mary the boss?')
        .click(RadioButtonsPage.newMethodsOfOrganisingExternalRelationshipsWithOtherFirmsOrPublicInstitutions())
        .click(RadioButtonsPage.submit())
        .getText(SummaryPage.nameAnswer()).should.eventually.contain('Mary')
        .getText(SummaryPage.summaryQuestionText()).should.eventually.contain('Did Mary make changes to this business?');
    });
  });
});
