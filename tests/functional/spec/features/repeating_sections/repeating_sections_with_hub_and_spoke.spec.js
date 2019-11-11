const PrimaryPersonPage = require('../../../generated_pages/repeating_sections_with_hub_and_spoke/primary-person-list-collector.page');
const PrimaryPersonAddPage = require('../../../generated_pages/repeating_sections_with_hub_and_spoke/primary-person-list-collector-add.page');

const FirstListCollectorPage = require('../../../generated_pages/repeating_sections_with_hub_and_spoke/list-collector.page');
const FirstListCollectorAddPage = require('../../../generated_pages/repeating_sections_with_hub_and_spoke/list-collector-add.page');

const SecondListCollectorInterstitialPage = require('../../../generated_pages/repeating_sections_with_hub_and_spoke/next-interstitial.page');
const SecondListCollectorPage = require('../../../generated_pages/repeating_sections_with_hub_and_spoke/another-list-collector-block.page');
const SecondListCollectorAddPage = require('../../../generated_pages/repeating_sections_with_hub_and_spoke/another-list-collector-block-add.page');

const VisitorsListCollectorPage = require('../../../generated_pages/repeating_sections_with_hub_and_spoke/visitors-block.page');
const VisitorsListCollectorAddPage = require('../../../generated_pages/repeating_sections_with_hub_and_spoke/visitors-block-add.page');
const VisitorsListCollectorRemovePage = require('../../../generated_pages/repeating_sections_with_hub_and_spoke/visitors-block-remove.page');
const VisitorsDateOfBirthPage = require('../../../generated_pages/repeating_sections_with_hub_and_spoke/visitors-date-of-birth.page');

const PersonalSummaryPage = require('../../../generated_pages/repeating_sections_with_hub_and_spoke/personal-summary.page');

const ProxyPage = require('../../../generated_pages/repeating_sections_with_hub_and_spoke/proxy.page');
const DateOfBirthPage = require('../../../generated_pages/repeating_sections_with_hub_and_spoke/date-of-birth.page');
const ConfirmDateOfBirthPage = require('../../../generated_pages/repeating_sections_with_hub_and_spoke/confirm-dob.page');
const SexPage = require('../../../generated_pages/repeating_sections_with_hub_and_spoke/sex.page');

const HubPage = require('../../../base_pages/hub.page.js');


describe('Feature: Repeating Sections with Hub and Spoke', function () {
  describe('Given the user has added some members to the household and is on the Hub', function () {
    before('Open survey and add household members', function () {
      browser.openQuestionnaire('test_repeating_sections_with_hub_and_spoke.json');
      // Ensure we are on the Hub
      expect(browser.getUrl()).to.contain(HubPage.url());
      // Ensure the first section is not started
      expect($(HubPage.summaryRowState(1)).getText()).to.equal('Not started');
      // Start first section to add household members
      $(HubPage.summaryRowLink(1)).click();

      // Add a primary person
      $(PrimaryPersonPage.yes()).click();
      $(PrimaryPersonPage.submit()).click();
      $(PrimaryPersonAddPage.firstName()).setValue('Marcus');
      $(PrimaryPersonAddPage.lastName()).setValue('Twin');
      $(PrimaryPersonPage.submit()).click();

      // Add other household members (First list collector)
      $(FirstListCollectorPage.yes()).click();
      $(FirstListCollectorPage.submit()).click();
      $(FirstListCollectorAddPage.firstName()).setValue('Jean');
      $(FirstListCollectorAddPage.lastName()).setValue('Clemens');
      $(FirstListCollectorAddPage.submit()).click();

      $(FirstListCollectorPage.yes()).click();
      $(FirstListCollectorPage.submit()).click();
      $(FirstListCollectorAddPage.firstName()).setValue('Samuel');
      $(FirstListCollectorAddPage.lastName()).setValue('Clemens');
      $(FirstListCollectorAddPage.submit()).click();

      // Go to second list collector
      $(FirstListCollectorPage.no()).click();
      $(FirstListCollectorPage.submit()).click();
      $(SecondListCollectorInterstitialPage.submit()).click();

      // Add other household members (Second list collector)
      $(SecondListCollectorPage.yes()).click();
      $(SecondListCollectorPage.submit()).click();
      $(SecondListCollectorAddPage.firstName()).setValue('John');
      $(SecondListCollectorAddPage.lastName()).setValue('Doe');
      $(SecondListCollectorAddPage.submit()).click();

      // Go back to the Hub
      $(SecondListCollectorPage.no()).click();
      $(SecondListCollectorPage.submit()).click();
      $(VisitorsListCollectorPage.no()).click();
      $(VisitorsListCollectorPage.submit()).click();
    });

    beforeEach('Navigate to the Hub', function () {
      return browser.url(HubPage.url());
    });

    it('Then a section for each household member should be displayed', function () {
      expect(browser.getUrl()).to.contain(HubPage.url());

      expect($(HubPage.summaryRowState(1)).getText()).to.equal('Completed');
      expect($(HubPage.summaryRowState(2)).getText()).to.equal('Not started');
      expect($(HubPage.summaryRowTitle(2)).getText()).to.equal('Marcus Twin');
      expect($(HubPage.summaryRowState(3)).getText()).to.equal('Not started');
      expect($(HubPage.summaryRowTitle(3)).getText()).to.equal('Jean Clemens');
      expect($(HubPage.summaryRowState(4)).getText()).to.equal('Not started');
      expect($(HubPage.summaryRowTitle(4)).getText()).to.equal('Samuel Clemens');
      expect($(HubPage.summaryRowState(5)).getText()).to.equal('Not started');
      expect($(HubPage.summaryRowTitle(5)).getText()).to.equal('John Doe');

      expect($(HubPage.summaryRowState(6)).isExisting()).to.be.false;
    });

    it('When the user starts a repeating section and clicks the Previous link on the first question, Then they should be taken back to the Hub', function () {
      $(HubPage.summaryRowLink(3)).click();
      $(ProxyPage.previous()).click();

      expect(browser.getUrl()).to.contain(HubPage.url());
    });

    it('When the user partially completes a repeating section, Then that section should be marked as \'Partially completed\' on the Hub', function () {
      $(HubPage.summaryRowLink(2)).click();
      $(ProxyPage.yes()).click();
      $(ProxyPage.submit()).click();

      $(DateOfBirthPage.day()).setValue('01');
      $(DateOfBirthPage.month()).setValue('03');
      $(DateOfBirthPage.year()).setValue('2000');
      $(DateOfBirthPage.submit()).click();

      $(ConfirmDateOfBirthPage.confirmDateOfBirthYes()).click();
      $(ConfirmDateOfBirthPage.submit()).click();

      browser.url(HubPage.url());

      expect(browser.getUrl()).to.contain(HubPage.url());
      expect($(HubPage.summaryRowState(2)).getText()).to.equal('Partially completed');

      expect($(HubPage.summaryRowTitle(2)).getAttribute('class')).to.not.contain('summary__item-title--has-icon');

    });

    it('When the user continues with a partially completed repeating section, Then they are taken to the last complete block', function () {
      $(HubPage.summaryRowLink(2)).click();

      expect($(ConfirmDateOfBirthPage.questionText()).getText()).to.equal('Marcus Twin is 19 years old. Is this correct?');
      expect($(ConfirmDateOfBirthPage.confirmDateOfBirthYes()).isSelected()).to.be.true;
    });

    it('When the user completes a repeating section, Then that section should be marked as \'Completed\' on the Hub', function () {
      $(HubPage.summaryRowLink(3)).click();
      $(ProxyPage.yes()).click();
      $(ProxyPage.submit()).click();

      $(DateOfBirthPage.day()).setValue('09');
      $(DateOfBirthPage.month()).setValue('09');
      $(DateOfBirthPage.year()).setValue('1995');
      $(DateOfBirthPage.submit()).click();

      $(ConfirmDateOfBirthPage.confirmDateOfBirthYes()).click();
      $(ConfirmDateOfBirthPage.submit()).click();

      $(SexPage.female()).click();
      $(SexPage.submit()).click();

      $(PersonalSummaryPage.submit()).click();

      expect(browser.getUrl()).to.contain(HubPage.url());
      expect($(HubPage.summaryRowState(3)).getText()).to.equal('Completed');

      expect($(HubPage.summaryRowTitle(3)).getAttribute('class')).to.contain('summary__item-title--has-icon');
    });

    it('When the user clicks \'View answers\' for a completed repeating section, Then they are taken to the summary', function () {
      $(HubPage.summaryRowLink(3)).click();
      expect(browser.getUrl()).to.contain(PersonalSummaryPage.url().split('/').slice(-1)[0]);
    });

    it('When the user adds 2 visitors to the household then a section for each visitor should be display on the hub', function () {
      // Ensure no other sections exist
      expect($(HubPage.summaryRowState(6)).isExisting()).to.be.false;

      // Start section for first visitor
      $(HubPage.summaryRowLink(1)).click();
      $(PrimaryPersonPage.submit()).click();
      $(PrimaryPersonAddPage.submit()).click();
      $(FirstListCollectorPage.submit()).click();
      $(SecondListCollectorInterstitialPage.submit()).click();
      $(SecondListCollectorPage.submit()).click();
      expect($(SexPage.questionText()).getText()).to.equal('This is the visitors list collector. Add a visitor?');

      // Add first visitor
      $(VisitorsListCollectorPage.yes()).click();
      $(VisitorsListCollectorPage.submit()).click();
      $(VisitorsListCollectorAddPage.firstName()).setValue('Joe');
      $(VisitorsListCollectorAddPage.lastName()).setValue('Public');
      $(VisitorsListCollectorAddPage.submit()).click();

      // Add second visitor
      $(VisitorsListCollectorPage.yes()).click();
      $(VisitorsListCollectorPage.submit()).click();
      $(VisitorsListCollectorAddPage.firstName()).setValue('Yvonne');
      $(VisitorsListCollectorAddPage.lastName()).setValue('Yoe');
      $(VisitorsListCollectorAddPage.submit()).click();
      $(VisitorsListCollectorPage.no()).click();
      $(VisitorsListCollectorPage.submit()).click();

      expect($(HubPage.summaryRowState(6)).getText()).to.equal('Not started');
      expect($(HubPage.summaryRowTitle(6)).getText()).to.equal('Joe Public');
      expect($(HubPage.summaryRowState(7)).getText()).to.equal('Not started');
      expect($(HubPage.summaryRowTitle(7)).getText()).to.equal('Yvonne Yoe');

      expect($(HubPage.summaryRowState(8)).isExisting()).to.be.false;
    });

    it('When the user clicks \'Continue\' from the Hub, Then they should progress to the first incomplete section', function () {
      $(HubPage.submit()).click();
      expect($(ConfirmDateOfBirthPage.questionText()).getText()).to.equal('What is Marcus Twin’s sex?');
    });

    it('When the user answers on their behalf, Then they are shown the non proxy question variant', function () {
      $(HubPage.summaryRowLink(5)).click();
      $(ProxyPage.no()).click();
      $(ProxyPage.submit()).click();

      expect($(DateOfBirthPage.questionText()).getText()).to.equal('What is your date of birth?');

      $(DateOfBirthPage.day()).setValue('07');
      $(DateOfBirthPage.month()).setValue('07');
      $(DateOfBirthPage.year()).setValue('1970');
      $(DateOfBirthPage.submit()).click();

      expect($(ConfirmDateOfBirthPage.questionText()).getText()).to.equal('You are 49 years old. Is this correct?');

      $(ConfirmDateOfBirthPage.confirmDateOfBirthYes()).click();
      $(ConfirmDateOfBirthPage.submit()).click();

      expect($(SexPage.questionText()).getText()).to.equal('What is your sex?');
    });

    it('When the user answers on on behalf of someone else, Then they are shown the proxy question variant for the relevant repeating section', function () {
      $(HubPage.summaryRowLink(4)).click();
      $(ProxyPage.yes()).click();
      $(ProxyPage.submit()).click();

      expect($(DateOfBirthPage.questionText()).getText()).to.equal('What is Samuel Clemens’ date of birth?');

      $(DateOfBirthPage.day()).setValue('11');
      $(DateOfBirthPage.month()).setValue('11');
      $(DateOfBirthPage.year()).setValue('1990');
      $(DateOfBirthPage.submit()).click();

      $(ConfirmDateOfBirthPage.confirmDateOfBirthYes()).click();
      $(ConfirmDateOfBirthPage.submit()).click();

      expect($(SexPage.questionText()).getText()).to.equal('What is Samuel Clemens’ sex?');
    });


    it('When the user completes all sections, Then the Hub should be in the completed state', function () {
      // Complete remaining sections
      $(HubPage.submit()).click();
      $(SexPage.male()).click();
      $(SexPage.submit()).click();
      $(PersonalSummaryPage.submit()).click();

      $(HubPage.submit()).click();
      $(SexPage.submit()).click();
      $(PersonalSummaryPage.submit()).click();

      $(HubPage.submit()).click();
      $(SexPage.female()).click();
      $(SexPage.submit()).click();
      $(PersonalSummaryPage.submit()).click();

      $(HubPage.submit()).click();
      $(VisitorsDateOfBirthPage.day()).setValue('03');
      $(VisitorsDateOfBirthPage.month()).setValue('09');
      $(VisitorsDateOfBirthPage.year()).setValue('1975');
      $(VisitorsDateOfBirthPage.submit()).click();

      $(HubPage.submit()).click();
      $(VisitorsDateOfBirthPage.day()).setValue('31');
      $(VisitorsDateOfBirthPage.month()).setValue('07');
      $(VisitorsDateOfBirthPage.year()).setValue('1999');
      $(VisitorsDateOfBirthPage.submit()).click();

      expect($(HubPage.submit()).getText()).to.equal('Submit survey');
      expect($(HubPage.displayedName()).getText()).to.equal('Submit survey');
    });

    it('When the user adds a new member to the household, Then the Hub should not be in the completed state', function () {
      $(HubPage.summaryRowLink(1)).click();
      $(PrimaryPersonPage.submit()).click();
      $(PrimaryPersonAddPage.submit()).click();
      $(FirstListCollectorPage.submit()).click();
      $(SecondListCollectorInterstitialPage.submit()).click();
      $(SecondListCollectorPage.submit()).click();

      // Add another householder
      $(VisitorsListCollectorPage.yes()).click();
      $(VisitorsListCollectorPage.submit()).click();

      $(VisitorsListCollectorAddPage.firstName()).setValue('Anna');
      $(VisitorsListCollectorAddPage.lastName()).setValue('Doe');

      $(SecondListCollectorAddPage.submit()).click();
      $(VisitorsListCollectorPage.no()).click();
      $(VisitorsListCollectorPage.submit()).click();

      // New householder added to hub
      expect($(HubPage.summaryRowState(8)).getText()).to.equal('Not started');
      expect($(HubPage.summaryRowState(8)).isExisting()).to.be.true;

      expect($(HubPage.submit()).getText()).to.not.equal('Submit survey');
      expect($(HubPage.submit()).getText()).to.equal('Continue');

      expect($(HubPage.displayedName()).getText()).to.not.equal('Submit survey');
      expect($(HubPage.displayedName()).getText()).to.equal('Choose another section to complete');
    });

    it('When the user removes a member from the household, Then their section is not longer displayed on he Hub', function () {
      // Ensure final householder exists
      expect($(HubPage.summaryRowState(8)).isExisting()).to.be.true;

      $(HubPage.summaryRowLink(1)).click();
      $(PrimaryPersonPage.submit()).click();
      $(PrimaryPersonAddPage.submit()).click();
      $(FirstListCollectorPage.submit()).click();
      $(SecondListCollectorInterstitialPage.submit()).click();
      $(SecondListCollectorPage.submit()).click();

      // Remove final householder
      $(VisitorsListCollectorPage.listRemoveLink(3)).click();
      $(VisitorsListCollectorRemovePage.yes()).click();
      $(VisitorsListCollectorPage.submit()).click();

      // Ensure final householder no longer exists
      expect($(HubPage.summaryRowState(8)).isExisting()).to.be.false;
    });

    it('When the user submits, it should show the thank you page', function () {
      $(HubPage.submit()).click();
      expect(browser.getUrl()).to.contain('thank-you');
    });
  });
});
