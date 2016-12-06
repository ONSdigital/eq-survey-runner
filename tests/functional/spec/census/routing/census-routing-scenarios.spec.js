  import chai from 'chai'
  import {openAndStartCensusQuestionnaire} from '../../../helpers'

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
  import MaritalStatus from '../../../pages/surveys/census/household/marital-status.page.js'
  import AnotherAddress from '../../../pages/surveys/census/household/another-address.page.js'
  import OtherAddress from '../../../pages/surveys/census/household/other-address.page.js'
  import AddressType from '../../../pages/surveys/census/household/address-type.page.js'
  import InEducation from '../../../pages/surveys/census/household/in-education.page.js'
  import TermTimeLocation from '../../../pages/surveys/census/household/term-time-location.page.js'
  import CountryOfBirth from '../../../pages/surveys/census/household/country-of-birth.page.js'
  import ArriveInUk from '../../../pages/surveys/census/household/arrive-in-uk.page.js'
  import LengthOfStay from '../../../pages/surveys/census/household/length-of-stay.page.js'
  import Carer from '../../../pages/surveys/census/household/carer.page.js'
  import NationalIdentity from '../../../pages/surveys/census/household/national-identity.page.js'
  import EthnicGroup from '../../../pages/surveys/census/household/ethnic-group.page.js'
  import WhiteEthnicGroup from '../../../pages/surveys/census/household/white-ethnic-group.page.js'
  import MixedEthnicGroup from '../../../pages/surveys/census/household/mixed-ethnic-group.page.js'
  import AsianEthnicGroup from '../../../pages/surveys/census/household/asian-ethnic-group.page.js'
  import BlackEthnicGroup from '../../../pages/surveys/census/household/black-ethnic-group.page.js'
  import OtherEthnicGroup from '../../../pages/surveys/census/household/other-ethnic-group.page.js'
  import SexualIdentity from '../../../pages/surveys/census/household/sexual-identity.page.js'
  import UnderstandWelsh from '../../../pages/surveys/census/household/understand-welsh.page.js'
  import Language from '../../../pages/surveys/census/household/language.page.js'
  import English from '../../../pages/surveys/census/household/english.page.js'
  import Religion from '../../../pages/surveys/census/household/religion.page.js'
  import PastUsualAddress from '../../../pages/surveys/census/household/past-usual-address.page.js'
  import LastYearAddress from '../../../pages/surveys/census/household/last-year-address.page.js'
  import Passports from '../../../pages/surveys/census/household/passports.page.js'
  import Disability from '../../../pages/surveys/census/household/disability.page.js'
  import Qualifications from '../../../pages/surveys/census/household/qualifications.page.js'
  import Volunteering from '../../../pages/surveys/census/household/volunteering.page.js'
  import EmploymentType from '../../../pages/surveys/census/household/employment-type.page.js'
  import Jobseeker from '../../../pages/surveys/census/household/jobseeker.page.js'
  import JobAvailability from '../../../pages/surveys/census/household/job-availability.page.js'
  import JobPending from '../../../pages/surveys/census/household/job-pending.page.js'
  import Occupation from '../../../pages/surveys/census/household/occupation.page.js'
  import EverWorked from '../../../pages/surveys/census/household/ever-worked.page.js'
  import MainJob from '../../../pages/surveys/census/household/main-job.page.js'
  import JobTitle from '../../../pages/surveys/census/household/job-title.page.js'
  import JobDescription from '../../../pages/surveys/census/household/job-description.page.js'
  import EmployersBusiness from '../../../pages/surveys/census/household/employers-business.page.js'
  import MainJobType from '../../../pages/surveys/census/household/main-job-type.page.js'
  import BusinessName from '../../../pages/surveys/census/household/business-name.page.js'
  import HouseholdMemberCompleted from '../../../pages/surveys/census/household/household-member-completed.page.js'
  import NumberOfVisitors from '../../../pages/surveys/census/household/number-of-visitors.page.js'
  import VisitorName from '../../../pages/surveys/census/household/visitor-name.page.js'
  import VisitorSex from '../../../pages/surveys/census/household/visitor-sex.page.js'
  import VisitorDateOfBirth from '../../../pages/surveys/census/household/visitor-date-of-birth.page.js'
  import VisitorUkResident from '../../../pages/surveys/census/household/visitor-uk-resident.page.js'
  import VisitorAddress from '../../../pages/surveys/census/household/visitor-address.page.js'
  import Confirmation from '../../../pages/confirmation.page.js'
  import ThankYou from '../../../pages/thank-you.page'

  const expect = chai.expect

  describe('Census routing Scenarios', function () {

    it('Given I am answering question 1 in the who lives here section, When I select -yes- as the respone, Then I am routed to Who lives here question 2 ', function () {
        openAndStartCensusQuestionnaire('census_household.json', true)
        PermanentOrFamilyHome.clickPermanentOrFamilyHomeAnswerYes().submit()
        HouseholdComposition.setPersonName(0, 'John Smith').addPerson().setPersonName(1, 'Jane Smith').submit()
    })

    it('Given I am answering question 1 in the who lives here section, When I select -no- as the respone, Then I am routed to Who lives here question 2 ', function () {
        openAndStartCensusQuestionnaire('census_household.json', true)
        PermanentOrFamilyHome.clickPermanentOrFamilyHomeAnswerNo().submit()
        ElsePermanentOrFamilyHome.clickElsePermanentOrFamilyHomeAnswerYes()
    })

    it('Given I am answering question 1 in the who lives here section, When I dont select any respone, Then I a alert msg saying mandatory field must be displayed ', function () {
        openAndStartCensusQuestionnaire('census_household.json', true)
        PermanentOrFamilyHome.submit()
        expect(PermanentOrFamilyHome.getAlertText()).to.contain('This field is mandatory.')
    })

    it('Given I am answering question 1a in the who lives here section, When I select -yes- as the respone, Then I am routed to Who lives here question 2 ', function () {
        openAndStartCensusQuestionnaire('census_household.json', true)
        PermanentOrFamilyHome.clickPermanentOrFamilyHomeAnswerNo().submit()
        ElsePermanentOrFamilyHome.clickElsePermanentOrFamilyHomeAnswerYes().submit()
        HouseholdComposition.setPersonName(0, 'John Smith').addPerson().setPersonName(1, 'Jane Smith').submit()
    })

    it('Given I am answering question 1a in the who lives here section, When I select -no- as the respone, Then I am routed to How many visitors... question 4 ', function () {
        openAndStartCensusQuestionnaire('census_household.json', true)
        PermanentOrFamilyHome.clickPermanentOrFamilyHomeAnswerNo().submit()
        ElsePermanentOrFamilyHome.clickElsePermanentOrFamilyHomeAnswerNo().submit()
        OvernightVisitors.setOvernightVisitorsAnswer(0).submit()
    })

    it('Given I am answering question 1a in the who lives here section, When I select -no- as the respone, Then I am routed to How many visitors... question 4 ', function () {
        openAndStartCensusQuestionnaire('census_household.json', true)
        PermanentOrFamilyHome.clickPermanentOrFamilyHomeAnswerNo().submit()
        ElsePermanentOrFamilyHome.submit()
        expect(ElsePermanentOrFamilyHome.getAlertText()).to.contain('This field is mandatory.')
    })

    it('Given I am answering question 3 in the who lives here section, When I select -yes- as the respone, Then I am routed to Who lives here question 4 ', function () {
        openAndStartCensusQuestionnaire('census_household.json', true)
        PermanentOrFamilyHome.clickPermanentOrFamilyHomeAnswerYes().submit()
        HouseholdComposition.setPersonName(0, 'John Smith').addPerson().setPersonName(1, 'Jane Smith').submit()
        EveryoneAtAddressConfirmation.clickEveryoneAtAddressConfirmationAnswerYes().submit()
        OvernightVisitors.setOvernightVisitorsAnswer(0).submit()
    })
    // issue present error 500
  /*  it('Given I am answering question 3 in the who lives here section, When I select -no- as the respone, Then I am routed back to Who lives here question 2 ', function () {
        openAndStartCensusQuestionnaire('census_household.json', true)
        PermanentOrFamilyHome.clickPermanentOrFamilyHomeAnswerYes().submit()
        HouseholdComposition.setPersonName(0, 'John Smith').addPerson().setPersonName(1, 'Jane Smith').submit()
        EveryoneAtAddressConfirmation.clickEveryoneAtAddressConfirmationAnswerNoINeedToAddAnotherPerson().submit()
        HouseholdComposition.submit()
    })
    // issue present - displaying on screen validation error which is not in spec
    it('Given I am answering question 3 in the who lives here section, When I dont select any respone, Then I am routed to Who lives here question 4 ', function () {
        openAndStartCensusQuestionnaire('census_household.json', true)
        PermanentOrFamilyHome.clickPermanentOrFamilyHomeAnswerYes().submit()
        HouseholdComposition.setPersonName(0, 'John Smith').addPerson().setPersonName(1, 'Jane Smith').submit()
        EveryoneAtAddressConfirmation.submit()
        OvernightVisitors.setOvernightVisitorsAnswer(0).submit()
    }) */

    it('Given I am answering question 1 in the individual detail section, When I select -yes- as respone, Then I am routed to What is you sex question 2 ', function () {
      openAndStartCensusQuestionnaire('census_household.json', true)
      PermanentOrFamilyHome.clickPermanentOrFamilyHomeAnswerYes().submit()
      HouseholdComposition.setPersonName(0, 'John Smith').addPerson().setPersonName(1, 'Jane Smith').submit()
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
      Sex.clickSexAnswerMale().submit()
  })

  it('Given I am answering question 1 in the individual detail section, When I select -no- as respone, Then I am routed to What is your correct name question 1a ', function () {
    openAndStartCensusQuestionnaire('census_household.json', true)
    PermanentOrFamilyHome.clickPermanentOrFamilyHomeAnswerYes().submit()
    HouseholdComposition.setPersonName(0, 'John Smith').addPerson().setPersonName(1, 'Jane Smith').submit()
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
    DetailsCorrect.clickDetailsCorrectAnswerNoINeedToChangeMyName().submit()
    CorrectName.setCorrectNameAnswer('Yoganand Kumar Kunche').submit()
  })

  //issue present - error 404

/*  it('Given I am answering question 1 in the individual detail section, When I do not select any respone, Then I am routed to What is you sex question 2 ', function () {
    openAndStartCensusQuestionnaire('census_household.json', true)
    PermanentOrFamilyHome.clickPermanentOrFamilyHomeAnswerYes().submit()
    HouseholdComposition.setPersonName(0, 'John Smith').addPerson().setPersonName(1, 'Jane Smith').submit()
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
    DetailsCorrect.submit()
    Sex.clickSexAnswerMale().submit()
  }) */

  it('Given I am answering question 5 in the individual detail section -Do you stay at another address for more than 30 days a year?, When I select -no- as respone, Then I am routed to 7. Are you a schoolchild or student in full-time education', function () {
    openAndStartCensusQuestionnaire('census_household.json', true)
    PermanentOrFamilyHome.clickPermanentOrFamilyHomeAnswerYes().submit()
    HouseholdComposition.setPersonName(0, 'John Smith').addPerson().setPersonName(1, 'Jane Smith').submit()
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
    Sex.clickSexAnswerMale().submit()
    DateOfBirth.setDateOfBirthAnswerDay(2).setDateOfBirthAnswerMonth(3).setDateOfBirthAnswerYear(1980).submit()
    Over16.clickOver16AnswerYes().submit()
    MaritalStatus.clickMaritalStatusAnswerMarried().submit()
    AnotherAddress.clickAnotherAddressAnswerNo().submit()
    InEducation.clickInEducationAnswerNo().submit()
  })

  it('Given I am answering question 5 in the individual detail section -Do you stay at another address for more than 30 days a year?, When I select -Yes, an address within the UK- as respone, Then I am routed to 5a. Enter details of the other UK address where you stay more than 30 days a year?', function () {
    openAndStartCensusQuestionnaire('census_household.json', true)
    PermanentOrFamilyHome.clickPermanentOrFamilyHomeAnswerYes().submit()
    HouseholdComposition.setPersonName(0, 'John Smith').addPerson().setPersonName(1, 'Jane Smith').submit()
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
    Sex.clickSexAnswerMale().submit()
    DateOfBirth.setDateOfBirthAnswerDay(2).setDateOfBirthAnswerMonth(3).setDateOfBirthAnswerYear(1980).submit()
    Over16.clickOver16AnswerYes().submit()
    MaritalStatus.clickMaritalStatusAnswerMarried().submit()
    AnotherAddress.clickAnotherAddressAnswerYesAnAddressWithinTheUk().submit()
    OtherAddress.setOtherAddressAnswerBuilding('Gov Buildings').submit()
  })

  it('Given I am answering question 5 in the individual detail section -Do you stay at another address for more than 30 days a year?, When I select -Yes, an address outside the UK- and enter text in other field as respone, Then I am routed to 6. What is that address?', function () {
    openAndStartCensusQuestionnaire('census_household.json', true)
    PermanentOrFamilyHome.clickPermanentOrFamilyHomeAnswerYes().submit()
    HouseholdComposition.setPersonName(0, 'John Smith').addPerson().setPersonName(1, 'Jane Smith').submit()
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
    Sex.clickSexAnswerMale().submit()
    DateOfBirth.setDateOfBirthAnswerDay(2).setDateOfBirthAnswerMonth(3).setDateOfBirthAnswerYear(1980).submit()
    Over16.clickOver16AnswerYes().submit()
    MaritalStatus.clickMaritalStatusAnswerMarried().submit()
    AnotherAddress.clickAnotherAddressAnswerOther().submit()
    AddressType.clickAddressTypeAnswerArmedForcesBaseAddress().submit()
  })

  it('Given I am answering question 7 in the individual detail section - 7. Are you a schoolchild or student in full-time education?, When I dselect -No- as respone, Then I am routed to 9. What is your country of birth?', function () {
    openAndStartCensusQuestionnaire('census_household.json', true)
    PermanentOrFamilyHome.clickPermanentOrFamilyHomeAnswerYes().submit()
    HouseholdComposition.setPersonName(0, 'John Smith').addPerson().setPersonName(1, 'Jane Smith').submit()
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
    Sex.clickSexAnswerMale().submit()
    DateOfBirth.setDateOfBirthAnswerDay(2).setDateOfBirthAnswerMonth(3).setDateOfBirthAnswerYear(1980).submit()
    Over16.clickOver16AnswerYes().submit()
    MaritalStatus.clickMaritalStatusAnswerMarried().submit()
    AnotherAddress.clickAnotherAddressAnswerNo().submit()
    InEducation.clickInEducationAnswerNo().submit()
    CountryOfBirth.clickCountryOfBirthEnglandAnswerEngland().submit()
  })

// Issue 404
/*  it('Given I am answering question 7 in the individual detail section - 7. Are you a schoolchild or student in full-time education?, When I do not select any respone, Then I am routed to 9. What is your country of birth?', function () {
    openAndStartCensusQuestionnaire('census_household.json', true)
    PermanentOrFamilyHome.clickPermanentOrFamilyHomeAnswerYes().submit()
    HouseholdComposition.setPersonName(0, 'John Smith').addPerson().setPersonName(1, 'Jane Smith').submit()
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
    Sex.clickSexAnswerMale().submit()
    DateOfBirth.setDateOfBirthAnswerDay(2).setDateOfBirthAnswerMonth(3).setDateOfBirthAnswerYear(1980).submit()
    Over16.clickOver16AnswerYes().submit()
    MaritalStatus.clickMaritalStatusAnswerMarried().submit()
    AnotherAddress.clickAnotherAddressAnswerNo().submit()
    InEducation.submit()
    CountryOfBirth.clickCountryOfBirthEnglandAnswerEngland().submit()
  }) */

  it('Given I am answering question 7 in the individual detail section - 7. Are you a schoolchild or student in full-time education?, When I select -Yes- as respone, Then I am routed to 8. During term time, do you live:', function () {
    openAndStartCensusQuestionnaire('census_household.json', true)
    PermanentOrFamilyHome.clickPermanentOrFamilyHomeAnswerYes().submit()
    HouseholdComposition.setPersonName(0, 'John Smith').addPerson().setPersonName(1, 'Jane Smith').submit()
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
    Sex.clickSexAnswerMale().submit()
    DateOfBirth.setDateOfBirthAnswerDay(2).setDateOfBirthAnswerMonth(3).setDateOfBirthAnswerYear(1980).submit()
    Over16.clickOver16AnswerYes().submit()
    MaritalStatus.clickMaritalStatusAnswerMarried().submit()
    AnotherAddress.clickAnotherAddressAnswerNo().submit()
    InEducation.clickInEducationAnswerYes().submit()
    TermTimeLocation.clickTermTimeLocationAnswerAtThisAddress().submit()
  })

  it('Given I am answering question 12. Do you look after, or give any help or support..., When I select -No- as respone, Then I am routed to 13. How would you describe your national identity?', function () {
    openAndStartCensusQuestionnaire('census_household.json', true)
    PermanentOrFamilyHome.clickPermanentOrFamilyHomeAnswerYes().submit()
    HouseholdComposition.setPersonName(0, 'John Smith').addPerson().setPersonName(1, 'Jane Smith').submit()
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
    Sex.clickSexAnswerMale().submit()
    DateOfBirth.setDateOfBirthAnswerDay(2).setDateOfBirthAnswerMonth(3).setDateOfBirthAnswerYear(1980).submit()
    Over16.clickOver16AnswerYes().submit()
    MaritalStatus.clickMaritalStatusAnswerMarried().submit()
    AnotherAddress.clickAnotherAddressAnswerNo().submit()
    InEducation.clickInEducationAnswerYes().submit()
    TermTimeLocation.clickTermTimeLocationAnswerAtThisAddress().submit()
    CountryOfBirth.clickCountryOfBirthEnglandAnswerEngland().submit()
    Carer.clickCarerAnswerNo().submit()
    NationalIdentity.clickNationalIdentityAnswerBritish().submit()
  })

  it('Given I am answering question 12. Do you look after, or give any help or support..., When I select -Yes 1-19 Hours A Week- as respone, Then I am routed to 13. How would you describe your national identity?', function () {
    openAndStartCensusQuestionnaire('census_household.json', true)
    PermanentOrFamilyHome.clickPermanentOrFamilyHomeAnswerYes().submit()
    HouseholdComposition.setPersonName(0, 'John Smith').addPerson().setPersonName(1, 'Jane Smith').submit()
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
    Sex.clickSexAnswerMale().submit()
    DateOfBirth.setDateOfBirthAnswerDay(2).setDateOfBirthAnswerMonth(3).setDateOfBirthAnswerYear(1980).submit()
    Over16.clickOver16AnswerYes().submit()
    MaritalStatus.clickMaritalStatusAnswerMarried().submit()
    AnotherAddress.clickAnotherAddressAnswerNo().submit()
    InEducation.clickInEducationAnswerYes().submit()
    TermTimeLocation.clickTermTimeLocationAnswerAtThisAddress().submit()
    CountryOfBirth.clickCountryOfBirthEnglandAnswerEngland().submit()
    Carer.clickCarerAnswerYes119HoursAWeek().submit()
    NationalIdentity.clickNationalIdentityAnswerNorthernIrish().submit()
  })

  it('Given I am answering question 12. Do you look after, or give any help or support..., When I select -Yes 20-49 Hours A Week- as respone, Then I am routed to 13. How would you describe your national identity?', function () {
    openAndStartCensusQuestionnaire('census_household.json', true)
    PermanentOrFamilyHome.clickPermanentOrFamilyHomeAnswerYes().submit()
    HouseholdComposition.setPersonName(0, 'John Smith').addPerson().setPersonName(1, 'Jane Smith').submit()
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
    Sex.clickSexAnswerMale().submit()
    DateOfBirth.setDateOfBirthAnswerDay(2).setDateOfBirthAnswerMonth(3).setDateOfBirthAnswerYear(1980).submit()
    Over16.clickOver16AnswerYes().submit()
    MaritalStatus.clickMaritalStatusAnswerMarried().submit()
    AnotherAddress.clickAnotherAddressAnswerNo().submit()
    InEducation.clickInEducationAnswerYes().submit()
    TermTimeLocation.clickTermTimeLocationAnswerAtThisAddress().submit()
    CountryOfBirth.clickCountryOfBirthEnglandAnswerEngland().submit()
    Carer.clickCarerAnswerYes2049HoursAWeek().submit()
    NationalIdentity.clickNationalIdentityAnswerEnglish().submit()
  })

  it('Given I am answering question 12. Do you look after, or give any help or support..., When I select -Yes 50 or more Hours A Week- as respone, Then I am routed to 13. How would you describe your national identity?', function () {
    openAndStartCensusQuestionnaire('census_household.json', true)
    PermanentOrFamilyHome.clickPermanentOrFamilyHomeAnswerYes().submit()
    HouseholdComposition.setPersonName(0, 'John Smith').addPerson().setPersonName(1, 'Jane Smith').submit()
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
    Sex.clickSexAnswerMale().submit()
    DateOfBirth.setDateOfBirthAnswerDay(2).setDateOfBirthAnswerMonth(3).setDateOfBirthAnswerYear(1980).submit()
    Over16.clickOver16AnswerYes().submit()
    MaritalStatus.clickMaritalStatusAnswerMarried().submit()
    AnotherAddress.clickAnotherAddressAnswerNo().submit()
    InEducation.clickInEducationAnswerYes().submit()
    TermTimeLocation.clickTermTimeLocationAnswerAtThisAddress().submit()
    CountryOfBirth.clickCountryOfBirthEnglandAnswerEngland().submit()
    Carer.clickCarerAnswerYes50OrMoreHoursAWeek().submit()
    NationalIdentity.clickNationalIdentityAnswerScottish().submit()
  })

  it('Given I am answering question 25. Thinking of the last 12 months, have you..., When I select -No- as respone, Then I am routed to 26. Last week were you:', function () {
      openAndStartCensusQuestionnaire('census_household.json')

      // who-lives-here
      PermanentOrFamilyHome.clickPermanentOrFamilyHomeAnswerYes().submit()
      HouseholdComposition.setPersonName(0, 'John Smith').addPerson().setPersonName(1, 'Jane Smith').submit()
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
      Sex.clickSexAnswerMale().submit()
      DateOfBirth.setDateOfBirthAnswerDay(2).setDateOfBirthAnswerMonth(3).setDateOfBirthAnswerYear(1980).submit()
      Over16.clickOver16AnswerYes().submit()
      MaritalStatus.clickMaritalStatusAnswerMarried().submit()
      AnotherAddress.clickAnotherAddressAnswerNo().submit()
      InEducation.clickInEducationAnswerNo().submit()
      CountryOfBirth.clickCountryOfBirthEnglandAnswerEngland().submit()
      Carer.clickCarerAnswerNo().submit()
      NationalIdentity.clickNationalIdentityAnswerBritish().submit()
      EthnicGroup.clickEthnicGroupAnswerWhite().submit()
      WhiteEthnicGroup.clickWhiteEthnicGroupAnswerEnglishWelshScottishNorthernIrishBritish().submit()
      UnderstandWelsh.clickUnderstandWelshAnswerNoneOfTheAbove().submit()
      Language.clickLanguageAnswerEnglish().submit()
      Religion.clickReligionAnswerNoReligion().submit()
      PastUsualAddress.clickPastUsualAddressAnswerThisAddress().submit()
      Passports.clickPassportsAnswerUnitedKingdom().submit()
      Disability.clickDisabilityAnswerNo().submit()
      Qualifications.clickQualificationsAnswerUndergraduateDegree().submit()
      Volunteering.clickVolunteeringAnswerNo().submit()
      EmploymentType.clickEmploymentTypeAnswerWorkingAsAnEmployee().submit()
      HouseholdMemberCompleted.submit()
    })

    it('Given I am answering question 25. Thinking of the last 12 months, have you..., When I select -Yes, at least once a week- as respone, Then I am routed to 26. Last week were you:', function () {
        openAndStartCensusQuestionnaire('census_household.json')

        // who-lives-here
        PermanentOrFamilyHome.clickPermanentOrFamilyHomeAnswerYes().submit()
        HouseholdComposition.setPersonName(0, 'John Smith').addPerson().setPersonName(1, 'Jane Smith').submit()
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
        Sex.clickSexAnswerMale().submit()
        DateOfBirth.setDateOfBirthAnswerDay(2).setDateOfBirthAnswerMonth(3).setDateOfBirthAnswerYear(1980).submit()
        Over16.clickOver16AnswerYes().submit()
        MaritalStatus.clickMaritalStatusAnswerMarried().submit()
        AnotherAddress.clickAnotherAddressAnswerNo().submit()
        InEducation.clickInEducationAnswerNo().submit()
        CountryOfBirth.clickCountryOfBirthEnglandAnswerEngland().submit()
        Carer.clickCarerAnswerNo().submit()
        NationalIdentity.clickNationalIdentityAnswerBritish().submit()
        EthnicGroup.clickEthnicGroupAnswerWhite().submit()
        WhiteEthnicGroup.clickWhiteEthnicGroupAnswerEnglishWelshScottishNorthernIrishBritish().submit()
        UnderstandWelsh.clickUnderstandWelshAnswerNoneOfTheAbove().submit()
        Language.clickLanguageAnswerEnglish().submit()
        Religion.clickReligionAnswerNoReligion().submit()
        PastUsualAddress.clickPastUsualAddressAnswerThisAddress().submit()
        Passports.clickPassportsAnswerUnitedKingdom().submit()
        Disability.clickDisabilityAnswerNo().submit()
        Qualifications.clickQualificationsAnswerUndergraduateDegree().submit()
        Volunteering.clickVolunteeringAnswerYesAtLeastOnceAWeek().submit()
        EmploymentType.clickEmploymentTypeAnswerWorkingAsAnEmployee().submit()
        HouseholdMemberCompleted.submit()
      })

      it('Given I am answering question 25. Thinking of the last 12 months, have you..., When I select -Yes, less than once a week but at least once a month-, at least once a week- as respone, Then I am routed to 26. Last week were you:', function () {
          openAndStartCensusQuestionnaire('census_household.json')

          // who-lives-here
          PermanentOrFamilyHome.clickPermanentOrFamilyHomeAnswerYes().submit()
          HouseholdComposition.setPersonName(0, 'John Smith').addPerson().setPersonName(1, 'Jane Smith').submit()
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
          Sex.clickSexAnswerMale().submit()
          DateOfBirth.setDateOfBirthAnswerDay(2).setDateOfBirthAnswerMonth(3).setDateOfBirthAnswerYear(1980).submit()
          Over16.clickOver16AnswerYes().submit()
          MaritalStatus.clickMaritalStatusAnswerMarried().submit()
          AnotherAddress.clickAnotherAddressAnswerNo().submit()
          InEducation.clickInEducationAnswerNo().submit()
          CountryOfBirth.clickCountryOfBirthEnglandAnswerEngland().submit()
          Carer.clickCarerAnswerNo().submit()
          NationalIdentity.clickNationalIdentityAnswerBritish().submit()
          EthnicGroup.clickEthnicGroupAnswerWhite().submit()
          WhiteEthnicGroup.clickWhiteEthnicGroupAnswerEnglishWelshScottishNorthernIrishBritish().submit()
          UnderstandWelsh.clickUnderstandWelshAnswerNoneOfTheAbove().submit()
          Language.clickLanguageAnswerEnglish().submit()
          Religion.clickReligionAnswerNoReligion().submit()
          PastUsualAddress.clickPastUsualAddressAnswerThisAddress().submit()
          Passports.clickPassportsAnswerUnitedKingdom().submit()
          Disability.clickDisabilityAnswerNo().submit()
          Qualifications.clickQualificationsAnswerUndergraduateDegree().submit()
          Volunteering.clickVolunteeringAnswerYesLessThanOnceAWeekButAtLeastOnceAMonth().submit()
          EmploymentType.clickEmploymentTypeAnswerWorkingAsAnEmployee().submit()
          HouseholdMemberCompleted.submit()
        })

      it('Given I am answering question 25. Thinking of the last 12 months, have you..., When I select -Yes, less often-, at least once a week- as respone, Then I am routed to 26. Last week were you:', function () {
            openAndStartCensusQuestionnaire('census_household.json')

            // who-lives-here
            PermanentOrFamilyHome.clickPermanentOrFamilyHomeAnswerYes().submit()
            HouseholdComposition.setPersonName(0, 'John Smith').addPerson().setPersonName(1, 'Jane Smith').submit()
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
            Sex.clickSexAnswerMale().submit()
            DateOfBirth.setDateOfBirthAnswerDay(2).setDateOfBirthAnswerMonth(3).setDateOfBirthAnswerYear(1980).submit()
            Over16.clickOver16AnswerYes().submit()
            MaritalStatus.clickMaritalStatusAnswerMarried().submit()
            AnotherAddress.clickAnotherAddressAnswerNo().submit()
            InEducation.clickInEducationAnswerNo().submit()
            CountryOfBirth.clickCountryOfBirthEnglandAnswerEngland().submit()
            Carer.clickCarerAnswerNo().submit()
            NationalIdentity.clickNationalIdentityAnswerBritish().submit()
            EthnicGroup.clickEthnicGroupAnswerWhite().submit()
            WhiteEthnicGroup.clickWhiteEthnicGroupAnswerEnglishWelshScottishNorthernIrishBritish().submit()
            UnderstandWelsh.clickUnderstandWelshAnswerNoneOfTheAbove().submit()
            Language.clickLanguageAnswerEnglish().submit()
            Religion.clickReligionAnswerNoReligion().submit()
            PastUsualAddress.clickPastUsualAddressAnswerThisAddress().submit()
            Passports.clickPassportsAnswerUnitedKingdom().submit()
            Disability.clickDisabilityAnswerNo().submit()
            Qualifications.clickQualificationsAnswerUndergraduateDegree().submit()
            Volunteering.clickVolunteeringAnswerYesLessOften().submit()
            EmploymentType.clickEmploymentTypeAnswerWorkingAsAnEmployee().submit()
            HouseholdMemberCompleted.submit()
    })
})
