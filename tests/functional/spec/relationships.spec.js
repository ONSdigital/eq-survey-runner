const helpers = require('../helpers');
const ListCollectorPage = require('../generated_pages/relationships/list-collector.page.js');
const ListCollectorAddPage = require('../generated_pages/relationships/list-collector-add.page.js');
const ListCollectorRemovePage = require('../generated_pages/relationships/list-collector-remove.page.js');
const RelationshipsPage = require('../generated_pages/relationships/relationships.page.js');
const ConfirmationPage = require('../generated_pages/relationships/confirmation.page.js');

describe('Relationships', function() {
  const schema = 'test_relationships.json';

  describe('Given I am completing the test_relationships survey,', function() {
    beforeEach('load the survey', function() {
      return helpers.openQuestionnaire(schema);
    });


    it('When I have one household member, Then I will be not be asked about relationships', function() {
      return browser
        .click(ListCollectorPage.yes())
        .click(ListCollectorPage.submit())
        .setValue(ListCollectorAddPage.firstName(), 'Marcus')
        .setValue(ListCollectorAddPage.lastName(), 'Twin')
        .click(ListCollectorAddPage.submit())
        .click(ListCollectorPage.no())
        .click(ListCollectorPage.submit())
        .getUrl().should.eventually.contain(ConfirmationPage.pageName);
    });

    it('When I add two household members, Then I will be asked about one relationship', function() {
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
        .click(ListCollectorPage.no())
        .click(ListCollectorPage.submit())
        .getUrl().should.eventually.contain(RelationshipsPage.pageName)
        .click(RelationshipsPage.husbandOrWife())
        .click(RelationshipsPage.submit())
        .getUrl().should.eventually.contain(ConfirmationPage.pageName);
    });

    describe('When I add three household members,', function() {
      beforeEach('add three people', function() {
        return addThreePeople();
      });

      it('Then I will be asked about all relationships', function() {
        return browser
          .click(ListCollectorPage.no())
          .click(ListCollectorPage.submit())
          .click(RelationshipsPage.husbandOrWife())
          .click(RelationshipsPage.submit())
          .click(RelationshipsPage.legallyRegisteredCivilPartner())
          .click(RelationshipsPage.submit())
          .click(RelationshipsPage.husbandOrWife())
          .click(RelationshipsPage.submit())
          .getUrl().should.eventually.contain(ConfirmationPage.pageName);
      });

      it('And go to the first relationship, Then the previous link should return to the list collector', function() {
        return browser
          .click(ListCollectorPage.no())
          .click(ListCollectorPage.submit())
          .click(RelationshipsPage.previous())
          .getUrl().should.eventually.contain(ListCollectorPage.pageName);
      });

      it('And go to the second relationship, Then the previous link should return to the first relationship', function() {
        return browser
          .click(ListCollectorPage.no())
          .click(ListCollectorPage.submit())
          .click(RelationshipsPage.husbandOrWife())
          .click(RelationshipsPage.submit())
          .click(RelationshipsPage.previous())
          .getUrl().should.eventually.contain(RelationshipsPage.pageName)
          .getText(RelationshipsPage.questionText()).should.eventually.contain('Marcus');
      });

      it('And go to the confirmation page, Then the previous link should return to the last relationship', function() {
        return browser
          .click(ListCollectorPage.no())
          .click(ListCollectorPage.submit())
          .click(RelationshipsPage.husbandOrWife())
          .click(RelationshipsPage.submit())
          .click(RelationshipsPage.legallyRegisteredCivilPartner())
          .click(RelationshipsPage.submit())
          .click(RelationshipsPage.husbandOrWife())
          .click(RelationshipsPage.submit())
          .getUrl().should.eventually.contain(ConfirmationPage.pageName)
          .click(ConfirmationPage.previous())
          .getUrl().should.eventually.contain(RelationshipsPage.pageName)
          .getText(RelationshipsPage.questionText()).should.eventually.contain('Olivia');
      });

      it('When I add all relationships and return to the relationships, Then the relationships should be populated', function() {
        return browser
          .click(ListCollectorPage.no())
          .click(ListCollectorPage.submit())
          .click(RelationshipsPage.husbandOrWife())
          .click(RelationshipsPage.submit())
          .click(RelationshipsPage.legallyRegisteredCivilPartner())
          .click(RelationshipsPage.submit())
          .click(RelationshipsPage.husbandOrWife())
          .click(RelationshipsPage.submit())
          .getUrl().should.eventually.contain(ConfirmationPage.pageName)
          .click(ConfirmationPage.previous())
          .isSelected(RelationshipsPage.husbandOrWife()).should.eventually.be.true
          .click(ConfirmationPage.previous())
          .isSelected(RelationshipsPage.legallyRegisteredCivilPartner()).should.eventually.be.true
          .click(ConfirmationPage.previous())
          .isSelected(RelationshipsPage.husbandOrWife()).should.eventually.be.true;
      });

      it('And go to the first relationship, Then the person\'s name should be in the question title and playback text', function() {
        return browser
          .click(ListCollectorPage.no())
          .click(ListCollectorPage.submit())
          .getText(ListCollectorPage.questionText()).should.eventually.contain('Marcus Twin')
          .getText(RelationshipsPage.playback()).should.eventually.contain('Marcus Twin');
      });

      it('And go to the first relationship and submit without selecting an option, Then an error should be displayed', function() {
        return browser
          .click(ListCollectorPage.no())
          .click(ListCollectorPage.submit())
          .click(RelationshipsPage.submit())
          .isVisible(RelationshipsPage.error()).should.eventually.be.true;
      });

      it('And go to a non existent relationship, Then I should be redirected to the first relationship', function() {
        return browser
          .click(ListCollectorPage.no())
          .click(ListCollectorPage.submit())
          .url('/questionnaire/relationships/fake-id/to/another-fake-id')
          .getUrl().should.eventually.contain(RelationshipsPage.pageName)
          .getText(RelationshipsPage.playback()).should.eventually.contain('Marcus Twin');
      });

      it('And go to the first relationship and click \'Save and sign out\', Then I should be signed out', function() {
        return browser
          .click(ListCollectorPage.no())
          .click(ListCollectorPage.submit())
          .click(RelationshipsPage.husbandOrWife())
          .click(RelationshipsPage.saveSignOut())
          .getUrl().should.eventually.not.contain('questionnaire');
      });

      it('And go to the first relationship, select a relationship and click \'Save and sign out\', Then I should be signed out', function() {
        return browser
          .click(ListCollectorPage.no())
          .click(ListCollectorPage.submit())
          .click(RelationshipsPage.saveSignOut())
          .getUrl().should.eventually.not.contain('questionnaire');
      });
    });

    describe('When I have added one or more household members after answering the relationships question,', function() {
      beforeEach('add three people and complete their relationships', function() {
        return addThreePeopleAndCompleteRelationships();
      });

      it('Then I delete one of the original household members I will not be asked for the original members relationships again', function() {
        return browser
          .url('/questionnaire/list-collector')
          .click(ListCollectorPage.listRemoveLink(3))
          .click(ListCollectorRemovePage.yes())
          .click(ListCollectorRemovePage.submit())
          .click(ListCollectorPage.no())
          .click(ListCollectorPage.submit())
          .getUrl().should.eventually.contain('/questionnaire/confirmation');
      });

      it('Then I will be asked for the original household members relationships to all new members', function() {
        return browser
          .url('/questionnaire/list-collector')
          .click(ListCollectorPage.yes())
          .click(ListCollectorPage.submit())
          .setValue(ListCollectorAddPage.firstName(), 'Tom')
          .setValue(ListCollectorAddPage.lastName(), 'Bowden')
          .click(ListCollectorAddPage.submit())
          .click(ListCollectorPage.no())
          .click(ListCollectorPage.submit())
          .isSelected(RelationshipsPage.husbandOrWife()).should.eventually.be.true
          .click(RelationshipsPage.submit())
          .isSelected(RelationshipsPage.legallyRegisteredCivilPartner()).should.eventually.be.true
          .click(RelationshipsPage.submit())
          .getText(RelationshipsPage.playback())
          .should.eventually.contain('Tom Bowden is Marcus Twin’s …')
          .click(RelationshipsPage.sonOrDaughter())
          .click(RelationshipsPage.submit())
          .isSelected(RelationshipsPage.husbandOrWife()).should.eventually.be.true
          .click(RelationshipsPage.submit())
          .getText(RelationshipsPage.playback())
          .should.eventually.contain('Tom Bowden is Samuel Clemens’ …')
          .click(RelationshipsPage.sonOrDaughter())
          .click(RelationshipsPage.submit())
          .pause(20000)
          .getText(RelationshipsPage.playback())
          .should.eventually.contain('Tom Bowden is Olivia Clemens’ …');
      });

      it('When I add a household member after answering the relationships question but remove them again before exiting the list-collector block, Then I will not be asked for the original household members relationships to the new member', function() {
        return browser
          .url('/questionnaire/list-collector')
          .click(ListCollectorPage.yes())
          .click(ListCollectorPage.submit())
          .setValue(ListCollectorAddPage.firstName(), 'Tom')
          .setValue(ListCollectorAddPage.lastName(), 'Bowden')
          .click(ListCollectorAddPage.submit())
          .click(ListCollectorPage.listRemoveLink(4))
          .click(ListCollectorRemovePage.yes())
          .click(ListCollectorRemovePage.submit())
          .click(ListCollectorPage.no())
          .click(ListCollectorPage.submit())
          .getUrl().should.eventually.contain('/questionnaire/confirmation');
      });
    });

    function addThreePeopleAndCompleteRelationships() {
      return addThreePeople()
        .click(ListCollectorPage.no())
        .click(ListCollectorPage.submit())
        .click(RelationshipsPage.husbandOrWife())
        .click(RelationshipsPage.submit())
        .click(RelationshipsPage.legallyRegisteredCivilPartner())
        .click(RelationshipsPage.submit())
        .click(RelationshipsPage.husbandOrWife())
        .click(RelationshipsPage.submit());
    }

    function addThreePeople() {
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
        .click(ListCollectorAddPage.submit());
    }
  });
});
