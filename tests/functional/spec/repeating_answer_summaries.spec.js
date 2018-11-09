const helpers = require('../helpers');

const PrimaryNamePage = require('../generated_pages/repeating_answer_summaries/primary-name-block.page.js');
const PrimaryAnyoneElsePage = require('../generated_pages/repeating_answer_summaries/primary-anyone-else-block.page.js');
const RepeatingNamePage = require('../generated_pages/repeating_answer_summaries/repeating-name-block.page.js');
const RepeatingAnyoneElsePage = require('../generated_pages/repeating_answer_summaries/repeating-anyone-else-block.page.js');

describe('Routing Repeat Until', function() {

  it('Given the test_routing_repeat_until survey is selected, a list of users will be shown on the next page, when more people are added they are shown in the does anyone else live here page.', function() {

    return helpers.openQuestionnaire('test_repeating_answer_summaries.json').then(() => {

      return browser
        .setValue(PrimaryNamePage.primaryFirstName(), 'Bob')
        .setValue(PrimaryNamePage.primaryMiddleNames(), 'Bertie')
        .setValue(PrimaryNamePage.primaryLastName(), 'Bourne')
        .click(PrimaryNamePage.submit())

        .getText(PrimaryAnyoneElsePage.displayedDescription()).should.eventually.contain('Bob Bertie Bourne')
        .click(PrimaryAnyoneElsePage.yes())
        .click(PrimaryAnyoneElsePage.submit())

        .setValue(RepeatingNamePage.repeatingFirstName(), 'Carrie')
        .setValue(RepeatingNamePage.repeatingMiddleNames(), 'Cormorant')
        .setValue(RepeatingNamePage.repeatingLastName(), 'Court')
        .click(RepeatingNamePage.submit())

        .getText(RepeatingAnyoneElsePage.displayedDescription()).should.eventually.contain('Bob Bertie Bourne')
        .getText(RepeatingAnyoneElsePage.displayedDescription()).should.eventually.contain('Carrie Cormorant Court')
        .click(RepeatingAnyoneElsePage.yes())
        .click(RepeatingAnyoneElsePage.submit())

        .setValue(RepeatingNamePage.repeatingFirstName(), 'David')
        .setValue(RepeatingNamePage.repeatingMiddleNames(), 'Dorian')
        .setValue(RepeatingNamePage.repeatingLastName(), 'Davies')
        .click(RepeatingNamePage.submit())

        .getText(RepeatingAnyoneElsePage.displayedDescription()).should.eventually.contain('Bob Bertie Bourne')
        .getText(RepeatingAnyoneElsePage.displayedDescription()).should.eventually.contain('Carrie Cormorant Court')
        .getText(RepeatingAnyoneElsePage.displayedDescription()).should.eventually.contain('David Dorian Davies');
    });
  });
});
