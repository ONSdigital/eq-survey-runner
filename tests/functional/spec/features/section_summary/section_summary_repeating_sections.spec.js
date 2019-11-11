const PrimaryPersonPage = require('../../../generated_pages/repeating_section_summaries/primary-person-list-collector.page');
const PrimaryPersonAddPage = require('../../../generated_pages/repeating_section_summaries/primary-person-list-collector-add.page');

const FirstListCollectorPage = require('../../../generated_pages/repeating_section_summaries/list-collector.page');
const FirstListCollectorAddPage = require('../../../generated_pages/repeating_section_summaries/list-collector-add.page');

const PersonalSummaryPage = require('../../../generated_pages/repeating_section_summaries/personal-summary.page');

const ProxyPage = require('../../../generated_pages/repeating_section_summaries/proxy.page');
const DateOfBirthPage = require('../../../generated_pages/repeating_section_summaries/date-of-birth.page');

const HubPage = require('../../../base_pages/hub.page.js');


describe('Feature: Repeating Section Summaries', function () {

  describe('Given the user has added some members to the household and is on the Hub', function () {
    before('Open survey and add household members', function () {
      browser.openQuestionnaire('test_repeating_section_summaries.json');
      // Ensure we are on the Hub
      expect(browser.getUrl()).to.contain(HubPage.url());
      // Start first section to add household members
      $(HubPage.summaryRowLink(1)).click();

      // Add a primary person
      $(PrimaryPersonPage.yes()).click();
      $(PrimaryPersonPage.submit()).click();
      $(PrimaryPersonAddPage.firstName()).setValue('Mark');
      $(PrimaryPersonAddPage.lastName()).setValue('Twain');
      $(PrimaryPersonPage.submit()).click();

      // Add other household members

      $(FirstListCollectorPage.yes()).click();
      $(FirstListCollectorPage.submit()).click();
      $(FirstListCollectorAddPage.firstName()).setValue('Jean');
      $(FirstListCollectorAddPage.lastName()).setValue('Clemens');
      $(FirstListCollectorAddPage.submit()).click();

      $(FirstListCollectorPage.no()).click();
      $(FirstListCollectorPage.submit()).click();
    });

    describe('When the user finishes a repeating section', function() {
      before('Enter information for a repeating section', function() {
        $(HubPage.summaryRowLink(2)).click();
        $(ProxyPage.yes()).click();
        $(ProxyPage.submit()).click();

        $(DateOfBirthPage.day()).setValue('30');
        $(DateOfBirthPage.month()).setValue('11');
        $(DateOfBirthPage.year()).setValue('1835');
        $(DateOfBirthPage.submit()).click();
      });

      beforeEach('Navigate to the Section Summary', function () {
        browser.url(HubPage.url());
        $(HubPage.summaryRowLink(2)).click();
      });

      it('shows their name in the section summary title', function() {
        expect($(PersonalSummaryPage.questionText()).getText()).to.contain('Mark Twain');
      });

      it('renders their name as part of the question title on the section summary', function() {
        expect($(PersonalSummaryPage.dateOfBirthQuestion()).getText()).to.contain('Mark Twain’s');
      });

      it('renders the correct date of birth answer', function() {
        expect($(PersonalSummaryPage.dateOfBirthAnswer()).getText()).to.contain('30 November 1835');
      });
    });
  });
});
