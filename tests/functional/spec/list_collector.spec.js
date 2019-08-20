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

const PrimaryPersonListCollectorPage = require('../generated_pages/list_collector_section_summary/primary-person-list-collector.page.js');
const PrimaryPersonListCollectorAddPage = require('../generated_pages/list_collector_section_summary/primary-person-list-collector-add.page.js');
const SectionSummaryListCollectorPage = require('../generated_pages/list_collector_section_summary/list-collector.page.js');
const SectionSummaryListCollectorAddPage = require('../generated_pages/list_collector_section_summary/list-collector-add.page.js');
const SectionSummaryListCollectorEditPage = require('../generated_pages/list_collector_section_summary/list-collector-edit.page.js');
const SectionSummaryListCollectorRemovePage = require('../generated_pages/list_collector_section_summary/list-collector-remove.page.js');
const VisitorListCollectorPage = require('../generated_pages/list_collector_section_summary/visitor-list-collector.page.js');
const VisitorListCollectorAddPage = require('../generated_pages/list_collector_section_summary/visitor-list-collector-add.page.js');
const VisitorListCollectorEditPage = require('../generated_pages/list_collector_section_summary/visitor-list-collector-edit.page.js');
const VisitorListCollectorRemovePage = require('../generated_pages/list_collector_section_summary/visitor-list-collector-remove.page.js');
const PeopleListSectionSummaryPage = require('../generated_pages/list_collector_section_summary/people-list-section-summary.page.js');

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

  describe.only('Given I start a list collector survey and complete to Section Summary', function() {

    beforeEach(function() {
      return helpers.openQuestionnaire('test_list_collector_section_summary.json').then(() => {
        return browser
            .click(PrimaryPersonListCollectorPage.yes())
            .click(PrimaryPersonListCollectorPage.submit())
            .setValue(PrimaryPersonListCollectorAddPage.firstName(), 'Marcus')
            .setValue(PrimaryPersonListCollectorAddPage.lastName(), 'Twin')
            .click(PrimaryPersonListCollectorAddPage.submit())
            .click(ListCollectorPage.yes())
            .click(ListCollectorPage.submit())
            .setValue(ListCollectorAddPage.firstName(), 'Samuel')
            .setValue(ListCollectorAddPage.lastName(), 'Clemens')
            .click(ListCollectorAddPage.submit())
            .click(ListCollectorPage.no())
            .click(ListCollectorPage.submit())
            .click(VisitorListCollectorPage.yes())
            .click(VisitorListCollectorPage.submit())
            .setValue(VisitorListCollectorAddPage.firstNameVisitor(), 'Olivia')
            .setValue(VisitorListCollectorAddPage.lastNameVisitor(), 'Clemens')
            .click(VisitorListCollectorAddPage.submit())
            .click(VisitorListCollectorPage.no())
            .click(VisitorListCollectorPage.submit());
        });
    });

    it('The section summary should display contents of the list collector', function() {
      return browser
        .getText(PeopleListSectionSummaryPage.peopleListLabel(1)).should.eventually.contain('Marcus Twin (You)')
        .getText(PeopleListSectionSummaryPage.peopleListLabel(2)).should.eventually.contain('Samuel Clemens')
        .getText(PeopleListSectionSummaryPage.visitorsListLabel(1)).should.eventually.contain('Olivia Clemens');
    });

    it('When the user adds an item to the list, They should return to the section summary and it should display the updated list', function() {
      return browser
        .click(PeopleListSectionSummaryPage.visitorsListAddLink(1))
        .setValue(VisitorListCollectorAddPage.firstNameVisitor(), 'Joe')
        .setValue(VisitorListCollectorAddPage.lastNameVisitor(), 'Bloggs')
        .click(VisitorListCollectorAddPage.submit())
        .click(VisitorListCollectorPage.no())
        .click(VisitorListCollectorPage.submit())
        .getText(PeopleListSectionSummaryPage.visitorsListLabel(2)).should.eventually.contain('Joe Bloggs');
    });

    it('When the user removes an item from the list, They should return to the section summary and it should display the updated list', function() {
      return browser
        .click(PeopleListSectionSummaryPage.peopleListRemoveLink(2))
        .click(ListCollectorRemovePage.yes())
        .click(ListCollectorRemovePage.submit())
        .click(ListCollectorPage.no())
        .click(ListCollectorPage.submit())
        .isExisting(PeopleListSectionSummaryPage.visitorsListLabel(2)).should.eventually.equal(false);
    });

    it('When the user updates the list, They should return to the section summary and it should display the updated list', function() {
      return browser
        .click(PeopleListSectionSummaryPage.peopleListEditLink(1))
        .setValue(PrimaryPersonListCollectorAddPage.firstName(), 'Mark')
        .setValue(PrimaryPersonListCollectorAddPage.lastName(), 'Twain')
        .click(PrimaryPersonListCollectorAddPage.submit())
        .click(ListCollectorPage.no())
        .click(ListCollectorPage.submit())
        .getText(PeopleListSectionSummaryPage.peopleListLabel(1)).should.eventually.contain('Mark Twain (You)');
    });
  });
});
