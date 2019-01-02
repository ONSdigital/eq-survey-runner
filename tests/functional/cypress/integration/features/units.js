import {openQuestionnaire} from '../../../helpers/helpers.js'

const SetLengthUnitsBlockPage = require('../../../generated_pages/unit_patterns/set-length-units-block.page.js');
const SetDurationUnitsBlockPage = require('../../../generated_pages/unit_patterns/set-duration-units-block.page.js');
const SetAreaUnitsBlockPage = require('../../../generated_pages/unit_patterns/set-area-units-block.page.js');
const SetVolumeUnitsBlockPage = require('../../../generated_pages/unit_patterns/set-volume-units-block.page.js');
const SummaryPage = require('../../../generated_pages/unit_patterns/summary.page.js');

describe('Units', function() {

  it('Given we do not set a language code and run the questionnaire, when we enter values for durations, they should be displayed on the summary with their units.', function() {
    //openQuestionnaire('test_unit_patterns.json')
    openQuestionnaire('test_unit_patterns.json', { language: 'en' })
                  .get(SetLengthUnitsBlockPage.submit()).click()
          .get(SetDurationUnitsBlockPage.durationHourUnit()).stripText().should('equal', 'hours')
          .get(SetDurationUnitsBlockPage.durationYearUnit()).stripText().should('equal', 'years')
          .get(SetDurationUnitsBlockPage.durationHour()).type(123)
          .get(SetDurationUnitsBlockPage.durationYear()).type(321)
          .get(SetDurationUnitsBlockPage.submit()).click()
          .get(SetAreaUnitsBlockPage.submit()).click()
          .get(SetVolumeUnitsBlockPage.submit()).click()
          .get(SummaryPage.durationHour()).stripText().should('equal', '123 hours')
          .get(SummaryPage.durationYear()).stripText().should('equal', '321 years');
        });
    });

  it('Given we set a language code for welsh and run the questionnaire, when we enter values for durations, they should be displayed on the summary with their units.', function() {
    openQuestionnaire('test_unit_patterns.json', { language: 'cy' })
                  .get(SetLengthUnitsBlockPage.submit()).click()
          .get(SetDurationUnitsBlockPage.durationHourUnit()).stripText().should('equal', 'awr')
          .get(SetDurationUnitsBlockPage.durationYearUnit()).stripText().should('equal', 'flynedd')
          .get(SetDurationUnitsBlockPage.durationHour()).type(123)
          .get(SetDurationUnitsBlockPage.durationYear()).type(321)
          .get(SetDurationUnitsBlockPage.submit()).click()
          .get(SetAreaUnitsBlockPage.submit()).click()
          .get(SetVolumeUnitsBlockPage.submit()).click()
          .get(SummaryPage.durationHour()).stripText().should('equal', '123 awr')
          .get(SummaryPage.durationYear()).stripText().should('equal', '321 mlynedd');
        });
    });
});

