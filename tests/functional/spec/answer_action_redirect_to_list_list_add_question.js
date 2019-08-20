const helpers = require('../helpers');
const ListCollectorPage = require('../generated_pages/answer_action_redirect_to_list_add_question/list-collector.page');
const ListCollectorAddPage = require('../generated_pages/answer_action_redirect_to_list_add_question/list-collector-add.page');
const ListCollectorRemovePage = require('../generated_pages/answer_action_redirect_to_list_add_question/list-collector-remove.page');
const AnyoneElseLiveHereBlock = require('../generated_pages/answer_action_redirect_to_list_add_question/anyone-else-live-here-block.page');

function checkPeopleInList(peopleExpected) {
  let chain = browser.waitForVisible(ListCollectorPage.listLabel(1)).should.eventually.be.true;

  for (let i = 1; i <= peopleExpected.length; i++) {
    chain = chain.then(() => {
      return browser.getText(ListCollectorPage.listLabel(i)).should.eventually.equal(peopleExpected[i - 1]);
    });
  }

  return chain;
}

describe('Answer Action: Redirect To List Add Question', function () {

  describe('Given the user is on a question with a "RedirectToListAddQuestion" action enabled', function () {

    before('Launch survey', function () {
      return helpers.openQuestionnaire('test_answer_action_redirect_to_list_add_question.json');
    });

    it('When the user answers "No", Then, they should be taken to straight the list collector add question.', function () {
      return browser
        .click(AnyoneElseLiveHereBlock.no())
        .click(AnyoneElseLiveHereBlock.submit())
        .getUrl().should.eventually.contain(ListCollectorPage.pageName);
    });

    it('When the user answers "Yes" then they should be taken to the list collector add question.', function () {
      return browser
        .url(AnyoneElseLiveHereBlock.url())
        .click(AnyoneElseLiveHereBlock.yes())
        .click(AnyoneElseLiveHereBlock.submit())
        .getUrl().should.eventually.contain(ListCollectorAddPage.pageName)
        .getUrl().should.eventually.contain('?return_to=anyone-else-live-here-block');
    });

    it('When the user clicks the "Previous" link from the add question then they should be taken to the block they came from, not the list collector', function () {
      return browser
        .click(ListCollectorAddPage.previous())
        .getUrl().should.eventually.contain(AnyoneElseLiveHereBlock.pageName);
    });

    it('When the user adds a household member, Then, they are taken to the list collector', function () {
      return browser
        .click(AnyoneElseLiveHereBlock.submit())
        .setValue(ListCollectorAddPage.firstName(), 'Marcus')
        .setValue(ListCollectorAddPage.lastName(), 'Twin')
        .click(ListCollectorAddPage.submit())
        .getUrl().should.eventually.contain(ListCollectorPage.pageName);
    });

    it('The list collector shows the household members in the list summary', function () {
      const peopleExpected = ['Marcus Twin'];
      return checkPeopleInList(peopleExpected);
    });

    it('When the user adds another household member, Then, the list collector displays two household members', function () {
      return browser
        .click(ListCollectorPage.yes())
        .click(ListCollectorPage.submit())
        .setValue(ListCollectorAddPage.firstName(), 'Clara')
        .setValue(ListCollectorAddPage.lastName(), 'Clemens')
        .click(ListCollectorAddPage.submit())
        .getUrl().should.eventually.contain(ListCollectorPage.pageName);
    });

    it('The list collector shows the household members in the list summary', function () {
      const peopleExpected = ['Marcus Twin', 'Clara Clemens'];
      return checkPeopleInList(peopleExpected);
    });

    it('When the users removes the only person (Mark Twain), Then, they are shown an empty list collector', function () {
      return browser
        .click(ListCollectorPage.listRemoveLink(1))
        .click(ListCollectorRemovePage.yes())
        .click(ListCollectorRemovePage.submit())
        .getUrl().should.eventually.contain(ListCollectorPage.pageName)
        .getText(ListCollectorPage.listLabel(1)).should.not.eventually.have.string('Mark Twain');

    });

    it('When the user click the "Previous" link from the list collector, Then, they are taken to the last complete block', function () {
      return browser
        .click(ListCollectorPage.previous())
        .getUrl().should.eventually.contain(AnyoneElseLiveHereBlock.pageName);

    });

    it('When the user resubmits the first block and then list is not empty, Then they are taken to the list collector', function () {
      return browser
        .click(AnyoneElseLiveHereBlock.submit())
        .getUrl().should.eventually.contain(ListCollectorPage.pageName);

    });

    it('When the user resubmits the first block and then list is empty, Then they are taken to the add question', function () {
      return browser
        .click(ListCollectorPage.listRemoveLink(1))
        .click(ListCollectorRemovePage.yes())
        .click(ListCollectorRemovePage.submit())

        .getUrl().should.eventually.contain(ListCollectorPage.pageName)

        .click(ListCollectorPage.previous())
        .getUrl().should.eventually.contain(AnyoneElseLiveHereBlock.pageName)

        .click(AnyoneElseLiveHereBlock.submit())
        .getUrl().should.eventually.contain(ListCollectorAddPage.pageName);

    });

  });

});
