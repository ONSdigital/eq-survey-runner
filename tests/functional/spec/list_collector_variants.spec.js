const helpers = require('../helpers');
const YouLiveHerePage = require('../generated_pages/list_collector_variants/you-live-here-block.page.js');
const ListCollectorPage = require('../generated_pages/list_collector_variants/list-collector.page.js');
const ListCollectorAddPage = require('../generated_pages/list_collector_variants/list-collector-add.page.js');
const ListCollectorEditPage = require('../generated_pages/list_collector_variants/list-collector-edit.page.js');
const ListCollectorRemovePage = require('../generated_pages/list_collector_variants/list-collector-remove.page.js');
const ConfirmationPage = require('../generated_pages/list_collector_variants/confirmation.page.js');

function checkPeopleInList(peopleExpected) {
  let chain = browser.waitForVisible(ListCollectorPage.listLabel(1)).should.eventually.be.true;

  for (let i=1; i<=peopleExpected.length; i++) {
    chain = chain.then(() => {
      return browser.getText(ListCollectorPage.listLabel(i)).should.eventually.equal(peopleExpected[i-1]);
    });
  }

  return chain;
}

describe('List Collector With Variants', function() {

  describe('Given that a person lives in house', function() {
    before('Load the survey', function() {
      return helpers.openQuestionnaire('test_list_collector_variants.json');
    });

    it('The user is asked questions about whether they live there', function() {
      return browser
        .click(YouLiveHerePage.yes())
        .click(YouLiveHerePage.submit())
        .getText(ListCollectorPage.questionText()).should.eventually.equal('Does anyone else live at 1 Pleasant Lane?');
    });

    it('The user is able to add members of the household', function() {
      return browser
        .click(ListCollectorPage.anyoneElseYes())
        .click(ListCollectorPage.submit())
        .getText(ListCollectorAddPage.questionText()).should.eventually.equal('What is the name of the person?')
        .setValue(ListCollectorAddPage.firstName(), 'Samuel')
        .setValue(ListCollectorAddPage.lastName(), 'Clemens')
        .click(ListCollectorAddPage.submit());
    });

    it('The user can see all household members in the summary', function() {
      const peopleExpected = ['Samuel Clemens'];
      return checkPeopleInList(peopleExpected);
    });

    it('The questionnaire has the correct question text on the change and remove pages', function() {
      return browser
        .click(ListCollectorPage.listEditLink(1))
        .getText(ListCollectorEditPage.questionText()).should.eventually.equal('What is the name of the person?')
        .click(ListCollectorEditPage.previous())
        .click(ListCollectorPage.listRemoveLink(1))
        .getText(ListCollectorRemovePage.questionText()).should.eventually.equal('Are you sure you want to remove this person?')
        .click(ListCollectorRemovePage.previous());
    });

    it('The questionnaire shows the confirmation page when no more people to add', function() {
      return browser
        .click(ListCollectorPage.anyoneElseNo())
        .click(ListCollectorPage.submit())
        .getUrl().should.eventually.contain(ConfirmationPage.pageName);
    });

    it('The questionnaire allows submission', function() {
      return browser
        .click(ConfirmationPage.submit())
        .getUrl().should.eventually.contain('thank-you');
    });

  });

  describe('Given a person does not live in house', function() {
    before('Load the survey', function () {
      return helpers.openQuestionnaire('test_list_collector_variants.json');
    });

    it('The user is asked questions about whether they live there', function() {
      return browser
        .click(YouLiveHerePage.no())
        .click(YouLiveHerePage.submit())
        .getText(ListCollectorPage.questionText()).should.eventually.equal('Does anyone live at 1 Pleasant Lane?');
    });

    it('The user is able to add members of the household', function() {
      return browser
        .click(ListCollectorPage.anyoneElseYes())
        .click(ListCollectorPage.submit())
        .getText(ListCollectorAddPage.questionText()).should.eventually.equal('What is the name of the person who isn\'t you?')
        .setValue(ListCollectorAddPage.firstName(), 'Samuel')
        .setValue(ListCollectorAddPage.lastName(), 'Clemens')
        .click(ListCollectorAddPage.submit());
    });

    it('The user can see all household members in the summary', function() {
      const peopleExpected = ['Samuel Clemens'];
      return checkPeopleInList(peopleExpected);
    });

    it('The questionnaire has the correct question text on the change and remove pages', function() {
      return browser
        .click(ListCollectorPage.listEditLink(1))
        .getText(ListCollectorEditPage.questionText()).should.eventually.equal('What is the name of the person who isn\'t you?')
        .click(ListCollectorEditPage.previous())
        .click(ListCollectorPage.listRemoveLink(1))
        .getText(ListCollectorRemovePage.questionText()).should.eventually.equal('Are you sure you want to remove this person who isn\'t you?')
        .click(ListCollectorRemovePage.previous());
    });

    it('The questionnaire shows the confirmation page when no more people to add', function() {
      return browser
        .click(ListCollectorPage.anyoneElseNo())
        .click(ListCollectorPage.submit())
        .getUrl().should.eventually.contain(ConfirmationPage.pageName);
    });

    it('The questionnaire allows submission', function() {
      return browser
        .click(ConfirmationPage.submit())
        .getUrl().should.eventually.contain('thank-you');
    });

  });
});
