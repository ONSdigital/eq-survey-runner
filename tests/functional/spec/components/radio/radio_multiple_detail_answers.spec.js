const helpers = require('../../../helpers');

const MandatoryRadioPage = require('../../../generated_pages/radio_multiple_detail_answers/radio-mandatory.page');
const SummaryPage = require('../../../generated_pages/radio_multiple_detail_answers/summary.page');

describe('Radio with multiple "detail_answer" options', function() {

  const radio_schema = 'test_radio_multiple_detail_answers.json';

  it('Given detail answer options are available, When the user clicks an option, Then the detail answer input should be visible.', function() {
    return helpers.openQuestionnaire(radio_schema).then(() => {
      return browser
        .click(MandatoryRadioPage.eggs())
        .isVisible(MandatoryRadioPage.eggsDetail()).should.eventually.be.true
        .click(MandatoryRadioPage.favouriteNotListed())
        .isVisible(MandatoryRadioPage.favouriteNotListedDetail()).should.eventually.be.true;
    });
  });

  it('Given a mandatory detail answer, When I select the option but leave the input field empty and submit, Then an error should be displayed.', function() {
    // Given
    return helpers.openQuestionnaire(radio_schema).then(() => {
      return browser
      // When
        .click(MandatoryRadioPage.favouriteNotListed())
        .click(MandatoryRadioPage.submit())
      // Then
        .isVisible(MandatoryRadioPage.error()).should.eventually.be.true
        .getText(MandatoryRadioPage.errorNumber(1)).should.eventually.contain('Enter your favourite to continue');
    });
  });

  it('Given a selected radio answer with an error for a mandatory detail answer, When I enter valid value and submit the page, Then the error is cleared and I navigate to next page.', function() {
    // Given
    return helpers.openQuestionnaire(radio_schema).then(() => {
      return browser
        .click(MandatoryRadioPage.favouriteNotListed())
        .click(MandatoryRadioPage.submit())
        .isVisible(MandatoryRadioPage.error()).should.eventually.be.true

      // When
        .setValue(MandatoryRadioPage.favouriteNotListedDetail(), 'Bacon')
        .click(MandatoryRadioPage.submit())
        .getUrl().should.eventually.contain(SummaryPage.pageName);
    });
  });


  it('Given a non-mandatory detail answer, When the user does not provide any text, Then just the option value should be displayed on the summary screen', function() {
    // Given
    return helpers.openQuestionnaire(radio_schema).then(() => {
      return browser
      // When
        .click(MandatoryRadioPage.eggs())
        .isVisible(MandatoryRadioPage.eggsDetail()).should.eventually.be.true
        .click(MandatoryRadioPage.submit())
      // Then
        .getText(SummaryPage.radioMandatoryAnswer()).should.eventually.equal('Eggs');
    });
  });

  it('Given a detail answer, When the user provides text, Then that text should be displayed on the summary screen', function() {
    // Given
    return helpers.openQuestionnaire(radio_schema).then(() => {
      return browser
      // When
        .click(MandatoryRadioPage.eggs())
        .setValue(MandatoryRadioPage.eggsDetail(), 'Scrambled')
        .click(MandatoryRadioPage.submit())
      // Then
        .getText(SummaryPage.radioMandatoryAnswer()).should.eventually.equal('Eggs\nScrambled');
    });
  });


  it('Given I have previously added text in a detail answer and saved, When I select a different radio and save, Then the text entered in the detail answer field should be empty.', function() {
    // Given
    return helpers.openQuestionnaire(radio_schema).then(() => {
      return browser
      // When
        .click(MandatoryRadioPage.favouriteNotListed())
        .setValue(MandatoryRadioPage.favouriteNotListedDetail(), 'Bacon')
        .click(MandatoryRadioPage.submit())
        .click(SummaryPage.previous())
        .click(MandatoryRadioPage.eggs())
        .click(MandatoryRadioPage.submit())
        .click(SummaryPage.previous())
      // Then
        .click(MandatoryRadioPage.favouriteNotListed())
        .getValue(MandatoryRadioPage.favouriteNotListedDetail()).should.eventually.be.equal('');
    });

  });

});
