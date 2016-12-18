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
import SelfContainedAccommodation from '../../../pages/surveys/census/household/self-contained-accommodation.page.js'
import NumberOfBedrooms from '../../../pages/surveys/census/household/number-of-bedrooms.page.js'
import CentralHeating from '../../../pages/surveys/census/household/central-heating.page.js'
import OwnOrRent from '../../../pages/surveys/census/household/own-or-rent.page.js'
import NumberOfVehicles from '../../../pages/surveys/census/household/number-of-vehicles.page.js'
import HouseholdAndAccommodationCompleted from '../../../pages/surveys/census/household/household-and-accommodation-completed.page.js'
import HouseholdMemberBegin from '../../../pages/surveys/census/household/household-member-begin.page.js'
import DetailsCorrect from '../../../pages/surveys/census/household/details-correct.page.js'
import Sex from '../../../pages/surveys/census/household/sex.page.js'
import DateOfBirth from '../../../pages/surveys/census/household/date-of-birth.page.js'
import Over16 from '../../../pages/surveys/census/household/over-16.page.js'
import PrivateResponse from '../../../pages/surveys/census/household/private-response.page.js'
import MaritalStatus from '../../../pages/surveys/census/household/marital-status.page.js'
import AnotherAddress from '../../../pages/surveys/census/household/another-address.page.js'
import InEducation from '../../../pages/surveys/census/household/in-education.page.js'
import TermTimeLocation from '../../../pages/surveys/census/household/term-time-location.page.js'
import CountryOfBirth from '../../../pages/surveys/census/household/country-of-birth.page.js'
import Carer from '../../../pages/surveys/census/household/carer.page.js'
import NationalIdentity from '../../../pages/surveys/census/household/national-identity.page.js'

const expect = chai.expect

describe('Carer routing Scenarios', function () {

  it('Given I am answering question 13. Do you look after, or give any help or support..., When I select -No- as response, Then I am routed to 14. How would you describe your national identity?', function () {
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
    InEducation.clickInEducationAnswerYes().submit()
    TermTimeLocation.clickTermTimeLocationAnswerHereAtThisAddress().submit()
    CountryOfBirth.clickCountryOfBirthEnglandAnswerEngland().submit()
    Carer.clickCarerAnswerNo().submit()
    expect(NationalIdentity.isOpen()).to.equal(true, 'Expecting go to national identity')
  })

  it('Given I am answering question 13. Do you look after, or give any help or support..., When I select -Yes 1-19 Hours A Week- as response, Then I am routed to 14. How would you describe your national identity?', function () {
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
    InEducation.clickInEducationAnswerYes().submit()
    TermTimeLocation.clickTermTimeLocationAnswerHereAtThisAddress().submit()
    CountryOfBirth.clickCountryOfBirthEnglandAnswerEngland().submit()
    Carer.clickCarerAnswerYes119HoursAWeek().submit()
    expect(NationalIdentity.isOpen()).to.equal(true, 'Expecting go to national identity')
  })

  it('Given I am answering question 13. Do you look after, or give any help or support..., When I select -Yes 20-49 Hours A Week- as response, Then I am routed to 14. How would you describe your national identity?', function () {
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
    InEducation.clickInEducationAnswerYes().submit()
    TermTimeLocation.clickTermTimeLocationAnswerHereAtThisAddress().submit()
    CountryOfBirth.clickCountryOfBirthEnglandAnswerEngland().submit()
    Carer.clickCarerAnswerYes2049HoursAWeek().submit()
    expect(NationalIdentity.isOpen()).to.equal(true, 'Expecting go to national identity')
  })

  it('Given I am answering question 13. Do you look after, or give any help or support..., When I select -Yes 50 or more Hours A Week- as response, Then I am routed to 14. How would you describe your national identity?', function () {
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
    InEducation.clickInEducationAnswerYes().submit()
    TermTimeLocation.clickTermTimeLocationAnswerHereAtThisAddress().submit()
    CountryOfBirth.clickCountryOfBirthEnglandAnswerEngland().submit()
    Carer.clickCarerAnswerYes50OrMoreHoursAWeek().submit()
    expect(NationalIdentity.isOpen()).to.equal(true, 'Expecting go to national identity')
  })
})
