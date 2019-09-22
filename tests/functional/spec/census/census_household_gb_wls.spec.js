import helpers from '../../helpers';
import HubPage from '../../base_pages/hub.page.js';
import JobAvailability from '../../generated_pages/census_household_gb_wls/job-availability.page.js';
import Disability from '../../generated_pages/census_household_gb_wls/disability.page.js';
import AnyoneElseTempAwayListCollectorEdit from '../../generated_pages/census_household_gb_wls/anyone-else-temp-away-list-collector-edit.page.js';
import Proxy from '../../generated_pages/census_household_gb_wls/proxy.page.js';
import Passports from '../../generated_pages/census_household_gb_wls/passports.page.js';
import MainEmploymentBlock from '../../generated_pages/census_household_gb_wls/main-employment-block.page.js';
import AccommodationSectionSummary from '../../generated_pages/census_household_gb_wls/accommodation-section-summary.page.js';
import BlackEthnicGroup from '../../generated_pages/census_household_gb_wls/black-ethnic-group.page.js';
import VisitorListCollectorAdd from '../../generated_pages/census_household_gb_wls/visitor-list-collector-add.page.js';
import WhiteEthnicGroup from '../../generated_pages/census_household_gb_wls/white-ethnic-group.page.js';
import IndividualInterstitial from '../../generated_pages/census_household_gb_wls/individual-interstitial.page.js';
import VisitorInterstitial from '../../generated_pages/census_household_gb_wls/visitor-interstitial.page.js';
import PreviousMarriageStatus from '../../generated_pages/census_household_gb_wls/previous-marriage-status.page.js';
import HoursWorked from '../../generated_pages/census_household_gb_wls/hours-worked.page.js';
import EmployerAddressWorkplace from '../../generated_pages/census_household_gb_wls/employer-address-workplace.page.js';
import LastYearAddress from '../../generated_pages/census_household_gb_wls/last-year-address.page.js';
import WhenArriveInUk from '../../generated_pages/census_household_gb_wls/when-arrive-in-uk.page.js';
import ALevel from '../../generated_pages/census_household_gb_wls/a-level.page.js';
import LengthOfStay from '../../generated_pages/census_household_gb_wls/length-of-stay.page.js';
import JobPending from '../../generated_pages/census_household_gb_wls/job-pending.page.js';
import EmployersBusiness from '../../generated_pages/census_household_gb_wls/employers-business.page.js';
import VisitorListCollectorEdit from '../../generated_pages/census_household_gb_wls/visitor-list-collector-edit.page.js';
import CentralHeating from '../../generated_pages/census_household_gb_wls/central-heating.page.js';
import NvqLevel from '../../generated_pages/census_household_gb_wls/nvq-level.page.js';
import DisabilityLimitation from '../../generated_pages/census_household_gb_wls/disability-limitation.page.js';
import Language from '../../generated_pages/census_household_gb_wls/language.page.js';
import NationalIdentity from '../../generated_pages/census_household_gb_wls/national-identity.page.js';
import ConfirmDob from '../../generated_pages/census_household_gb_wls/confirm-dob.page.js';
import Gcse from '../../generated_pages/census_household_gb_wls/gcse.page.js';
import VisitorDateOfBirth from '../../generated_pages/census_household_gb_wls/visitor-date-of-birth.page.js';
import PreviousPartnershipStatus from '../../generated_pages/census_household_gb_wls/previous-partnership-status.page.js';
import Religion from '../../generated_pages/census_household_gb_wls/religion.page.js';
import ArriveInCountry from '../../generated_pages/census_household_gb_wls/arrive-in-country.page.js';
import CurrentPartnershipStatus from '../../generated_pages/census_household_gb_wls/current-partnership-status.page.js';
import Carer from '../../generated_pages/census_household_gb_wls/carer.page.js';
import NumberOfVehicles from '../../generated_pages/census_household_gb_wls/number-of-vehicles.page.js';
import MainJobType from '../../generated_pages/census_household_gb_wls/main-job-type.page.js';
import UsualAddressDetails from '../../generated_pages/census_household_gb_wls/usual-address-details.page.js';
import WhoLivesHereSectionSummary from '../../generated_pages/census_household_gb_wls/who-lives-here-section-summary.page.js';
import OtherAddress from '../../generated_pages/census_household_gb_wls/other-address.page.js';
import Health from '../../generated_pages/census_household_gb_wls/health.page.js';
import EmployerAddressDepot from '../../generated_pages/census_household_gb_wls/employer-address-depot.page.js';
import VisitorListCollector from '../../generated_pages/census_household_gb_wls/visitor-list-collector.page.js';
import Apprenticeship from '../../generated_pages/census_household_gb_wls/apprenticeship.page.js';
import AnyoneElseListCollector from '../../generated_pages/census_household_gb_wls/anyone-else-list-collector.page.js';
import VisitorSummary from '../../generated_pages/census_household_gb_wls/visitor-summary.page.js';
import TermTimeAddressDetails from '../../generated_pages/census_household_gb_wls/term-time-address-details.page.js';
import DateOfBirth from '../../generated_pages/census_household_gb_wls/date-of-birth.page.js';
import OtherEthnicGroup from '../../generated_pages/census_household_gb_wls/other-ethnic-group.page.js';
import Summary from '../../generated_pages/census_household_gb_wls/summary.page.js';
import English from '../../generated_pages/census_household_gb_wls/english.page.js';
import AnyoneElseTempAwayListCollector from '../../generated_pages/census_household_gb_wls/anyone-else-temp-away-list-collector.page.js';
import PrimaryPersonListCollectorAdd from '../../generated_pages/census_household_gb_wls/primary-person-list-collector-add.page.js';
import PastUsualHouseholdAddress from '../../generated_pages/census_household_gb_wls/past-usual-household-address.page.js';
import EverWorked from '../../generated_pages/census_household_gb_wls/ever-worked.page.js';
import AddressType from '../../generated_pages/census_household_gb_wls/address-type.page.js';
import OtherQualifications from '../../generated_pages/census_household_gb_wls/other-qualifications.page.js';
import UnderstandWelsh from '../../generated_pages/census_household_gb_wls/understand-welsh.page.js';
import CountryOfBirth from '../../generated_pages/census_household_gb_wls/country-of-birth.page.js';
import ArmedForces from '../../generated_pages/census_household_gb_wls/armed-forces.page.js';
import AccommodationIntroduction from '../../generated_pages/census_household_gb_wls/accommodation-introduction.page.js';
import TermTimeAddressCountry from '../../generated_pages/census_household_gb_wls/term-time-address-country.page.js';
import AsianEthnicGroup from '../../generated_pages/census_household_gb_wls/asian-ethnic-group.page.js';
import RelationshipsInterstitial from '../../generated_pages/census_household_gb_wls/relationships-interstitial.page.js';
import AnyoneElseTempAwayListCollectorAdd from '../../generated_pages/census_household_gb_wls/anyone-else-temp-away-list-collector-add.page.js';
import VisitorSex from '../../generated_pages/census_household_gb_wls/visitor-sex.page.js';
import VisitorListCollectorRemove from '../../generated_pages/census_household_gb_wls/visitor-list-collector-remove.page.js';
import InEducation from '../../generated_pages/census_household_gb_wls/in-education.page.js';
import SexualIdentity from '../../generated_pages/census_household_gb_wls/sexual-identity.page.js';
import AnyoneElseListCollectorAdd from '../../generated_pages/census_household_gb_wls/anyone-else-list-collector-add.page.js';
import WhoRentFrom from '../../generated_pages/census_household_gb_wls/who-rent-from.page.js';
import AnyVisitors from '../../generated_pages/census_household_gb_wls/any-visitors.page.js';
import JobTitle from '../../generated_pages/census_household_gb_wls/job-title.page.js';
import Supervise from '../../generated_pages/census_household_gb_wls/supervise.page.js';
import Relationships from '../../generated_pages/census_household_gb_wls/relationships.page.js';
import AnotherAddress from '../../generated_pages/census_household_gb_wls/another-address.page.js';
import TypeOfFlat from '../../generated_pages/census_household_gb_wls/type-of-flat.page.js';
import AnyoneUsuallyLiveAt from '../../generated_pages/census_household_gb_wls/anyone-usually-live-at.page.js';
import WhoLivesHereInterstitial from '../../generated_pages/census_household_gb_wls/who-lives-here-interstitial.page.js';
import WorkTravel from '../../generated_pages/census_household_gb_wls/work-travel.page.js';
import AnyoneElseTempAwayListCollectorRemove from '../../generated_pages/census_household_gb_wls/anyone-else-temp-away-list-collector-remove.page.js';
import EmploymentType from '../../generated_pages/census_household_gb_wls/employment-type.page.js';
import Jobseeker from '../../generated_pages/census_household_gb_wls/jobseeker.page.js';
import NumberOfBedrooms from '../../generated_pages/census_household_gb_wls/number-of-bedrooms.page.js';
import BusinessName from '../../generated_pages/census_household_gb_wls/business-name.page.js';
import Qualifications from '../../generated_pages/census_household_gb_wls/qualifications.page.js';
import PrimaryPersonListCollector from '../../generated_pages/census_household_gb_wls/primary-person-list-collector.page.js';
import BirthGender from '../../generated_pages/census_household_gb_wls/birth-gender.page.js';
import CurrentMarriageStatus from '../../generated_pages/census_household_gb_wls/current-marriage-status.page.js';
import Degree from '../../generated_pages/census_household_gb_wls/degree.page.js';
import TypeOfHouse from '../../generated_pages/census_household_gb_wls/type-of-house.page.js';
import Sex from '../../generated_pages/census_household_gb_wls/sex.page.js';
import AnyoneElseListCollectorRemove from '../../generated_pages/census_household_gb_wls/anyone-else-list-collector-remove.page.js';
import MarriageType from '../../generated_pages/census_household_gb_wls/marriage-type.page.js';
import EmployerTypeOfAddress from '../../generated_pages/census_household_gb_wls/employer-type-of-address.page.js';
import EmploymentStatus from '../../generated_pages/census_household_gb_wls/employment-status.page.js';
import EthnicGroup from '../../generated_pages/census_household_gb_wls/ethnic-group.page.js';
import AccommodationType from '../../generated_pages/census_household_gb_wls/accommodation-type.page.js';
import TermTimeLocation from '../../generated_pages/census_household_gb_wls/term-time-location.page.js';
import SelfContained from '../../generated_pages/census_household_gb_wls/self-contained.page.js';
import UsualHouseholdAddress from '../../generated_pages/census_household_gb_wls/usual-household-address.page.js';
import JobDescription from '../../generated_pages/census_household_gb_wls/job-description.page.js';
import OwnOrRent from '../../generated_pages/census_household_gb_wls/own-or-rent.page.js';
import AnyoneElseListCollectorEdit from '../../generated_pages/census_household_gb_wls/anyone-else-list-collector-edit.page.js';
import MixedEthnicGroup from '../../generated_pages/census_household_gb_wls/mixed-ethnic-group.page.js';

const HAS_PRIMARY = true;
const NO_OF_HOUSEHOLDERS = 2;
const NO_OF_HOUSEHOLDER_TEMP_AWAY = 2;
const NO_OF_VISITORS = 2; // Default 1

const TOTAL_HOUSEHOLDERS = HAS_PRIMARY + NO_OF_HOUSEHOLDERS + NO_OF_HOUSEHOLDER_TEMP_AWAY;


const addPeople = (noOfPeople, listCollectorScreen, listCollectorAddScreen, firstName = 'Person', isVisitor = false) => {
  let chain = browser.waitForVisible(listCollectorScreen.listLabel(1)).should.eventually.be.true;

  for (let i = 1; i <= noOfPeople; i++) {
    chain = chain.then(() => browser

      .click(listCollectorScreen.yesINeedToAddSomeone())
      .click(listCollectorScreen.submit())

      .setValue(listCollectorAddScreen.firstName(), `${firstName}`)
      .setValue(listCollectorAddScreen.lastName(), `${i + isVisitor}`)

      .click(listCollectorAddScreen.submit()));
  }

  return chain;
};


const completeRelationships = () => {
  let chain = browser.waitForVisible(Relationships.questionText()).should.eventually.be.true;
  let totalRelationships = (TOTAL_HOUSEHOLDERS * (TOTAL_HOUSEHOLDERS - 1)) / 2;

  let relationships = [
    Relationships.relationshipBrotherOrSister,
    Relationships.relationshipLegallyRegisteredCivilPartner,
    Relationships.relationshipPartner,
    Relationships.relationshipSonOrDaughter,
    Relationships.relationshipStepchild,
    Relationships.relationshipBrotherOrSister,
    Relationships.relationshipMotherOrFather,
    Relationships.relationshipStepmotherOrStepfather,
    Relationships.relationshipGrandchild,
    Relationships.relationshipGrandparent,
    Relationships.relationshipOtherRelation,
    Relationships.relationshipUnrelated
  ];

  for (let i = 1; i <= totalRelationships; i++) {
    chain = chain.then(() => {
      console.log(`${i} Relationships Completed`);
      var today = new Date();
      var time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
      console.log(time);

      return browser
      // Pick a random relationship
        .click(relationships[Math.floor(Math.random() * relationships.length)]())
        .click(Relationships.submit());
    });
  }

  return chain;
};


const completeHouseholderRepeatingSection = () => {
  let chain = browser.waitForVisible(IndividualInterstitial.questionText()).should.eventually.be.true;

  for (let i = 1; i <= TOTAL_HOUSEHOLDERS; i++) {
    chain = chain.then(() => {
        console.log(`${i} Householders Repeating Section Completed`);
        var today = new Date();
        var time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
        console.log(time);

        return browser
          .click(HubPage.submit())
          .click(IndividualInterstitial.submit())

          .click(Proxy.no())
          .click(Proxy.submit())

          .setValue(DateOfBirth.day(), 1)
          .setValue(DateOfBirth.month(), 1)
          .setValue(DateOfBirth.year(), 2000)
          .click(DateOfBirth.submit())

          .click(ConfirmDob.confirmDateOfBirthYes())
          .click(ConfirmDob.submit())

          .click(Sex.male())
          .click(Sex.submit())

          .click(MarriageType.never())
          .click(MarriageType.submit())

          .click(AnotherAddress.no())
          .click(AnotherAddress.submit())

          .click(InEducation.yes())
          .click(InEducation.submit())

          .click(TermTimeLocation.householdAddress())
          .click(TermTimeLocation.submit())

          .click(CountryOfBirth.wales())
          .click(DateOfBirth.submit())

          .click(UnderstandWelsh.exclusiveNoneOfTheseApply())
          .click(UnderstandWelsh.submit())

          .click(Language.englishOrWelsh())
          .click(Language.submit())

          .click(NationalIdentity.welsh())
          .click(NationalIdentity.submit())

          .click(EthnicGroup.white())
          .click(EthnicGroup.submit())

          .click(WhiteEthnicGroup.welshEnglishScottishNorthernIrishOrBritish())
          .click(WhiteEthnicGroup.submit())

          .click(Religion.noReligion())
          .click(Religion.submit())

          .click(PastUsualHouseholdAddress.pastUsualAddressHouseholdHouseholdAddress())
          .click(PastUsualHouseholdAddress.submit())

          .click(Passports.unitedKingdom())
          .click(Passports.submit())

          .click(Health.veryGood())
          .click(Health.submit())

          .click(Disability.yes())
          .click(Disability.submit())

          .click(DisabilityLimitation.yesALittle())
          .click(DisabilityLimitation.submit())

          .click(Carer.no())
          .click(Carer.submit())

          .click(SexualIdentity.straightOrHeterosexual())
          .click(SexualIdentity.submit())

          .click(BirthGender.yes())
          .click(BirthGender.submit())

          .click(Qualifications.submit())

          .click(Apprenticeship.no())
          .click(Apprenticeship.submit())

          .click(Degree.yes())
          .click(Degree.submit())

          .click(NvqLevel.exclusiveNoneOfTheseApply())
          .click(NvqLevel.submit())

          .click(ALevel.answer2OrMoreALevels())
          .click(ALevel.submit())

          .click(Gcse.answer5OrMoreGcses())
          .click(Gcse.submit())

          .click(ArmedForces.no())
          .click(ArmedForces.submit())

          .click(EmploymentStatus.workingAsAnEmployee())
          .click(EmploymentStatus.submit())

          .click(MainEmploymentBlock.submit())

          .click(MainJobType.employee())
          .click(MainJobType.submit())

          .setValue(BusinessName.answer(), 'ONS')
          .click(BusinessName.submit())

          .setValue(JobTitle.answer(), 'Part time Dev')
          .click(JobTitle.submit())

          .setValue(JobDescription.answer(), 'Browse Stack Overflow')
          .click(JobDescription.submit())

          .setValue(EmployersBusiness.answer(), 'Publish statistics')
          .click(EmployersBusiness.submit())

          .click(Supervise.no())
          .click(Supervise.submit())

          .click(HoursWorked.answer0To15Hours())
          .click(HoursWorked.submit())

          .click(WorkTravel.drivingACarOrVan())
          .click(WorkTravel.submit())

          .click(EmployerTypeOfAddress.atAWorkplace())
          .click(EmployerTypeOfAddress.submit())

          .setValue(EmployerAddressWorkplace.building(), 'Government Buildings')
          .setValue(EmployerAddressWorkplace.street(), 'Cardiff Rd')
          .setValue(EmployerAddressWorkplace.city(), 'Duffryn, Newport')
          .setValue(EmployerAddressWorkplace.county(), 'Gwent')
          .setValue(EmployerAddressWorkplace.employerAdressWorkplacePostcode(), 'NP10 8XG')
          .click(EmployerAddressWorkplace.submit())

          .click(Summary.submit());
      }
    );
  }

  return chain;
};

const completeVisitorRepeatingSection = () => {
  let chain = browser.waitForVisible(VisitorInterstitial.questionText()).should.eventually.be.true;

  for (let i = 1; i <= NO_OF_VISITORS; i++) {
    chain = chain.then(() => {
        console.log(`${i} Visitors Repeating Section Completed`);
        var today = new Date();
        var time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
        console.log(time);

        return browser

          .click(HubPage.submit())
          .click(VisitorInterstitial.submit())

          .click(VisitorSex.female())
          .click(VisitorSex.submit())

          .setValue(VisitorDateOfBirth.day(), 3)
          .setValue(VisitorDateOfBirth.month(), 7)
          .setValue(VisitorDateOfBirth.year(), 2003)
          .click(VisitorDateOfBirth.submit())

          .click(UsualHouseholdAddress.anAddressInTheUk())
          .click(UsualHouseholdAddress.submit())

          .setValue(UsualAddressDetails.street(), '1 Evelyn Street')
          .setValue(UsualAddressDetails.city(), 'Barry')
          .setValue(UsualAddressDetails.county(), 'Vale of Glamorgan')
          .setValue(UsualAddressDetails.postcode(), 'CF63 4HT')
          .click(UsualAddressDetails.submit())

          .click(VisitorSummary.submit());
      }
    );
  }

  return chain;
};


describe('@watch Census Household: GB-WLS', () => {

  before('Open Questionnaire', () => helpers.openQuestionnaire('census_household_gb_wls.json')
    .then(() => browser.pause(3000)
      .getUrl().should.eventually.contain(WhoLivesHereInterstitial.url())
      .click(WhoLivesHereInterstitial.submit()))
  );

  it('Add Primary Person', () => browser
    .click(PrimaryPersonListCollector.yesIUsuallyLiveHere())
    .click(PrimaryPersonListCollector.submit())

    .setValue(PrimaryPersonListCollectorAdd.firstName(), 'Primary')
    .setValue(PrimaryPersonListCollectorAdd.middleNames(), 'Classified')
    .setValue(PrimaryPersonListCollectorAdd.lastName(), 'Person')

    .click(PrimaryPersonListCollectorAdd.submit())
  );

  it(`Add ${NO_OF_HOUSEHOLDERS} Household Member(s)`, () => addPeople(NO_OF_HOUSEHOLDERS, AnyoneElseListCollector, AnyoneElseListCollectorAdd)

    .click(AnyoneElseListCollector.noIDoNotNeedToAddAnyone())
    .click(AnyoneElseListCollector.submit())
  );

  it(`Add ${NO_OF_HOUSEHOLDER_TEMP_AWAY} Temporarily Away Household Member(s)`, () => addPeople(NO_OF_HOUSEHOLDER_TEMP_AWAY, AnyoneElseTempAwayListCollector, AnyoneElseTempAwayListCollectorAdd, 'Person Temp Away')
    .click(AnyoneElseTempAwayListCollector.noIDoNotNeedToAddAnyone())
    .click(AnyoneElseTempAwayListCollector.submit())
  );

  it(`Add ${NO_OF_VISITORS} Visitor(s)`, () => browser
    .click(AnyVisitors.peopleHereOnHoliday())
    .click(AnyVisitors.submit())

    .setValue(VisitorListCollectorAdd.firstName(), 'Visitor')
    .setValue(VisitorListCollectorAdd.lastName(), '1')
    .click(VisitorListCollectorAdd.submit())

    .then(() => addPeople(NO_OF_VISITORS - 1, VisitorListCollector, VisitorListCollectorAdd, 'Visitor', true)

      .click(VisitorListCollector.noIDoNotNeedToAddAnyone())
      .click(VisitorListCollector.submit())
      .click(WhoLivesHereSectionSummary.submit()))
  );

  it('Complete Relationship(s)', () => browser
    .click(RelationshipsInterstitial.submit())
    .then(() => completeRelationships())
  );

  it('Complete Household Accommodation', () => browser
    .click(HubPage.submit())
    .click(AccommodationIntroduction.submit())

    .click(AccommodationType.wholeHouseOrBungalow())
    .click(AccommodationType.submit())

    .click(TypeOfHouse.detached())
    .click(TypeOfHouse.submit())

    .click(SelfContained.yes())
    .click(SelfContained.submit())

    .setValue(NumberOfBedrooms.answer(), '4')
    .click(NumberOfBedrooms.submit())

    .click(CentralHeating.mainsGas())
    .click(CentralHeating.submit())

    .click(OwnOrRent.rents())
    .click(OwnOrRent.submit())

    .click(WhoRentFrom.privateLandlordOrLettingAgency())
    .click(WhoRentFrom.submit())

    .click(NumberOfVehicles.answer2())
    .click(NumberOfVehicles.submit())

    .click(AccommodationSectionSummary.submit())
  );

  it('Complete Householder\'s Repeating Section', () => completeHouseholderRepeatingSection());

  it('Complete Visitor\'s Repeating Section', () => completeVisitorRepeatingSection());

  it('Hub Completed State', () => browser
    .getText(HubPage.submit()).should.eventually.contain('Submit')
    .getText(HubPage.displayedName()).should.eventually.contain('Submit survey')
  );

  it('Thank You Page Displayed When Submitted', () => browser
    .pause(5000)
    .click(HubPage.submit())
    .getUrl().should.eventually.contain('thank-you')
  );

});
