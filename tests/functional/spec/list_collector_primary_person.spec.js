const helpers = require('../helpers');
const ListCollectorPage = require('../generated_pages/list_collector_primary_person/list-collector.page.js');
const ListCollectorAddPage = require('../generated_pages/list_collector_primary_person/list-collector-add.page.js');
const ListCollectorEditPage = require('../generated_pages/list_collector_primary_person/list-collector-edit.page.js');
const PrimaryPersonListCollectorPage = require('../generated_pages/list_collector_primary_person/primary-person-list-collector.page.js');
const PrimaryPersonListCollectorAddPage = require('../generated_pages/list_collector_primary_person/primary-person-list-collector-add.page.js');
const SummaryPage = require('../generated_pages/list_collector/summary.page.js');
const ThankYouPage = require('../base_pages/thank-you.page.js');


describe('Primary Person List Collector Survey', function() {

  describe('Given the user starts on the \'do you live here\' question', function() {
    before('Load the survey', function () {
      return helpers.openQuestionnaire('test_list_collector_primary_person.json');
    });

    it('When the user says they do not live there, and changes their answer to yes, then the user can\'t navigate to the list collector', function () {
      return browser
        .click(PrimaryPersonListCollectorPage.noLabel())
        .click(PrimaryPersonListCollectorPage.submit())
        .click(PrimaryPersonListCollectorAddPage.previous())
        .click(PrimaryPersonListCollectorPage.yesLabel())
        .click(PrimaryPersonListCollectorPage.submit())
        .url('questionnaire/list-collector')
        .getText(PrimaryPersonListCollectorPage.questionText()).should.eventually.contain('Do you live here');
    });
  });

  describe('Given the user starts on the \'do you live here\' question', function() {
    before('Load the survey', function () {
      return helpers.openQuestionnaire('test_list_collector_primary_person.json');
    });

    it('When the user says that they do live there, then they are shown as the primary person', function () {
      return browser
        .click(PrimaryPersonListCollectorPage.yesLabel())
        .click(PrimaryPersonListCollectorPage.submit())
        .setValue(PrimaryPersonListCollectorAddPage.firstName(), 'Mark')
        .setValue(PrimaryPersonListCollectorAddPage.lastName(), 'Twin')
        .click(PrimaryPersonListCollectorAddPage.submit())
        .getText(ListCollectorPage.listLabel(1)).should.eventually.equal('Mark Twin (You)');
    });

    it('When the user adds another person, they are shown in the summary', function () {
      return browser
        .click(ListCollectorPage.yesLabel())
        .click(ListCollectorPage.submit())
        .setValue(ListCollectorAddPage.firstName(), 'Samuel')
        .setValue(ListCollectorAddPage.lastName(), 'Clemens')
        .click(ListCollectorAddPage.submit())
        .getText(ListCollectorPage.listLabel(2)).should.eventually.equal('Samuel Clemens');
    });

    it('When the user goes back and answers No, the primary person is not shown', function () {
      return browser
        .click(ListCollectorPage.previous())
        .click(PrimaryPersonListCollectorPage.no())
        .click(PrimaryPersonListCollectorPage.submit())
        .getText(ListCollectorPage.listLabel(1)).should.eventually.equal('Samuel Clemens');
    });

    it('When the user adds the primary person again, then the primary person is first in the list', function () {
      return browser
        .click(ListCollectorPage.previous())
        .click(PrimaryPersonListCollectorPage.yes())
        .click(PrimaryPersonListCollectorPage.submit())
        .setValue(PrimaryPersonListCollectorAddPage.firstName(), 'Mark')
        .setValue(PrimaryPersonListCollectorAddPage.lastName(), 'Twin')
        .click(PrimaryPersonListCollectorAddPage.submit())
        .getText(ListCollectorPage.listLabel(1)).should.eventually.equal('Mark Twin (You)');
    });

    it('When the user views the summary, then it does not show the remove link for the primary person', function () {
      return browser
        .isExisting(ListCollectorPage.listRemoveLink(1)).should.eventually.be.false
        .isExisting(ListCollectorPage.listRemoveLink(2)).should.eventually.be.true;
    });

    it('When the user changes the primary person\'s name on the summary, then the name should be updated', function () {
      return browser
        .click(ListCollectorPage.listEditLink(1))
        .setValue(ListCollectorEditPage.firstName(), 'Mark')
        .setValue(ListCollectorEditPage.lastName(), 'Twain')
        .click(ListCollectorEditPage.submit())
        .getText(ListCollectorPage.listLabel(1)).should.eventually.equal('Mark Twain (You)')
        .getText(ListCollectorPage.listLabel(2)).should.eventually.equal('Samuel Clemens');
    });

    it('When the user attempts to submit, then they are shown the confirmation page', function () {
      return browser
        .click(ListCollectorPage.no())
        .click(ListCollectorPage.submit())
        .getText(SummaryPage.questionText()).should.eventually.contain('Check your answers');
    });

    it('When the user submits, then they are allowed to submit the survey', function () {
      return browser
        .click(SummaryPage.submit())
        .getText(ThankYouPage.submissionSuccessfulTitle()).should.eventually.contain('Submission successful');
    });
  });

  describe('Given the user starts on the \'do you live here\' question', function() {
    before('Load the survey', function() {
      return helpers.openQuestionnaire('test_list_collector_primary_person.json');
    });

    it('When the user says they do not live there, then an empty list is displayed', function() {
      return browser
        .click(PrimaryPersonListCollectorPage.no())
        .click(PrimaryPersonListCollectorPage.submit())
        .isExisting(ListCollectorPage.listLabel(1)).should.eventually.be.false;
    });

    it('When the user clicks on the add person button multiple times, then only one person is added', function() {
      return browser
        .click(ListCollectorPage.previous())
        .click(PrimaryPersonListCollectorPage.yes())
        .click(PrimaryPersonListCollectorPage.submit())
        .setValue(PrimaryPersonListCollectorAddPage.firstName(), 'Mark')
        .setValue(PrimaryPersonListCollectorAddPage.lastName(), 'Twain')
        .click(PrimaryPersonListCollectorPage.submit())
        .click(PrimaryPersonListCollectorPage.submit())
        .getText(ListCollectorPage.listLabel(1)).should.eventually.equal('Mark Twain (You)')
        .isExisting(ListCollectorPage.listLabel(2)).should.eventually.be.false;
    });
  });

});
