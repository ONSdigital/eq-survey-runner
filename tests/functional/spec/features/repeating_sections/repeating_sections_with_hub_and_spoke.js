const helpers = require('../../../helpers');

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

  const Hub_and_spoke_schema = 'test_repeating_sections_with_hub_and_spoke.json';

  describe('Given the user has added some members to the household and is on the Hub', function () {

    before('Open survey and add household members', function () {
      return helpers.openQuestionnaire(Hub_and_spoke_schema)
        .then(() => {
          return browser
            // Ensure we are on the Hub
            .getUrl().should.eventually.contain(HubPage.url())
            // Ensure the first section is not started
            .getText(HubPage.summaryRowState(1)).should.eventually.equal('Not started')
            // Start first section to add household members
            .click(HubPage.summaryRowLink(1))

            // Add a primary person
            .click(PrimaryPersonPage.yes())
            .click(PrimaryPersonPage.submit())
            .setValue(PrimaryPersonAddPage.firstName(), 'Marcus')
            .setValue(PrimaryPersonAddPage.lastName(), 'Twin')
            .click(PrimaryPersonPage.submit())

            // Add other household members (First list collector)

            .click(FirstListCollectorPage.yes())
            .click(FirstListCollectorPage.submit())
            .setValue(FirstListCollectorAddPage.firstName(), 'Jean')
            .setValue(FirstListCollectorAddPage.lastName(), 'Clemens')
            .click(FirstListCollectorAddPage.submit())

            .click(FirstListCollectorPage.yes())
            .click(FirstListCollectorPage.submit())
            .setValue(FirstListCollectorAddPage.firstName(), 'Samuel')
            .setValue(FirstListCollectorAddPage.lastName(), 'Clemens')
            .click(FirstListCollectorAddPage.submit())

            // Go to second list collector

            .click(FirstListCollectorPage.no())
            .click(FirstListCollectorPage.submit())
            .click(SecondListCollectorInterstitialPage.submit())

            // Add other household members (Second list collector)

            .click(SecondListCollectorPage.yes())
            .click(SecondListCollectorPage.submit())
            .setValue(SecondListCollectorAddPage.firstName(), 'John')
            .setValue(SecondListCollectorAddPage.lastName(), 'Doe')
            .click(SecondListCollectorAddPage.submit())

            // Go back to the Hub

            .click(SecondListCollectorPage.no())
            .click(SecondListCollectorPage.submit())
            .click(VisitorsListCollectorPage.no())
            .click(VisitorsListCollectorPage.submit());
        });
    });

    beforeEach('Navigate to the Hub', function () {
      return browser.url(HubPage.url());
    });

    it('Then a section for each household member should be displayed', function () {
      return browser
        .getUrl().should.eventually.contain(HubPage.url())

        .getText(HubPage.summaryRowState(1)).should.eventually.equal('Completed')
        .getText(HubPage.summaryRowState(2)).should.eventually.equal('Not started')
        .getText(HubPage.summaryRowTitle(2)).should.eventually.equal('Marcus Twin')
        .getText(HubPage.summaryRowState(3)).should.eventually.equal('Not started')
        .getText(HubPage.summaryRowTitle(3)).should.eventually.equal('Jean Clemens')
        .getText(HubPage.summaryRowState(4)).should.eventually.equal('Not started')
        .getText(HubPage.summaryRowTitle(4)).should.eventually.equal('Samuel Clemens')
        .getText(HubPage.summaryRowState(5)).should.eventually.equal('Not started')
        .getText(HubPage.summaryRowTitle(5)).should.eventually.equal('John Doe')

        .isExisting(HubPage.summaryRowState(6)).should.eventually.be.false;
    });

    it('When the user starts a repeating section and clicks the Previous link on the first question, Then they should be taken back to the Hub', function () {
      return browser
        .click(HubPage.summaryRowLink(3))
        .click(ProxyPage.previous())

        .getUrl().should.eventually.contain(HubPage.url());
    });

    it('When the user partially completes a repeating section, Then that section should be marked as \'Partially completed\' on the Hub', function () {
      return browser
        .click(HubPage.summaryRowLink(2))
        .click(ProxyPage.yes())
        .click(ProxyPage.submit())

        .setValue(DateOfBirthPage.day(), '01')
        .setValue(DateOfBirthPage.month(), '03')
        .setValue(DateOfBirthPage.year(), '2000')
        .click(DateOfBirthPage.submit())

        .click(ConfirmDateOfBirthPage.confirmDateOfBirthYes())
        .click(ConfirmDateOfBirthPage.submit())

        .url(HubPage.url())

        .getUrl().should.eventually.contain(HubPage.url())
        .getText(HubPage.summaryRowState(2)).should.eventually.equal('Partially completed')
        .getAttribute(HubPage.summaryRowTitle(2), 'class').should.not.eventually.contain('summary__item-title--has-icon');
    });

    it('When the user continues with a partially completed repeating section, Then they are taken to the last complete block', function () {
      return browser
        .click(HubPage.summaryRowLink(2))

        .getText(ConfirmDateOfBirthPage.questionText()).should.eventually.equal('Marcus Twin is 19 years old. Is this correct?')
        .isSelected(ConfirmDateOfBirthPage.confirmDateOfBirthYes()).should.eventually.be.true;
    });

    it('When the user completes a repeating section, Then that section should be marked as \'Completed\' on the Hub', function () {
      return browser
        .click(HubPage.summaryRowLink(3))
        .click(ProxyPage.yes())
        .click(ProxyPage.submit())

        .setValue(DateOfBirthPage.day(), '09')
        .setValue(DateOfBirthPage.month(), '09')
        .setValue(DateOfBirthPage.year(), '1995')
        .click(DateOfBirthPage.submit())

        .click(ConfirmDateOfBirthPage.confirmDateOfBirthYes())
        .click(ConfirmDateOfBirthPage.submit())

        .click(SexPage.female())
        .click(SexPage.submit())

        .click(PersonalSummaryPage.submit())

        .getUrl().should.eventually.contain(HubPage.url())
        .getText(HubPage.summaryRowState(3)).should.eventually.equal('Completed')
        .getAttribute(HubPage.summaryRowTitle(3), 'class').should.eventually.contain('summary__item-title--has-icon');
    });

    it('When the user clicks \'View answers\' for a completed repeating section, Then they are taken to the summary', function () {
      return browser
        .click(HubPage.summaryRowLink(3))
        .getUrl().should.eventually.contain(PersonalSummaryPage.url().split('/').slice(-1)[0]);
    });

    it('When the user adds 2 visitors to the household then a section for each visitor should be display on the hub', function () {
      return browser
        // Ensure no other sections exist
        .isExisting(HubPage.summaryRowState(6)).should.eventually.be.false

        // Start section for first visitor
        .click(HubPage.summaryRowLink(1))
        .click(PrimaryPersonPage.submit())
        .click(PrimaryPersonAddPage.submit())
        .click(FirstListCollectorPage.submit())
        .click(SecondListCollectorInterstitialPage.submit())
        .click(SecondListCollectorPage.submit())
        .getText(SexPage.questionText()).should.eventually.equal('This is the visitors list collector. Add a visitor?')

        // Add first visitor
        .click(VisitorsListCollectorPage.yes())
        .click(VisitorsListCollectorPage.submit())
        .setValue(VisitorsListCollectorAddPage.firstName(), 'Joe')
        .setValue(VisitorsListCollectorAddPage.lastName(), 'Public')
        .click(VisitorsListCollectorAddPage.submit())

        // Add second visitor
        .click(VisitorsListCollectorPage.yes())
        .click(VisitorsListCollectorPage.submit())
        .setValue(VisitorsListCollectorAddPage.firstName(), 'Yvonne')
        .setValue(VisitorsListCollectorAddPage.lastName(), 'Yoe')
        .click(VisitorsListCollectorAddPage.submit())
        .click(VisitorsListCollectorPage.no())
        .click(VisitorsListCollectorPage.submit())

        .getText(HubPage.summaryRowState(6)).should.eventually.equal('Not started')
        .getText(HubPage.summaryRowTitle(6)).should.eventually.equal('Joe Public')
        .getText(HubPage.summaryRowState(7)).should.eventually.equal('Not started')
        .getText(HubPage.summaryRowTitle(7)).should.eventually.equal('Yvonne Yoe')

        .isExisting(HubPage.summaryRowState(8)).should.eventually.be.false;
    });

    it('When the user clicks \'Continue\' from the Hub, Then they should progress to the first incomplete section', function () {
      return browser
        .click(HubPage.submit())
        .getText(ConfirmDateOfBirthPage.questionText()).should.eventually.equal('What is Marcus Twin’s sex?');
    });

    it('When the user answers on their behalf, Then they are shown the non proxy question variant', function () {
      return browser
        .click(HubPage.summaryRowLink(5))
        .click(ProxyPage.no())
        .click(ProxyPage.submit())

        .getText(DateOfBirthPage.questionText()).should.eventually.equal('What is your date of birth?')

        .setValue(DateOfBirthPage.day(), '07')
        .setValue(DateOfBirthPage.month(), '07')
        .setValue(DateOfBirthPage.year(), '1970')
        .click(DateOfBirthPage.submit())

        .getText(ConfirmDateOfBirthPage.questionText()).should.eventually.equal('You are 49 years old. Is this correct?')

        .click(ConfirmDateOfBirthPage.confirmDateOfBirthYes())
        .click(ConfirmDateOfBirthPage.submit())

        .getText(SexPage.questionText()).should.eventually.equal('What is your sex?');
    });

    it('When the user answers on on behalf of someone else, Then they are shown the proxy question variant for the relevant repeating section', function () {
      return browser
        .click(HubPage.summaryRowLink(4))
        .click(ProxyPage.yes())
        .click(ProxyPage.submit())

        .getText(DateOfBirthPage.questionText()).should.eventually.equal('What is Samuel Clemens’ date of birth?')

        .setValue(DateOfBirthPage.day(), '11')
        .setValue(DateOfBirthPage.month(), '11')
        .setValue(DateOfBirthPage.year(), '1990')
        .click(DateOfBirthPage.submit())

        .getText(ConfirmDateOfBirthPage.questionText()).should.eventually.equal('Samuel Clemens is 28 years old. Is this correct?')

        .click(ConfirmDateOfBirthPage.confirmDateOfBirthYes())
        .click(ConfirmDateOfBirthPage.submit())

        .getText(SexPage.questionText()).should.eventually.equal('What is Samuel Clemens’ sex?');
    });


    it('When the user completes all sections, Then the Hub should be in the completed state', function () {
      return browser

        // Complete remaining sections
        .click(HubPage.submit())
        .click(SexPage.male())
        .click(SexPage.submit())
        .click(PersonalSummaryPage.submit())

        .click(HubPage.submit())
        .click(SexPage.submit())
        .click(PersonalSummaryPage.submit())

        .click(HubPage.submit())
        .click(SexPage.female())
        .click(SexPage.submit())
        .click(PersonalSummaryPage.submit())

        .click(HubPage.submit())
        .setValue(VisitorsDateOfBirthPage.day(), '03')
        .setValue(VisitorsDateOfBirthPage.month(), '09')
        .setValue(VisitorsDateOfBirthPage.year(), '1975')
        .click(VisitorsDateOfBirthPage.submit())

        .click(HubPage.submit())
        .setValue(VisitorsDateOfBirthPage.day(), '31')
        .setValue(VisitorsDateOfBirthPage.month(), '07')
        .setValue(VisitorsDateOfBirthPage.year(), '1999')
        .click(VisitorsDateOfBirthPage.submit())

        .getText(HubPage.submit()).should.eventually.equal('Submit survey')
        .getText(HubPage.displayedName()).should.eventually.equal('Submit survey');
    });

    it('When the user adds a new member to the household, Then the Hub should not be in the completed state', function () {
      return browser
        .click(HubPage.summaryRowLink(1))
        .click(PrimaryPersonPage.submit())
        .click(PrimaryPersonAddPage.submit())
        .click(FirstListCollectorPage.submit())
        .click(SecondListCollectorInterstitialPage.submit())
        .click(SecondListCollectorPage.submit())

        // Add another householder
        .click(VisitorsListCollectorPage.yes())
        .click(VisitorsListCollectorPage.submit())

        .setValue(VisitorsListCollectorAddPage.firstName(), 'Anna')
        .setValue(VisitorsListCollectorAddPage.lastName(), 'Doe')

        .click(SecondListCollectorAddPage.submit())
        .click(VisitorsListCollectorPage.no())
        .click(VisitorsListCollectorPage.submit())

        // New householder added to hub
        .getText(HubPage.summaryRowState(8)).should.eventually.equal('Not started')
        .isExisting(HubPage.summaryRowState(8)).should.eventually.be.true

        .getText(HubPage.submit()).should.not.eventually.equal('Submit survey')
        .getText(HubPage.submit()).should.eventually.equal('Continue')

        .getText(HubPage.displayedName()).should.not.eventually.equal('Submit survey')
        .getText(HubPage.displayedName()).should.eventually.equal('Choose another section to complete');
    });

    it('When the user removes a member from the household, Then their section is not longer displayed on he Hub', function () {
      return browser
        // Ensure final householder exists
        .isExisting(HubPage.summaryRowState(8)).should.eventually.be.true

        .click(HubPage.summaryRowLink(1))
        .click(PrimaryPersonPage.submit())
        .click(PrimaryPersonAddPage.submit())
        .click(FirstListCollectorPage.submit())
        .click(SecondListCollectorInterstitialPage.submit())
        .click(SecondListCollectorPage.submit())

        // Remove final householder
        .click(VisitorsListCollectorPage.listRemoveLink(3))
        .click(VisitorsListCollectorRemovePage.yes())
        .click(VisitorsListCollectorPage.submit())

        // Ensure final householder no longer exists
        .isExisting(HubPage.summaryRowState(8)).should.eventually.be.false;
    });

    it('When the user submits, it should show the thank you page', function () {
      return browser
        .click(HubPage.submit())
        .getUrl().should.eventually.contain('thank-you');
    });

  });

});
