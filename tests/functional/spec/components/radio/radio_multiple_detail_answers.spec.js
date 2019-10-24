const MandatoryRadioPage = require('../../../generated_pages/radio_multiple_detail_answers/radio-mandatory.page');
const SummaryPage = require('../../../generated_pages/radio_multiple_detail_answers/summary.page');

describe('Radio with multiple "detail_answer" options', function() {
  const radio_schema = 'test_radio_multiple_detail_answers.json';

  it('Given detail answer options are available, When the user clicks an option, Then the detail answer input should be visible.', function() {
    browser.openQuestionnaire(radio_schema);
    $(MandatoryRadioPage.eggs()).click();
    expect($(MandatoryRadioPage.eggsDetail()).isDisplayed()).to.be.true;
    $(MandatoryRadioPage.favouriteNotListed()).click();
    expect($(MandatoryRadioPage.favouriteNotListedDetail()).isDisplayed()).to.be.true;
  });

  it('Given a mandatory detail answer, When I select the option but leave the input field empty and submit, Then an error should be displayed.', function() {
    // Given
    browser.openQuestionnaire(radio_schema);
  // When
    $(MandatoryRadioPage.favouriteNotListed()).click();
    $(MandatoryRadioPage.submit()).click();
  // Then
    expect($(MandatoryRadioPage.error()).isDisplayed()).to.be.true;
    expect($(MandatoryRadioPage.errorNumber(1)).getText()).to.contain('Enter your favourite to continue');
  });

  it('Given a selected radio answer with an error for a mandatory detail answer, When I enter valid value and submit the page, Then the error is cleared and I navigate to next page.', function() {
    // Given
    browser.openQuestionnaire(radio_schema);
    $(MandatoryRadioPage.favouriteNotListed()).click();
    $(MandatoryRadioPage.submit()).click();
    expect($(MandatoryRadioPage.error()).isDisplayed()).to.be.true;

  // When
    $(MandatoryRadioPage.favouriteNotListedDetail()).setValue('Bacon');
    $(MandatoryRadioPage.submit()).click();
    expect(browser.getUrl()).to.contain(SummaryPage.pageName);
  });


  it('Given a non-mandatory detail answer, When the user does not provide any text, Then just the option value should be displayed on the summary screen', function() {
    // Given
    browser.openQuestionnaire(radio_schema);
  // When
    $(MandatoryRadioPage.eggs()).click();
    expect($(MandatoryRadioPage.eggsDetail()).isDisplayed()).to.be.true;
    $(MandatoryRadioPage.submit()).click();
  // Then
    expect($(SummaryPage.radioMandatoryAnswer()).getText()).to.equal('Eggs');
  });

  it('Given a detail answer, When the user provides text, Then that text should be displayed on the summary screen', function() {
    // Given
    browser.openQuestionnaire(radio_schema);
    // When
    $(MandatoryRadioPage.eggs()).click();
    $(MandatoryRadioPage.eggsDetail()).setValue('Scrambled');
    $(MandatoryRadioPage.submit()).click();
    // Then
    expect($(SummaryPage.radioMandatoryAnswer()).getText()).to.equal('Eggs\nScrambled');
  });


  it('Given I have previously added text in a detail answer and saved, When I select a different radio and save, Then the text entered in the detail answer field should be empty.', function() {
    // Given
    browser.openQuestionnaire(radio_schema);
    // When
    $(MandatoryRadioPage.favouriteNotListed()).click();
    $(MandatoryRadioPage.favouriteNotListedDetail()).setValue('Bacon');
    $(MandatoryRadioPage.submit()).click();
    $(SummaryPage.previous()).click();
    $(MandatoryRadioPage.eggs()).click();
    $(MandatoryRadioPage.submit()).click();
    $(SummaryPage.previous()).click();
    // Then
    $(MandatoryRadioPage.favouriteNotListed()).click();
    expect($(MandatoryRadioPage.favouriteNotListedDetail()).getValue()).to.equal('');
  });
});
