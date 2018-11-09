const helpers = require('../helpers');

const LanguagePage = require('../generated_pages/language/language-block.page');
const SummaryPage = require('../generated_pages/language/summary.page');
const ThankYouPage = require('../base_pages/thank-you.page.js');

describe('Language Code', function() {

  it('Given the language code cy is specified I should see Welsh text', function() {

    return helpers.openQuestionnaire('test_language.json', helpers.getRandomString(10), helpers.getRandomString(10), '201605', 'May 2016', 'GB-ENG', 'cy').then(() => {

      return browser
        .getText(LanguagePage.displayedName()).should.eventually.equal('Holiadur Cymraeg')
        .selectByValue(LanguagePage.Month(), 4)
        .setValue(LanguagePage.Year(), 2018)
        .click(LanguagePage.submit())

        .getUrl().should.eventually.contain(SummaryPage.pageName)
        .getText(SummaryPage.monthYearAnswer()).should.eventually.contain('Ebrill 2018')
        .click(SummaryPage.submit());

        // We can only test this once we have a proper welsh translation file committed
        //.getUrl().should.eventually.contain('thank-you')
        //.getText(ThankYouPage.submissionSuccessfulTitle()).should.eventually.contain("Cyflwyno'n llwyddiannus")
    });
  });

  it('Given the language code en is specified I should see English text', function() {

    return helpers.openQuestionnaire('test_language.json', helpers.getRandomString(10), helpers.getRandomString(10), '201605', 'May 2016', 'GB-ENG', 'en').then(() => {

      return browser
        .getText(LanguagePage.displayedName()).should.eventually.equal('English Questionnaire')
        .selectByValue(LanguagePage.Month(), 4)
        .setValue(LanguagePage.Year(), 2018)
        .click(LanguagePage.submit())

        .getUrl().should.eventually.contain(SummaryPage.pageName)
        .getText(SummaryPage.monthYearAnswer()).should.eventually.contain('April 2018')
        .click(SummaryPage.submit())

        .getUrl().should.eventually.contain('thank-you')
        .getText(ThankYouPage.submissionSuccessfulTitle()).should.eventually.contain('Submission successful');
    });
  });

  it('Given the language code en, When I select Cymraeg lanuage, Then the language should be switched to Welsh', function() {

    return helpers.openQuestionnaire('test_language.json', helpers.getRandomString(10), helpers.getRandomString(10), '201605', 'May 2016', 'GB-ENG', 'en').then(() => {

      return browser
        .getText(LanguagePage.displayedName()).should.eventually.equal('English Questionnaire')
        .click(SummaryPage.switchLanguage('cy'))
        .getText(LanguagePage.displayedName()).should.eventually.equal('Holiadur Cymraeg')
        .click(SummaryPage.switchLanguage('en'))
        .selectByValue(LanguagePage.Month(), 4)
        .setValue(LanguagePage.Year(), 2018)
        .click(LanguagePage.submit())

        .getUrl().should.eventually.contain(SummaryPage.pageName)
        .getText(SummaryPage.monthYearAnswer()).should.eventually.contain('April 2018')

        .click(SummaryPage.switchLanguage('cy'))
        .getText(SummaryPage.monthYearAnswer()).should.eventually.contain('Ebrill 2018');
    });
  });

  it('Given the language code cy, When I select English lanuage, Then the language should be switched to English', function() {

    return helpers.openQuestionnaire('test_language.json', helpers.getRandomString(10), helpers.getRandomString(10), '201605', 'May 2016', 'GB-ENG', 'cy').then(() => {

      return browser
        .getText(LanguagePage.displayedName()).should.eventually.equal('Holiadur Cymraeg')
        .click(SummaryPage.switchLanguage('en'))
        .getText(LanguagePage.displayedName()).should.eventually.equal('English Questionnaire')
        .click(SummaryPage.switchLanguage('cy'))
        .selectByValue(LanguagePage.Month(), 4)
        .setValue(LanguagePage.Year(), 2018)
        .click(LanguagePage.submit())

        .getUrl().should.eventually.contain(SummaryPage.pageName)
        .getText(SummaryPage.monthYearAnswer()).should.eventually.contain('Ebrill 2018')

        .click(LanguagePage.switchLanguage('en'))
        .getText(SummaryPage.monthYearAnswer()).should.eventually.contain('April 2018');
    });
  });

});
