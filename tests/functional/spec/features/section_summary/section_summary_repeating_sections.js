const helpers = require('../../../helpers');

const PrimaryPersonPage = require('../../../generated_pages/repeating_section_summaries/primary-person-list-collector.page');
const PrimaryPersonAddPage = require('../../../generated_pages/repeating_section_summaries/primary-person-list-collector-add.page');

const FirstListCollectorPage = require('../../../generated_pages/repeating_section_summaries/list-collector.page');
const FirstListCollectorAddPage = require('../../../generated_pages/repeating_section_summaries/list-collector-add.page');

const PersonalSummaryPage = require('../../../generated_pages/repeating_section_summaries/personal-summary.page');

const ProxyPage = require('../../../generated_pages/repeating_section_summaries/proxy.page');
const DateOfBirthPage = require('../../../generated_pages/repeating_section_summaries/date-of-birth.page');

const HubPage = require('../../../base_pages/hub.page.js');


describe('Feature: Repeating Section Summaries', function () {

  const repeating_section_summaries_schema = 'test_repeating_section_summaries.json';

  describe('Given the user has added some members to the household and is on the Hub', function () {

    before('Open survey and add household members', function () {
      return helpers.openQuestionnaire(repeating_section_summaries_schema)
        .then(() => {
          return browser
            // Ensure we are on the Hub
            .getUrl().should.eventually.contain(HubPage.url())
            // Start first section to add household members
            .click(HubPage.summaryRowLink(1))

            // Add a primary person
            .click(PrimaryPersonPage.yes())
            .click(PrimaryPersonPage.submit())
            .setValue(PrimaryPersonAddPage.firstName(), 'Mark')
            .setValue(PrimaryPersonAddPage.lastName(), 'Twain')
            .click(PrimaryPersonPage.submit())

            // Add other household members

            .click(FirstListCollectorPage.yes())
            .click(FirstListCollectorPage.submit())
            .setValue(FirstListCollectorAddPage.firstName(), 'Jean')
            .setValue(FirstListCollectorAddPage.lastName(), 'Clemens')
            .click(FirstListCollectorAddPage.submit())

            .click(FirstListCollectorPage.no())
            .click(FirstListCollectorPage.submit());
        });
    });


    describe('When the user finishes a repeating section', function() {

      before('Enter information for a repeating section', function() {
        return browser
          .click(HubPage.summaryRowLink(2))
          .click(ProxyPage.yes())
          .click(ProxyPage.submit())

          .setValue(DateOfBirthPage.day(), '30')
          .setValue(DateOfBirthPage.month(), '11')
          .setValue(DateOfBirthPage.year(), '1835')
          .click(DateOfBirthPage.submit());
      });

      beforeEach('Navigate to the Section Summary', function () {
        return browser
          .url(HubPage.url())
          .click(HubPage.summaryRowLink(2));
      });

      it('shows their name in the section summary title', function() {
        return browser
          .getText(PersonalSummaryPage.questionText()).should.eventually.contain('Mark Twain');
      });

      it('renders their name as part of the question title on the section summary', function() {
        return browser
          .getText(PersonalSummaryPage.dateOfBirthQuestion()).should.eventually.contain('Mark Twain’s');
      });

      it('renders the correct date of birth answer', function() {
        return browser
          .getText(PersonalSummaryPage.dateOfBirthAnswer()).should.eventually.contain('30 November 1835');
      });

    });

  });

});
