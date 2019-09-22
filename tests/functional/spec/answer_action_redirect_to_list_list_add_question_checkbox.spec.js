const helpers = require('../helpers');
const AnyoneLiveAtListCollector = require('../generated_pages/answer_action_redirect_to_list_add_question_checkbox/anyone-else-live-at.page');
const AnyoneLiveAtListCollectorAddPage = require('../generated_pages/answer_action_redirect_to_list_add_question_checkbox/anyone-else-live-at-add.page');
const AnyoneLiveAtListCollectorRemovePage = require('../generated_pages/answer_action_redirect_to_list_add_question_checkbox/anyone-else-live-at-remove.page');
const AnyoneUsuallyLiveAt = require('../generated_pages/answer_action_redirect_to_list_add_question_checkbox/anyone-usually-live-at.page');

function checkPeopleInList(peopleExpected) {
  let chain = browser.waitForVisible(AnyoneLiveAtListCollector.listLabel(1)).should.eventually.be.true;

  for (let i = 1; i <= peopleExpected.length; i++) {
    chain = chain.then(() => {
      return browser.getText(AnyoneLiveAtListCollector.listLabel(i)).should.eventually.equal(peopleExpected[i - 1]);
    });
  }

  return chain;
}

describe('Answer Action: Redirect To List Add Question (Checkbox)', function () {

  describe('Given the user is on a question with a "RedirectToListAddQuestion" action enabled', function () {

    before('Launch survey', function () {
      return helpers.openQuestionnaire('test_answer_action_redirect_to_list_add_question_checkbox.json');
    });

    it('When the user selects "No", Then, they should be taken to straight the list collector.', function () {
      return browser
        .click(AnyoneUsuallyLiveAt.no())
        .click(AnyoneUsuallyLiveAt.submit())
        .getUrl().should.eventually.contain(AnyoneLiveAtListCollector.pageName);
    });

    it('When the user selects "Yes" then they should be taken to the list collector add question.', function () {
      return browser
        .url(AnyoneUsuallyLiveAt.url())
        .click(AnyoneUsuallyLiveAt.iThinkSo())
        .click(AnyoneUsuallyLiveAt.submit())
        .getUrl().should.eventually.contain(AnyoneLiveAtListCollectorAddPage.pageName)
        .getUrl().should.eventually.contain('?previous=anyone-usually-live-at');
    });

    it('When the user clicks the "Previous" link from the add question then they should be taken to the block they came from, not the list collector', function () {
      return browser
        .click(AnyoneLiveAtListCollectorAddPage.previous())
        .getUrl().should.eventually.contain(AnyoneUsuallyLiveAt.pageName);
    });

    it('When the user adds a household member, Then, they are taken to the list collector and the household members are displayed', function () {
      return browser
        .click(AnyoneUsuallyLiveAt.submit())
        .setValue(AnyoneLiveAtListCollectorAddPage.firstName(), 'Marcus')
        .setValue(AnyoneLiveAtListCollectorAddPage.lastName(), 'Twin')
        .click(AnyoneLiveAtListCollectorAddPage.submit())
        .getUrl().should.eventually.contain(AnyoneLiveAtListCollector.pageName).then(function () {
          const peopleExpected = ['Marcus Twin'];
          return checkPeopleInList(peopleExpected);
        });
    });

    it('When the user click the "Previous" link from the list collector, Then, they are taken to the last complete block', function () {
      return browser
        .click(AnyoneLiveAtListCollector.previous())
        .getUrl().should.eventually.contain(AnyoneUsuallyLiveAt.pageName);

    });

    it('When the user resubmits the first block and then list is not empty, Then they are taken to the list collector', function () {
      return browser
        .click(AnyoneUsuallyLiveAt.submit())
        .getUrl().should.eventually.contain(AnyoneLiveAtListCollector.pageName);

    });

    it('When the users removes the only person (Marcus Twain), Then, they are shown an empty list collector', function () {
      return browser
        .click(AnyoneLiveAtListCollector.listRemoveLink(1))
        .click(AnyoneLiveAtListCollectorRemovePage.yes())
        .click(AnyoneLiveAtListCollectorRemovePage.submit())
        .getUrl().should.eventually.contain(AnyoneLiveAtListCollector.pageName)
        .isExisting(AnyoneLiveAtListCollector.listLabel(1)).should.eventually.be.false;

    });

    it('When the user resubmits the first block and then list is empty, Then they are taken to the add question', function () {
      return browser
        .getUrl().should.eventually.contain(AnyoneLiveAtListCollector.pageName)

        .click(AnyoneLiveAtListCollector.previous())
        .getUrl().should.eventually.contain(AnyoneUsuallyLiveAt.pageName)

        .click(AnyoneUsuallyLiveAt.submit())
        .getUrl().should.eventually.contain(AnyoneLiveAtListCollectorAddPage.pageName);

    });

  });

});
