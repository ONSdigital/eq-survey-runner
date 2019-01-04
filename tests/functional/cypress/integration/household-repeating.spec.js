import {startQuestionnaire} from '../helpers/helpers.js';

const HouseholdCompositionPage = require('../../generated_pages/repeating_household/household-composition.page.js');
const RepeatingBlock1Page = require('../../generated_pages/repeating_household/repeating-block-1.page.js');
const RepeatingBlock2Page = require('../../generated_pages/repeating_household/repeating-block-2.page.js');
const RepeatingBlock3Page = require('../../generated_pages/repeating_household/repeating-block-3.page.js');
const SummaryPage = require('../../generated_pages/repeating_household/summary.page.js');

describe('Household Repeating', function() {

  beforeEach(() => {
    startQuestionnaire('test_repeating_household.json');
  });

  it('Given I enter one name, when I navigate through the subsequent group, I should see the name on each block.', function() {
    cy
      .get(HouseholdCompositionPage.firstName()).type('Alpha')
      .get(HouseholdCompositionPage.lastName()).type('One')
      .get(HouseholdCompositionPage.submit()).click()
      .get(RepeatingBlock1Page.displayedDescription()).stripText().should('contain', 'Alpha One')
      .get(RepeatingBlock1Page.whatIsYourAge()).type('99')
      .get(RepeatingBlock1Page.submit()).click()
      .get(RepeatingBlock2Page.displayedName()).stripText().should('contain', 'Alpha One');
  });

  it('Given I enter multiple names, when I navigate through the subsequent groups, I should the names on their respective blocks.', function() {
    cy
      .get(HouseholdCompositionPage.firstName()).type('Alpha')
      .get(HouseholdCompositionPage.lastName()).type('One')
      .get(HouseholdCompositionPage.addPerson()).click()
      .get(HouseholdCompositionPage.firstName('_1')).type('Bravo')
      .get(HouseholdCompositionPage.lastName('_1')).type('Two')
      .get(HouseholdCompositionPage.addPerson()).click()
      .get(HouseholdCompositionPage.firstName('_2')).type('Charlie')
      .get(HouseholdCompositionPage.lastName('_2')).type('Three')
      .get(HouseholdCompositionPage.submit()).click()

      .get(RepeatingBlock1Page.displayedDescription()).stripText().should('contain', 'Alpha One')
      .get(RepeatingBlock1Page.whatIsYourAge()).type('60')
      .get(RepeatingBlock1Page.submit()).click()
      .get(RepeatingBlock2Page.displayedName()).stripText().should('contain', 'Alpha One')
      .get(RepeatingBlock2Page.whatIsYourShoeSize()).type('10')
      .get(RepeatingBlock2Page.submit()).click()
      .get(RepeatingBlock3Page.questionText()).stripText().should('contain', '60')
      .get(RepeatingBlock3Page.questionText()).stripText().should('contain', '10')
      .get(RepeatingBlock3Page.yes()).click()
      .get(RepeatingBlock3Page.submit()).click()

      .get(RepeatingBlock1Page.displayedDescription()).stripText().should('contain', 'Bravo Two')
      .get(RepeatingBlock1Page.whatIsYourAge()).type('50')
      .get(RepeatingBlock1Page.submit()).click()
      .get(RepeatingBlock2Page.displayedName()).stripText().should('contain', 'Bravo Two')
      .get(RepeatingBlock2Page.whatIsYourShoeSize()).type('11')
      .get(RepeatingBlock2Page.submit()).click()
      .get(RepeatingBlock3Page.questionText()).stripText().should('contain', '50')
      .get(RepeatingBlock3Page.questionText()).stripText().should('contain', '11')
      .get(RepeatingBlock3Page.yes()).click()
      .get(RepeatingBlock3Page.submit()).click()

      .get(RepeatingBlock1Page.displayedDescription()).stripText().should('contain', 'Charlie Three')
      .get(RepeatingBlock1Page.whatIsYourAge()).type('40')
      .get(RepeatingBlock1Page.submit()).click()
      .get(RepeatingBlock2Page.displayedName()).stripText().should('contain', 'Charlie Three')
      .get(RepeatingBlock2Page.whatIsYourShoeSize()).type('12')
      .get(RepeatingBlock2Page.submit()).click()
      .get(RepeatingBlock3Page.questionText()).stripText().should('contain', '40')
      .get(RepeatingBlock3Page.questionText()).stripText().should('contain', '12')
      .get(RepeatingBlock3Page.yes()).click()
      .get(RepeatingBlock3Page.submit()).click()

      .then(checkSummaryBlockPage);
  });
});


function checkSummaryBlockPage() {
  cy
    .url().should('contain', SummaryPage.pageName)

    .get(SummaryPage.multipleQuestionsGroupTitle()).stripText().should('contain', 'Group 1')

    .get(SummaryPage.firstName()).stripText().should('contain', 'Alpha')
    .get(SummaryPage.middleNames()).stripText().should('contain', 'No answer provided')
    .get(SummaryPage.lastName()).stripText().should('contain', 'One')

    .get(SummaryPage.repeatingGroupTitle()).stripText().should('contain', 'Alpha One')
    .get(SummaryPage.whatIsYourAge()).stripText().should('contain', '60')
    .get(SummaryPage.whatIsYourShoeSize()).stripText().should('contain', '10')
    .get(SummaryPage.confirmAnswer()).stripText().should('contain', 'Yes')

    .get(SummaryPage.repeatingGroupTitle(1)).stripText().should('contain', 'Bravo Two')
    .get(SummaryPage.whatIsYourAge(1)).stripText().should('contain', '50')
    .get(SummaryPage.whatIsYourShoeSize(1)).stripText().should('contain', '11')
    .get(SummaryPage.confirmAnswer(1)).stripText().should('contain', 'Yes')

    .get(SummaryPage.repeatingGroupTitle(2)).stripText().should('contain', 'Charlie Three')
    .get(SummaryPage.whatIsYourAge(2)).stripText().should('contain', '40')
    .get(SummaryPage.whatIsYourShoeSize(2)).stripText().should('contain', '12')
    .get(SummaryPage.confirmAnswer(2)).stripText().should('contain', 'Yes');
}
