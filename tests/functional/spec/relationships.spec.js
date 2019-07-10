const helpers = require('../helpers');
const ListCollectorPage = require('../generated_pages/relationships/list-collector.page.js');
const ListCollectorAddPage = require('../generated_pages/relationships/list-collector-add.page.js');
const RelationshipsPage = require('../generated_pages/relationships/relationships.page.js');
const ConfirmationPage = require('../generated_pages/relationships/confirmation.page.js');

describe('Relationships', function() {

  beforeEach(function() {
    return helpers.openQuestionnaire('test_relationships.json');
  });

  it('Given I am completing the survey, When I have one household member, Then I will be not be asked about relationships', function () {
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

  it('Given I am completing the survey, When I add two household members, Then I will be asked about one relationship', function () {
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

  it('Given I am completing the survey, When I add three household members, Then I will be asked about all relationships', function () {
    return helpers.openQuestionnaire('test_relationships.json')
    .then(addThreePeople)
    .then(() => {
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
  });

  it('Given I am completing the survey, When I add three household members and go to the first relationship, Then the previous link should return to the list collector', function () {
    return helpers.openQuestionnaire('test_relationships.json')
    .then(addThreePeople)
    .then(() => {
      return browser
        .click(ListCollectorPage.no())
        .click(ListCollectorPage.submit())
        .click(RelationshipsPage.previous())
        .getUrl().should.eventually.contain(ListCollectorPage.pageName);
    });
  });

  it('Given I am completing the survey, When I add three household members and go to the second relationship, Then the previous link should return to the first relationship', function () {
    return helpers.openQuestionnaire('test_relationships.json')
    .then(addThreePeople)
    .then(() => {
      return browser
        .click(ListCollectorPage.no())
        .click(ListCollectorPage.submit())
        .click(RelationshipsPage.husbandOrWife())
        .click(RelationshipsPage.submit())
        .click(RelationshipsPage.previous())
        .getUrl().should.eventually.contain(RelationshipsPage.pageName)
        .getText(RelationshipsPage.questionText()).should.eventually.contain('Marcus');
    });
  });

  it('Given I am completing the survey, When I add all relationships and go to the confirmation page, Then the previous link should return to the last relationship', function () {
    return helpers.openQuestionnaire('test_relationships.json')
    .then(addThreePeople)
    .then(() => {
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
  });

  it('Given I am completing the survey, When I add all relationships and return to the relationships, Then the relationships should be populated', function () {
    return helpers.openQuestionnaire('test_relationships.json')
    .then(addThreePeople)
    .then(() => {
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
  });

  it('Given I am completing the survey, When I add three household members and go to the first relationship, Then the person\'s name should be in the question title and playback text', function () {
    return helpers.openQuestionnaire('test_relationships.json')
    .then(addThreePeople)
    .then(() => {
      return browser
        .click(ListCollectorPage.no())
        .click(ListCollectorPage.submit())
        .getText(ListCollectorPage.questionText()).should.eventually.contain('Marcus Twin')
        .getText(RelationshipsPage.playback()).should.eventually.contain('Marcus Twin');
    });
  });

  it('Given I am completing the survey, When I add three household members and go to the first relationship and submit without selecting an option, Then an error should be displayed', function () {
    return helpers.openQuestionnaire('test_relationships.json')
    .then(addThreePeople)
    .then(() => {
      return browser
        .click(ListCollectorPage.no())
        .click(ListCollectorPage.submit())
        .click(RelationshipsPage.submit())
        .isVisible(RelationshipsPage.error()).should.eventually.be.true;
    });
  });

  it('Given I am completing the survey, When I add three household members and go to a non existent relationship, Then I should be redirected to the first relationship', function () {
    return helpers.openQuestionnaire('test_relationships.json')
    .then(addThreePeople)
    .then(() => {
      return browser
        .click(ListCollectorPage.no())
        .click(ListCollectorPage.submit())
        .url('/questionnaire/relationships/fake-id/to/another-fake-id')
        .getUrl().should.eventually.contain(RelationshipsPage.pageName)
        .getText(RelationshipsPage.playback()).should.eventually.contain('Marcus Twin');
    });
  });

  it('Given I am completing the survey, When I add three household members and go to the first relationship and click \'Save and sign out\', Then I should be signed out', function () {
    return helpers.openQuestionnaire('test_relationships.json')
    .then(addThreePeople)
    .then(() => {
      return browser
        .click(ListCollectorPage.no())
        .click(ListCollectorPage.submit())
        .click(RelationshipsPage.husbandOrWife())
        .click(RelationshipsPage.saveSignOut())
        .getUrl().should.eventually.not.contain('questionnaire');
    });
  });

  it('Given I am completing the survey, When I add three household members and go to the first relationship, select a relationship and click \'Save and sign out\', Then I should be signed out', function () {
    return helpers.openQuestionnaire('test_relationships.json')
    .then(addThreePeople)
    .then(() => {
      return browser
        .click(ListCollectorPage.no())
        .click(ListCollectorPage.submit())
        .click(RelationshipsPage.saveSignOut())
        .getUrl().should.eventually.not.contain('questionnaire');
    });
  });

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
