import {openQuestionnaire} from '../helpers/helpers.js'

const PrimaryNamePage = require('../generated_pages/routing_repeat_until/primary-name-block.page.js');
const RepeatingNamePage = require('../generated_pages/routing_repeat_until/repeating-name-block.page.js');
const RepeatingAnyoneElsePage = require('../generated_pages/routing_repeat_until/repeating-anyone-else-block.page.js');
const SexPage = require('../generated_pages/routing_repeat_until/sex-block.page.js');
const SummaryPage = require('../generated_pages/routing_repeat_until/summary.page.js');

describe('Routing Repeat Until', function() {

  it('Given the test_routing_repeat_until survey is selected when one additional member is entered we are asked about the the sex of them and the primary member', function() {

    openQuestionnaire('test_routing_repeat_until.json')

              .get(PrimaryNamePage.primaryName()).type('Bob')
        .get(PrimaryNamePage.submit()).click()

        .get(RepeatingAnyoneElsePage.yes()).click()
        .get(RepeatingAnyoneElsePage.submit()).click()

        .get(RepeatingNamePage.repeatingName()).type('Alice')
        .get(RepeatingNamePage.submit()).click()

        .get(RepeatingAnyoneElsePage.no()).click()
        .get(RepeatingAnyoneElsePage.submit()).click()

        .get(SexPage.questionText()).stripText().should('contain', 'Bob')
        .get(SexPage.male()).click()
        .get(SexPage.submit()).click()

        .get(SexPage.questionText()).stripText().should('contain', 'Alice')
        .get(SexPage.female()).click()
        .get(SexPage.submit()).click()

        .url().should('contain', SummaryPage.pageName)

        .get(SummaryPage.primaryGroupTitle(0)).stripText().should('contain', "Your Details")
        .get(SummaryPage.primaryName(0)).stripText().should('contain', "Bob")

        .get(SummaryPage.repeatingGroupTitle(0)).stripText().should('contain', "Other Household Members")
        .get(SummaryPage.repeatingName(0)).stripText().should('contain', "Alice")

        .get(SummaryPage.submit()).click();
    });
  });

  it('Given the test_routing_repeat_until survey is selected when multiple additional members are entered we are asked about the sex of all of them and the primary member', function() {

    openQuestionnaire('test_routing_repeat_until.json')

              .get(PrimaryNamePage.primaryName()).type('Bob')
        .get(PrimaryNamePage.submit()).click()

        .get(RepeatingAnyoneElsePage.yes()).click()
        .get(RepeatingAnyoneElsePage.submit()).click()

        .get(RepeatingNamePage.repeatingName()).type('Alice')
        .get(RepeatingNamePage.submit()).click()

        .get(RepeatingAnyoneElsePage.yes()).click()
        .get(RepeatingAnyoneElsePage.submit()).click()

        .get(RepeatingNamePage.repeatingName()).type('John')
        .get(RepeatingNamePage.submit()).click()

        .get(RepeatingAnyoneElsePage.no()).click()
        .get(RepeatingAnyoneElsePage.submit()).click()

        .get(SexPage.questionText()).stripText().should('contain', 'Bob')
        .get(SexPage.male()).click()
        .get(SexPage.submit()).click()

        .get(SexPage.questionText()).stripText().should('contain', 'Alice')
        .get(SexPage.female()).click()
        .get(SexPage.submit()).click()

        .get(SexPage.questionText()).stripText().should('contain', 'John')
        .get(SexPage.male()).click()
        .get(SexPage.submit()).click()

        .url().should('contain', SummaryPage.pageName)

        .get(SummaryPage.primaryGroupTitle(0)).stripText().should('contain', "Your Details")
        .get(SummaryPage.primaryName(0)).stripText().should('contain', "Bob")

        .get(SummaryPage.repeatingGroupTitle(0)).stripText().should('contain', "Other Household Members")
        .get(SummaryPage.repeatingName(0)).stripText().should('contain', "Alice")

        .get(SummaryPage.repeatingGroupTitle(0)).stripText().should('contain', "Other Household Members")
        .get(SummaryPage.repeatingName(1)).stripText().should('contain', "John")

        .get(SummaryPage.sexAnswer(0)).stripText().should('contain', "Male")
        .get(SummaryPage.sexAnswer(1)).stripText().should('contain', "Female")
        .get(SummaryPage.sexAnswer(2)).stripText().should('contain', "Male")

        .get(SummaryPage.submit()).click();
    });
  });

  it('Given the test_routing_repeat_until survey is selected when no additional members are entered we are asked about the sex of the primary member', function() {

    openQuestionnaire('test_routing_repeat_until.json')

              .get(PrimaryNamePage.primaryName()).type('Bob')
        .get(PrimaryNamePage.submit()).click()

        .get(RepeatingAnyoneElsePage.no()).click()
        .get(RepeatingAnyoneElsePage.submit()).click()

        .get(SexPage.questionText()).stripText().should('contain', 'Bob')
        .get(SexPage.male()).click()
        .get(SexPage.submit()).click()

        .url().should('contain', SummaryPage.pageName)
        .get(SummaryPage.submit()).click();
    });
  });

});

