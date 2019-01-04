import {openQuestionnaire} from '../helpers/helpers.js';
const DefinitionPage = require('../../generated_pages/question_definition/definition-block.page');

describe('Component: Definition', function() {
  describe('Given I start a survey which contains question definition', function() {

    beforeEach(function() {
      openQuestionnaire('test_question_definition.json');
    });

    it('When I click the title link, then the description and "Hide this" button should be visible', function() {
      cy
        .get(DefinitionPage.definitionContent1()).should('not.be.visible')
        .get(DefinitionPage.definitionButton1()).should('not.be.visible')

        // When
        .get(DefinitionPage.definitionTitle1()).click()

        // Then
        .get(DefinitionPage.definitionContent1(), {timeout: 300})
        .get(DefinitionPage.definitionButton1(), {timeout: 300});

    });

    it('When I click the title link twice, then the description and "Hide this" button should not be visible', function() {
      cy
        .get(DefinitionPage.definitionContent1()).should('not.be.visible')
        .get(DefinitionPage.definitionButton1()).should('not.be.visible')

        // When
        .get(DefinitionPage.definitionTitle1()).click()
        .get(DefinitionPage.definitionTitle1()).click()

        // Then
        .get(DefinitionPage.definitionContent1(), {timeout: 300}).should('not.be.visible')
        .get(DefinitionPage.definitionButton1(), {timeout: 300}).should('not.be.visible');

    });

    it('When I click the title link then click "Hide this" button, then the description and button should not be visible', function() {
      cy
        .get(DefinitionPage.definitionContent1()).should('not.be.visible')
        .get(DefinitionPage.definitionButton1()).should('not.be.visible')

        // When
        .get(DefinitionPage.definitionTitle1()).click()

        // Then
        .get(DefinitionPage.definitionContent1(), {timeout: 300})
        .get(DefinitionPage.definitionButton1(), {timeout: 300})

        // When
        .get(DefinitionPage.definitionButton1()).click()

        // Then
        .get(DefinitionPage.definitionContent1(), {timeout: 300}).should('not.be.visible')
        .get(DefinitionPage.definitionButton1(), {timeout: 300}).should('not.be.visible');

    });


    it('When I click the second definition\'s title link then the description and "Hide this" button for the second definition should be visible', function() {
      cy
        .get(DefinitionPage.definitionContent2()).should('not.be.visible')
        .get(DefinitionPage.definitionButton2()).should('not.be.visible')

        // When
        .get(DefinitionPage.definitionTitle2()).click()

        // Then
        .get(DefinitionPage.definitionContent2(), {timeout: 300})
        .get(DefinitionPage.definitionButton2(), {timeout: 300});

    });

  });
});
