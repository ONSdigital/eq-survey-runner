import {openQuestionnaire} from '../helpers/helpers.js'
const TextFieldPage = require('../../generated_pages/textfield/name-block.page.js');
const MinMaxBlockPage = require('../../generated_pages/textfield/min-max-block.page');
const SummaryPage = require('../../generated_pages/textfield/summary.page.js');

describe('Textfield', function() {
  beforeEach(() => {
    openQuestionnaire('test_textfield.json')
  })

  it('Given a textfield option, a user should be able to click the label of the textfield to focus', function() {
    cy
      .get(TextFieldPage.nameLabel()).click()
      .focused().should('match', TextFieldPage.name())
  });

  it('Given a text entered in textfield , When user submits and revisits the textfield, Then the textfield must contain the text entered previously', function() {
    cy
      .get(TextFieldPage.name()).type("'Twenty><&Five'")
      .get(TextFieldPage.submit()).click()
      // Interstitial displaying min-max formats
      .get(MinMaxBlockPage.submit()).click()
      .url().should('contain', SummaryPage.pageName)
      .get(SummaryPage.nameAnswer()).stripText().should('contain', "Twenty><&Five'")
      .get(SummaryPage.nameAnswerEdit()).click()
      .get(TextFieldPage.name()).invoke('val').should('contain', "'Twenty><&Five'");
  });
});
