const helpers = require('../helpers');
const AnotherListCollectorPage = require('../generated_pages/list_collector/another-list-collector-block.page.js');
const AnotherListCollectorAddPage = require('../generated_pages/list_collector/another-list-collector-block-add.page.js');
const AnotherListCollectorEditPage = require('../generated_pages/list_collector/another-list-collector-block-edit.page.js');
const AnotherListCollectorRemovePage = require('../generated_pages/list_collector/another-list-collector-block-remove.page.js');
const ListCollectorPage = require('../generated_pages/list_collector/list-collector.page.js');
const ListCollectorAddPage = require('../generated_pages/list_collector/list-collector-add.page.js');
const ListCollectorEditPage = require('../generated_pages/list_collector/list-collector-edit.page.js');
const ListCollectorRemovePage = require('../generated_pages/list_collector/list-collector-remove.page.js');
const NextInterstitialPage = require('../generated_pages/list_collector/next-interstitial.page.js');
const SummaryPage = require('../generated_pages/list_collector/summary.page.js');

function checkPeopleInList(peopleExpected) {
  let chain = browser.waitForVisible(ListCollectorPage.listLabel(1)).should.eventually.be.true;

  for (let i=1; i<=peopleExpected.length; i++) {
    chain = chain.then(() => {
      return browser.getText(ListCollectorPage.listLabel(i)).should.eventually.equal(peopleExpected[i-1]);
    });
  }

  return chain;
}

describe('List Collector', function() {

  describe('Given a normal journey through the list collector without variants', function() {
    before('Load the survey', function() {
      return helpers.openQuestionnaire('test_list_collector.json');
    });

    it('The user is able to add members of the household', function() {
      return browser
        .click(ListCollectorPage.yes())
        .click(ListCollectorPage.submit())
        .setValue(ListCollectorAddPage.firstName(), 'Marcus')
        .setValue(ListCollectorAddPage.lastName(), 'Twin')
        .click(ListCollectorAddPage.submit())
        .click(ListCollectorPage.yes())
        .click(ListCollectorPage.submit())
        .setValue(ListCollectorAddPage.firstName(), 'Samuel')
        .setValue(ListCollectorAddPage.lastName(), 'Clemens')
        .click(ListCollectorAddPage.submit())
        .click(ListCollectorPage.yes())
        .click(ListCollectorPage.submit())
        .setValue(ListCollectorAddPage.firstName(), 'Olivia')
        .setValue(ListCollectorAddPage.lastName(), 'Clemens')
        .click(ListCollectorAddPage.submit())
        .click(ListCollectorPage.yes())
        .click(ListCollectorPage.submit())
        .setValue(ListCollectorAddPage.firstName(), 'Suzy')
        .setValue(ListCollectorAddPage.lastName(), 'Clemens')
        .click(ListCollectorAddPage.submit());
    });

    it('The collector shows all of the household members in the summary', function() {
      const peopleExpected = ['Marcus Twin', 'Samuel Clemens', 'Olivia Clemens', 'Suzy Clemens'];
      return checkPeopleInList(peopleExpected);
    });

    it('The questionnaire allows the name of a person to be changed', function() {
      return browser
        .click(ListCollectorPage.listEditLink(1))
        .setValue(ListCollectorEditPage.firstName(), 'Mark')
        .setValue(ListCollectorEditPage.lastName(), 'Twain')
        .click(ListCollectorEditPage.submit())
        .getText(ListCollectorPage.listLabel(1)).should.eventually.equal('Mark Twain');
    });

    it('The questionnaire allows me to remove the first person (Mark Twain) from the summary', function() {
      return browser
        .click(ListCollectorPage.listRemoveLink(1))
        .click(ListCollectorRemovePage.yes())
        .click(ListCollectorRemovePage.submit());
    });

    it('The collector summary does not show Mark Twain anymore.', function() {
      return browser
        .getText(ListCollectorPage.listLabel(1)).should.not.eventually.have.string('Mark Twain')
        .getText(ListCollectorPage.listLabel(3)).should.eventually.equal('Suzy Clemens');
    });

    it('The questionnaire allows more people to be added', function() {
      return browser
        .click(ListCollectorPage.yes())
        .click(ListCollectorPage.submit())
        .getText(ListCollectorAddPage.questionText()).should.eventually.contain('What is the name of the person')
        .setValue(ListCollectorAddPage.firstName(), 'Clara')
        .setValue(ListCollectorAddPage.lastName(), 'Clemens')
        .click(ListCollectorAddPage.submit())
        .click(ListCollectorPage.yes())
        .click(ListCollectorPage.submit())
        .setValue(ListCollectorAddPage.firstName(), 'Jean')
        .setValue(ListCollectorAddPage.lastName(), 'Clemens')
        .click(ListCollectorAddPage.submit());
    });

    it('The collector shows everyone on the summary', function() {
      const peopleExpected = ['Samuel Clemens', 'Olivia Clemens', 'Suzy Clemens', 'Clara Clemens', 'Jean Clemens'];
      return checkPeopleInList(peopleExpected);
    });

    it('When No is answered on the list collector the user sees an interstitial', function() {
      return browser
        .click(ListCollectorPage.no())
        .click(ListCollectorPage.submit())
        .getUrl().should.eventually.contain(NextInterstitialPage.pageName)
        .click(NextInterstitialPage.submit());
    });

    it('After the interstitial, the user should be on the second list collector page', function() {
      return browser
        .getUrl().should.eventually.contain(AnotherListCollectorPage.pageName);
    });

    it('The collector still shows the same list of people on the summary', function() {
      const peopleExpected = ['Samuel Clemens', 'Olivia Clemens', 'Suzy Clemens', 'Clara Clemens', 'Jean Clemens'];
      return checkPeopleInList(peopleExpected);
    });

    it('The collector allows the user to add another person to the same list', function() {
      return browser
        .click(AnotherListCollectorPage.yes())
        .click(AnotherListCollectorPage.submit())
        .setValue(AnotherListCollectorAddPage.firstName(), 'Someone')
        .setValue(AnotherListCollectorAddPage.lastName(), 'Else')
        .click(AnotherListCollectorAddPage.submit())
        .getText(AnotherListCollectorPage.listLabel(6)).should.eventually.equal('Someone Else');
    });

    it('The collector allows the user to remove a person again', function() {
      return browser
        .click(AnotherListCollectorPage.listRemoveLink(6))
        .click(AnotherListCollectorRemovePage.yes())
        .click(AnotherListCollectorRemovePage.submit());
    });

    it('The user is redirected to the summary when the user visits a non-existant list item id', function() {
      return browser
        .url('/questionnaire/people/somerandomid/another-edit-person')
        .getUrl().should.eventually.contain(AnotherListCollectorPage.pageName);
    });

    it('The user is returned to the list collector when the previous link is clicked.', function() {
      return browser
        .click(AnotherListCollectorPage.listRemoveLink(1))
        .click(AnotherListCollectorRemovePage.previous())
        .getUrl().should.eventually.contain(AnotherListCollectorPage.pageName)
        .click(AnotherListCollectorPage.listEditLink(1))
        .click(AnotherListCollectorEditPage.previous())
        .getUrl().should.eventually.contain(AnotherListCollectorPage.pageName)
        .click(AnotherListCollectorPage.yes())
        .click(AnotherListCollectorPage.submit())
        .click(AnotherListCollectorEditPage.previous())
        .getUrl().should.eventually.contain(AnotherListCollectorPage.pageName);
    });

    it('The questionnaire shows the confirmation page when no more people to add', function() {
      return browser
        .click(AnotherListCollectorPage.no())
        .click(AnotherListCollectorPage.submit())
        .getUrl().should.eventually.contain(SummaryPage.pageName);
    });

    it('The questionnaire allows submission', function() {
      return browser
        .click(SummaryPage.submit())
        .getUrl().should.eventually.contain('thank-you');
    });

  });
});
