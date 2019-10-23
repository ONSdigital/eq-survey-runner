const helpers = require('../helpers');
const HubPage = require('../base_pages/hub.page.js');
const AnyoneUsuallyLiveAtPage = require('../generated_pages/list_collector_driving_question/anyone-usually-live-at.page.js');
const AnyoneElseLiveAtListCollectorPage = require('../generated_pages/list_collector_driving_question/anyone-else-live-at.page.js');
const AnyoneElseLiveAtListCollectorAddPage = require('../generated_pages/list_collector_driving_question/anyone-else-live-at-add.page.js');
const AnyoneElseLiveAtListCollectorRemovePage = require('../generated_pages/list_collector_driving_question/anyone-else-live-at-remove.page.js');
const SummaryPage = require('../generated_pages/list_collector_driving_question/summary.page.js');


  function checkPeopleInList(peopleExpected) {
    $(SummaryPage.peopleListLabel(1)).waitForDisplayed();

    for (let i=1; i<=peopleExpected.length; i++) {
      expect($(SummaryPage.peopleListLabel(i)).getText()).to.equal(peopleExpected[i-1]);
    }
  }


describe('List Collector Driving Question', function() {
  let browser;

  beforeEach('Load the survey', function() {
    browser = helpers.openQuestionnaire('test_list_collector_driving_question.json').then(openBrowser => browser = openBrowser);
    $(HubPage.submit()).click();
  });

  describe('Given a happy journey through the list collector', function() {
    it('The collector shows all of the household members in the summary', function() {
        $(AnyoneUsuallyLiveAtPage.yes()).click();
        $(AnyoneUsuallyLiveAtPage.submit()).click();
        $(AnyoneElseLiveAtListCollectorAddPage.firstName()).setValue('Marcus');
        $(AnyoneElseLiveAtListCollectorAddPage.lastName()).setValue('Twin');
        $(AnyoneElseLiveAtListCollectorAddPage.submit()).click();
        $(AnyoneElseLiveAtListCollectorPage.yes()).click();
        $(AnyoneElseLiveAtListCollectorPage.submit()).click();
        $(AnyoneElseLiveAtListCollectorAddPage.firstName()).setValue('Suzy');
        $(AnyoneElseLiveAtListCollectorAddPage.lastName()).setValue('Clemens');
        $(AnyoneElseLiveAtListCollectorAddPage.submit()).click();
        $(AnyoneElseLiveAtListCollectorPage.no()).click();
        $(AnyoneElseLiveAtListCollectorPage.submit()).click();
        
        const peopleExpected = ['Marcus Twin', 'Suzy Clemens'];

        checkPeopleInList(peopleExpected);
    });
   });

  describe('Given the user answers no to the driving question', function() {
    it('The summary add link returns to the driving question', function() {
        $(AnyoneUsuallyLiveAtPage.no()).click();
        $(AnyoneUsuallyLiveAtPage.submit()).click();
        $(SummaryPage.peopleListAddLink()).click();
        expect(browser.getUrl()).to.contain(AnyoneUsuallyLiveAtPage.url());
    });
  });


  describe('Given the user answers yes to the driving question, adds someone and later removes them', function() {
    it('The summary add link should return to the original list collector', function() {
        $(AnyoneUsuallyLiveAtPage.yes()).click();
        $(AnyoneUsuallyLiveAtPage.submit()).click();
        $(AnyoneElseLiveAtListCollectorAddPage.firstName()).setValue('Marcus');
        $(AnyoneElseLiveAtListCollectorAddPage.lastName()).setValue('Twin');
        $(AnyoneElseLiveAtListCollectorAddPage.submit()).click();
        $(AnyoneElseLiveAtListCollectorPage.no()).click();
        $(AnyoneElseLiveAtListCollectorPage.submit()).click();
        $(SummaryPage.peopleListRemoveLink(1)).click();
        $(AnyoneElseLiveAtListCollectorRemovePage.yes()).click();
        $(AnyoneElseLiveAtListCollectorRemovePage.submit()).click();
        $(SummaryPage.peopleListAddLink()).click();
        expect(browser.getUrl()).to.contain(AnyoneElseLiveAtListCollectorAddPage.pageName);
    });
  });
});
