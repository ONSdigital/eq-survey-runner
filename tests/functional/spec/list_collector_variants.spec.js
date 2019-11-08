const YouLiveHerePage = require('../generated_pages/list_collector_variants/you-live-here-block.page.js');
const ListCollectorPage = require('../generated_pages/list_collector_variants/list-collector.page.js');
const ListCollectorAddPage = require('../generated_pages/list_collector_variants/list-collector-add.page.js');
const ListCollectorEditPage = require('../generated_pages/list_collector_variants/list-collector-edit.page.js');
const ListCollectorRemovePage = require('../generated_pages/list_collector_variants/list-collector-remove.page.js');
const ConfirmationPage = require('../generated_pages/list_collector_variants/confirmation.page.js');

describe('List Collector With Variants', function() {
  function checkPeopleInList(peopleExpected) {
    $(ListCollectorPage.listLabel(1)).waitForDisplayed();

    for (let i=1; i<=peopleExpected.length; i++) {
      expect($(ListCollectorPage.listLabel(i)).getText()).to.equal(peopleExpected[i-1]);
    }
  }

  describe('Given that a person lives in house', function() {
    before('Load the survey', function() {
      browser.openQuestionnaire('test_list_collector_variants.json');
    });

    it('The user is asked questions about whether they live there', function() {
        $(YouLiveHerePage.yes()).click();
        $(YouLiveHerePage.submit()).click();
        expect($(ListCollectorPage.questionText()).getText()).to.equal('Does anyone else live at 1 Pleasant Lane?');
    });

    it('The user is able to add members of the household', function() {
        $(ListCollectorPage.anyoneElseYes()).click();
        $(ListCollectorPage.submit()).click();
        expect($(ListCollectorAddPage.questionText()).getText()).to.equal('What is the name of the person?');
        $(ListCollectorAddPage.firstName()).setValue('Samuel');
        $(ListCollectorAddPage.lastName()).setValue('Clemens');
        $(ListCollectorAddPage.submit()).click();
    });

    it('The user can see all household members in the summary', function() {
      const peopleExpected = ['Samuel Clemens'];
      checkPeopleInList(peopleExpected);
    });

    it('The questionnaire has the correct question text on the change and remove pages', function() {
        $(ListCollectorPage.listEditLink(1)).click();
        expect($(ListCollectorEditPage.questionText()).getText()).to.equal('What is the name of the person?');
        $(ListCollectorEditPage.previous()).click();
        $(ListCollectorPage.listRemoveLink(1)).click();
        expect($(ListCollectorRemovePage.questionText()).getText()).to.equal('Are you sure you want to remove this person?');
        $(ListCollectorRemovePage.previous()).click();
    });

    it('The questionnaire shows the confirmation page when no more people to add', function() {
        $(ListCollectorPage.anyoneElseNo()).click();
        $(ListCollectorPage.submit()).click();
        expect(browser.getUrl()).to.contain(ConfirmationPage.pageName);
    });

    it('The questionnaire allows submission', function() {
        $(ConfirmationPage.submit()).click();
        expect(browser.getUrl()).to.contain('thank-you');
    });

  });

  describe('Given a person does not live in house', function() {
    before('Load the survey', function () {
      browser.openQuestionnaire('test_list_collector_variants.json');
    });

    it('The user is asked questions about whether they live there', function() {
      $(YouLiveHerePage.no()).click();
      $(YouLiveHerePage.submit()).click();
      expect($(ListCollectorPage.questionText()).getText()).to.equal('Does anyone live at 1 Pleasant Lane?');
    });

    it('The user is able to add members of the household', function() {
      $(ListCollectorPage.anyoneElseYes()).click();
      $(ListCollectorPage.submit()).click();
      expect($(ListCollectorAddPage.questionText()).getText()).to.equal('What is the name of the person who isn’t you?');
      $(ListCollectorAddPage.firstName()).setValue('Samuel');
      $(ListCollectorAddPage.lastName()).setValue('Clemens');
      $(ListCollectorAddPage.submit()).click();
    });

    it('The user can see all household members in the summary', function() {
      const peopleExpected = ['Samuel Clemens'];
      checkPeopleInList(peopleExpected);
    });

    it('The questionnaire has the correct question text on the change and remove pages', function() {
      $(ListCollectorPage.listEditLink(1)).click();
      expect($(ListCollectorEditPage.questionText()).getText()).to.equal('What is the name of the person who isn’t you?');
      $(ListCollectorEditPage.previous()).click();
      $(ListCollectorPage.listRemoveLink(1)).click();
      expect($(ListCollectorRemovePage.questionText()).getText()).to.equal('Are you sure you want to remove this person who isn’t you?');
      $(ListCollectorRemovePage.previous()).click();
    });

    it('The questionnaire shows the confirmation page when no more people to add', function() {
      $(ListCollectorPage.anyoneElseNo()).click();
      $(ListCollectorPage.submit()).click();
      expect(browser.getUrl()).to.contain(ConfirmationPage.pageName);
    });

    it('The questionnaire allows submission', function() {
      $(ConfirmationPage.submit()).click();
      expect(browser.getUrl()).to.contain('thank-you');
    });
  });
});
