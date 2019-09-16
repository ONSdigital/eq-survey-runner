const helpers = require('../helpers');
const HubPage = require('../base_pages/hub.page.js');
const AnyoneUsuallyLiveAtPage = require('../generated_pages/list_collector_driving_question/anyone-usually-live-at.page.js');
const AnyoneElseLiveAtListCollectorPage = require('../generated_pages/list_collector_driving_question/anyone-else-live-at.page.js');
const AnyoneElseLiveAtListCollectorAddPage = require('../generated_pages/list_collector_driving_question/anyone-else-live-at-add.page.js');
const AnyoneElseLiveAtListCollectorRemovePage = require('../generated_pages/list_collector_driving_question/anyone-else-live-at-remove.page.js');
const SummaryPage = require('../generated_pages/list_collector_driving_question/summary.page.js');

function checkPeopleInList(peopleExpected) {
  let chain = browser.waitForVisible(SummaryPage.peopleListLabel(1)).should.eventually.be.true;

  for (let i=1; i<=peopleExpected.length; i++) {
    chain = chain.then(() => {
      return browser.getText(SummaryPage.peopleListLabel(i)).should.eventually.equal(peopleExpected[i-1]);
    });
  }

  return chain;
}

describe('List Collector Driving Question', function() {

  beforeEach('Load the survey', function() {
    return helpers.openQuestionnaire('test_list_collector_driving_question.json')
      .then(() => {
        return browser
          .click(HubPage.submit());
      });
  });

  describe('Given a happy journey through the list collector', function() {
    it('The collector shows all of the household members in the summary', function() {
      return browser
        .click(AnyoneUsuallyLiveAtPage.yes())
        .click(AnyoneUsuallyLiveAtPage.submit())
        .setValue(AnyoneElseLiveAtListCollectorAddPage.firstName(), 'Marcus')
        .setValue(AnyoneElseLiveAtListCollectorAddPage.lastName(), 'Twin')
        .click(AnyoneElseLiveAtListCollectorAddPage.submit())
        .click(AnyoneElseLiveAtListCollectorPage.yes())
        .click(AnyoneElseLiveAtListCollectorPage.submit())
        .setValue(AnyoneElseLiveAtListCollectorAddPage.firstName(), 'Suzy')
        .setValue(AnyoneElseLiveAtListCollectorAddPage.lastName(), 'Clemens')
        .click(AnyoneElseLiveAtListCollectorAddPage.submit())
        .click(AnyoneElseLiveAtListCollectorPage.no())
        .click(AnyoneElseLiveAtListCollectorPage.submit())
        .then(() => {
          const peopleExpected = ['Marcus Twin', 'Suzy Clemens'];

          return checkPeopleInList(peopleExpected);
        });
    });
   });

  describe('Given the user answers no to the driving question', function() {
    it('The summary add link returns to the driving question', function() {
      return browser
        .click(AnyoneUsuallyLiveAtPage.no())
        .click(AnyoneUsuallyLiveAtPage.submit())
        .click(SummaryPage.peopleListAddLink())
        .getUrl().should.eventually.contain(AnyoneUsuallyLiveAtPage.url());
    });
  });


  describe('Given the user answers yes to the driving question, adds someone and later removes them', function() {
    it('The summary add link should return to the original list collector', function() {
      return browser
        .click(AnyoneUsuallyLiveAtPage.yes())
        .click(AnyoneUsuallyLiveAtPage.submit())
        .setValue(AnyoneElseLiveAtListCollectorAddPage.firstName(), 'Marcus')
        .setValue(AnyoneElseLiveAtListCollectorAddPage.lastName(), 'Twin')
        .click(AnyoneElseLiveAtListCollectorAddPage.submit())
        .click(AnyoneElseLiveAtListCollectorPage.no())
        .click(AnyoneElseLiveAtListCollectorPage.submit())
        .click(SummaryPage.peopleListRemoveLink(1))
        .click(AnyoneElseLiveAtListCollectorRemovePage.yes())
        .click(AnyoneElseLiveAtListCollectorRemovePage.submit())
        .click(SummaryPage.peopleListAddLink())
        .getUrl().should.eventually.contain(AnyoneElseLiveAtListCollectorAddPage.pageName);
    });
  });
});
