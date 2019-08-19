const helpers = require('../helpers');
const PrimaryPersonListCollectorPage = require('../generated_pages/relationships_primary/primary-person-list-collector.page.js');
const PrimaryPersonListCollectorAddPage = require('../generated_pages/relationships_primary/primary-person-list-collector-add.page.js');
const ListCollectorPage = require('../generated_pages/relationships_primary/list-collector.page.js');
const ListCollectorAddPage = require('../generated_pages/relationships_primary/list-collector-add.page.js');
const RelationshipsPage = require('../generated_pages/relationships_primary/relationships.page.js');

describe('Relationships - Primary Person', function() {
  const schema = 'test_relationships_primary.json';

  describe('Given I am completing the test_relationships_primary survey', function() {
    beforeEach(function() {
      return helpers.openQuestionnaire(schema);
    });

    it('When I add household members, Then I will be asked my relationships as a primary person', function() {
      return addPrimaryAndTwoOthers()
        .click(ListCollectorPage.no())
        .click(ListCollectorPage.submit())
        .getText(RelationshipsPage.questionText()).should.eventually.contain('is your');
    });

    it('When I add household members, Then non-primary relationships will be asked as a non primary person', function() {
      return addPrimaryAndTwoOthers()
        .click(ListCollectorPage.no())
        .click(ListCollectorPage.submit())
        .click(RelationshipsPage.relationshipBrotherOrSister())
        .click(RelationshipsPage.submit())
        .click(RelationshipsPage.relationshipSonOrDaughter())
        .click(RelationshipsPage.submit())
        .getText(RelationshipsPage.questionText()).should.eventually.contain('is their');
    });

    it('When I add household members And add thir relationships And remove the primary person And add a new primary person then I will be asked for the relationships again', function() {
      return addPrimaryAndTwoOthersAndCompleteRelationships()
        .url('/questionnaire/primary-person-list-collector')
        .click(PrimaryPersonListCollectorPage.no())
        .click(PrimaryPersonListCollectorPage.submit())
        .url('/questionnaire/primary-person-list-collector')
        .click(PrimaryPersonListCollectorPage.yes())
        .click(PrimaryPersonListCollectorPage.submit())
        .setValue(PrimaryPersonListCollectorAddPage.firstName(), 'Marcus')
        .setValue(PrimaryPersonListCollectorAddPage.lastName(), 'Twin')
        .click(PrimaryPersonListCollectorAddPage.submit())
        .click(ListCollectorPage.no())
        .click(ListCollectorPage.submit())
        .getText(RelationshipsPage.questionText()).should.eventually.contain('Samuel Clemens is your');
    });

    function addPrimaryAndTwoOthersAndCompleteRelationships() {
      return addPrimaryAndTwoOthers()
        .click(ListCollectorPage.no())
        .click(ListCollectorPage.submit())
        .click(RelationshipsPage.relationshipBrotherOrSister())
        .click(RelationshipsPage.submit())
        .click(RelationshipsPage.relationshipSonOrDaughter())
        .click(RelationshipsPage.submit())
        .click(RelationshipsPage.relationshipBrotherOrSister());
    }

    function addPrimaryAndTwoOthers() {
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
        .click(ListCollectorPage.yes())
        .click(ListCollectorPage.submit())
        .setValue(ListCollectorAddPage.firstName(), 'Olivia')
        .setValue(ListCollectorAddPage.lastName(), 'Clemens')
        .click(ListCollectorAddPage.submit());
    }
  });
});
