const helpers = require('../helpers');
const TextareaBlock = require('../generated_pages/textarea/textarea-block.page.js');
const TextareaSummary = require('../generated_pages/textarea/textarea-summary.page.js');

describe('Textarea', function() {
  let browser;

  const textarea_schema = 'test_textarea.json';
  const textarea_limit = `${TextareaBlock.answer()} + [data-charcount-singular]`;

  it('Given a textarea option, a user should be able to click the label of the textarea to focus', function() {
    browser = helpers.openQuestionnaire(textarea_schema);
    $(TextareaBlock.answerLabel()).click();
    expect($(TextareaBlock.answer()).isFocused()).to.be.true;
  });

  it('Given a textarea option, When no text is entered, Then the summary should display "No answer provided"', function() {
    browser = helpers.openQuestionnaire(textarea_schema);
    $(TextareaBlock.submit()).click();
    expect($(TextareaSummary.answer()).getText()).to.contain('No answer provided');
  });

  it('Given a textarea option, When some text is entered, Then the summary should display the text', function() {
    browser = helpers.openQuestionnaire(textarea_schema);
    $(TextareaBlock.answer()).setValue('Some text');
    $(TextareaBlock.submit()).click();
    expect($(TextareaSummary.answer()).getText()).to.contain('Some text');
  });

  it('Given a text entered in textarea , When user submits and revisits the textarea, Then the textarea must contain the text entered previously', function() {
    browser = helpers.openQuestionnaire(textarea_schema);
    $(TextareaBlock.answer()).setValue("'Twenty><&Five'");
    $(TextareaBlock.submit()).click();
    expect($(TextareaSummary.answer()).getText()).to.contain("'Twenty><&Five'");
    $(TextareaSummary.answerEdit()).click();
    $(TextareaBlock.answer()).getValue();
  });

  it('Displays the number of characters remaining', function() {
    browser = helpers.openQuestionnaire(textarea_schema);
    expect($(textarea_limit).getText()).to.contain('20');
  });

  it('Updates the number of characters remaining when the user adds content', function() {
    browser = helpers.openQuestionnaire(textarea_schema);
    $(TextareaBlock.answer()).setValue('Banjo');
    expect($(textarea_limit).getText()).to.contain('15');
  });

  it('The user is unable to add more characters when the limit is reached', function() {
    browser = helpers.openQuestionnaire(textarea_schema);
    $(TextareaBlock.answer()).setValue('This sentence is over twenty characters long');
    expect($(textarea_limit).getText()).to.contain('0');
    $(TextareaBlock.answer()).getValue();
  });
});
