import chai from 'chai'
import {startCensusQuestionnaire} from '../../../helpers'

import PermanentOrFamilyHome from '../../../pages/surveys/census/household/permanent-or-family-home.page.js'
import HouseholdComposition from '../../../pages/surveys/census/household/household-composition.page.js'
import EveryoneAtAddressConfirmation from '../../../pages/surveys/census/household/everyone-at-address-confirmation.page.js'
import OvernightVisitors from '../../../pages/surveys/census/household/overnight-visitors.page.js'

const expect = chai.expect

describe('ArriveInUk', function () {

  it('Given I am answering question 3 in the who lives here section, When I dont select any respone, Then I am routed to Who lives here question 4 ', function () {
    startCensusQuestionnaire('census_household.json', true)
    PermanentOrFamilyHome.clickPermanentOrFamilyHomeAnswerYes().submit()
    HouseholdComposition.setPersonName(0, 'John Smith').addPerson().setPersonName(1, 'Jane Smith').submit()
    EveryoneAtAddressConfirmation.submit()
    OvernightVisitors.setOvernightVisitorsAnswer(0).submit()
  })
})
