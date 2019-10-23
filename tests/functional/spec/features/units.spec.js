const helpers = require('../../helpers');

const SetLengthUnitsBlockPage = require('../../generated_pages/unit_patterns/set-length-units-block.page.js');
const SetDurationUnitsBlockPage = require('../../generated_pages/unit_patterns/set-duration-units-block.page.js');
const SetAreaUnitsBlockPage = require('../../generated_pages/unit_patterns/set-area-units-block.page.js');
const SetVolumeUnitsBlockPage = require('../../generated_pages/unit_patterns/set-volume-units-block.page.js');
const SummaryPage = require('../../generated_pages/unit_patterns/summary.page.js');

describe('Units', function() {
  let browser;

  it('Given we do not set a language code and run the questionnaire, when we enter values for durations, they should be displayed on the summary with their units.', function() {
      //return helpers.openQuestionnaire('test_unit_patterns.json').then(() => {
      helpers.openQuestionnaire('test_unit_patterns.json', { language: 'en' }).then(openBrowser => browser = openBrowser);
      $(SetLengthUnitsBlockPage.submit()).click();
      expect($(SetDurationUnitsBlockPage.durationHourUnit()).getText()).to.equal('hours');
      expect($(SetDurationUnitsBlockPage.durationYearUnit()).getText()).to.equal('years');
      $(SetDurationUnitsBlockPage.durationHour()).setValue(123);
      $(SetDurationUnitsBlockPage.durationYear()).setValue(321);
      $(SetDurationUnitsBlockPage.submit()).click();
      $(SetAreaUnitsBlockPage.submit()).click();
      $(SetVolumeUnitsBlockPage.submit()).click();
      expect($(SummaryPage.durationHour()).getText()).to.equal('123 hours');
      expect($(SummaryPage.durationYear()).getText()).to.equal('321 years');
    });

  it('Given we set a language code for welsh and run the questionnaire, when we enter values for durations, they should be displayed on the summary with their units.', function() {
    helpers.openQuestionnaire('test_unit_patterns.json', { language: 'cy' }).then(openBrowser => browser = openBrowser);
    $(SetLengthUnitsBlockPage.submit()).click();
    expect($(SetDurationUnitsBlockPage.durationHourUnit()).getText()).to.equal('awr');
    expect($(SetDurationUnitsBlockPage.durationYearUnit()).getText()).to.equal('flynedd');
    $(SetDurationUnitsBlockPage.durationHour()).setValue(123);
    $(SetDurationUnitsBlockPage.durationYear()).setValue(321);
    $(SetDurationUnitsBlockPage.submit()).click();
    $(SetAreaUnitsBlockPage.submit()).click();
    $(SetVolumeUnitsBlockPage.submit()).click();
    expect($(SummaryPage.durationHour()).getText()).to.equal('123 awr');
    expect($(SummaryPage.durationYear()).getText()).to.equal('321 mlynedd');
  });
});

