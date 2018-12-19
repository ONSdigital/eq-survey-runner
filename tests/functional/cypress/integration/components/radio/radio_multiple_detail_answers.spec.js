import {openQuestionnaire} from ../../../helpers/helpers.js

const MandatoryRadioPage = require('../../../../generated_pages/radio_multiple_detail_answers/radio-mandatory.page');
const SummaryPage = require('../../../../generated_pages/radio_multiple_detail_answers/summary.page');

describe('Radio with multiple "detail_answer" options', function() {

  const radio_schema = 'test_radio_multiple_detail_answers.json';

  it('Given detail answer options are available, When the user clicks an option, Then the detail answer input should be visible.', function() {
    openQuestionnaire(radio_schema)
              .get().click()
        .get(MandatoryRadioPage.eggsDetail()).should('be.visible')
        .get().click()
        .get(MandatoryRadioPage.favouriteNotListedDetail()).should('be.visible');
    });
  });

  it('Given a mandatory detail answer, When I select the option but leave the input field empty and submit, Then an error should be displayed.', function() {
    // Given
    openQuestionnaire(radio_schema)
            // When
        .get().click()
        .get().click()
      // Then
        .get(MandatoryRadioPage.error()).should('be.visible')
        .get(MandatoryRadioPage.errorNumber(1)).stripText().should('contain', 'Enter your favourite to continue');
    });
  });

  it('Given a selected checkbox answer with an error for a mandatory detail answer, When I enter valid value and submit the page, Then the error is cleared and I navigate to next page.', function() {
    // Given
    openQuestionnaire(radio_schema)
              .get().click()
        .get().click()
        .get(MandatoryRadioPage.error()).should('be.visible')

      // When
        .get(MandatoryRadioPage.favouriteNotListedDetail()).type('Bacon')
        .get().click()
        .url().should('contain', SummaryPage.pageName);
    });
  });


  it('Given a non-mandatory detail answer, When the user does not provide any text, Then just the option value should be displayed on the summary screen', function() {
    // Given
    openQuestionnaire(radio_schema)
            // When
        .get().click()
        .get(MandatoryRadioPage.eggsDetail()).should('be.visible')
        .get().click()
      // Then
        .get(SummaryPage.radioMandatoryAnswer()).stripText().should('equal', 'Eggs');
    });
  });

  it('Given a detail answer, When the user provides text, Then that text should be displayed on the summary screen', function() {
    // Given
    openQuestionnaire(radio_schema)
            // When
        .get().click()
        .get(MandatoryRadioPage.eggsDetail()).type('Scrambled')
        .get().click()
      // Then
        .get(SummaryPage.radioMandatoryAnswer()).stripText().should('equal', 'Eggs\nScrambled');
    });
  });


  it('Given I have previously added text in a detail answer and saved, When I select a different radio and save, Then the text entered in the detail answer field should be empty.', function() {
    // Given
    openQuestionnaire(radio_schema)
            // When
        .get().click()
        .get(MandatoryRadioPage.favouriteNotListedDetail()).type('Bacon')
        .get().click()
        .get().click()
        .get().click()
        .get().click()
        .get(SummaryPage.previous()).click()
      // Then
        .get(MandatoryRadioPage.favouriteNotListed()).click()
        .getValue(MandatoryRadioPage.favouriteNotListedDetail()).should.eventually.be.equal('');
    });

  });

});
