import chai from 'chai'
import {getRandomString} from '../helpers'
import devPage from '../pages/dev.page'
import landingPage from '../pages/landing.page'

import HouseholdMemberBegin from '../pages/surveys/census/household/household-member-begin.page.js'
import DetailsCorrect from '../pages/surveys/census/household/details-correct.page.js'
import CorrectName from '../pages/surveys/census/household/correct-name.page.js'
import Sex from '../pages/surveys/census/household/sex.page.js'
import DateOfBirth from '../pages/surveys/census/household/date-of-birth.page.js'
import Over16 from '../pages/surveys/census/household/over-16.page.js'
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
import Confirmation from '../pages/confirmation.page.js'
import ThankYou from '../pages/thank-you.page'

const expect = chai.expect

describe('Census Individual', function () {

    const openAndStartQuestionnaire = (schema, sexual_identity = false, region = 'GB-ENG') => {
        devPage.open()
            .setUserId(getRandomString(10))
            .setCollectionId(getRandomString(10))
            .setSchema(schema)
            .setRegionCode(region)

        if (sexual_identity)
            devPage.checkSexualIdentity()

        devPage.submit()
        landingPage.getStarted()
    }

    it('Given Respondent Home has identified the respondent should have the Individual Questionnaire without the sexual id question, When I complete the EQ, Then I should not be asked the sexual id question', function () {
        openAndStartQuestionnaire('census_individual.json')

        // household-member
        HouseholdMemberBegin.submit()
        DetailsCorrect.clickDetailsCorrectAnswerYesThisIsMyFullName().submit()
        Sex.clickSexAnswerMale().submit()
        DateOfBirth.setDateOfBirthAnswerDay(2).setDateOfBirthAnswerYear(1980).submit()
        Over16.clickOver16AnswerYes().submit()
        MaritalStatus.clickMaritalStatusAnswerMarried().submit()
        AnotherAddress.clickAnotherAddressAnswerNo().submit()
        InEducation.clickInEducationAnswerNo().submit()
        CountryOfBirth.clickCountryOfBirthEnglandAnswerEngland().submit()
        Carer.clickCarerAnswerNo().submit()
        NationalIdentity.clickNationalIdentityAnswerBritish().submit()
        EthnicGroup.clickEthnicGroupAnswerWhite().submit()
        WhiteEthnicGroup.clickWhiteEthnicGroupAnswerEnglishWelshScottishNorthernIrishBritish().submit()
        // SexualIdentity.clickSexualIdentityAnswerHeterosexualOrStraight().submit()
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

        browser.debug

        Confirmation.submit()

        // Thank You
        expect(ThankYou.isOpen()).to.be.true

    })

    it('Given Respondent Home has identified the respondent should have the Individual Questionnaire with the sexual id question, When I complete the EQ, Then I should be asked the sexual id question', function () {
        openAndStartQuestionnaire('census_individual.json', true)

        // household-member
        HouseholdMemberBegin.submit()
        DetailsCorrect.clickDetailsCorrectAnswerYesThisIsMyFullName().submit()
        Sex.clickSexAnswerMale().submit()
        DateOfBirth.setDateOfBirthAnswerDay(2).setDateOfBirthAnswerYear(1980).submit()
        Over16.clickOver16AnswerYes().submit()
        MaritalStatus.clickMaritalStatusAnswerMarried().submit()
        AnotherAddress.clickAnotherAddressAnswerNo().submit()
        InEducation.clickInEducationAnswerNo().submit()
        CountryOfBirth.clickCountryOfBirthEnglandAnswerEngland().submit()
        Carer.clickCarerAnswerNo().submit()
        NationalIdentity.clickNationalIdentityAnswerBritish().submit()
        EthnicGroup.clickEthnicGroupAnswerWhite().submit()
        WhiteEthnicGroup.clickWhiteEthnicGroupAnswerEnglishWelshScottishNorthernIrishBritish().submit()
        SexualIdentity.clickSexualIdentityAnswerHeterosexualOrStraight().submit()
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

        Confirmation.submit()

        // Thank You
        expect(ThankYou.isOpen()).to.be.true

    })

})

