const AnyoneLiveAtListCollector = require('../generated_pages/answer_action_redirect_to_list_add_question_checkbox/anyone-else-live-at.page');
const AnyoneLiveAtListCollectorAddPage = require('../generated_pages/answer_action_redirect_to_list_add_question_checkbox/anyone-else-live-at-add.page');
const AnyoneLiveAtListCollectorRemovePage = require('../generated_pages/answer_action_redirect_to_list_add_question_checkbox/anyone-else-live-at-remove.page');
const AnyoneUsuallyLiveAt = require('../generated_pages/answer_action_redirect_to_list_add_question_checkbox/anyone-usually-live-at.page');


function checkPeopleInList(peopleExpected) {
  $(AnyoneLiveAtListCollector.listLabel(1)).waitForDisplayed();

  for (let i=1; i<=peopleExpected.length; i++) {
    expect($(AnyoneLiveAtListCollector.listLabel(i)).getText()).to.equal(peopleExpected[i-1]);
  }
}


describe('Answer Action: Redirect To List Add Question (Checkbox)', function () {
  describe('Given the user is on a question with a "RedirectToListAddQuestion" action enabled', function () {

    before('Launch survey', function () {
      browser.openQuestionnaire('test_answer_action_redirect_to_list_add_question_checkbox.json');
    });

    it('When the user selects "No", Then, they should be taken to straight the list collector.', function () {
        $(AnyoneUsuallyLiveAt.no()).click();
        $(AnyoneUsuallyLiveAt.submit()).click();
        expect(browser.getUrl()).to.contain(AnyoneLiveAtListCollector.pageName);
    });

    it('When the user selects "Yes" then they should be taken to the list collector add question.', function () {
        browser.url(AnyoneUsuallyLiveAt.url());
        $(AnyoneUsuallyLiveAt.iThinkSo()).click();
        $(AnyoneUsuallyLiveAt.submit()).click();
        expect(browser.getUrl()).to.contain(AnyoneLiveAtListCollectorAddPage.pageName);
        expect(browser.getUrl()).to.contain('?previous=anyone-usually-live-at');
    });

    it('When the user clicks the "Previous" link from the add question then they should be taken to the block they came from, not the list collector', function () {
        $(AnyoneLiveAtListCollectorAddPage.previous()).click();
        expect(browser.getUrl()).to.contain(AnyoneUsuallyLiveAt.pageName);
    });

    it('When the user adds a household member, Then, they are taken to the list collector and the household members are displayed', function () {
        $(AnyoneUsuallyLiveAt.submit()).click();
        $(AnyoneLiveAtListCollectorAddPage.firstName()).setValue('Marcus');
        $(AnyoneLiveAtListCollectorAddPage.lastName()).setValue('Twin');
        $(AnyoneLiveAtListCollectorAddPage.submit()).click();
        expect(browser.getUrl()).to.contain(AnyoneLiveAtListCollector.pageName);
        const peopleExpected = ['Marcus Twin'];

        checkPeopleInList(peopleExpected);
    });

    it('When the user click the "Previous" link from the list collector, Then, they are taken to the last complete block', function () {
        $(AnyoneLiveAtListCollector.previous()).click();
        expect(browser.getUrl()).to.contain(AnyoneUsuallyLiveAt.pageName);

    });

    it('When the user resubmits the first block and then list is not empty, Then they are taken to the list collector', function () {
        $(AnyoneUsuallyLiveAt.submit()).click();
        expect(browser.getUrl()).to.contain(AnyoneLiveAtListCollector.pageName);

    });

    it('When the users removes the only person (Marcus Twain), Then, they are shown an empty list collector', function () {
        $(AnyoneLiveAtListCollector.listRemoveLink(1)).click();
        $(AnyoneLiveAtListCollectorRemovePage.yes()).click();
        $(AnyoneLiveAtListCollectorRemovePage.submit()).click();
        expect(browser.getUrl()).to.contain(AnyoneLiveAtListCollector.pageName);
        expect($(AnyoneLiveAtListCollector.listLabel(1)).isExisting()).to.be.false;

    });

    it('When the user resubmits the first block and then list is empty, Then they are taken to the add question', function () {
        expect(browser.getUrl()).to.contain(AnyoneLiveAtListCollector.pageName);

        $(AnyoneLiveAtListCollector.previous()).click();
        expect(browser.getUrl()).to.contain(AnyoneUsuallyLiveAt.pageName);

        $(AnyoneUsuallyLiveAt.submit()).click();
        expect(browser.getUrl()).to.contain(AnyoneLiveAtListCollectorAddPage.pageName);

    });

  });

});
