import {openQuestionnaire} from '../helpers/helpers.js'
const TextFieldPage = require('../../generated_pages/textfield/name-block.page.js');
const MinMaxBlockPage = require('../../generated_pages/textfield/min-max-block.page');
const SummaryPage = require('../../generated_pages/textfield/summary.page.js');

describe('Textfield', function() {

  it('Given a textfield option, a user should be able to click the label of the textfield to focus', function() {
    openQuestionnaire('test_textfield.json')
              .get(TextFieldPage.nameLabel()).click()
        .focused().should('match', TextFieldPage.name())
      });
    });

  it('Given a text entered in textfield , When user submits and revisits the textfield, Then the textfield must contain the text entered previously', function() {
    openQuestionnaire('test_textfield.json')
              .get(TextFieldPage.name()).type("'Twenty><&Five'")
        .get(TextFieldPage.submit()).click()
        // Interstitial displaying min-max formats
        .get(MinMaxBlockPage.submit()).click()
        .url().should('contain', SummaryPage.pageName)
        .get(SummaryPage.nameAnswer()).stripText().should('contain', "Twenty><&Five'")
        .get(SummaryPage.nameAnswerEdit()).click()
        .getValue(TextFieldPage.name()).should.eventually.contain("'Twenty><&Five'");
      });
    });
});
