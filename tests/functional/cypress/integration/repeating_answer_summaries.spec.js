import {openQuestionnaire} from '../helpers/helpers.js';

const PrimaryNamePage = require('../../generated_pages/repeating_answer_summaries/primary-name-block.page.js');
const PrimaryAnyoneElsePage = require('../../generated_pages/repeating_answer_summaries/primary-anyone-else-block.page.js');
const RepeatingNamePage = require('../../generated_pages/repeating_answer_summaries/repeating-name-block.page.js');
const RepeatingAnyoneElsePage = require('../../generated_pages/repeating_answer_summaries/repeating-anyone-else-block.page.js');

describe('Routing Repeat Until', function() {
  beforeEach(() => {
    openQuestionnaire('test_repeating_answer_summaries.json');
  });

  it('Given the test_routing_repeat_until survey is selected, a list of users will be shown on the next page, when more people are added they are shown in the does anyone else live here page.', function() {
    cy
      .get(PrimaryNamePage.primaryFirstName()).type('Bob')
      .get(PrimaryNamePage.primaryMiddleNames()).type('Bertie')
      .get(PrimaryNamePage.primaryLastName()).type('Bourne')
      .get(PrimaryNamePage.submit()).click()

      .get(PrimaryAnyoneElsePage.displayedDescription()).stripText().should('contain', 'Bob Bertie Bourne')
      .get(PrimaryAnyoneElsePage.yes()).click()
      .get(PrimaryAnyoneElsePage.submit()).click()

      .get(RepeatingNamePage.repeatingFirstName()).type('Carrie')
      .get(RepeatingNamePage.repeatingMiddleNames()).type('Cormorant')
      .get(RepeatingNamePage.repeatingLastName()).type('Court')
      .get(RepeatingNamePage.submit()).click()

      .get(RepeatingAnyoneElsePage.displayedDescription()).stripText().should('contain', 'Bob Bertie Bourne')
      .get(RepeatingAnyoneElsePage.displayedDescription()).stripText().should('contain', 'Carrie Cormorant Court')
      .get(RepeatingAnyoneElsePage.yes()).click()
      .get(RepeatingAnyoneElsePage.submit()).click()

      .get(RepeatingNamePage.repeatingFirstName()).type('David')
      .get(RepeatingNamePage.repeatingMiddleNames()).type('Dorian')
      .get(RepeatingNamePage.repeatingLastName()).type('Davies')
      .get(RepeatingNamePage.submit()).click()

      .get(RepeatingAnyoneElsePage.displayedDescription()).stripText().should('contain', 'Bob Bertie Bourne')
      .get(RepeatingAnyoneElsePage.displayedDescription()).stripText().should('contain', 'Carrie Cormorant Court')
      .get(RepeatingAnyoneElsePage.displayedDescription()).stripText().should('contain', 'David Dorian Davies');
  });
});
