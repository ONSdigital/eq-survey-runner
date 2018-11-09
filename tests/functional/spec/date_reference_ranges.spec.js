const helpers = require('../helpers');

const ManualRangeBlockPage = require('../generated_pages/date_reference_ranges/manual-range-block.page.js');
const DateSeparateBlockPage = require('../generated_pages/date_reference_ranges/date-separate-block.page.js');
const DateRangeBlockPage = require('../generated_pages/date_reference_ranges/date-range-block.page.js');
const SummaryPage = require('../generated_pages/date_reference_ranges/summary.page.js');

describe('Reference Date Range Checks', function() {
  // We have no way to mock out started_at, the unit and integration tests cover the date values
  // this test is only to validate the general questionnaire functionality and to make sure
  // the date format is correct.
  it('Given we start the survey, when we click the button, the dates should be in the correct format...', function() {
    return helpers.openQuestionnaire('test_date_reference_ranges.json').then(() => {
        return browser
          // Should show a date range in the right format

          // Matches `in the week Friday 24 August 2018 to`. The day of the month can be 1 or two characters
          .getText(SummaryPage.questionText()).should.eventually.match(new RegExp('in the week [a-zA-Z]+ \\d(?:\\d)? [a-zA-Z]+ \\d{4} to'))
          // Matches `to Saturday 25 August 2018 to`. The day of the month can be 1 or two characters
          .getText(SummaryPage.questionText()).should.eventually.match(new RegExp('to [a-zA-Z]+ \\d(?:\\d)? [a-zA-Z]+ \\d{4}$'))

          .click(ManualRangeBlockPage.yes())
          .click(ManualRangeBlockPage.submit())

          // Matches `week starting Saturday 25 August 2018 would`. The day of the month can be 1 or two characters
          .getText(DateSeparateBlockPage.questionText()).should.eventually.match(new RegExp('week starting [a-zA-Z]+ \\d(?:\\d)? [a-zA-Z]+ would'))
          // Matches `before Saturday 25 August 2018`. The day of the month can be 1 or two characters
          .getText(DateSeparateBlockPage.questionText()).should.eventually.match(new RegExp('before [a-zA-Z]+ \\d(?:\\d)? [a-zA-Z]*$'))

          .click(DateSeparateBlockPage.yes())
          .click(DateSeparateBlockPage.submit())

          // Matches `between Friday 24 August 2018 to Saturday 25 September 2019`. The day of the month can be 1 or two characters
          // In this case, the month and the year can be ommitted if they are both the same in the range.
          .getText(DateRangeBlockPage.questionText()).should.eventually.match(new RegExp('between \\d(?:\\d)?(?:[a-zA-Z ]+)?(?:[\\d ]{4})? to \\d(?:\\d)? \\w+ \\d{4} did'));


        });
    });
});

