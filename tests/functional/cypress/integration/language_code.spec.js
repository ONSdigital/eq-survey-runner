import {openQuestionnaire} from '../helpers/helpers.js'

const LanguagePage = require('../../generated_pages/language/language-block.page');
const SummaryPage = require('../../generated_pages/language/summary.page');
const ThankYouPage = require('../../base_pages/thank-you.page.js');

describe('Language Code', function() {

  it('Given the language code cy is specified I should see Welsh text', function() {
    openQuestionnaire('test_language.json', {language: 'cy'})
      .get(LanguagePage.displayedName()).stripText().should('equal', 'Holiadur Cymraeg')
      .get(LanguagePage.Month()).select('4')
      .get(LanguagePage.Year()).type(2018)
      .get(LanguagePage.submit()).click()

      .url().should('contain', SummaryPage.pageName)
      .get(SummaryPage.monthYearAnswer()).stripText().should('contain', 'Ebrill 2018')
      .get(SummaryPage.submit()).click();

      // We can only test this once we have a proper welsh translation file committed
      //.url().should('contain', 'thank-you')
      //.get(ThankYouPage.submissionSuccessfulTitle()).stripText().should('contain', "Cyflwyno'n llwyddiannus")
  });

  it('Given the language code en is specified I should see English text', function() {
    openQuestionnaire('test_language.json', {language: 'en'})
      .get(LanguagePage.displayedName()).stripText().should('equal', 'English Questionnaire')
      .get(LanguagePage.Month()).select('4')
      .get(LanguagePage.Year()).type(2018)
      .get(LanguagePage.submit()).click()

      .url().should('contain', SummaryPage.pageName)
      .get(SummaryPage.monthYearAnswer()).stripText().should('contain', 'April 2018')
      .get(SummaryPage.submit()).click()

      .url().should('contain', 'thank-you')
      .get(ThankYouPage.submissionSuccessfulTitle()).stripText().should('contain', 'Submission successful');
  });

  it('Given the language code en, When I select Cymraeg lanuage, Then the language should be switched to Welsh', function() {
    openQuestionnaire('test_language.json', {language: 'en'})
      .get(LanguagePage.displayedName()).stripText().should('equal', 'English Questionnaire')
      .get(SummaryPage.switchLanguage('cy')).click()
      .get(LanguagePage.displayedName()).stripText().should('equal', 'Holiadur Cymraeg')
      .get(SummaryPage.switchLanguage('en')).click()
      .get(LanguagePage.Month()).select('4')
      .get(LanguagePage.Year()).type(2018)
      .get(LanguagePage.submit()).click()

      .url().should('contain', SummaryPage.pageName)
      .get(SummaryPage.monthYearAnswer()).stripText().should('contain', 'April 2018')

      .get(SummaryPage.switchLanguage('cy')).click()
      .get(SummaryPage.monthYearAnswer()).stripText().should('contain', 'Ebrill 2018');
  });

  it('Given the language code cy, When I select English lanuage, Then the language should be switched to English', function() {
    openQuestionnaire('test_language.json', {language: 'cy'})
      .get(LanguagePage.displayedName()).stripText().should('equal', 'Holiadur Cymraeg')
      .get(SummaryPage.switchLanguage('en')).click()
      .get(LanguagePage.displayedName()).stripText().should('equal', 'English Questionnaire')
      .get(SummaryPage.switchLanguage('cy')).click()
      .get(LanguagePage.Month()).select('4')
      .get(LanguagePage.Year()).type(2018)
      .get(LanguagePage.submit()).click()

      .url().should('contain', SummaryPage.pageName)
      .get(SummaryPage.monthYearAnswer()).stripText().should('contain', 'Ebrill 2018')

      .get(LanguagePage.switchLanguage('en')).click()
      .get(SummaryPage.monthYearAnswer()).stripText().should('contain', 'April 2018');
  });

});
