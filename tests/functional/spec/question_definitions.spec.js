const helpers = require('../helpers');
const DefinitionPage = require('../generated_pages/question_definition/definition-block.page');

describe('Component: Definition', function() {
  describe('Given I start a survey which contains question definition', function() {

    beforeEach(async function() {
      await helpers.openQuestionnaire('test_question_definition.json');
    });

    it('When I click the title link, then the description and "Hide this" button should be visible', function() {

        expect($(DefinitionPage.definitionContent2()).isDisplayed()).to.be.false;
        expect($(DefinitionPage.definitionButton2()).isDisplayed()).to.be.false;

        // When
        $(DefinitionPage.definitionTitle2()).click();

        // Then
        $(DefinitionPage.definitionContent2()).waitForDisplayed(300);
        $(DefinitionPage.definitionButton2()).waitForDisplayed(300);
    });

    it('When I click the title link twice, then the description and "Hide this" button should not be visible', function() {

        expect($(DefinitionPage.definitionContent2()).isDisplayed()).to.be.false;
        expect($(DefinitionPage.definitionButton2()).isDisplayed()).to.be.false;

        // When
        $(DefinitionPage.definitionTitle2()).click();
        $(DefinitionPage.definitionTitle2()).click();

        // Then
        $(DefinitionPage.definitionContent2()).waitForDisplayed(300, true);
        $(DefinitionPage.definitionButton2()).waitForDisplayed(300, true);
    });

    it('When I click the title link then click "Hide this" button, then the description and button should not be visible', function() {

        expect($(DefinitionPage.definitionContent2()).isDisplayed()).to.be.false;
        expect($(DefinitionPage.definitionButton2()).isDisplayed()).to.be.false;

        // When
        $(DefinitionPage.definitionTitle2()).click();

        // Then
        $(DefinitionPage.definitionContent2()).waitForDisplayed(300);
        $(DefinitionPage.definitionButton2()).waitForDisplayed(300);


        // When
        $(DefinitionPage.definitionButton2()).click();

        // Then
        $(DefinitionPage.definitionContent2()).waitForDisplayed(300, true);
        $(DefinitionPage.definitionButton2()).waitForDisplayed(300, true);


    });

    it('When I click the second definition\'s title link then the description and "Hide this" button for the second definition should be visible', function() {

        expect($(DefinitionPage.definitionContent3()).isDisplayed()).to.be.false;
        expect($(DefinitionPage.definitionButton3()).isDisplayed()).to.be.false;

        // When
        $(DefinitionPage.definitionTitle3()).click();

        // Then
        $(DefinitionPage.definitionContent3()).waitForDisplayed(300);
        $(DefinitionPage.definitionButton3()).waitForDisplayed(300);
    });

  });
});
