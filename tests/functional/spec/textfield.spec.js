const TextFieldPage = require('../generated_pages/textfield/name-block.page.js');
const SummaryPage = require('../generated_pages/textfield/summary.page.js');

describe('Textfield', function() {
  it('Given a textfield option, a user should be able to click the label of the textfield to focus', function() {
    browser.openQuestionnaire('test_textfield.json');
    $(TextFieldPage.nameLabel()).click();
    expect($(TextFieldPage.name()).isFocused()).to.be.true;
  });

  it('Given a text entered in textfield , When user submits and revisits the textfield, Then the textfield must contain the text entered previously', function() {
    browser.openQuestionnaire('test_textfield.json');
    $(TextFieldPage.name()).setValue("'Twenty><&Five'");
    $(TextFieldPage.submit()).click();
    expect(browser.getUrl()).to.contain(SummaryPage.pageName);
    expect($(SummaryPage.nameAnswer()).getText()).to.contain("Twenty><&Five'");
    $(SummaryPage.nameAnswerEdit()).click();
    $(TextFieldPage.name()).getValue();
  });
});
