const helpers = require('../helpers');
const ListCollectorPage = require('../generated_pages/relationships/list-collector.page.js');
const ListCollectorAddPage = require('../generated_pages/relationships/list-collector-add.page.js');
const ListCollectorRemovePage = require('../generated_pages/relationships/list-collector-remove.page.js');
const RelationshipsPage = require('../generated_pages/relationships/relationships.page.js');
const ConfirmationPage = require('../generated_pages/relationships/confirmation.page.js');

describe('Relationships', function() {
  let browser;
  const schema = 'test_relationships.json';

  describe('Given I am completing the test_relationships survey,', function() {
    beforeEach('load the survey', function() {
      helpers.openQuestionnaire(schema).then(openBrowser => browser = openBrowser);
    });


    it('When I have one household member, Then I will be not be asked about relationships', function() {
      $(ListCollectorPage.yes()).click();
      $(ListCollectorPage.submit()).click();
      $(ListCollectorAddPage.firstName()).setValue('Marcus');
      $(ListCollectorAddPage.lastName()).setValue('Twin');
      $(ListCollectorAddPage.submit()).click();
      $(ListCollectorPage.no()).click();
      $(ListCollectorPage.submit()).click();
      expect(browser.getUrl()).to.contain(ConfirmationPage.pageName);
    });

    it('When I add two household members, Then I will be asked about one relationship', function() {
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
      $(ListCollectorPage.no()).click();
      $(ListCollectorPage.submit()).click();
      expect(browser.getUrl()).to.contain(RelationshipsPage.pageName);
      $(RelationshipsPage.husbandOrWife()).click();
      $(RelationshipsPage.submit()).click();
      expect(browser.getUrl()).to.contain(ConfirmationPage.pageName);
    });

    describe('When I add three household members,', function() {
      beforeEach('add three people', function() {
        addThreePeople();
      });

      it('Then I will be asked about all relationships', function() {
        $(ListCollectorPage.no()).click();
        $(ListCollectorPage.submit()).click();
        $(RelationshipsPage.husbandOrWife()).click();
        $(RelationshipsPage.submit()).click();
        $(RelationshipsPage.legallyRegisteredCivilPartner()).click();
        $(RelationshipsPage.submit()).click();
        $(RelationshipsPage.husbandOrWife()).click();
        $(RelationshipsPage.submit()).click();
        expect(browser.getUrl()).to.contain(ConfirmationPage.pageName);
      });

      it('And go to the first relationship, Then the previous link should return to the list collector', function() {
        $(ListCollectorPage.no()).click();
        $(ListCollectorPage.submit()).click();
        $(RelationshipsPage.previous()).click();
        expect(browser.getUrl()).to.contain(ListCollectorPage.pageName);
      });

      it('And go to the first relationship, Then the \'Brother or Sister\' option should have the text \'Including half brother or half sister\'', function() {
        $(ListCollectorPage.no()).click();
        $(ListCollectorPage.submit()).click();
        expect($(RelationshipsPage.brotherOrSisterLabel()).getText()).to.contain('Including half brother or half sister');
      });

      it('And go to the second relationship, Then the previous link should return to the first relationship', function() {
        $(ListCollectorPage.no()).click();
        $(ListCollectorPage.submit()).click();
        $(RelationshipsPage.husbandOrWife()).click();
        $(RelationshipsPage.submit()).click();
        $(RelationshipsPage.previous()).click();
        expect(browser.getUrl()).to.contain(RelationshipsPage.pageName);
        expect($(RelationshipsPage.questionText()).getText()).to.contain('Marcus');
      });

      it('And go to the confirmation page, Then the previous link should return to the last relationship', function() {
        $(ListCollectorPage.no()).click();
        $(ListCollectorPage.submit()).click();
        $(RelationshipsPage.husbandOrWife()).click();
        $(RelationshipsPage.submit()).click();
        $(RelationshipsPage.legallyRegisteredCivilPartner()).click();
        $(RelationshipsPage.submit()).click();
        $(RelationshipsPage.husbandOrWife()).click();
        $(RelationshipsPage.submit()).click();
        expect(browser.getUrl()).to.contain(ConfirmationPage.pageName);
        $(ConfirmationPage.previous()).click();
        expect(browser.getUrl()).to.contain(RelationshipsPage.pageName);
        expect($(RelationshipsPage.questionText()).getText()).to.contain('Olivia');
      });

      it('When I add all relationships and return to the relationships, Then the relationships should be populated', function() {
        $(ListCollectorPage.no()).click();
        $(ListCollectorPage.submit()).click();
        $(RelationshipsPage.husbandOrWife()).click();
        $(RelationshipsPage.submit()).click();
        $(RelationshipsPage.legallyRegisteredCivilPartner()).click();
        $(RelationshipsPage.submit()).click();
        $(RelationshipsPage.husbandOrWife()).click();
        $(RelationshipsPage.submit()).click();
        expect(browser.getUrl()).to.contain(ConfirmationPage.pageName);
        $(ConfirmationPage.previous()).click();
        expect($(RelationshipsPage.husbandOrWife()).isSelected()).to.be.true;
        $(ConfirmationPage.previous()).click();
        expect($(RelationshipsPage.legallyRegisteredCivilPartner()).isSelected()).to.be.true;
        $(ConfirmationPage.previous()).click();
        expect($(RelationshipsPage.husbandOrWife()).isSelected()).to.be.true;
      });

      it('And go to the first relationship, Then the person\'s name should be in the question title and playback text', function() {
        $(ListCollectorPage.no()).click();
        $(ListCollectorPage.submit()).click();
        expect($(ListCollectorPage.questionText()).getText()).to.contain('Marcus Twin');
        expect($(RelationshipsPage.playback()).getText()).to.contain('Marcus Twin');
      });

      it('And go to the first relationship and submit without selecting an option, Then an error should be displayed', function() {
        $(ListCollectorPage.no()).click();
        $(ListCollectorPage.submit()).click();
        $(RelationshipsPage.submit()).click();
        expect($(RelationshipsPage.error()).isDisplayed()).to.be.true;
      });

      it('And go to a non existent relationship, Then I should be redirected to the first relationship', function() {
        $(ListCollectorPage.no()).click();
        $(ListCollectorPage.submit()).click();
        browser.url('/questionnaire/relationships/fake-id/to/another-fake-id');
        expect(browser.getUrl()).to.contain(RelationshipsPage.pageName);
        expect($(RelationshipsPage.playback()).getText()).to.contain('Marcus Twin');
      });

      it('And go to the first relationship and click \'Save and sign out\', Then I should be signed out', function() {
        $(ListCollectorPage.no()).click();
        $(ListCollectorPage.submit()).click();
        $(RelationshipsPage.husbandOrWife()).click();
        $(RelationshipsPage.saveSignOut()).click();
        expect(browser.getUrl()).to.not.contain('questionnaire');
      });

      it('And go to the first relationship, select a relationship and click \'Save and sign out\', Then I should be signed out', function() {
        $(ListCollectorPage.no()).click();
        $(ListCollectorPage.submit()).click();
        $(RelationshipsPage.saveSignOut()).click();
        expect(browser.getUrl()).to.not.contain('questionnaire');
      });
    });

    describe('When I have added one or more household members after answering the relationships question,', function() {
      beforeEach('add three people and complete their relationships', function() {
        addThreePeopleAndCompleteRelationships();
      });

      it('Then I delete one of the original household members I will not be asked for the original members relationships again', function() {
        browser.url('/questionnaire/list-collector');
        $(ListCollectorPage.listRemoveLink(3)).click();
        $(ListCollectorRemovePage.yes()).click();
        $(ListCollectorRemovePage.submit()).click();
        $(ListCollectorPage.no()).click();
        $(ListCollectorPage.submit()).click();
        expect(browser.getUrl()).to.contain('/questionnaire/confirmation');
      });

      it('Then I will be asked for the original household members relationships to all new members', function() {
        browser.url('/questionnaire/list-collector');
        $(ListCollectorPage.yes()).click();
        $(ListCollectorPage.submit()).click();
        $(ListCollectorAddPage.firstName()).setValue('Tom');
        $(ListCollectorAddPage.lastName()).setValue('Bowden');
        $(ListCollectorAddPage.submit()).click();
        $(ListCollectorPage.no()).click();
        $(ListCollectorPage.submit()).click();
        expect($(RelationshipsPage.husbandOrWife()).isSelected()).to.be.true;
        $(RelationshipsPage.submit()).click();
        expect($(RelationshipsPage.legallyRegisteredCivilPartner()).isSelected()).to.be.true;
        $(RelationshipsPage.submit()).click();
        expect($(RelationshipsPage.playback()).getText()).to.contain('Tom Bowden is Marcus Twin’s …');

        $(RelationshipsPage.sonOrDaughter()).click();
        $(RelationshipsPage.submit()).click();
        expect($(RelationshipsPage.husbandOrWife()).isSelected()).to.be.true;
        $(RelationshipsPage.submit()).click();
        expect($(RelationshipsPage.playback()).getText()).to.contain('Tom Bowden is Samuel Clemens’ …');

        $(RelationshipsPage.sonOrDaughter()).click();
        $(RelationshipsPage.submit()).click();
        browser.pause(20000);
        expect($(RelationshipsPage.playback()).getText()).to.contain('Tom Bowden is Olivia Clemens’ …');
      });

      it('When I add a household member after answering the relationships question but remove them again before exiting the list-collector block, Then I will not be asked for the original household members relationships to the new member', function() {
        browser.url('/questionnaire/list-collector');
        $(ListCollectorPage.yes()).click();
        $(ListCollectorPage.submit()).click();
        $(ListCollectorAddPage.firstName()).setValue('Tom');
        $(ListCollectorAddPage.lastName()).setValue('Bowden');
        $(ListCollectorAddPage.submit()).click();
        $(ListCollectorPage.listRemoveLink(4)).click();
        $(ListCollectorRemovePage.yes()).click();
        $(ListCollectorRemovePage.submit()).click();
        $(ListCollectorPage.no()).click();
        $(ListCollectorPage.submit()).click();
        expect(browser.getUrl()).to.contain('/questionnaire/confirmation');
      });
    });

    function addThreePeopleAndCompleteRelationships() {
      addThreePeople();

      $(ListCollectorPage.no()).click();
      $(ListCollectorPage.submit()).click();
      $(RelationshipsPage.husbandOrWife()).click();
      $(RelationshipsPage.submit()).click();
      $(RelationshipsPage.legallyRegisteredCivilPartner()).click();
      $(RelationshipsPage.submit()).click();
      $(RelationshipsPage.husbandOrWife()).click();
      $(RelationshipsPage.submit()).click();
    }

    function addThreePeople() {
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
    }

  });
});
