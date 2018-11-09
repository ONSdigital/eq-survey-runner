const helpers = require('../../helpers');

const SetLengthUnitsBlockPage = require('../../generated_pages/unit_patterns/set-length-units-block.page.js');
const SetDurationUnitsBlockPage = require('../../generated_pages/unit_patterns/set-duration-units-block.page.js');
const SetAreaUnitsBlockPage = require('../../generated_pages/unit_patterns/set-area-units-block.page.js');
const SetVolumeUnitsBlockPage = require('../../generated_pages/unit_patterns/set-volume-units-block.page.js');
const SummaryPage = require('../../generated_pages/unit_patterns/summary.page.js');

describe('Units', function() {

  it('Given we do not set a language code and run the questionnaire, when we enter values for durations, they should be displayed on the summary with their units.', function() {
    //return helpers.openQuestionnaire('test_unit_patterns.json').then(() => {
    return helpers.openQuestionnaire('test_unit_patterns.json', helpers.getRandomString(10), helpers.getRandomString(10), '201605', 'May 2016', 'GB-ENG', 'en').then(() => {
        return browser
          .click(SetLengthUnitsBlockPage.submit())
          .getText(SetDurationUnitsBlockPage.durationHourUnit()).should.eventually.equal('hours')
          .getText(SetDurationUnitsBlockPage.durationYearUnit()).should.eventually.equal('years')
          .setValue(SetDurationUnitsBlockPage.durationHour(), 123)
          .setValue(SetDurationUnitsBlockPage.durationYear(), 321)
          .click(SetDurationUnitsBlockPage.submit())
          .click(SetAreaUnitsBlockPage.submit())
          .click(SetVolumeUnitsBlockPage.submit())
          .getText(SummaryPage.durationHour()).should.eventually.equal('123 hours')
          .getText(SummaryPage.durationYear()).should.eventually.equal('321 years');
        });
    });

  it('Given we set a language code for welsh and run the questionnaire, when we enter values for durations, they should be displayed on the summary with their units.', function() {
    return helpers.openQuestionnaire('test_unit_patterns.json', helpers.getRandomString(10), helpers.getRandomString(10), '201605', 'May 2016', 'GB-ENG', 'cy').then(() => {
        return browser
          .click(SetLengthUnitsBlockPage.submit())
          .getText(SetDurationUnitsBlockPage.durationHourUnit()).should.eventually.equal('awr')
          .getText(SetDurationUnitsBlockPage.durationYearUnit()).should.eventually.equal('flynedd')
          .setValue(SetDurationUnitsBlockPage.durationHour(), 123)
          .setValue(SetDurationUnitsBlockPage.durationYear(), 321)
          .click(SetDurationUnitsBlockPage.submit())
          .click(SetAreaUnitsBlockPage.submit())
          .click(SetVolumeUnitsBlockPage.submit())
          .getText(SummaryPage.durationHour()).should.eventually.equal('123 awr')
          .getText(SummaryPage.durationYear()).should.eventually.equal('321 mlynedd');
        });
    });
});

