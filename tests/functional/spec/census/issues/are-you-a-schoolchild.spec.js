import chai from 'chai'
import {startCensusQuestionnaire} from '../../../helpers'

import PermanentOrFamilyHome from '../../../pages/surveys/census/household/permanent-or-family-home.page.js'
import ElsePermanentOrFamilyHome from '../../../pages/surveys/census/household/else-permanent-or-family-home.page.js'
import HouseholdComposition from '../../../pages/surveys/census/household/household-composition.page.js'
import EveryoneAtAddressConfirmation from '../../../pages/surveys/census/household/everyone-at-address-confirmation.page.js'
import OvernightVisitors from '../../../pages/surveys/census/household/overnight-visitors.page.js'
import HouseholdRelationships from '../../../pages/surveys/census/household/household-relationships.page.js'
import WhoLivesHereCompleted from '../../../pages/surveys/census/household/who-lives-here-completed.page.js'
import TypeOfAccommodation from '../../../pages/surveys/census/household/type-of-accommodation.page.js'
import TypeOfHouse from '../../../pages/surveys/census/household/type-of-house.page.js'
import TypeOfFlat from '../../../pages/surveys/census/household/type-of-flat.page.js'
import SelfContainedAccommodation from '../../../pages/surveys/census/household/self-contained-accommodation.page.js'
import NumberOfBedrooms from '../../../pages/surveys/census/household/number-of-bedrooms.page.js'
import CentralHeating from '../../../pages/surveys/census/household/central-heating.page.js'
import OwnOrRent from '../../../pages/surveys/census/household/own-or-rent.page.js'
import Landlord from '../../../pages/surveys/census/household/landlord.page.js'
import NumberOfVehicles from '../../../pages/surveys/census/household/number-of-vehicles.page.js'
import HouseholdAndAccommodationCompleted from '../../../pages/surveys/census/household/household-and-accommodation-completed.page.js'
import HouseholdMemberBegin from '../../../pages/surveys/census/household/household-member-begin.page.js'
import DetailsCorrect from '../../../pages/surveys/census/household/details-correct.page.js'
import CorrectName from '../../../pages/surveys/census/household/correct-name.page.js'
import Sex from '../../../pages/surveys/census/household/sex.page.js'
import DateOfBirth from '../../../pages/surveys/census/household/date-of-birth.page.js'
import Over16 from '../../../pages/surveys/census/household/over-16.page.js'
import PrivateResponse from '../../../pages/surveys/census/household/private-response.page.js'
import MaritalStatus from '../../../pages/surveys/census/household/marital-status.page.js'
import AnotherAddress from '../../../pages/surveys/census/household/another-address.page.js'
import OtherAddress from '../../../pages/surveys/census/household/other-address.page.js'
import AddressType from '../../../pages/surveys/census/household/address-type.page.js'
import InEducation from '../../../pages/surveys/census/household/in-education.page.js'
import TermTimeLocation from '../../../pages/surveys/census/household/term-time-location.page.js'
import CountryOfBirth from '../../../pages/surveys/census/household/country-of-birth.page.js'

const expect = chai.expect

describe('Are-you-a-schoolchild', function () {

  it('Given I am answering question 7 in the individual detail section - 7. Are you a schoolchild or student in full-time education?, When I do not select any respone, Then I am routed to 9. What is your country of birth?', function () {
   startCensusQuestionnaire('census_household.json', true)
   PermanentOrFamilyHome.clickPermanentOrFamilyHomeAnswerYes().submit()
   HouseholdComposition.setFirstName('John').addPerson().setFirstName('Jane', 1).submit()
   EveryoneAtAddressConfirmation.clickEveryoneAtAddressConfirmationAnswerYes().submit()
   OvernightVisitors.setOvernightVisitorsAnswer(0).submit()
   HouseholdRelationships.clickHouseholdRelationshipsAnswerHusbandOrWife().submit()
   WhoLivesHereCompleted.submit()

 // household-and-accommodation
   TypeOfAccommodation.clickTypeOfAccommodationAnswerWholeHouseOrBungalow().submit()
   TypeOfHouse.clickTypeOfHouseAnswerSemiDetached().submit()
   SelfContainedAccommodation.clickSelfContainedAccommodationAnswerYesAllTheRoomsAreBehindADoorThatOnlyThisHouseholdCanUse().submit()
   NumberOfBedrooms.setNumberOfBedroomsAnswer(3).submit()
   CentralHeating.clickCentralHeatingAnswerGas().submit()
   OwnOrRent.clickOwnOrRentAnswerOwnsOutright().submit()
   NumberOfVehicles.setNumberOfVehiclesAnswer(2).submit()
   HouseholdAndAccommodationCompleted.submit()

 // household-member
   HouseholdMemberBegin.submit()
   DetailsCorrect.clickDetailsCorrectAnswerYesThisIsMyFullName().submit()
   Over16.clickOver16AnswerYes().submit()
   PrivateResponse.clickPrivateResponseAnswerNoIDoNotWantToRequestAPersonalForm().submit()
   Sex.clickSexAnswerMale().submit()
   DateOfBirth.setDateOfBirthAnswerDay(2).setDateOfBirthAnswerMonth(3).setDateOfBirthAnswerYear(1980).submit()
   MaritalStatus.clickMaritalStatusAnswerMarried().submit()
   AnotherAddress.clickAnotherAddressAnswerNo().submit()
   InEducation.submit()
   expect(CountryOfBirth.isOpen()).to.be.true
 })
})
