const ListCollectorPage = require('../generated_pages/list_collector_primary_person/list-collector.page.js');
const ListCollectorAddPage = require('../generated_pages/list_collector_primary_person/list-collector-add.page.js');
const ListCollectorEditPage = require('../generated_pages/list_collector_primary_person/list-collector-edit.page.js');
const PrimaryPersonListCollectorPage = require('../generated_pages/list_collector_primary_person/primary-person-list-collector.page.js');
const PrimaryPersonListCollectorAddPage = require('../generated_pages/list_collector_primary_person/primary-person-list-collector-add.page.js');
const SectionSummaryPage = require('../generated_pages/list_collector/group-summary.page.js');
const ConfirmationPage = require('../generated_pages/list_collector/confirmation.page.js');
const ThankYouPage = require('../base_pages/thank-you.page.js');
const AnyoneUsuallyLiveAtPage = require('../generated_pages/list_collector_primary_person/anyone-usually-live-at.page.js');


describe('Primary Person List Collector Survey', function() {
  describe('Given the user starts on the \'do you live here\' question', function() {
    before('Load the survey', function () {
      browser.openQuestionnaire('test_list_collector_primary_person.json');
    });

    it.skip('When the user says they do not live there, and changes their answer to yes, then the user can\'t navigate to the list collector', function () {
      $(PrimaryPersonListCollectorPage.noLabel()).click();
      $(PrimaryPersonListCollectorPage.submit()).click();
      $(PrimaryPersonListCollectorAddPage.previous()).click();
      $(PrimaryPersonListCollectorPage.yesLabel()).click();
      $(PrimaryPersonListCollectorPage.submit()).click();
      browser.url('questionnaire/list-collector');
      expect($(PrimaryPersonListCollectorPage.questionText()).getText()).to.contain('Do you live here');
    });
  });

  describe('Given the user starts on the \'do you live here\' question', function() {
    before('Load the survey', function () {
      browser.openQuestionnaire('test_list_collector_primary_person.json');
    });

    it('When the user says that they do live there, then they are shown as the primary person', function () {
      $(PrimaryPersonListCollectorPage.yesLabel()).click();
      $(PrimaryPersonListCollectorPage.submit()).click();
      $(PrimaryPersonListCollectorAddPage.firstName()).setValue('Mark');
      $(PrimaryPersonListCollectorAddPage.lastName()).setValue('Twin');
      $(PrimaryPersonListCollectorAddPage.submit()).click();
      expect($(ListCollectorPage.listLabel(1)).getText()).to.equal('Mark Twin (You)');
    });

    it('When the user adds another person, they are shown in the summary', function () {
      $(ListCollectorPage.yesLabel()).click();
      $(ListCollectorPage.submit()).click();
      $(ListCollectorAddPage.firstName()).setValue('Samuel');
      $(ListCollectorAddPage.lastName()).setValue('Clemens');
      $(ListCollectorAddPage.submit()).click();
      expect($(ListCollectorPage.listLabel(2)).getText()).to.equal('Samuel Clemens');
    });

    it('When the user goes back and answers No, the primary person is not shown', function () {
      $(ListCollectorPage.previous()).click();
      $(PrimaryPersonListCollectorPage.no()).click();
      $(PrimaryPersonListCollectorPage.submit()).click();
      $(AnyoneUsuallyLiveAtPage.no()).click();
      $(AnyoneUsuallyLiveAtPage.submit()).click();
      expect($(ListCollectorPage.listLabel(1)).getText()).to.equal('Samuel Clemens');
    });

    it('When the user adds the primary person again, then the primary person is first in the list', function () {
      $(ListCollectorPage.previous()).click();
      $(AnyoneUsuallyLiveAtPage.previous()).click();
      $(PrimaryPersonListCollectorPage.yes()).click();
      $(PrimaryPersonListCollectorPage.submit()).click();
      $(PrimaryPersonListCollectorAddPage.firstName()).setValue('Mark');
      $(PrimaryPersonListCollectorAddPage.lastName()).setValue('Twin');
      $(PrimaryPersonListCollectorAddPage.submit()).click();
      expect($(ListCollectorPage.listLabel(1)).getText()).to.equal('Mark Twin (You)');
    });

    it('When the user views the summary, then it does not show the remove link for the primary person', function () {
      expect($(ListCollectorPage.listRemoveLink(1)).isExisting()).to.be.false;
      expect($(ListCollectorPage.listRemoveLink(2)).isExisting()).to.be.true;
    });


    it('When the user changes the primary person\'s name on the summary, then the name should be updated', function () {
      $(ListCollectorPage.listEditLink(1)).click();
      $(ListCollectorEditPage.firstName()).setValue('Mark');
      $(ListCollectorEditPage.lastName()).setValue('Twain');
      $(ListCollectorEditPage.submit()).click();
      expect($(ListCollectorPage.listLabel(1)).getText()).to.equal('Mark Twain (You)');
      expect($(ListCollectorPage.listLabel(2)).getText()).to.equal('Samuel Clemens');
    });

    it('When the user views the summary, then it does not show the does anyone usually live here question', function () {
      $(ListCollectorPage.no()).click();
      $(ListCollectorPage.submit()).click();
      expect($('body').getText()).to.not.equal('usually live here');
    });

    it('When the user attempts to submit, then they are shown the confirmation page', function () {
      $(SectionSummaryPage.submit()).click();
      expect($('body').getText()).to.contain('Thank you for your answers, do you wish to submit');
    });

    it('When the user submits, then they are allowed to submit the survey', function () {
      $(ConfirmationPage.submit()).click();
      expect($(ThankYouPage.questionText()).getText()).to.contain('Thank you for submitting your census');
    });
  });

  describe('Given the user starts on the \'do you live here\' question', function() {
    before('Load the survey', function() {
      browser.openQuestionnaire('test_list_collector_primary_person.json');
    });

    it('When the user says they do not live there, then an empty list is displayed', function() {
      $(PrimaryPersonListCollectorPage.no()).click();
      $(PrimaryPersonListCollectorPage.submit()).click();
      expect($(ListCollectorPage.listLabel(1)).isExisting()).to.be.false;
    });

    it('When the user clicks on the add person button multiple times, then only one person is added', function() {
      $(ListCollectorPage.previous()).click();
      $(PrimaryPersonListCollectorPage.yes()).click();
      $(PrimaryPersonListCollectorPage.submit()).click();
      $(PrimaryPersonListCollectorAddPage.firstName()).setValue('Mark');
      $(PrimaryPersonListCollectorAddPage.lastName()).setValue('Twain');
      $(PrimaryPersonListCollectorPage.submit()).click();
      $(PrimaryPersonListCollectorPage.submit()).click();
      expect($(ListCollectorPage.listLabel(1)).getText()).to.equal('Mark Twain (You)');
      expect($(ListCollectorPage.listLabel(2)).isExisting()).to.be.false;
    });
  });

});
