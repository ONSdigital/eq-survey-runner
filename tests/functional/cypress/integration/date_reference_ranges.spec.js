import {openQuestionnaire} from '../helpers/helpers.js';

const ManualRangeBlockPage = require('../../generated_pages/date_reference_ranges/manual-range-block.page.js');
const DateSeparateBlockPage = require('../../generated_pages/date_reference_ranges/date-separate-block.page.js');
const DateRangeBlockPage = require('../../generated_pages/date_reference_ranges/date-range-block.page.js');
const SummaryPage = require('../../generated_pages/date_reference_ranges/summary.page.js');

describe('Reference Date Range Checks', function() {
  beforeEach(() => {
    openQuestionnaire('test_date_reference_ranges.json');
  });

  it('Given we start the survey, when we click the button, the dates should be in the correct format...', function() {
    /* We have no way to mock out started_at, the unit and integration tests cover the date values
     * this test is only to validate the general questionnaire functionality and to make sure
     * the date format is correct.
     */

    cy
      // Matches `in the week Friday 24 August 2018 to`. The day of the month can be 1 or two characters
      .get(SummaryPage.questionText()).stripText().should('match', new RegExp('in the week [a-zA-Z]+ \\d(?:\\d)? [a-zA-Z]+ \\d{4} to'))
      // Matches `to Saturday 25 August 2018 to`. The day of the month can be 1 or two characters
      .get(SummaryPage.questionText()).stripText().should('match', new RegExp('to [a-zA-Z]+ \\d(?:\\d)? [a-zA-Z]+ \\d{4}$'))

      .get(ManualRangeBlockPage.yes()).click()
      .get(ManualRangeBlockPage.submit()).click()

      // Matches `week starting Saturday 25 August 2018 would`. The day of the month can be 1 or two characters
      .get(DateSeparateBlockPage.questionText()).stripText().should('match', new RegExp('week starting [a-zA-Z]+ \\d(?:\\d)? [a-zA-Z]+ would'))
      // Matches `before Saturday 25 August 2018`. The day of the month can be 1 or two characters
      .get(DateSeparateBlockPage.questionText()).stripText().should('match', new RegExp('before [a-zA-Z]+ \\d(?:\\d)? [a-zA-Z]*$'))

      .get(DateSeparateBlockPage.yes()).click()
      .get(DateSeparateBlockPage.submit()).click()

      // Matches `between Friday 24 August 2018 to Saturday 25 September 2019`. The day of the month can be 1 or two characters
      // In this case, the month and the year can be omitted if they are both the same in the range.
      .get(DateRangeBlockPage.questionText()).stripText().should('match', new RegExp('between \\d(?:\\d)?(?:[a-zA-Z ]+)?(?:[\\d ]{4})? to \\d(?:\\d)? \\w+ \\d{4} did'));
  });
});

