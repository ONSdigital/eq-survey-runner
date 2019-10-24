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
    browser.openQuestionnaire(hub_and_spoke_schema);
    expect($(HubPage.submit()).getText()).to.contain('Continue');
    expect($(HubPage.displayedName()).getText()).to.contain('Choose another section to complete');
    expect($(HubPage.summaryRowState(1)).getText()).to.contain('Not started');
    expect($(HubPage.summaryRowState(2)).getText()).to.contain('Not started');
  });


  describe('Given a user is on the Hub page', function () {
    it('When the user click the \'Save and sign out\' button then they should be on the signed out page', function () {
      browser.openQuestionnaire(hub_and_spoke_schema);

      $(HubPage.saveSignOut()).click();

      let expectedUrl = browser.getUrl();

      expect(expectedUrl).to.contain('/signed-out');
    });
  });


  describe('Given a user has not started a section', function () {
    beforeEach('Open survey', function () {
      browser.openQuestionnaire(hub_and_spoke_schema);
      expect($(HubPage.summaryRowState(1)).getText()).to.contain('Not started');
      expect($(HubPage.summaryRowState(2)).getText()).to.contain('Not started');
    });

    it('When the user starts a section, Then the first question in the section should be displayed', function () {
        $(HubPage.submit()).click();
        let expectedUrl = browser.getUrl();
        expect(expectedUrl).to.contain(EmploymentStatusBlockPage.url());
    });

    it('When the user starts a section and clicks the Previous link on the first question, Then they should be taken back to the Hub', function () {
        $(HubPage.submit()).click();
        $(EmploymentStatusBlockPage.previous()).click();
        let expectedUrl = browser.getUrl();
        expect(expectedUrl).to.contain(HubPage.url());
    });

  });

  describe('Given a user has started a section', function () {
    before('Start section', function () {
      browser.openQuestionnaire(hub_and_spoke_schema);
      $(HubPage.summaryRowLink(1)).click();
      $(EmploymentStatusBlockPage.exclusiveNoneOfTheseApply()).click();
      $(EmploymentStatusBlockPage.submit()).click();
    });

    it('When the user returns to the Hub, Then the Hub should be in a continue state', function () {
      browser.url(HubPage.url());
      expect($(HubPage.submit()).getText()).to.contain('Continue');
      expect($(HubPage.displayedName()).getText()).to.contain('Choose another section to complete');
    });

    it('When the user returns to the Hub, Then the section should be marked as \'Partially completed\'', function () {
      browser.url(HubPage.url());
      expect($(HubPage.summaryRowState(1)).getText()).to.contain('Partially completed');
    });

    it('When the user return to the Hub and restarts the same section, Then they should be returned to the last completed question', function () {
      browser.url(HubPage.url());
      $(HubPage.summaryRowLink(1)).click();
      let expectedUrl = browser.getUrl();
      expect(expectedUrl).to.contain(EmploymentStatusBlockPage.url());
    });
  });


  describe('Given a user has completed a section', function () {
    beforeEach('Complete section', function () {
      browser.openQuestionnaire(hub_and_spoke_schema);
      $(HubPage.summaryRowLink(1)).click();
      $(EmploymentStatusBlockPage.exclusiveNoneOfTheseApply()).click();
      $(EmploymentStatusBlockPage.submit()).click();
      $(EmploymentTypeBlockPage.studying()).click();
    });

    it('When the user clicks the \'Continue\' button, it should return them to the hub', function () {
      $(EmploymentTypeBlockPage.submit()).click();
      let expectedUrl = browser.getUrl();
      expect(expectedUrl).to.contain(HubPage.url());
    });

    it('When the user returns to the Hub, Then the Hub should be in a continue state', function () {
      $(EmploymentTypeBlockPage.submit()).click();
      expect($(HubPage.submit()).getText()).to.contain('Continue');
      expect($(HubPage.displayedName()).getText()).to.contain('Choose another section to complete');
    });

    it('When the user returns to the Hub, Then the section should be marked as \'Completed\'', function () {
      $(EmploymentTypeBlockPage.submit()).click();
      expect($(HubPage.summaryRowState(1)).getText()).to.contain('Completed');

      expect($(HubPage.summaryRowTitle(1)).getAttribute('class')).to.contain('summary__item-title--has-icon');
    });

    it('When the user returns to the Hub and clicks the \'View answers\' link on the Hub, if this no summary they are returned to the first block', function () {
      $(EmploymentTypeBlockPage.submit()).click();
      $(HubPage.summaryRowLink(1)).click();
      let expectedUrl = browser.getUrl();
      expect(expectedUrl).to.contain(EmploymentStatusBlockPage.url());
    });

    it('When the user returns to the Hub and continues, Then they should progress to the next section', function () {
      $(EmploymentTypeBlockPage.submit()).click();
      expect(browser.getUrl()).to.contain(HubPage.url());
      $(HubPage.submit()).click();
      let expectedUrl = browser.getUrl();
      expect(expectedUrl).to.contain(ProxyPage.url());
    });
  });

  describe('Given a user has completed a section and is on the Hub page', function () {
    beforeEach('Complete section', function () {
      browser.openQuestionnaire(hub_and_spoke_schema);
      $(HubPage.summaryRowLink(1)).click();
      $(EmploymentStatusBlockPage.workingAsAnEmployee()).click();
      $(EmploymentStatusBlockPage.submit()).click();

      expect($(HubPage.summaryRowState(1)).getText()).to.contain('Completed');
      expect($(HubPage.summaryRowTitle(1)).getAttribute('class')).to.contain('summary__item-title--has-icon');
    });

    it('When the user clicks the \'View answers\' link and incompletes the section, Then they the should be taken to the next incomplete question on \'Continue', function () {
      $(HubPage.summaryRowLink(1)).click();
      expect(browser.getUrl()).to.contain(EmploymentStatusBlockPage.url());
      $(EmploymentStatusBlockPage.exclusiveNoneOfTheseApply()).click();
      $(EmploymentStatusBlockPage.submit()).click();
      let expectedUrl = browser.getUrl();
      expect(expectedUrl).to.contain(EmploymentTypeBlockPage.url());
    });

    it('When the user clicks the \'View answers\' link and incompletes the section and returns to the hub, Then the section should be marked as \'Partially completed\'', function () {
      $(HubPage.summaryRowLink(1)).click();
      expect(browser.getUrl()).to.contain(EmploymentStatusBlockPage.url());
      $(EmploymentStatusBlockPage.exclusiveNoneOfTheseApply()).click();
      $(EmploymentStatusBlockPage.submit()).click();
      browser.url(HubPage.url());
      let expectedUrl = browser.getUrl();
      expect(expectedUrl).to.contain(HubPage.url());
      expect($(HubPage.summaryRowState(1)).getText()).to.contain('Partially completed');
      expect($(HubPage.summaryRowTitle(1)).getAttribute('class')).not.to.contain('summary__item-title--has-icon');
    });
  });

  describe('Given a user has completed all sections', function () {
    beforeEach('Complete all sections', function () {
      browser.openQuestionnaire(hub_and_spoke_schema);
      $(HubPage.summaryRowLink(1)).click();
      $(EmploymentStatusBlockPage.exclusiveNoneOfTheseApply()).click();
      $(EmploymentStatusBlockPage.submit()).click();
      $(EmploymentTypeBlockPage.studying()).click();
      $(EmploymentTypeBlockPage.submit()).click();
      $(HubPage.submit()).click();
      $(ProxyPage.yes()).click();
      $(ProxyPage.submit()).click();
      $(AccomodationDetailsSummaryBlockPage.submit()).click();
      $(HubPage.submit()).click();
      $(DoesAnyoneLiveHere.no()).click();
      $(DoesAnyoneLiveHere.submit()).click();
      $(HouseholdSummary.submit()).click();
    });

    it('It should return them to the hub', function () {
      let expectedUrl = browser.getUrl();
      expect(expectedUrl).to.contain(HubPage.url());
    });

    it('When the user returns to the Hub, Then the Hub should be in a completed state', function () {
      expect($(HubPage.submit()).getText()).to.contain('Submit');
      expect($(HubPage.displayedName()).getText()).to.contain('Submit survey');
    });

    it('When the user submits, it should show the thankyou page', function () {
      $(HubPage.submit()).click();
      let expectedUrl = browser.getUrl();
      expect(expectedUrl).to.contain('thank-you');
    });
  });

  describe('Given a user opens a schema with required sections', function () {
    beforeEach('Load survey',  function(){
      browser.openQuestionnaire('test_hub_complete_sections.json');
    });

    it('The hub should not show first of all', function () {
      expect(browser.getUrl()).to.contain(EmploymentStatusBlockPage.url());
    });

    it('The hub should only display when required sections are complete', function () {
      $(EmploymentStatusBlockPage.exclusiveNoneOfTheseApply()).click();
      $(EmploymentStatusBlockPage.submit()).click();
      $(EmploymentTypeBlockPage.studying()).click();
      $(EmploymentTypeBlockPage.submit()).click();
      expect(browser.getUrl()).to.contain(HubPage.url());
    });
  });

    describe('Given the user has completed a section with a summary mid section', function () {
      it('When the user clicks \'View answers\' it will return to that section summary', function () {
        browser.openQuestionnaire('test_hub_and_spoke.json');
        $(HubPage.summaryRowLink(3)).click();
        $(DoesAnyoneLiveHere.no()).click();
        $(DoesAnyoneLiveHere.submit()).click();
        $(HouseholdSummary.submit()).click();
        $(HubPage.summaryRowLink(3)).click();
        let expectedUrl = browser.getUrl();
        expect(expectedUrl).to.contain(HouseholdSummary.url());
      });
    });
    describe('Given a section is complete and the user has been returned to a section summary by clicking the \'View answers\' link ', function () {
      beforeEach('Complete section', function () {
        browser.openQuestionnaire(hub_and_spoke_schema);
        $(HubPage.summaryRowLink(3)).click();
        $(DoesAnyoneLiveHere.no()).click();
        $(DoesAnyoneLiveHere.submit()).click();
        $(HouseholdSummary.submit()).click();
      });

      it('When there are no changes, continue returns directly to the hub', function () {
        $(HubPage.summaryRowLink(3)).click();
        $(HouseholdSummary.submit()).click();
        let expectedUrl = browser.getUrl();
        expect(expectedUrl).to.contain(HubPage.url());
      });

      it('When there are changes which would set the section to in_progress it routes accordingly', function () {
        $(HubPage.summaryRowLink(3)).click();
        $(HouseholdSummary.doesAnyoneLiveHereAnswerEdit()).click();
        $(DoesAnyoneLiveHere.yes()).click();
        $(DoesAnyoneLiveHere.submit()).click();
        $(HouseholdSummary.submit()).click();
        let expectedUrl = browser.getUrl();
        expect(expectedUrl).to.contain(HowManyPeopleLiveHere.url());
      });
  });
});
