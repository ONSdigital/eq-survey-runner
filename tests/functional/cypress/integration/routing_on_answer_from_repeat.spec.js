import {openQuestionnaire} from ../helpers/helpers.js

const PrimaryNamePage = require('../generated_pages/routing_on_answer_from_driving_repeating_group/primary-name-block.page.js');
const PrimaryLiveHereBlockPage = require('../generated_pages/routing_on_answer_from_driving_repeating_group/primary-live-here-block.page.js');
const RepeatingNamePage = require('../generated_pages/routing_on_answer_from_driving_repeating_group/repeating-name-block.page.js');
const RepeatingAnyoneElsePage = require('../generated_pages/routing_on_answer_from_driving_repeating_group/repeating-anyone-else-block.page.js');
const SexPage = require('../generated_pages/routing_on_answer_from_driving_repeating_group/sex-block.page.js');
const SexNoPrimaryPage = require('../generated_pages/routing_on_answer_from_driving_repeating_group/sex-block-no-primary.page.js');
const RelationshipsPage = require('../generated_pages/routing_on_answer_from_driving_repeating_group/relationships.page.js');
const RelationshipsNoPrimaryPage = require('../generated_pages/routing_on_answer_from_driving_repeating_group/relationships-no-primary.page.js');
const SummaryPage = require('../generated_pages/routing_on_answer_from_driving_repeating_group/summary.page.js');

describe('Routing on Answer from repeat', function() {

  it('Given I am completing a survey where I dont live in the house, When I select I dont live here, Then I should not be asked questions about myself', function() {

    openQuestionnaire('test_routing_on_answer_from_driving_repeating_group.json')

              .get(PrimaryNamePage.primaryName()).type('Bob')
        .get(PrimaryNamePage.submit()).click()

        .get(PrimaryLiveHereBlockPage.no()).click()
        .get(PrimaryLiveHereBlockPage.submit()).click()

        .get(RepeatingAnyoneElsePage.yes()).click()
        .get(RepeatingAnyoneElsePage.submit()).click()

        .get(RepeatingNamePage.repeatingName()).type('Alice')
        .get(RepeatingNamePage.submit()).click()

        .get(RepeatingAnyoneElsePage.yes()).click()
        .get(RepeatingAnyoneElsePage.submit()).click()

        .get(RepeatingNamePage.repeatingName()).type('Jamie')
        .get(RepeatingNamePage.submit()).click()

        .get(RepeatingAnyoneElsePage.no()).click()
        .get(RepeatingAnyoneElsePage.submit()).click()

        .get(RelationshipsNoPrimaryPage.relationship(0, 'Husband or wife')).click()
        .get(RelationshipsNoPrimaryPage.submit()).click()

        .get(SexNoPrimaryPage.questionText()).stripText().should('contain', 'Alice')
        .get(SexNoPrimaryPage.female()).click()
        .get(SexNoPrimaryPage.submit()).click()

        .get(SexNoPrimaryPage.questionText()).stripText().should('contain', 'Jamie')
        .get(SexNoPrimaryPage.male()).click()
        .get(SexNoPrimaryPage.submit()).click()

        .url().should('contain', SummaryPage.pageName)
        .get(SummaryPage.submit()).click();
    });
  });

});

