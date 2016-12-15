import chai from 'chai'
import {startCensusQuestionnaire} from '../helpers'

import PermanentOrFamilyHome from '../pages/surveys/census/household/permanent-or-family-home.page.js'
import ElsePermanentOrFamilyHome from '../pages/surveys/census/household/else-permanent-or-family-home.page.js'
import HouseholdComposition from '../pages/surveys/census/household/household-composition.page.js'
import EveryoneAtAddressConfirmation from '../pages/surveys/census/household/everyone-at-address-confirmation.page.js'
import OvernightVisitors from '../pages/surveys/census/household/overnight-visitors.page.js'
import HouseholdRelationships from '../pages/surveys/census/household/household-relationships.page.js'
import WhoLivesHereCompleted from '../pages/surveys/census/household/who-lives-here-completed.page.js'
import TypeOfAccommodation from '../pages/surveys/census/household/type-of-accommodation.page.js'
import TypeOfHouse from '../pages/surveys/census/household/type-of-house.page.js'
import TypeOfFlat from '../pages/surveys/census/household/type-of-flat.page.js'
import SelfContainedAccommodation from '../pages/surveys/census/household/self-contained-accommodation.page.js'
import NumberOfBedrooms from '../pages/surveys/census/household/number-of-bedrooms.page.js'
import CentralHeating from '../pages/surveys/census/household/central-heating.page.js'
import OwnOrRent from '../pages/surveys/census/household/own-or-rent.page.js'
import Landlord from '../pages/surveys/census/household/landlord.page.js'
import NumberOfVehicles from '../pages/surveys/census/household/number-of-vehicles.page.js'
import HouseholdAndAccommodationCompleted from '../pages/surveys/census/household/household-and-accommodation-completed.page.js'
import HouseholdMemberBegin from '../pages/surveys/census/household/household-member-begin.page.js'
import DetailsCorrect from '../pages/surveys/census/household/details-correct.page.js'
import CorrectName from '../pages/surveys/census/household/correct-name.page.js'
import Over16 from '../pages/surveys/census/household/over-16.page.js'
import PrivateResponse from '../pages/surveys/census/household/private-response.page.js'
import RequestPrivateResponse from '../pages/surveys/census/household/request-private-response.page.js'
import Sex from '../pages/surveys/census/household/sex.page.js'
import DateOfBirth from '../pages/surveys/census/household/date-of-birth.page.js'
import MaritalStatus from '../pages/surveys/census/household/marital-status.page.js'
import AnotherAddress from '../pages/surveys/census/household/another-address.page.js'
import OtherAddress from '../pages/surveys/census/household/other-address.page.js'
import AddressType from '../pages/surveys/census/household/address-type.page.js'
import InEducation from '../pages/surveys/census/household/in-education.page.js'
import TermTimeLocation from '../pages/surveys/census/household/term-time-location.page.js'
import CountryOfBirth from '../pages/surveys/census/household/country-of-birth.page.js'
import ArriveInUk from '../pages/surveys/census/household/arrive-in-uk.page.js'
import LengthOfStay from '../pages/surveys/census/household/length-of-stay.page.js'
import Carer from '../pages/surveys/census/household/carer.page.js'
import NationalIdentity from '../pages/surveys/census/household/national-identity.page.js'
import EthnicGroup from '../pages/surveys/census/household/ethnic-group.page.js'
import WhiteEthnicGroup from '../pages/surveys/census/household/white-ethnic-group.page.js'
import MixedEthnicGroup from '../pages/surveys/census/household/mixed-ethnic-group.page.js'
import AsianEthnicGroup from '../pages/surveys/census/household/asian-ethnic-group.page.js'
import BlackEthnicGroup from '../pages/surveys/census/household/black-ethnic-group.page.js'
import OtherEthnicGroup from '../pages/surveys/census/household/other-ethnic-group.page.js'
import SexualIdentity from '../pages/surveys/census/household/sexual-identity.page.js'
import UnderstandWelsh from '../pages/surveys/census/household/understand-welsh.page.js'
import Language from '../pages/surveys/census/household/language.page.js'
import English from '../pages/surveys/census/household/english.page.js'
import Religion from '../pages/surveys/census/household/religion.page.js'
import PastUsualAddress from '../pages/surveys/census/household/past-usual-address.page.js'
import LastYearAddress from '../pages/surveys/census/household/last-year-address.page.js'
import Passports from '../pages/surveys/census/household/passports.page.js'
import OtherPassports from '../pages/surveys/census/household/other-passports.page.js'
import Disability from '../pages/surveys/census/household/disability.page.js'
import Qualifications from '../pages/surveys/census/household/qualifications.page.js'
import Volunteering from '../pages/surveys/census/household/volunteering.page.js'
import EmploymentType from '../pages/surveys/census/household/employment-type.page.js'
import Jobseeker from '../pages/surveys/census/household/jobseeker.page.js'
import JobAvailability from '../pages/surveys/census/household/job-availability.page.js'
import JobPending from '../pages/surveys/census/household/job-pending.page.js'
import Occupation from '../pages/surveys/census/household/occupation.page.js'
import EverWorked from '../pages/surveys/census/household/ever-worked.page.js'
import MainJob from '../pages/surveys/census/household/main-job.page.js'
import JobTitle from '../pages/surveys/census/household/job-title.page.js'
import JobDescription from '../pages/surveys/census/household/job-description.page.js'
import EmployersBusiness from '../pages/surveys/census/household/employers-business.page.js'
import MainJobType from '../pages/surveys/census/household/main-job-type.page.js'
import BusinessName from '../pages/surveys/census/household/business-name.page.js'
import HouseholdMemberCompleted from '../pages/surveys/census/household/household-member-completed.page.js'
import VisitorBegin from '../pages/surveys/census/household/visitor-begin.page.js'
import VisitorName from '../pages/surveys/census/household/visitor-name.page.js'
import VisitorSex from '../pages/surveys/census/household/visitor-sex.page.js'
import VisitorDateOfBirth from '../pages/surveys/census/household/visitor-date-of-birth.page.js'
import VisitorUkResident from '../pages/surveys/census/household/visitor-uk-resident.page.js'
import VisitorAddress from '../pages/surveys/census/household/visitor-address.page.js'
import VisitorCompleted from '../pages/surveys/census/household/visitor-completed.page.js'
import VisitorsCompleted from '../pages/surveys/census/household/visitors-completed.page.js'
import Confirmation from '../pages/confirmation.page.js'
import ThankYou from '../pages/thank-you.page'

const expect = chai.expect

describe('Census Household', function () {

    it('Given Respondent Home has identified the respondent should have the Household Questionnaire without the sexual id question, When I complete the EQ, Then I should not be asked the sexual id question', function () {
        startCensusQuestionnaire('census_household.json')

        // who-lives-here
        PermanentOrFamilyHome.clickPermanentOrFamilyHomeAnswerYes().submit()
        HouseholdComposition.setFirstName('John').submit()
        EveryoneAtAddressConfirmation.clickEveryoneAtAddressConfirmationAnswerYes().submit()
        OvernightVisitors.setOvernightVisitorsAnswer(1).submit()
        WhoLivesHereCompleted.submit()

        // household-and-accommodation
        completeHouseholdAndAccommodation()

        // household-member
        completeHouseholdDetails()

        // visitors
        completeVisitorSection()
        VisitorsCompleted.submit()

        Confirmation.submit()

        // Thank You
        expect(ThankYou.isOpen()).to.be.true
    })

    it('Given Respondent Home has identified the respondent should have the Household Questionnaire with the sexual id question, When I complete the EQ, Then I should be asked the sexual id question', function () {
        startCensusQuestionnaire('census_household.json', true)

        // who-lives-here
        PermanentOrFamilyHome.clickPermanentOrFamilyHomeAnswerYes().submit()
        HouseholdComposition.setFirstName('John').submit()
        EveryoneAtAddressConfirmation.clickEveryoneAtAddressConfirmationAnswerYes().submit()
        OvernightVisitors.setOvernightVisitorsAnswer(1).submit()
        WhoLivesHereCompleted.submit()

        // household-and-accommodation
        completeHouseholdAndAccommodation()

        // household-member
        HouseholdMemberBegin.submit()
        DetailsCorrect.clickDetailsCorrectAnswerYesThisIsMyFullName().submit()
        Over16.clickOver16AnswerYes().submit()
        PrivateResponse.clickPrivateResponseAnswerNoIDoNotWantToRequestAPersonalForm().submit()
        Sex.clickSexAnswerMale().submit()
        DateOfBirth.setDateOfBirthAnswerDay(2).setDateOfBirthAnswerMonth(3).setDateOfBirthAnswerYear(1980).submit()
        MaritalStatus.clickMaritalStatusAnswerMarried().submit()
        AnotherAddress.clickAnotherAddressAnswerNo().submit()
        InEducation.clickInEducationAnswerNo().submit()
        CountryOfBirth.clickCountryOfBirthEnglandAnswerEngland().submit()
        Carer.clickCarerAnswerNo().submit()
        NationalIdentity.clickNationalIdentityEnglandAnswerEnglish().submit()
        EthnicGroup.clickEthnicGroupEnglandAnswerMixedMultipleEthnicGroups().submit()
        MixedEthnicGroup.clickMixedEthnicGroupAnswerWhiteAndAsian().submit()
        SexualIdentity.clickSexualIdentityAnswerHeterosexualOrStraight().submit()
        Language.clickLanguageEnglandAnswerEnglish().submit()
        Religion.clickReligionAnswerNoReligion().submit()
        PastUsualAddress.clickPastUsualAddressAnswerThisAddress().submit()
        Passports.clickPassportsAnswerUnitedKingdom().submit()
        Disability.clickDisabilityAnswerNo().submit()
        Qualifications.clickQualificationsEnglandAnswerUndergraduateDegree().submit()
        Volunteering.clickVolunteeringAnswerNo().submit()
        EmploymentType.clickEmploymentTypeAnswerWorkingAsAnEmployee().submit()
        MainJob.clickMainJobAnswerAnEmployee().submit()
        JobTitle.setJobTitleAnswer('Dev').submit()
        JobDescription.setJobDescriptionAnswer('writing lots of code').submit()
        EmployersBusiness.setEmployersBusinessAnswer('something statistical').submit()
        MainJobType.clickMainJobTypeAnswerEmployedByAnOrganisationOrBusiness().submit()
        BusinessName.setBusinessNameAnswer('ONS').submit()
        HouseholdMemberCompleted.submit()

        // visitors
        completeVisitorSection()
        VisitorsCompleted.submit()

        Confirmation.submit()

        // Thank You
        expect(ThankYou.isOpen()).to.be.true
    })

    it('Given I have added a householder, When I request a private response for that person, Then I don\'t have to complete any more questions for them', function () {
        startCensusQuestionnaire('census_household.json', true)

        // who-lives-here
        PermanentOrFamilyHome.clickPermanentOrFamilyHomeAnswerYes().submit()

        // Given I have added a householder
        HouseholdComposition.setFirstName(0, 'Pete').submit()
        EveryoneAtAddressConfirmation.clickEveryoneAtAddressConfirmationAnswerYes().submit()
        OvernightVisitors.setOvernightVisitorsAnswer(1).submit()
        WhoLivesHereCompleted.submit()

        // household-and-accommodation
        completeHouseholdAndAccommodation()

        // household-member
        HouseholdMemberBegin.submit()
        DetailsCorrect.clickDetailsCorrectAnswerYesThisIsMyFullName().submit()
        Over16.clickOver16AnswerYes().submit()

        // When I request a private response for that person
        PrivateResponse.clickPrivateResponseAnswerYesIWantToRequestAPersonalForm().submit()
        RequestPrivateResponse.submit()

        // Then I don\'t have to complete any more questions for them
        HouseholdMemberCompleted.submit()

        // visitors
        completeVisitorSection()
        VisitorsCompleted.submit()

        Confirmation.submit()

        // Thank You
        expect(ThankYou.isOpen()).to.be.true
    })

    it('Given a census household survey with welsh region, When i enter valid data, Then the survey should submit successfully', function () {
        startCensusQuestionnaire('census_household.json', false, 'GB-WLS')

        // who-lives-here
        PermanentOrFamilyHome.clickPermanentOrFamilyHomeAnswerYes().submit()
        HouseholdComposition.setFirstName('John').submit()
        EveryoneAtAddressConfirmation.clickEveryoneAtAddressConfirmationAnswerYes().submit()
        OvernightVisitors.setOvernightVisitorsAnswer(1).submit()
        WhoLivesHereCompleted.submit()

        // household-and-accommodation
        completeHouseholdAndAccommodation()

        // household-member
        HouseholdMemberBegin.submit()
        DetailsCorrect.clickDetailsCorrectAnswerYesThisIsMyFullName().submit()
        Over16.clickOver16AnswerYes().submit()
        PrivateResponse.clickPrivateResponseAnswerNoIDoNotWantToRequestAPersonalForm().submit()
        Sex.clickSexAnswerMale().submit()
        DateOfBirth.setDateOfBirthAnswerDay(2).setDateOfBirthAnswerMonth(4).setDateOfBirthAnswerYear(1980).submit()
        MaritalStatus.clickMaritalStatusAnswerMarried().submit()
        AnotherAddress.clickAnotherAddressAnswerNo().submit()
        InEducation.clickInEducationAnswerNo().submit()
        CountryOfBirth.clickCountryOfBirthWalesAnswerWales().submit()
        Carer.clickCarerAnswerNo().submit()
        NationalIdentity.clickNationalIdentityWalesAnswerWelsh().submit()
        EthnicGroup.clickEthnicGroupWalesAnswerAsianAsianBritish().submit()
        AsianEthnicGroup.clickAsianEthnicGroupAnswerIndian().submit()
        UnderstandWelsh.clickUnderstandWelshAnswerNoneOfTheAbove().submit()
        Language.clickLanguageWelshAnswerEnglishOrWelsh().submit()
        Religion.clickReligionWelshAnswerNoReligion().submit()
        PastUsualAddress.clickPastUsualAddressAnswerThisAddress().submit()
        Passports.clickPassportsAnswerUnitedKingdom().submit()
        Disability.clickDisabilityAnswerNo().submit()
        Qualifications.clickQualificationsWelshAnswerUndergraduateDegree().submit()
        Volunteering.clickVolunteeringAnswerNo().submit()
        EmploymentType.clickEmploymentTypeAnswerWorkingAsAnEmployee().clickEmploymentTypeAnswerOnAGovernmentSponsoredTrainingScheme().submit()
        MainJob.clickMainJobAnswerAnEmployee().submit()
        JobTitle.setJobTitleAnswer('Dev').submit()
        JobDescription.setJobDescriptionAnswer('writing lots of code').submit()
        EmployersBusiness.setEmployersBusinessAnswer('something statistical').submit()
        MainJobType.clickMainJobTypeAnswerEmployedByAnOrganisationOrBusiness().submit()
        BusinessName.setBusinessNameAnswer('ONS').submit()
        HouseholdMemberCompleted.submit()

        // visitors
        completeVisitorSection()
        VisitorsCompleted.submit()

        Confirmation.submit()

        // Thank You
        expect(ThankYou.isOpen()).to.be.true
    })

    it('Given a census household survey, When one person in household, Then persons name should appear on member details pages.', function () {
        startCensusQuestionnaire('census_household.json', false, 'GB-WLS')

        // who-lives-here
        var person = 'John'

        PermanentOrFamilyHome.clickPermanentOrFamilyHomeAnswerYes().submit()
        HouseholdComposition.setFirstName(person).submit()
        EveryoneAtAddressConfirmation.clickEveryoneAtAddressConfirmationAnswerYes().submit()
        OvernightVisitors.setOvernightVisitorsAnswer(1).submit()
        WhoLivesHereCompleted.submit()

        // household-and-accommodation
        completeHouseholdAndAccommodation()

        // household-member
        HouseholdMemberBegin.submit()
        expect(HouseholdMemberBegin.getDisplayedName()).to.contain(person)
        DetailsCorrect.clickDetailsCorrectAnswerYesThisIsMyFullName().submit()
        expect(DetailsCorrect.getDisplayedName()).to.contain(person)
        Over16.clickOver16AnswerYes().submit()
        expect(Over16.getDisplayedName()).to.contain(person)
        PrivateResponse.clickPrivateResponseAnswerNoIDoNotWantToRequestAPersonalForm().submit()
        expect(PrivateResponse.getDisplayedName()).to.contain(person)
        Sex.clickSexAnswerMale().submit()
        expect(Sex.getDisplayedName()).to.contain(person)
        DateOfBirth.setDateOfBirthAnswerDay(2).setDateOfBirthAnswerMonth(4).setDateOfBirthAnswerYear(1980).submit()
        expect(DateOfBirth.getDisplayedName()).to.contain(person)
        MaritalStatus.clickMaritalStatusAnswerMarried().submit()
        expect(MaritalStatus.getDisplayedName()).to.contain(person)
        AnotherAddress.clickAnotherAddressAnswerNo().submit()
        expect(AnotherAddress.getDisplayedName()).to.contain(person)
        InEducation.clickInEducationAnswerNo().submit()
        expect(InEducation.getDisplayedName()).to.contain(person)
        CountryOfBirth.clickCountryOfBirthWalesAnswerWales().submit()
        expect(CountryOfBirth.getDisplayedName()).to.contain(person)
        Carer.clickCarerAnswerNo().submit()
        expect(Carer.getDisplayedName()).to.contain(person)
        NationalIdentity.clickNationalIdentityWalesAnswerWelsh().submit()
        expect(NationalIdentity.getDisplayedName()).to.contain(person)
        EthnicGroup.clickEthnicGroupWalesAnswerBlackAfricanCaribbeanBlackBritish().submit()
        expect(EthnicGroup.getDisplayedName()).to.contain(person)
        BlackEthnicGroup.clickBlackEthnicGroupAnswerAfrican().submit()
        expect(WhiteEthnicGroup.getDisplayedName()).to.contain(person)
        UnderstandWelsh.clickUnderstandWelshAnswerNoneOfTheAbove().submit()
        expect(UnderstandWelsh.getDisplayedName()).to.contain(person)
        Language.clickLanguageWelshAnswerEnglishOrWelsh().submit()
        expect(Language.getDisplayedName()).to.contain(person)
        Religion.clickReligionWelshAnswerNoReligion().submit()
        expect(Religion.getDisplayedName()).to.contain(person)
        PastUsualAddress.clickPastUsualAddressAnswerThisAddress().submit()
        expect(PastUsualAddress.getDisplayedName()).to.contain(person)
        Passports.clickPassportsAnswerUnitedKingdom().submit()
        expect(Passports.getDisplayedName()).to.contain(person)
        Disability.clickDisabilityAnswerNo().submit()
        expect(Disability.getDisplayedName()).to.contain(person)
        Qualifications.clickQualificationsWelshAnswerUndergraduateDegree().submit()
        expect(Qualifications.getDisplayedName()).to.contain(person)
        Volunteering.clickVolunteeringAnswerNo().submit()
        expect(Volunteering.getDisplayedName()).to.contain(person)
        EmploymentType.clickEmploymentTypeAnswerNoneOfTheAbove().submit()
        Jobseeker.clickJobseekerAnswerYes().submit()
        JobAvailability.clickJobAvailabilityAnswerYes().submit()
        JobPending.clickJobPendingAnswerNo().submit()
        Occupation.clickOccupationAnswerAStudent().submit()
        EverWorked.clickEverWorkedAnswerYes().submit()
        MainJob.clickMainJobAnswerAnEmployee().submit()
        JobTitle.setJobTitleAnswer('Dev').submit()
        JobDescription.setJobDescriptionAnswer('writing lots of code').submit()
        EmployersBusiness.setEmployersBusinessAnswer('something statistical').submit()
        MainJobType.clickMainJobTypeAnswerEmployedByAnOrganisationOrBusiness().submit()
        BusinessName.setBusinessNameAnswer('ONS').submit()
        HouseholdMemberCompleted.submit()

        // visitors
        completeVisitorSection()
        VisitorsCompleted.submit()

        Confirmation.submit()

        // Thank You
        expect(ThankYou.isOpen()).to.be.true
    })

    it('Given two people are in the household, When I complete the household details for person one, Then I should be asked household details for person two.', function () {
        startCensusQuestionnaire('census_household.json')

        // who-lives-here
        PermanentOrFamilyHome.clickPermanentOrFamilyHomeAnswerYes().submit()
        HouseholdComposition.setFirstName('John').addPerson().setFirstName('Jane', 1).submit()
        EveryoneAtAddressConfirmation.clickEveryoneAtAddressConfirmationAnswerYes().submit()
        OvernightVisitors.setOvernightVisitorsAnswer(1).submit()
        HouseholdRelationships.clickHouseholdRelationshipsAnswerHusbandOrWife().submit()
        WhoLivesHereCompleted.submit()

        // household-and-accommodation
        completeHouseholdAndAccommodation()

        // household-member
        completeHouseholdDetails()
        completeHouseholdDetails()

        // visitors
        completeVisitorSection()
        VisitorsCompleted.submit()

        Confirmation.submit()

        // Thank You
        expect(ThankYou.isOpen()).to.be.true
    })

    it('Given I have two visitors, When I complete the visitor details for person one, Then I should be asked visitor details for person two.', function () {
        startCensusQuestionnaire('census_household.json')

        // who-lives-here
        PermanentOrFamilyHome.clickPermanentOrFamilyHomeAnswerYes().submit()
        HouseholdComposition.setFirstName('John').submit()
        EveryoneAtAddressConfirmation.clickEveryoneAtAddressConfirmationAnswerYes().submit()
        OvernightVisitors.setOvernightVisitorsAnswer(2).submit()
        WhoLivesHereCompleted.submit()

        // household-and-accommodation
        completeHouseholdAndAccommodation()

        // household-member
        completeHouseholdDetails()

        // Complete visitors for 2 people
        completeVisitorSection()
        completeVisitorSection()
        VisitorsCompleted.submit()

        Confirmation.submit()

        // Thank You
        expect(ThankYou.isOpen()).to.be.true
    })

    it('Given I do not enter a first name, When I save and continue, Then I should see errors that suggests first name is mandatory.', function () {
        startCensusQuestionnaire('census_household.json', false, 'GB-WLS')

        // who-lives-here
        PermanentOrFamilyHome.clickPermanentOrFamilyHomeAnswerYes().submit()
        HouseholdComposition.submit()

        expect(HouseholdComposition.getErrorMsg()).to.contain('Please enter a name or remove the person to continue')
    })

    it('Given I enter a first name but no middle or surname, When I save and continue, Then I should not see any errors', function () {
        startCensusQuestionnaire('census_household.json', false, 'GB-WLS')

        // who-lives-here
        PermanentOrFamilyHome.clickPermanentOrFamilyHomeAnswerYes().submit()
        HouseholdComposition.setFirstName('John').submit()
        expect(EveryoneAtAddressConfirmation.isOpen()).to.be.true
    })

    function completeHouseholdAndAccommodation() {
        TypeOfAccommodation.clickTypeOfAccommodationAnswerWholeHouseOrBungalow().submit()
        TypeOfHouse.clickTypeOfHouseAnswerSemiDetached().submit()
        SelfContainedAccommodation.clickSelfContainedAccommodationAnswerYesAllTheRoomsAreBehindADoorThatOnlyThisHouseholdCanUse().submit()
        NumberOfBedrooms.setNumberOfBedroomsAnswer(3).submit()
        CentralHeating.clickCentralHeatingAnswerGas().submit()
        OwnOrRent.clickOwnOrRentAnswerOwnsOutright().submit()
        NumberOfVehicles.setNumberOfVehiclesAnswer(2).submit()
        HouseholdAndAccommodationCompleted.submit()
    }

    function completeVisitorSection() {
        VisitorBegin.submit()
        VisitorName.setVisitorFirstName("Jane").setVisitorLastName("Doe").submit()
        VisitorSex.clickVisitorSexAnswerFemale().submit()
        VisitorDateOfBirth.setVisitorDateOfBirthAnswerDay(10).setVisitorDateOfBirthAnswerMonth(7).setVisitorDateOfBirthAnswerYear(1990).submit()
        VisitorUkResident.clickVisitorUkResidentAnswerYesUsuallyLivesInTheUnitedKingdom().submit()
        VisitorAddress.setVisitorAddressAnswerBuilding(50).setVisitorAddressAnswerStreet("My Road").setVisitorAddressAnswerCity("Newport").setVisitorAddressAnswerPostcode("AB123CD").submit()
        VisitorCompleted.submit()
    }

    function completeHouseholdDetails() {
        HouseholdMemberBegin.submit()
        DetailsCorrect.clickDetailsCorrectAnswerYesThisIsMyFullName().submit()
        Over16.clickOver16AnswerYes().submit()
        PrivateResponse.clickPrivateResponseAnswerNoIDoNotWantToRequestAPersonalForm().submit()
        Sex.clickSexAnswerMale().submit()
        DateOfBirth.setDateOfBirthAnswerDay(2).setDateOfBirthAnswerMonth(3).setDateOfBirthAnswerYear(1980).submit()
        MaritalStatus.clickMaritalStatusAnswerMarried().submit()
        AnotherAddress.clickAnotherAddressAnswerNo().submit()
        InEducation.clickInEducationAnswerNo().submit()
        CountryOfBirth.clickCountryOfBirthEnglandAnswerEngland().submit()
        Carer.clickCarerAnswerNo().submit()
        NationalIdentity.clickNationalIdentityEnglandAnswerEnglish().submit()
        EthnicGroup.clickEthnicGroupEnglandAnswerWhite().submit()
        WhiteEthnicGroup.clickWhiteEthnicGroupEnglandAnswerEnglishWelshScottishNorthernIrishBritish().submit()
        Language.clickLanguageEnglandAnswerEnglish().submit()
        Religion.clickReligionAnswerNoReligion().submit()
        PastUsualAddress.clickPastUsualAddressAnswerThisAddress().submit()
        Passports.clickPassportsAnswerUnitedKingdom().submit()
        Disability.clickDisabilityAnswerNo().submit()
        Qualifications.clickQualificationsEnglandAnswerUndergraduateDegree().submit()
        Volunteering.clickVolunteeringAnswerNo().submit()
        EmploymentType.clickEmploymentTypeAnswerNoneOfTheAbove().submit()
        Jobseeker.clickJobseekerAnswerYes().submit()
        JobAvailability.clickJobAvailabilityAnswerYes().submit()
        JobPending.clickJobPendingAnswerNo().submit()
        Occupation.clickOccupationAnswerAStudent().submit()
        EverWorked.clickEverWorkedAnswerYes().submit()
        MainJob.clickMainJobAnswerAnEmployee().submit()
        JobTitle.setJobTitleAnswer('Dev').submit()
        JobDescription.setJobDescriptionAnswer('writing lots of code').submit()
        EmployersBusiness.setEmployersBusinessAnswer('something statistical').submit()
        MainJobType.clickMainJobTypeAnswerEmployedByAnOrganisationOrBusiness().submit()
        BusinessName.setBusinessNameAnswer('ONS').submit()
        HouseholdMemberCompleted.submit()
    }

})
