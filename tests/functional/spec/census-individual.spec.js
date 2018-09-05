const helpers = require('../helpers');

const CorrectNamePage = require('../pages/surveys/census/individual/correct-name.page.js');
const SexPage = require('../pages/surveys/census/individual/sex.page.js');
const DateOfBirthPage = require('../pages/surveys/census/individual/date-of-birth.page.js');
const MaritalStatusPage = require('../pages/surveys/census/individual/marital-status.page.js');
const AnotherAddressPage = require('../pages/surveys/census/individual/another-address.page.js');
const InEducationPage = require('../pages/surveys/census/individual/in-education.page.js');
const CountryOfBirthPage = require('../pages/surveys/census/individual/country-of-birth.page.js');
const CarerPage = require('../pages/surveys/census/individual/carer.page.js');
const NationalIdentityPage = require('../pages/surveys/census/individual/national-identity.page.js');
const EthnicGroupPage = require('../pages/surveys/census/individual/ethnic-group.page.js');
const WhiteEthnicGroupPage = require('../pages/surveys/census/individual/white-ethnic-group.page.js');
const SexualIdentityPage = require('../pages/surveys/census/individual/sexual-identity.page.js');
const UnderstandWelshPage = require('../pages/surveys/census/individual/understand-welsh.page.js');
const LanguagePage = require('../pages/surveys/census/individual/language.page.js');
const ReligionPage = require('../pages/surveys/census/individual/religion.page.js');
const PastUsualAddressPage = require('../pages/surveys/census/individual/past-usual-address.page.js');
const PassportsPage = require('../pages/surveys/census/individual/passports.page.js');
const DisabilityPage = require('../pages/surveys/census/individual/disability.page.js');
const QualificationsPage = require('../pages/surveys/census/individual/qualifications.page.js');
const VolunteeringPage = require('../pages/surveys/census/individual/volunteering.page.js');
const EmploymentTypePage = require('../pages/surveys/census/individual/employment-type.page.js');
const MainJobPage = require('../pages/surveys/census/individual/main-job.page.js');
const JobTitlePage = require('../pages/surveys/census/individual/job-title.page.js');
const JobDescriptionPage = require('../pages/surveys/census/individual/job-description.page.js');
const EmployersBusinessPage = require('../pages/surveys/census/individual/employers-business.page.js');
const MainJobTypePage = require('../pages/surveys/census/individual/main-job-type.page.js');
const BusinessNamePage = require('../pages/surveys/census/individual/business-name.page.js');
const WorkPage = require('../pages/surveys/census/individual/hours-worked.page.js');
const TravelPage = require('../pages/surveys/census/individual/work-travel.page.js');
const ConfirmationPage = require('../pages/surveys/census/individual/confirmation.page.js');
const ThankYou = require('../pages/thank-you.page');


describe('Census Individual', function() {

  it('Given Respondent Home has identified the respondent should have the Individual Questionnaire without the sexual id question, When I complete the EQ, Then I should not be asked the sexual id question', function() {
    return helpers.openCensusQuestionnaire('census_individual.json').then(() => {
        return browser
          .setValue(CorrectNamePage.firstName(),"John")
          .setValue(CorrectNamePage.lastName(),"Smith")
          .click(CorrectNamePage.submit())

          .click(SexPage.male())
          .click(CorrectNamePage.submit())

          .setValue(DateOfBirthPage.day(),2)
          .selectByValue(DateOfBirthPage.month(),8)
          .setValue(DateOfBirthPage.year(),1980)
          .click(DateOfBirthPage.submit())

          .click(MaritalStatusPage.married())
          .click(MaritalStatusPage.submit())

          .click(AnotherAddressPage.no())
          .click(AnotherAddressPage.submit())

          .click(InEducationPage.no())
          .click(InEducationPage.submit())

          .click(CountryOfBirthPage.englandWales())
          .click(CountryOfBirthPage.submit())

          .click(CarerPage.no())
          .click(CarerPage.submit())

          .click(NationalIdentityPage.englandWelsh())
          .click(NationalIdentityPage.englandBritish())
          .click(NationalIdentityPage.submit())

          .click(EthnicGroupPage.englandWhite())
          .click(EthnicGroupPage.submit())

          .click(WhiteEthnicGroupPage.englandEnglishWelshScottishNorthernIrishBritish())
          .click(WhiteEthnicGroupPage.submit())

          .click(LanguagePage.englandEnglish())
          .click(LanguagePage.submit())

          .click(ReligionPage.noReligion())
          .click(ReligionPage.submit())

          .click(PastUsualAddressPage.thisAddress())
          .click(PastUsualAddressPage.submit())

          .click(PassportsPage.unitedKingdom())
          .click(PassportsPage.submit())

          .click(DisabilityPage.no())
          .click(DisabilityPage.submit())

          .click(QualificationsPage.englandUndergraduateDegree())
          .click(QualificationsPage.submit())

          .click(VolunteeringPage.no())
          .click(VolunteeringPage.submit())

          .click(EmploymentTypePage.workingAsAnEmployee())
          .click(EmploymentTypePage.submit())

          .click(MainJobPage.anEmployee())
          .click(MainJobPage.submit())

          .setValue(JobTitlePage.answer(),"Software Engineer")
          .click(JobTitlePage.submit())

          .setValue(JobDescriptionPage.answer(),"Coding wizardry")
          .click(JobDescriptionPage.submit())

          .click(WorkPage.answer3148())
          .click(WorkPage.submit())

          .click(TravelPage.train())
          .click(TravelPage.submit())

          .setValue(EmployersBusinessPage.answer(),"Codezilla")
          .click(EmployersBusinessPage.submit())

          .click(MainJobTypePage.employedByAnOrganisationOrBusiness())
          .click(MainJobTypePage.submit())

          .setValue(BusinessNamePage.answer(),"Code Warehouse")
          .click(BusinessNamePage.submit())

          .click(ConfirmationPage.submit())

          .getUrl().should.eventually.contain(ThankYou.pageName);
    });
  });

  it('Given Respondent Home has identified the respondent should have the Individual Questionnaire in welsh, When I enter valid data, Then I should complete the questionnaire', function() {
    return helpers.openCensusQuestionnaire('census_individual.json', false, 'GB-WLS', 'cy').then(() => {
        return browser
          .setValue(CorrectNamePage.firstName(),"John")
          .setValue(CorrectNamePage.lastName(),"Smith")
          .click(CorrectNamePage.submit())

          .click(SexPage.male())
          .click(CorrectNamePage.submit())

          .setValue(DateOfBirthPage.day(),2)
          .selectByValue(DateOfBirthPage.month(),8)
          .setValue(DateOfBirthPage.year(),1980)
          .click(DateOfBirthPage.submit())

          .click(MaritalStatusPage.married())
          .click(MaritalStatusPage.submit())

          .click(AnotherAddressPage.no())
          .click(AnotherAddressPage.submit())

          .click(InEducationPage.no())
          .click(InEducationPage.submit())

          .click(CountryOfBirthPage.walesWales())
          .click(CountryOfBirthPage.submit())

          .click(CarerPage.no())
          .click(CarerPage.submit())

          .click(NationalIdentityPage.walesWelsh())
          .click(NationalIdentityPage.walesBritish())
          .click(NationalIdentityPage.submit())

          .click(EthnicGroupPage.walesWhite())
          .click(EthnicGroupPage.submit())

          .click(WhiteEthnicGroupPage.walesWelshEnglishScottishNorthernIrishBritishLabel())
          .click(WhiteEthnicGroupPage.submit())

          .click(UnderstandWelshPage.understandSpokenWelsh())
          .click(UnderstandWelshPage.readWelsh())
          .click(UnderstandWelshPage.submit())

          .click(LanguagePage.welshEnglishOrWelsh())
          .click(LanguagePage.submit())

          .click(ReligionPage.welshNoReligion())
          .click(ReligionPage.submit())

          .click(PastUsualAddressPage.thisAddress())
          .click(PastUsualAddressPage.submit())

          .click(PassportsPage.unitedKingdom())
          .click(PassportsPage.submit())

          .click(DisabilityPage.no())
          .click(DisabilityPage.submit())

          .click(QualificationsPage.welshApprenticeshipFoundationModernOrHigher())
          .click(QualificationsPage.submit())

          .click(VolunteeringPage.no())
          .click(VolunteeringPage.submit())

          .click(EmploymentTypePage.workingAsAnEmployee())
          .click(EmploymentTypePage.submit())

          .click(MainJobPage.anEmployee())
          .click(MainJobPage.submit())

          .setValue(JobTitlePage.answer(),"Software Engineer")
          .click(JobTitlePage.submit())

          .setValue(JobDescriptionPage.answer(),"Coding wizardry")
          .click(JobDescriptionPage.submit())

          .click(WorkPage.answer3148())
          .click(WorkPage.submit())

          .click(TravelPage.train())
          .click(TravelPage.submit())

          .setValue(EmployersBusinessPage.answer(),"Codezilla")
          .click(EmployersBusinessPage.submit())

          .click(MainJobTypePage.employedByAnOrganisationOrBusiness())
          .click(MainJobTypePage.submit())

          .setValue(BusinessNamePage.answer(),"Code Warehouse")
          .click(BusinessNamePage.submit())

          .click(ConfirmationPage.submit())

          .getUrl().should.eventually.contain(ThankYou.pageName);
    });
  });

  it('Given Respondent Home has identified the respondent should have the Individual Questionnaire without the sexual id question, When I complete the EQ, Then I should not be asked the sexual id question', function() {
    return helpers.openCensusQuestionnaire('census_individual.json', true).then(() => {
        return browser
          .setValue(CorrectNamePage.firstName(),"John")
          .setValue(CorrectNamePage.lastName(),"Smith")
          .click(CorrectNamePage.submit())

          .click(SexPage.male())
          .click(CorrectNamePage.submit())

          .setValue(DateOfBirthPage.day(),2)
          .selectByValue(DateOfBirthPage.month(),8)
          .setValue(DateOfBirthPage.year(),1980)
          .click(DateOfBirthPage.submit())

          .click(MaritalStatusPage.married())
          .click(MaritalStatusPage.submit())

          .click(AnotherAddressPage.no())
          .click(AnotherAddressPage.submit())

          .click(InEducationPage.no())
          .click(InEducationPage.submit())

          .click(CountryOfBirthPage.englandWales())
          .click(CountryOfBirthPage.submit())

          .click(CarerPage.no())
          .click(CarerPage.submit())

          .click(NationalIdentityPage.englandWelsh())
          .click(NationalIdentityPage.englandBritish())
          .click(NationalIdentityPage.submit())

          .click(EthnicGroupPage.englandWhite())
          .click(EthnicGroupPage.submit())

          .click(WhiteEthnicGroupPage.englandEnglishWelshScottishNorthernIrishBritish())
          .click(WhiteEthnicGroupPage.submit())

          .getUrl().should.eventually.contain(SexualIdentityPage.pageName)
          .click(SexualIdentityPage.heterosexualOrStraight())
          .click(SexualIdentityPage.submit())

          .getUrl().should.eventually.contain(LanguagePage.pageName);
    });
  });

});

