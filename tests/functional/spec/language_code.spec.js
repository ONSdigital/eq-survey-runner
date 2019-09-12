const helpers = require('../helpers');

const NamePage = require('../generated_pages/language/name-block.page');
const DobPage = require('../generated_pages/language/dob-block.page');
const SummaryPage = require('../generated_pages/language/summary.page');
const ThankYouPage = require('../base_pages/thank-you.page.js');

describe('Language Code', function() {

  it('Given a launch language of Welsh, I should see Welsh text', function() {

    return helpers.openQuestionnaire('test_language.json', { language: 'cy' }).then(() => {

      return browser
        .getText(NamePage.questionText()).should.eventually.contain('Rhowch enw')
        .setValue(NamePage.firstName(), 'Catherine')
        .setValue(NamePage.lastName(), 'Zeta-Jones')
        .click(NamePage.submit())

        .setValue(DobPage.day(), 25)
        .setValue(DobPage.month(), 9)
        .setValue(DobPage.year(), 1969)
        .click(DobPage.submit())

        .getUrl().should.eventually.contain(SummaryPage.pageName)
        .getText(SummaryPage.dobQuestion()).should.eventually.contain('Beth yw dyddiad geni Catherine Zeta-Jones?')
        .getText(SummaryPage.dateOfBirthAnswer()).should.eventually.contain('25 Medi 1969')
        .click(SummaryPage.submit())

        .getUrl().should.eventually.contain('thank-you')
        .getText(ThankYouPage.submissionSuccessfulTitle()).should.eventually.contain("Diolch am gyflwyno eich cyfrifiad");
      });
  });

  it('Given a launch language of English, I should see English text', function() {

    return helpers.openQuestionnaire('test_language.json', { language: 'en' }).then(() => {

      return browser
        .getText(NamePage.questionText()).should.eventually.contain('Please enter a name')
        .setValue(NamePage.firstName(), 'Catherine')
        .setValue(NamePage.lastName(), 'Zeta-Jones')
        .click(NamePage.submit())

        .setValue(DobPage.day(), 25)
        .setValue(DobPage.month(), 9)
        .setValue(DobPage.year(), 1969)
        .click(DobPage.submit())

        .getUrl().should.eventually.contain(SummaryPage.pageName)
        .getText(SummaryPage.dobQuestion()).should.eventually.contain('What is Catherine Zeta-Jones’ date of birth?')
        .getText(SummaryPage.dateOfBirthAnswer()).should.eventually.contain('25 September 1969')
        .click(SummaryPage.submit())

        .getUrl().should.eventually.contain('thank-you')
        .getText(ThankYouPage.submissionSuccessfulTitle()).should.eventually.contain("Thank you for submitting your census");
      });
  });

  it('Given a launch language of English, When I select Cymraeg, Then the language should be switched to Welsh', function() {

    return helpers.openQuestionnaire('test_language.json', { language: 'en' }).then(() => {

      return browser
        .getText(NamePage.questionText()).should.eventually.contain('Please enter a name')
        .click(NamePage.switchLanguage('cy'))
        .getText(NamePage.questionText()).should.eventually.contain('Rhowch enw')
        .click(NamePage.switchLanguage('en'))

        .setValue(NamePage.firstName(), 'Catherine')
        .setValue(NamePage.lastName(), 'Zeta-Jones')
        .click(NamePage.submit())

        .setValue(DobPage.day(), 25)
        .setValue(DobPage.month(), 9)
        .setValue(DobPage.year(), 1969)
        .click(DobPage.submit())

        .getUrl().should.eventually.contain(SummaryPage.pageName)
        .getText(SummaryPage.dateOfBirthAnswer()).should.eventually.contain('25 September 1969')
        .click(SummaryPage.switchLanguage('cy'))
        .getText(SummaryPage.dateOfBirthAnswer()).should.eventually.contain('25 Medi 1969')
        .click(SummaryPage.submit())

        .getUrl().should.eventually.contain('thank-you')
        .getText(ThankYouPage.submissionSuccessfulTitle()).should.eventually.contain("Diolch am gyflwyno eich cyfrifiad")
        .click(ThankYouPage.switchLanguage('en'))
        .getText(ThankYouPage.submissionSuccessfulTitle()).should.eventually.contain("Thank you for submitting your census");
      });
  });

  it('Given a launch language of Welsh, When I select English, Then the language should be switched to English', function() {

    return helpers.openQuestionnaire('test_language.json', { language: 'cy' }).then(() => {

      return browser
        .getText(NamePage.questionText()).should.eventually.contain('Rhowch enw')
        .click(NamePage.switchLanguage('en'))
        .getText(NamePage.questionText()).should.eventually.contain('Please enter a name');
      });
  });

});
