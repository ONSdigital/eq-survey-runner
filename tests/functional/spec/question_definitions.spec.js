const helpers = require('../helpers');
const DefinitionPage = require('../generated_pages/question_definition/definition-block.page');

describe('Component: Definition', function() {
  describe('Given I start a survey which contains question definition', function() {

    beforeEach(function() {
      return helpers.openQuestionnaire('test_question_definition.json');
    });

    it('When I click the title link, then the description and "Hide this" button should be visible', function() {

      return browser
        .isVisible(DefinitionPage.definitionContent1()).should.eventually.be.false
        .isVisible(DefinitionPage.definitionButton1()).should.eventually.be.false

        // When
        .click(DefinitionPage.definitionTitle1())

        // Then
        .waitForVisible(DefinitionPage.definitionContent1(), 300)
        .waitForVisible(DefinitionPage.definitionButton1(), 300);

    });

    it('When I click the title link twice, then the description and "Hide this" button should not be visible', function() {

      return browser
        .isVisible(DefinitionPage.definitionContent1()).should.eventually.be.false
        .isVisible(DefinitionPage.definitionButton1()).should.eventually.be.false

        // When
        .click(DefinitionPage.definitionTitle1())
        .click(DefinitionPage.definitionTitle1())

        // Then
        .waitForVisible(DefinitionPage.definitionContent1(), 300, true)
        .waitForVisible(DefinitionPage.definitionButton1(), 300, true);

    });

    it('When I click the title link then click "Hide this" button, then the description and button should not be visible', function() {

      return browser
        .isVisible(DefinitionPage.definitionContent1()).should.eventually.be.false
        .isVisible(DefinitionPage.definitionButton1()).should.eventually.be.false

        // When
        .click(DefinitionPage.definitionTitle1())

        // Then
        .waitForVisible(DefinitionPage.definitionContent1(), 300)
        .waitForVisible(DefinitionPage.definitionButton1(), 300)

        // When
        .click(DefinitionPage.definitionButton1())

        // Then
        .waitForVisible(DefinitionPage.definitionContent1(), 300, true)
        .waitForVisible(DefinitionPage.definitionButton1(), 300, true);

    });


    it('When I click the second definition\'s title link then the description and "Hide this" button for the second definition should be visible', function() {

      return browser
        .isVisible(DefinitionPage.definitionContent2()).should.eventually.be.false
        .isVisible(DefinitionPage.definitionButton2()).should.eventually.be.false

        // When
        .click(DefinitionPage.definitionTitle2())

        // Then
        .waitForVisible(DefinitionPage.definitionContent2(), 300)
        .waitForVisible(DefinitionPage.definitionButton2(), 300);

    });

  });
});
