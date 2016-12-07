import {openAndStartCensusQuestionnaire} from '../../../helpers'

import PermanentOrFamilyHome from '../../../pages/surveys/census/household/permanent-or-family-home.page.js'
import HouseholdComposition from '../../../pages/surveys/census/household/household-composition.page.js'
import EveryoneAtAddressConfirmation from '../../../pages/surveys/census/household/everyone-at-address-confirmation.page.js'

describe('ArriveInUk', function () {
  // issue present error 500
     it('Given I am answering question 3 in the who lives here section, When I select -no- as the respone, Then I am routed back to Who lives here question 2 ', function () {
         openAndStartCensusQuestionnaire('census_household.json', true)
         PermanentOrFamilyHome.clickPermanentOrFamilyHomeAnswerYes().submit()
         HouseholdComposition.setPersonName(0, 'John Smith').addPerson().setPersonName(1, 'Jane Smith').submit()
         EveryoneAtAddressConfirmation.clickEveryoneAtAddressConfirmationAnswerNoINeedToAddAnotherPerson().submit()
         HouseholdComposition.submit()
     })
})
