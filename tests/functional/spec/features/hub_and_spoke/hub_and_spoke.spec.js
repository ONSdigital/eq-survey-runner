const helpers = require('../../../helpers');

const EmploymentStatusBlockPage = require('../../../generated_pages/hub_and_spoke/employment-status.page.js');
const EmploymentTypeBlockPage = require('../../../generated_pages/hub_and_spoke/employment-type.page.js');
const HouseholdSummary = require('../../../generated_pages/hub_and_spoke/household-summary.page.js');
const HowManyPeopleLiveHere = require('../../../generated_pages/hub_and_spoke/how-many-people-live-here.page.js');
const ProxyPage = require('../../../generated_pages/hub_and_spoke/proxy.page.js');
const AccomodationDetailsSummaryBlockPage = require('../../../generated_pages/hub_and_spoke/accommodation-details-summary.page.js');
const DoesAnyoneLiveHere = require('../../../generated_pages/hub_and_spoke/does-anyone-live-here.page.js');

const HubPage = require('../../../base_pages/hub.page.js');


describe('Feature: Hub and Spoke', function () {

  const hub_and_spoke_schema = 'test_hub_and_spoke.json';

  it('When a user first views the Hub, The Hub should be in a continue state', function () {
    return helpers.openQuestionnaire(hub_and_spoke_schema)
      .then(() => {
        return browser
          .getText(HubPage.submit()).should.eventually.contain('Continue')
          .getText(HubPage.displayedName()).should.eventually.contain('Choose another section to complete')
          .getText(HubPage.summaryRowState(1)).should.eventually.contain('Not started')
          .getText(HubPage.summaryRowState(2)).should.eventually.contain('Not started');
      });
  });


  describe('Given a user is on the Hub page', function () {

    before('Open survey', function () {
      return helpers.openQuestionnaire(hub_and_spoke_schema)
        .then(() => {
          return browser
            .getUrl().should.eventually.contain(HubPage.url());
        });
    });

    it('When the user click the \'Save and sign out\' button then they should be on the signed out page', function () {
      return browser
        .getUrl().should.eventually.contain(HubPage.url())
        .click(HubPage.saveSignOut())
        .getUrl().should.eventually.contain('/signed-out');
    });

  });


  describe('Given a user has not started a section', function () {

    beforeEach('Open survey', function () {
      return helpers.openQuestionnaire(hub_and_spoke_schema)
        .then(() => {
          return browser
            .getUrl().should.eventually.contain(HubPage.url())
            .getText(HubPage.summaryRowState(1)).should.eventually.contain('Not started')
            .getText(HubPage.summaryRowState(2)).should.eventually.contain('Not started');
        });
    });

    it('When the user starts a section, Then the first question in the section should be displayed', function () {
      return browser
        .click(HubPage.submit())
        .getUrl().should.eventually.contain(EmploymentStatusBlockPage.url());
    });

    it('When the user starts a section and clicks the Previous link on the first question, Then they should be taken back to the Hub', function () {
      return browser
        .click(HubPage.submit())
        .click(EmploymentStatusBlockPage.previous())
        .getUrl().should.eventually.contain(HubPage.url());
    });

  });

  describe('Given a user has started a section', function () {

    before('Start section', function () {
      return helpers.openQuestionnaire(hub_and_spoke_schema)
        .then(() => {
          return browser
            .click(HubPage.summaryRowLink(1))
            .click(EmploymentStatusBlockPage.exclusiveNoneOfTheseApply())
            .click(EmploymentStatusBlockPage.submit());
        });
    });

    it('When the user returns to the Hub, Then the Hub should be in a continue state', function () {
      return browser
        .url(HubPage.url())
        .getText(HubPage.submit()).should.eventually.contain('Continue')
        .getText(HubPage.displayedName()).should.eventually.contain('Choose another section to complete');
    });

    it('When the user returns to the Hub, Then the section should be marked as \'Partially completed\'', function () {
      return browser
        .url(HubPage.url())
        .getText(HubPage.summaryRowState(1)).should.eventually.contain('Partially completed');
    });

    it('When the user return to the Hub and restarts the same section, Then they should be returned to the last completed question', function () {
      return browser
        .url(HubPage.url())
        .click(HubPage.summaryRowLink(1))
        .getUrl().should.eventually.contain(EmploymentStatusBlockPage.url());
    });

  });


  describe('Given a user has completed a section', function () {

    beforeEach('Complete section', function () {
      return helpers.openQuestionnaire(hub_and_spoke_schema)
        .then(() => {
          return browser
            .click(HubPage.summaryRowLink(1))
            .click(EmploymentStatusBlockPage.exclusiveNoneOfTheseApply())
            .click(EmploymentStatusBlockPage.submit())
            .click(EmploymentTypeBlockPage.studying());
        });
    });

    it('When the user clicks the \'Continue\' button, it should return them to the hub', function () {
      return browser
        .click(EmploymentTypeBlockPage.submit())
        .getUrl().should.eventually.contain(HubPage.url());
    });

    it('When the user returns to the Hub, Then the Hub should be in a continue state', function () {
      return browser
        .click(EmploymentTypeBlockPage.submit())
        .getText(HubPage.submit()).should.eventually.contain('Continue')
        .getText(HubPage.displayedName()).should.eventually.contain('Choose another section to complete');
    });

    it('When the user returns to the Hub, Then the section should be marked as \'Completed\'', function () {
      return browser
        .click(EmploymentTypeBlockPage.submit())
        .getText(HubPage.summaryRowState(1)).should.eventually.contain('Completed')
        .getAttribute(HubPage.summaryRowTitle(1), 'class').should.eventually.contain('summary__item-title--has-icon');
    });

    it('When the user returns to the Hub and clicks the \'View answers\' link on the Hub, if this no summary they are returned to the first block', function () {
      return browser
        .click(EmploymentTypeBlockPage.submit())
        .click(HubPage.summaryRowLink(1))
        .getUrl().should.eventually.contain(EmploymentStatusBlockPage.url());
    });

    it('When the user returns to the Hub and continues, Then they should progress to the next section', function () {
      return browser
        .click(EmploymentTypeBlockPage.submit())
        .getUrl().should.eventually.contain(HubPage.url())
        .click(HubPage.submit())
        .getUrl().should.eventually.contain(ProxyPage.url());
    });

  });

  describe('Given a user has completed a section and is on the Hub page', function () {

    beforeEach('Complete section', function () {
      return helpers.openQuestionnaire(hub_and_spoke_schema)
        .then(() => {
          return browser
            .click(HubPage.summaryRowLink(1))
            .click(EmploymentStatusBlockPage.workingAsAnEmployee())
            .click(EmploymentStatusBlockPage.submit())
            .getText(HubPage.summaryRowState(1)).should.eventually.contain('Completed')
            .getAttribute(HubPage.summaryRowTitle(1), 'class').should.eventually.contain('summary__item-title--has-icon');
        });
    });

    it('When the user clicks the \'View answers\' link and incompletes the section, Then they the should be taken to the next incomplete question on \'Continue', function () {
      return browser
        .click(HubPage.summaryRowLink(1))
        .getUrl().should.eventually.contain(EmploymentStatusBlockPage.url())
        .click(EmploymentStatusBlockPage.exclusiveNoneOfTheseApply())
        .click(EmploymentStatusBlockPage.submit())
        .getUrl().should.eventually.contain(EmploymentTypeBlockPage.url());
    });

    it('When the user clicks the \'View answers\' link and incompletes the section and returns to the hub, Then the section should be marked as \'Partially completed\'', function () {
      return browser
        .click(HubPage.summaryRowLink(1))
        .getUrl().should.eventually.contain(EmploymentStatusBlockPage.url())
        .click(EmploymentStatusBlockPage.exclusiveNoneOfTheseApply())
        .click(EmploymentStatusBlockPage.submit())
        .url(HubPage.url())
        .getUrl().should.eventually.contain(HubPage.url())
        .getText(HubPage.summaryRowState(1)).should.eventually.contain('Partially completed')
        .getAttribute(HubPage.summaryRowTitle(1), 'class').should.not.eventually.contain('summary__item-title--has-icon');
    });

  });


  describe('Given a user has completed all sections', function () {

    beforeEach('Complete all sections', function () {
      return helpers.openQuestionnaire(hub_and_spoke_schema)
        .then(() => {
          return browser
            .click(HubPage.summaryRowLink(1))
            .click(EmploymentStatusBlockPage.exclusiveNoneOfTheseApply())
            .click(EmploymentStatusBlockPage.submit())
            .click(EmploymentTypeBlockPage.studying())
            .click(EmploymentTypeBlockPage.submit())
            .click(HubPage.submit())
            .click(ProxyPage.yes())
            .click(ProxyPage.submit())
            .click(AccomodationDetailsSummaryBlockPage.submit())
            .click(HubPage.submit())
            .click(DoesAnyoneLiveHere.no())
            .click(DoesAnyoneLiveHere.submit())
            .click(HouseholdSummary.submit());
        });
    });

    it('It should return them to the hub', function () {
      return browser.getUrl().should.eventually.contain(HubPage.url());
    });

    it('When the user returns to the Hub, Then the Hub should be in a completed state', function () {
      return browser
        .getText(HubPage.submit()).should.eventually.contain('Submit')
        .getText(HubPage.displayedName()).should.eventually.contain('Submit survey');
    });

    it('When the user submits, it should show the thankyou page', function () {
      return browser
        .click(HubPage.submit())
        .getUrl().should.eventually.contain('thank-you');
    });
  });

  describe('Given a user opens a schema with required sections', function () {
    it('The hub should not show first of all', function () {
      return helpers.openQuestionnaire('test_hub_complete_sections.json')
        .then(() => {
          return browser
            .getUrl().should.eventually.contain(EmploymentStatusBlockPage.url());
       });
    });

    it('The hub should only display when required sections are complete', function () {
      return helpers.openQuestionnaire('test_hub_complete_sections.json')
        .then(() => {
          return browser
            .click(EmploymentStatusBlockPage.exclusiveNoneOfTheseApply())
            .click(EmploymentStatusBlockPage.submit())
            .click(EmploymentTypeBlockPage.studying())
            .click(EmploymentTypeBlockPage.submit())
            .getUrl().should.eventually.contain(HubPage.url());
       });
    });
  });

    describe('Given the user has completed a section with a summary mid section', function () {
    it('When the user clicks \'View answers\' it will return to that section summary', function () {
      return helpers.openQuestionnaire('test_hub_and_spoke.json')
        .then(() => {
          return browser
            .click(HubPage.summaryRowLink(3))
            .click(DoesAnyoneLiveHere.no())
            .click(DoesAnyoneLiveHere.submit())
            .click(HouseholdSummary.submit())
            .click(HubPage.summaryRowLink(3))
            .getUrl().should.eventually.contain(HouseholdSummary.url());
       });
    });
  });
    describe('Given a section is complete and the user has been returned to a section summary by clicking the \'View answers\' link ', function () {
      beforeEach('Complete section', function () {
      return helpers.openQuestionnaire(hub_and_spoke_schema)
        .then(() => {
          return browser
            .click(HubPage.summaryRowLink(3))
            .click(DoesAnyoneLiveHere.no())
            .click(DoesAnyoneLiveHere.submit())
            .click(HouseholdSummary.submit());
        });
    });
    it('When there are no changes, continue returns directly to the hub', function () {
          return browser
            .click(HubPage.summaryRowLink(3))
            .click(HouseholdSummary.submit())
            .getUrl().should.eventually.contain(HubPage.url());
    });
    it('When there are changes which would set the section to in_progress it routes accordingly', function () {
          return browser
            .click(HubPage.summaryRowLink(3))
            .click(HouseholdSummary.doesAnyoneLiveHereAnswerEdit())
            .click(DoesAnyoneLiveHere.yes())
            .click(DoesAnyoneLiveHere.submit())
            .click(HouseholdSummary.submit())
            .getUrl().should.eventually.contain(HowManyPeopleLiveHere.url());
    });
  });
});
