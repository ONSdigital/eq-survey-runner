const helpers = require('../helpers');

const NamePage = require('../generated_pages/language/name-block.page');
const DobPage = require('../generated_pages/language/dob-block.page');
const SummaryPage = require('../generated_pages/language/summary.page');
const ThankYouPage = require('../base_pages/thank-you.page.js');

describe('Language Code', function() {
  let browser;

  it('Given a launch language of Welsh, I should see Welsh text', function() {

    browser = helpers.openQuestionnaire('test_language.json', { language: 'cy' }).then(openBrowser => browser = openBrowser);

    expect($(NamePage.questionText()).getText()).to.contain('Rhowch enw');

    $(NamePage.firstName()).setValue('Catherine');
    $(NamePage.lastName()).setValue('Zeta-Jones');
    $(NamePage.submit()).click();

    $(DobPage.day()).setValue(25);
    $(DobPage.month()).setValue(9);
    $(DobPage.year()).setValue(1969);
    $(DobPage.submit()).click();

    expect(browser.getUrl()).to.contain(SummaryPage.pageName);
    expect($(SummaryPage.dobQuestion()).getText()).to.contain('Beth yw dyddiad geni Catherine Zeta-Jones?');
    expect($(SummaryPage.dateOfBirthAnswer()).getText()).to.contain('25 Medi 1969');
    $(SummaryPage.submit()).click();

    expect(browser.getUrl()).to.contain('thank-you');
    expect($(ThankYouPage.submissionSuccessfulTitle()).getText()).to.contain("Diolch am gyflwyno eich cyfrifiad");
  });

  it('Given a launch language of English, I should see English text', function() {

    browser = helpers.openQuestionnaire('test_language.json', { language: 'en' }).then(openBrowser => browser = openBrowser);

    expect($(NamePage.questionText()).getText()).to.contain('Please enter a name');
    $(NamePage.firstName()).setValue('Catherine');
    $(NamePage.lastName()).setValue('Zeta-Jones');
    $(NamePage.submit()).click();

    $(DobPage.day()).setValue(25);
    $(DobPage.month()).setValue(9);
    $(DobPage.year()).setValue(1969);
    $(DobPage.submit()).click();

    expect(browser.getUrl()).to.contain(SummaryPage.pageName);
    expect($(SummaryPage.dobQuestion()).getText()).to.contain('What is Catherine Zeta-Jones’ date of birth?');
    expect($(SummaryPage.dateOfBirthAnswer()).getText()).to.contain('25 September 1969');
    $(SummaryPage.submit()).click();

    expect(browser.getUrl()).to.contain('thank-you');
    expect($(ThankYouPage.submissionSuccessfulTitle()).getText()).to.contain("Thank you for submitting your census");
  });

  it('Given a launch language of English, When I select Cymraeg, Then the language should be switched to Welsh', function() {

    browser = helpers.openQuestionnaire('test_language.json', { language: 'en' }).then(openBrowser => browser = openBrowser);

    expect($(NamePage.questionText()).getText()).to.contain('Please enter a name');
    $(NamePage.switchLanguage('cy')).click();
    expect($(NamePage.questionText()).getText()).to.contain('Rhowch enw');
    $(NamePage.switchLanguage('en')).click();

    $(NamePage.firstName()).setValue('Catherine');
    $(NamePage.lastName()).setValue('Zeta-Jones');
    $(NamePage.submit()).click();

    $(DobPage.day()).setValue(25);
    $(DobPage.month()).setValue(9);
    $(DobPage.year()).setValue(1969);
    $(DobPage.submit()).click();

    expect(browser.getUrl()).to.contain(SummaryPage.pageName);
    expect($(SummaryPage.dateOfBirthAnswer()).getText()).to.contain('25 September 1969');
    $(SummaryPage.switchLanguage('cy')).click();
    expect($(SummaryPage.dateOfBirthAnswer()).getText()).to.contain('25 Medi 1969');
    $(SummaryPage.submit()).click();

    expect(browser.getUrl()).to.contain('thank-you');
    expect($(ThankYouPage.submissionSuccessfulTitle()).getText()).to.contain("Diolch am gyflwyno eich cyfrifiad");
    $(ThankYouPage.switchLanguage('en')).click();
    expect($(ThankYouPage.submissionSuccessfulTitle()).getText()).to.contain("Thank you for submitting your census");
  });

  it('Given a launch language of Welsh, When I select English, Then the language should be switched to English', function() {
    browser = helpers.openQuestionnaire('test_language.json', { language: 'cy' }).then(openBrowser => browser = openBrowser);

    expect($(NamePage.questionText()).getText()).to.contain('Rhowch enw');
    $(NamePage.switchLanguage('en')).click();
    expect($(NamePage.questionText()).getText()).to.contain('Please enter a name');
  });

});
