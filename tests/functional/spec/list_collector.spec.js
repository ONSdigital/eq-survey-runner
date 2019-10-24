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
const SummaryPage = require('../generated_pages/list_collector/group-summary.page.js');

const PrimaryPersonListCollectorPage = require('../generated_pages/list_collector_section_summary/primary-person-list-collector.page.js');
const PrimaryPersonListCollectorAddPage = require('../generated_pages/list_collector_section_summary/primary-person-list-collector-add.page.js');
const SectionSummaryListCollectorPage = require('../generated_pages/list_collector_section_summary/list-collector.page.js');
const SectionSummaryListCollectorAddPage = require('../generated_pages/list_collector_section_summary/list-collector-add.page.js');
const SectionSummaryListCollectorEditPage = require('../generated_pages/list_collector_section_summary/list-collector-edit.page.js');
const SectionSummaryListCollectorRemovePage = require('../generated_pages/list_collector_section_summary/list-collector-remove.page.js');
const VisitorListCollectorPage = require('../generated_pages/list_collector_section_summary/visitor-list-collector.page.js');
const VisitorListCollectorAddPage = require('../generated_pages/list_collector_section_summary/visitor-list-collector-add.page.js');
const PeopleListSectionSummaryPage = require('../generated_pages/list_collector_section_summary/people-list-section-summary.page.js');
const ConfirmationPage = require('../generated_pages/list_collector/confirmation.page.js');





describe('List Collector', function() {
  let browser;

  function checkPeopleInList(peopleExpected) {
    $(ListCollectorPage.listLabel(1)).waitForDisplayed();

    for (let i=1; i<=peopleExpected.length; i++) {
        expect($(ListCollectorPage.listLabel(i)).getText()).to.equal(peopleExpected[i-1]);
    }
  }

  describe('Given a normal journey through the list collector without variants', function() {
    before('Load the survey', function() {
      helpers.openQuestionnaire('test_list_collector.json').then(openBrowser => browser = openBrowser);
    });

    it('The user is able to add members of the household', function() {
      $(ListCollectorPage.yes()).click();
      $(ListCollectorPage.submit()).click();
      $(ListCollectorAddPage.firstName()).setValue('Marcus');
      $(ListCollectorAddPage.lastName()).setValue('Twin');
      $(ListCollectorAddPage.submit()).click();
      $(ListCollectorPage.yes()).click();
      $(ListCollectorPage.submit()).click();
      $(ListCollectorAddPage.firstName()).setValue('Samuel');
      $(ListCollectorAddPage.lastName()).setValue('Clemens');
      $(ListCollectorAddPage.submit()).click();
      $(ListCollectorPage.yes()).click();
      $(ListCollectorPage.submit()).click();
      $(ListCollectorAddPage.firstName()).setValue('Olivia');
      $(ListCollectorAddPage.lastName()).setValue('Clemens');
      $(ListCollectorAddPage.submit()).click();
      $(ListCollectorPage.yes()).click();
      $(ListCollectorPage.submit()).click();
      $(ListCollectorAddPage.firstName()).setValue('Suzy');
      $(ListCollectorAddPage.lastName()).setValue('Clemens');
      $(ListCollectorAddPage.submit()).click();
    });

    it('The collector shows all of the household members in the summary', function() {
      const peopleExpected = ['Marcus Twin', 'Samuel Clemens', 'Olivia Clemens', 'Suzy Clemens'];
      checkPeopleInList(peopleExpected);
    });

    it('The questionnaire allows the name of a person to be changed', function() {
      $(ListCollectorPage.listEditLink(1)).click();
      $(ListCollectorEditPage.firstName()).setValue('Mark');
      $(ListCollectorEditPage.lastName()).setValue('Twain');
      $(ListCollectorEditPage.submit()).click();
      expect($(ListCollectorPage.listLabel(1)).getText()).to.equal('Mark Twain');
    });

    it('The questionnaire allows me to remove the first person (Mark Twain) from the summary', function() {
      $(ListCollectorPage.listRemoveLink(1)).click();
      $(ListCollectorRemovePage.yes()).click();
      $(ListCollectorRemovePage.submit()).click();
    });

    it('The collector summary does not show Mark Twain anymore.', function() {
      expect($(ListCollectorPage.listLabel(1)).getText()).to.not.have.string('Mark Twain');
      expect($(ListCollectorPage.listLabel(3)).getText()).to.equal('Suzy Clemens');
    });

    it('The questionnaire allows more people to be added', function() {
      $(ListCollectorPage.yes()).click();
      $(ListCollectorPage.submit()).click();
      expect($(ListCollectorAddPage.questionText()).getText()).to.contain('What is the name of the person');
      $(ListCollectorAddPage.firstName()).setValue('Clara');
      $(ListCollectorAddPage.lastName()).setValue('Clemens');
      $(ListCollectorAddPage.submit()).click();
      $(ListCollectorPage.yes()).click();
      $(ListCollectorPage.submit()).click();
      $(ListCollectorAddPage.firstName()).setValue('Jean');
      $(ListCollectorAddPage.lastName()).setValue('Clemens');
      $(ListCollectorAddPage.submit()).click();
    });

    it('The collector shows everyone on the summary', function() {
      const peopleExpected = ['Samuel Clemens', 'Olivia Clemens', 'Suzy Clemens', 'Clara Clemens', 'Jean Clemens'];

      checkPeopleInList(peopleExpected);
    });

    it('When No is answered on the list collector the user sees an interstitial', function() {
      $(ListCollectorPage.no()).click();
      $(ListCollectorPage.submit()).click();
      expect(browser.getUrl()).to.contain(NextInterstitialPage.pageName);
      $(NextInterstitialPage.submit()).click();
    });

    it('After the interstitial, the user should be on the second list collector page', function() {
        expect(browser.getUrl()).to.contain(AnotherListCollectorPage.pageName);
    });

    it('The collector still shows the same list of people on the summary', function() {
      const peopleExpected = ['Samuel Clemens', 'Olivia Clemens', 'Suzy Clemens', 'Clara Clemens', 'Jean Clemens'];
      checkPeopleInList(peopleExpected);
    });

    it('The collector allows the user to add another person to the same list', function() {
      $(AnotherListCollectorPage.yes()).click();
      $(AnotherListCollectorPage.submit()).click();
      $(AnotherListCollectorAddPage.firstName()).setValue('Someone');
      $(AnotherListCollectorAddPage.lastName()).setValue('Else');
      $(AnotherListCollectorAddPage.submit()).click();
      expect($(AnotherListCollectorPage.listLabel(6)).getText()).to.equal('Someone Else');
    });

    it('The collector allows the user to remove a person again', function() {
      $(AnotherListCollectorPage.listRemoveLink(6)).click();
      $(AnotherListCollectorRemovePage.yes()).click();
      $(AnotherListCollectorRemovePage.submit()).click();
    });

    it('The user is redirected to the summary when the user visits a non-existant list item id', function() {
        browser.url('/questionnaire/people/somerandomid/another-edit-person');
        expect(browser.getUrl()).to.contain(AnotherListCollectorPage.pageName);
    });

    it('The user is returned to the list collector when the previous link is clicked.', function() {
      $(AnotherListCollectorPage.listRemoveLink(1)).click();
      $(AnotherListCollectorRemovePage.previous()).click();
      expect(browser.getUrl()).to.contain(AnotherListCollectorPage.pageName);
      $(AnotherListCollectorPage.listEditLink(1)).click();
      $(AnotherListCollectorEditPage.previous()).click();
      expect(browser.getUrl()).to.contain(AnotherListCollectorPage.pageName);
      $(AnotherListCollectorPage.yes()).click();
      $(AnotherListCollectorPage.submit()).click();
      $(AnotherListCollectorEditPage.previous()).click();
      expect(browser.getUrl()).to.contain(AnotherListCollectorPage.pageName);
    });

    it('The questionnaire shows the confirmation page when no more people to add', function() {
      $(AnotherListCollectorPage.no()).click();
      $(AnotherListCollectorPage.submit()).click();
      expect(browser.getUrl()).to.contain(SummaryPage.pageName);
    });

    it('The questionnaire allows submission', function() {
      $(SummaryPage.submit()).click();
      $(ConfirmationPage.submit()).click();
      expect(browser.getUrl()).to.contain('thank-you');
    });
  });

  describe('Given I start a list collector survey and complete to Section Summary', function() {

    beforeEach(function() {
      browser = helpers.openQuestionnaire('test_list_collector_section_summary.json');
      $(PrimaryPersonListCollectorPage.yes()).click();
      $(PrimaryPersonListCollectorPage.submit()).click();
      $(PrimaryPersonListCollectorAddPage.firstName()).setValue('Marcus');
      $(PrimaryPersonListCollectorAddPage.lastName()).setValue('Twin');
      $(PrimaryPersonListCollectorAddPage.submit()).click();
      $(SectionSummaryListCollectorPage.yes()).click();
      $(SectionSummaryListCollectorPage.submit()).click();
      $(SectionSummaryListCollectorAddPage.firstName()).setValue('Samuel');
      $(SectionSummaryListCollectorAddPage.lastName()).setValue('Clemens');
      $(SectionSummaryListCollectorAddPage.submit()).click();
      $(SectionSummaryListCollectorPage.no()).click();
      $(SectionSummaryListCollectorPage.submit()).click();
      $(VisitorListCollectorPage.yes()).click();
      $(VisitorListCollectorPage.submit()).click();
      $(VisitorListCollectorAddPage.firstNameVisitor()).setValue('Olivia');
      $(VisitorListCollectorAddPage.lastNameVisitor()).setValue('Clemens');
      $(VisitorListCollectorAddPage.submit()).click();
      $(VisitorListCollectorPage.no()).click();
      $(VisitorListCollectorPage.submit()).click();
    });

    it('The section summary should display contents of the list collector', function() {
      expect($(PeopleListSectionSummaryPage.peopleListLabel(1)).getText()).to.contain('Marcus Twin (You)');
      expect($(PeopleListSectionSummaryPage.peopleListLabel(2)).getText()).to.contain('Samuel Clemens');
      expect($(PeopleListSectionSummaryPage.visitorsListLabel(1)).getText()).to.contain('Olivia Clemens');
    });

    it('When the user adds an item to the list, They should return to the section summary and it should display the updated list', function() {
      $(PeopleListSectionSummaryPage.visitorsListAddLink(1)).click();
      $(VisitorListCollectorAddPage.firstNameVisitor()).setValue('Joe');
      $(VisitorListCollectorAddPage.lastNameVisitor()).setValue('Bloggs');
      $(VisitorListCollectorAddPage.submit()).click();
      expect($(PeopleListSectionSummaryPage.visitorsListLabel(2)).getText()).to.contain('Joe Bloggs');
    });

    it('When the user removes an item from the list, They should return to the section summary and it should display the updated list', function() {
      $(PeopleListSectionSummaryPage.peopleListRemoveLink(2)).click();
      $(SectionSummaryListCollectorRemovePage.yes()).click();
      $(SectionSummaryListCollectorRemovePage.submit()).click();
      expect($(PeopleListSectionSummaryPage.visitorsListLabel(2)).isExisting()).to.equal(false);
    });

    it('When the user updates the list, They should return to the section summary and it should display the updated list', function() {
      $(PeopleListSectionSummaryPage.peopleListEditLink(1)).click();
      $(SectionSummaryListCollectorEditPage.firstName()).setValue('Mark');
      $(SectionSummaryListCollectorEditPage.lastName()).setValue('Twain');
      $(SectionSummaryListCollectorEditPage.submit()).click();
      expect($(PeopleListSectionSummaryPage.peopleListLabel(1)).getText()).to.contain('Mark Twain (You)');
    });
  });
});
