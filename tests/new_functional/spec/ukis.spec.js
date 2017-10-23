const helpers = require('../helpers');

const GeographicMarketsPage = require('../pages/surveys/ukis/geographic-markets.page.js');
const SignificantEventsPage = require('../pages/surveys/ukis/significant-events.page.js');
const GeneralBusinessInformationCompletedPage = require('../pages/surveys/ukis/general-business-information-completed.page.js');
const BusinessChangesPage = require('../pages/surveys/ukis/business-changes.page.js');
const BusinessStrategyPracticesCompletedPage = require('../pages/surveys/ukis/business-strategy-practices-completed.page.js');
const InternalInvestmentRDPage = require('../pages/surveys/ukis/internal-investment-r-d.page.js');
const YearsInternalInvestmentRDPage = require('../pages/surveys/ukis/years-internal-investment-r-d.page.js');
const ExpenditureInternalInvestmentRDPage = require('../pages/surveys/ukis/expenditure-internal-investment-r-d.page.js');
const AcquisitionInternalInvestmentRDPage = require('../pages/surveys/ukis/acquisition-internal-investment-r-d.page.js');
const AmountAcquisitionInternalInvestmentRDPage = require('../pages/surveys/ukis/amount-acquisition-internal-investment-r-d.page.js');
const InvestmentAdvancedMachineryPage = require('../pages/surveys/ukis/investment-advanced-machinery.page.js');
const InvestmentPurposesInnovationPage = require('../pages/surveys/ukis/investment-purposes-innovation.page.js');
const AmountAcquisitionAdvancedMachineryPage = require('../pages/surveys/ukis/amount-acquisition-advanced-machinery.page.js');
const InvestmentExistingKnowledgeInnovationPage = require('../pages/surveys/ukis/investment-existing-knowledge-innovation.page.js');
const ExpenditureExisting2016Page = require('../pages/surveys/ukis/expenditure-existing-2016.page.js');
const InvestmentTrainingInnovativePage = require('../pages/surveys/ukis/investment-training-innovative.page.js');
const ExpenditureTrainingInnovative2016Page = require('../pages/surveys/ukis/expenditure-training-innovative-2016.page.js');
const InvestmentDesignFutureInnovationPage = require('../pages/surveys/ukis/investment-design-future-innovation.page.js');
const ExpenditureDesign2016Page = require('../pages/surveys/ukis/expenditure-design-2016.page.js');
const InvestmentIntroductionInnovationsPage = require('../pages/surveys/ukis/investment-introduction-innovations.page.js');
const InvestmentPurposesInnovation2Page = require('../pages/surveys/ukis/investment-purposes-innovation-2.page.js');
const ExpenditureIntroductionInnovations2016Page = require('../pages/surveys/ukis/expenditure-introduction-innovations-2016.page.js');
const InnovationInvestmentCompletedPage = require('../pages/surveys/ukis/innovation-investment-completed.page.js');
const IntroducingSignificantlyImprovedGoodsPage = require('../pages/surveys/ukis/introducing-significantly-improved-goods.page.js');
const EntityDevelopedTheseGoodsPage = require('../pages/surveys/ukis/entity-developed-these-goods.page.js');
const IntroduceSignificantlyImprovementPage = require('../pages/surveys/ukis/introduce-significantly-improvement.page.js');
const EntityMainlyDevelopedThesePage = require('../pages/surveys/ukis/entity-mainly-developed-these.page.js');
const NewGoodsServicesInnovationsPage = require('../pages/surveys/ukis/new-goods-services-innovations.page.js');
const GoodsServicesInnovationsNewPage = require('../pages/surveys/ukis/goods-services-innovations-new.page.js');
const PercentageTurnover2016Page = require('../pages/surveys/ukis/percentage-turnover-2016.page.js');
const GoodsAndServicesInnovationCompletedPage = require('../pages/surveys/ukis/goods-and-services-innovation-completed.page.js');
const ProcessImprovedPage = require('../pages/surveys/ukis/process-improved.page.js');
const DevelopedProcessesPage = require('../pages/surveys/ukis/developed-processes.page.js');
const ImprovedProcessesPage = require('../pages/surveys/ukis/improved-processes.page.js');
const ProcessInnovationCompletedPage = require('../pages/surveys/ukis/process-innovation-completed.page.js');
const ConstraintsInnovationActivitiesPage = require('../pages/surveys/ukis/constraints-innovation-activities.page.js');
const ConstrainingInnovationEconomicPage = require('../pages/surveys/ukis/constraining-innovation-economic.page.js');
const ConstrainingInnovationCostsPage = require('../pages/surveys/ukis/constraining-innovation-costs.page.js');
const ConstrainingInnovationFinancePage = require('../pages/surveys/ukis/constraining-innovation-finance.page.js');
const ConstrainingInnovationAvailableFinancePage = require('../pages/surveys/ukis/constraining-innovation-available-finance.page.js');
const ConstrainingInnovationLackQualifiedPage = require('../pages/surveys/ukis/constraining-innovation-lack-qualified.page.js');
const ConstrainingInnovationLackTechnologyPage = require('../pages/surveys/ukis/constraining-innovation-lack-technology.page.js');
const ConstrainingInnovationLackInformationPage = require('../pages/surveys/ukis/constraining-innovation-lack-information.page.js');
const ConstrainingInnovationDominatedPage = require('../pages/surveys/ukis/constraining-innovation-dominated.page.js');
const ConstrainingInnovationUncertainPage = require('../pages/surveys/ukis/constraining-innovation-uncertain.page.js');
const ConstrainingInnovationGovernmentPage = require('../pages/surveys/ukis/constraining-innovation-government.page.js');
const ConstrainingInnovationEuPage = require('../pages/surveys/ukis/constraining-innovation-eu.page.js');
const ConstrainingInnovationReferendumPage = require('../pages/surveys/ukis/constraining-innovation-referendum.page.js');
const ConstraintsOnInnovationCompletedPage = require('../pages/surveys/ukis/constraints-on-innovation-completed.page.js');
const FactorsAffectingIncreasingRangePage = require('../pages/surveys/ukis/factors-affecting-increasing-range.page.js');
const FactorsAffectingNewMarketsPage = require('../pages/surveys/ukis/factors-affecting-new-markets.page.js');
const FactorsAffectingMarketSharePage = require('../pages/surveys/ukis/factors-affecting-market-share.page.js');
const FactorsAffectingQualityPage = require('../pages/surveys/ukis/factors-affecting-quality.page.js');
const FactorsAffectingFlexibilityPage = require('../pages/surveys/ukis/factors-affecting-flexibility.page.js');
const FactorsAffectingCapacityPage = require('../pages/surveys/ukis/factors-affecting-capacity.page.js');
const FactorsAffectingValuePage = require('../pages/surveys/ukis/factors-affecting-value.page.js');
const FactorsAffectingReducingCostPage = require('../pages/surveys/ukis/factors-affecting-reducing-cost.page.js');
const FactorsAffectingHealthSafetyPage = require('../pages/surveys/ukis/factors-affecting-health-safety.page.js');
const FactorsAffectingEnvironmentalPage = require('../pages/surveys/ukis/factors-affecting-environmental.page.js');
const FactorsAffectingReplacingPage = require('../pages/surveys/ukis/factors-affecting-replacing.page.js');
const FactorsAffectingRegulatoryPage = require('../pages/surveys/ukis/factors-affecting-regulatory.page.js');
const FactorsAffectingCompletedPage = require('../pages/surveys/ukis/factors-affecting-completed.page.js');
const ImportancesInformationInnovationPage = require('../pages/surveys/ukis/importances-information-innovation.page.js');
const ImportancesInformationSuppliersPage = require('../pages/surveys/ukis/importances-information-suppliers.page.js');
const ImportancesInformationClientPage = require('../pages/surveys/ukis/importances-information-client.page.js');
const ImportancesInformationPublicSectorPage = require('../pages/surveys/ukis/importances-information-public-sector.page.js');
const ImportancesInformationCompetitorsPage = require('../pages/surveys/ukis/importances-information-competitors.page.js');
const ImportancesInformationConsultantsPage = require('../pages/surveys/ukis/importances-information-consultants.page.js');
const ImportancesInformationUniversitiesPage = require('../pages/surveys/ukis/importances-information-universities.page.js');
const ImportancesInformationGovernmentPage = require('../pages/surveys/ukis/importances-information-government.page.js');
const ImportancesInformationConferencesPage = require('../pages/surveys/ukis/importances-information-conferences.page.js');
const ImportancesInformationAssociationsPage = require('../pages/surveys/ukis/importances-information-associations.page.js');
const ImportancesInformationStandardsPage = require('../pages/surveys/ukis/importances-information-standards.page.js');
const ImportancesInformationPublicationsPage = require('../pages/surveys/ukis/importances-information-publications.page.js');
const InformationNeededForInnovationCompletedPage = require('../pages/surveys/ukis/information-needed-for-innovation-completed.page.js');
const CoOperationOtherBusinessesPage = require('../pages/surveys/ukis/co-operation-other-businesses.page.js');
const CoOperationSuppliersPage = require('../pages/surveys/ukis/co-operation-suppliers.page.js');
const CoOperationPrivateSectorPage = require('../pages/surveys/ukis/co-operation-private-sector.page.js');
const CoOperationPublicSectorPage = require('../pages/surveys/ukis/co-operation-public-sector.page.js');
const CoOperationCompetitorsPage = require('../pages/surveys/ukis/co-operation-competitors.page.js');
const CoOperationConsultantsPage = require('../pages/surveys/ukis/co-operation-consultants.page.js');
const CoOperationInstitutionsPage = require('../pages/surveys/ukis/co-operation-institutions.page.js');
const CoOperationGovernmentPage = require('../pages/surveys/ukis/co-operation-government.page.js');
const InnovationsProtectedPatentsPage = require('../pages/surveys/ukis/innovations-protected-patents.page.js');
const InnovationsProtectedDesignPage = require('../pages/surveys/ukis/innovations-protected-design.page.js');
const InnovationsProtectedCopyrightPage = require('../pages/surveys/ukis/innovations-protected-copyright.page.js');
const InnovationsProtectedTrademarkPage = require('../pages/surveys/ukis/innovations-protected-trademark.page.js');
const InnovationsProtectedLeadTimePage = require('../pages/surveys/ukis/innovations-protected-lead-time.page.js');
const InnovationsProtectedServicesPage = require('../pages/surveys/ukis/innovations-protected-services.page.js');
const InnovationsProtectedSecrecyPage = require('../pages/surveys/ukis/innovations-protected-secrecy.page.js');
const CoOperationOnInnovationCompletedPage = require('../pages/surveys/ukis/co-operation-on-innovation-completed.page.js');
const PublicFinancialSupportPage = require('../pages/surveys/ukis/public-financial-support.page.js');
const KindFinancialCentralGovernmentSupportPage = require('../pages/surveys/ukis/kind-financial-central-government-support.page.js');
const PublicFinancialSupportForInnovationCompletedPage = require('../pages/surveys/ukis/public-financial-support-for-innovation-completed.page.js');
const Turnover2014Page = require('../pages/surveys/ukis/turnover-2014.page.js');
const Turnover2016Page = require('../pages/surveys/ukis/turnover-2016.page.js');
const Exports2016Page = require('../pages/surveys/ukis/exports-2016.page.js');
const TurnoverAndExportsCompletedPage = require('../pages/surveys/ukis/turnover-and-exports-completed.page.js');
const Employees2014Page = require('../pages/surveys/ukis/employees-2014.page.js');
const Employees2016Page = require('../pages/surveys/ukis/employees-2016.page.js');
const EmployeesQualifications2016Page = require('../pages/surveys/ukis/employees-qualifications-2016.page.js');
const EmployeesInHouseSkillsPage = require('../pages/surveys/ukis/employees-in-house-skills.page.js');
const EmployeesAndSkillsCompletedPage = require('../pages/surveys/ukis/employees-and-skills-completed.page.js');
const AdditionalCommentsPage = require('../pages/surveys/ukis/additional-comments.page.js');
const HowLongPage = require('../pages/surveys/ukis/how-long.page.js');
const ApproachedTelephonePage = require('../pages/surveys/ukis/approached-telephone.page.js');
const ConfirmationPage = require('../pages/surveys/ukis/confirmation.page.js');
const ThankYou = require('../pages/thank-you.page');

describe('Example Test', function() {

  it('Given I am completing the UKIS survey, When I enter valid answers, Then I should be able to successfuly submit the survey', function() {
    return helpers.startQuestionnaire('1_0001.json').then(() => {
        return browser

        //General Business Information
        .click(GeographicMarketsPage.ukNational())
        .click(GeographicMarketsPage.submit())
        .click(SignificantEventsPage.establishedYes())
        .click(SignificantEventsPage.turnoverIncreaseYes())
        .click(SignificantEventsPage.turnoverDecreaseYes())
        .click(SignificantEventsPage.submit())
        .click(GeneralBusinessInformationCompletedPage.submit())

        //Business Strategy & Practices
        .click(BusinessChangesPage.businessPracticesYesLabel())
        .click(BusinessChangesPage.organisingYesLabel())
        .click(BusinessChangesPage.externalRelationshipsYes())
        .click(BusinessChangesPage.yes())
        .click(BusinessChangesPage.submit())
        .click(BusinessStrategyPracticesCompletedPage.submit())

        //Innovation Investment
        .click(InternalInvestmentRDPage.yes())
        .click(InternalInvestmentRDPage.submit())
        .click(YearsInternalInvestmentRDPage.answer2014())
        .click(YearsInternalInvestmentRDPage.answer2015())
        .click(YearsInternalInvestmentRDPage.answer2016())
        .click(YearsInternalInvestmentRDPage.submit())
        .setValue(ExpenditureInternalInvestmentRDPage.answer(), 1703000)
        .click(ExpenditureInternalInvestmentRDPage.submit())
        .click(AcquisitionInternalInvestmentRDPage.yes())
        .click(AcquisitionInternalInvestmentRDPage.submit())
        .setValue(AmountAcquisitionInternalInvestmentRDPage.answer(), 1703000)
        .click(AmountAcquisitionInternalInvestmentRDPage.submit())
        .click(InvestmentAdvancedMachineryPage.yes())
        .click(InvestmentAdvancedMachineryPage.submit())
        .click(InvestmentPurposesInnovationPage.advancedMachineryAndEquipment())
        .click(InvestmentPurposesInnovationPage.computerHardware())
        .click(InvestmentPurposesInnovationPage.computerSoftware())
        .click(InvestmentPurposesInnovationPage.submit())
        .setValue(AmountAcquisitionAdvancedMachineryPage.answer(), 1703000)
        .click(AmountAcquisitionAdvancedMachineryPage.submit())
        .click(InvestmentExistingKnowledgeInnovationPage.yes())
        .click(InvestmentExistingKnowledgeInnovationPage.submit())
        .setValue(ExpenditureExisting2016Page.answer(), 1703000)
        .click(ExpenditureExisting2016Page.submit())
        .click(InvestmentTrainingInnovativePage.yes())
        .click(InvestmentTrainingInnovativePage.submit())
        .setValue(ExpenditureTrainingInnovative2016Page.answer(), 1703000)
        .click(ExpenditureTrainingInnovative2016Page.submit())
        .click(InvestmentDesignFutureInnovationPage.yes())
        .click(InvestmentDesignFutureInnovationPage.submit())
        .setValue(ExpenditureDesign2016Page.answer(), 1703000)
        .click(ExpenditureDesign2016Page.submit())
        .click(InvestmentIntroductionInnovationsPage.yes())
        .click(InvestmentIntroductionInnovationsPage.submit())
        .click(InvestmentPurposesInnovation2Page.changesToProductOrServiceDesign())
        .click(InvestmentPurposesInnovation2Page.marketResearch())
        .click(InvestmentPurposesInnovation2Page.changesToMarketingMethods())
        .click(InvestmentPurposesInnovation2Page.launchAdvertising())
        .click(InvestmentPurposesInnovation2Page.submit())
        .setValue(ExpenditureIntroductionInnovations2016Page.answer(), 1703000)
        .click(ExpenditureIntroductionInnovations2016Page.submit())
        .click(InnovationInvestmentCompletedPage.submit())

        //Goods and Services Innovation
        .click(IntroducingSignificantlyImprovedGoodsPage.yes())
        .click(IntroducingSignificantlyImprovedGoodsPage.submit())
        .click(EntityDevelopedTheseGoodsPage.thisBusinessOrEnterpriseGroup())
        .click(EntityDevelopedTheseGoodsPage.thisBusinessWithOtherBusinessesOrOrganisations())
        .click(EntityDevelopedTheseGoodsPage.otherBusinessesOrOrganisations())
        .click(EntityDevelopedTheseGoodsPage.submit())
        .click(IntroduceSignificantlyImprovementPage.yes())
        .click(IntroduceSignificantlyImprovementPage.submit())
        .click(EntityMainlyDevelopedThesePage.thisBusinessOrEnterpriseGroup())
        .click(EntityMainlyDevelopedThesePage.thisBusinessWithOtherBusinessesOrOrganisations())
        .click(EntityMainlyDevelopedThesePage.otherBusinessesOrOrganisations())
        .click(EntityMainlyDevelopedThesePage.submit())
        .click(NewGoodsServicesInnovationsPage.yes())
        .click(NewGoodsServicesInnovationsPage.submit())
        .click(GoodsServicesInnovationsNewPage.yes())
        .click(GoodsServicesInnovationsNewPage.submit())
        .setValue(PercentageTurnover2016Page.marketNew(), 25)
        .setValue(PercentageTurnover2016Page.businessNew(), 25)
        .setValue(PercentageTurnover2016Page.improvement(), 25)
        .setValue(PercentageTurnover2016Page.modified(), 25)
        .click(PercentageTurnover2016Page.submit())
        .click(GoodsAndServicesInnovationCompletedPage.submit())

        //Process Innovation
        .click(ProcessImprovedPage.yes())
        .click(ProcessImprovedPage.submit())
        .click(DevelopedProcessesPage.thisBusinessOrEnterpriseGroup())
        .click(DevelopedProcessesPage.thisBusinessWithOtherBusinessesOrOrganisations())
        .click(DevelopedProcessesPage.otherBusinessesOrOrganisations())
        .click(DevelopedProcessesPage.submit())
        .click(ImprovedProcessesPage.yes())
        .click(ImprovedProcessesPage.submit())
        .click(ProcessInnovationCompletedPage.submit())

        //Constraints on Innovation
        .click(ConstraintsInnovationActivitiesPage.abandonedAnswserYes())
        .click(ConstraintsInnovationActivitiesPage.scaledBackAnswserYes())
        .click(ConstraintsInnovationActivitiesPage.ongoing2016AnswserYes())
        .click(ConstraintsInnovationActivitiesPage.submit())
        .click(ConstrainingInnovationEconomicPage.high())
        .click(ConstrainingInnovationEconomicPage.submit())
        .click(ConstrainingInnovationCostsPage.medium())
        .click(ConstrainingInnovationCostsPage.submit())
        .click(ConstrainingInnovationFinancePage.low())
        .click(ConstrainingInnovationFinancePage.submit())
        .click(ConstrainingInnovationAvailableFinancePage.notImportant())
        .click(ConstrainingInnovationAvailableFinancePage.submit())
        .click(ConstrainingInnovationLackQualifiedPage.high())
        .click(ConstrainingInnovationLackQualifiedPage.submit())
        .click(ConstrainingInnovationLackTechnologyPage.medium())
        .click(ConstrainingInnovationLackTechnologyPage.submit())
        .click(ConstrainingInnovationLackInformationPage.low())
        .click(ConstrainingInnovationLackInformationPage.submit())
        .click(ConstrainingInnovationDominatedPage.notImportant())
        .click(ConstrainingInnovationDominatedPage.submit())
        .click(ConstrainingInnovationUncertainPage.high())
        .click(ConstrainingInnovationUncertainPage.submit())
        .click(ConstrainingInnovationGovernmentPage.medium())
        .click(ConstrainingInnovationGovernmentPage.submit())
        .click(ConstrainingInnovationEuPage.low())
        .click(ConstrainingInnovationEuPage.submit())
        .click(ConstrainingInnovationReferendumPage.notImportant())
        .click(ConstrainingInnovationReferendumPage.submit())
        .click(ConstraintsOnInnovationCompletedPage.submit())

        //Factors Affecting Innovation
        .click(FactorsAffectingIncreasingRangePage.high())
        .click(FactorsAffectingIncreasingRangePage.submit())
        .click(FactorsAffectingNewMarketsPage.medium())
        .click(FactorsAffectingNewMarketsPage.submit())
        .click(FactorsAffectingMarketSharePage.low())
        .click(FactorsAffectingMarketSharePage.submit())
        .click(FactorsAffectingQualityPage.notImportant())
        .click(FactorsAffectingQualityPage.submit())
        .click(FactorsAffectingFlexibilityPage.medium())
        .click(FactorsAffectingFlexibilityPage.submit())
        .click(FactorsAffectingCapacityPage.notImportant())
        .click(FactorsAffectingCapacityPage.submit())
        .click(FactorsAffectingValuePage.high())
        .click(FactorsAffectingValuePage.submit())
        .click(FactorsAffectingReducingCostPage.medium())
        .click(FactorsAffectingReducingCostPage.submit())
        .click(FactorsAffectingHealthSafetyPage.low())
        .click(FactorsAffectingHealthSafetyPage.submit())
        .click(FactorsAffectingEnvironmentalPage.notImportant())
        .click(FactorsAffectingEnvironmentalPage.submit())
        .click(FactorsAffectingReplacingPage.high())
        .click(FactorsAffectingReplacingPage.submit())
        .click(FactorsAffectingRegulatoryPage.low())
        .click(FactorsAffectingRegulatoryPage.submit())
        .click(FactorsAffectingCompletedPage.submit())

        //Information Needed for Innovation
        .click(ImportancesInformationInnovationPage.high())
        .click(ImportancesInformationInnovationPage.submit())
        .click(ImportancesInformationSuppliersPage.medium())
        .click(ImportancesInformationSuppliersPage.submit())
        .click(ImportancesInformationClientPage.low())
        .click(ImportancesInformationClientPage.submit())
        .click(ImportancesInformationPublicSectorPage.notImportant())
        .click(ImportancesInformationPublicSectorPage.submit())
        .click(ImportancesInformationCompetitorsPage.medium())
        .click(ImportancesInformationCompetitorsPage.submit())
        .click(ImportancesInformationConsultantsPage.notImportant())
        .click(ImportancesInformationConsultantsPage.submit())
        .click(ImportancesInformationUniversitiesPage.high())
        .click(ImportancesInformationUniversitiesPage.submit())
        .click(ImportancesInformationGovernmentPage.medium())
        .click(ImportancesInformationGovernmentPage.submit())
        .click(ImportancesInformationConferencesPage.low())
        .click(ImportancesInformationConferencesPage.submit())
        .click(ImportancesInformationAssociationsPage.notImportant())
        .click(ImportancesInformationAssociationsPage.submit())
        .click(ImportancesInformationStandardsPage.high())
        .click(ImportancesInformationStandardsPage.submit())
        .click(ImportancesInformationPublicationsPage.low())
        .click(ImportancesInformationPublicationsPage.submit())
        .click(InformationNeededForInnovationCompletedPage.submit())

        //Co-operation on Innovation
        .click(CoOperationOtherBusinessesPage.ukRegional())
        .click(CoOperationOtherBusinessesPage.ukNational())
        .click(CoOperationOtherBusinessesPage.europeanCountries())
        .click(CoOperationOtherBusinessesPage.otherCountries())
        .click(CoOperationOtherBusinessesPage.submit())
        .click(CoOperationSuppliersPage.ukRegional())
        .click(CoOperationSuppliersPage.ukNational())
        .click(CoOperationSuppliersPage.europeanCountries())
        .click(CoOperationSuppliersPage.otherCountries())
        .click(CoOperationSuppliersPage.submit())
        .click(CoOperationPrivateSectorPage.ukRegional())
        .click(CoOperationPrivateSectorPage.ukNational())
        .click(CoOperationPrivateSectorPage.europeanCountries())
        .click(CoOperationPrivateSectorPage.otherCountries())
        .click(CoOperationPrivateSectorPage.submit())
        .click(CoOperationPublicSectorPage.ukRegional())
        .click(CoOperationPublicSectorPage.ukNational())
        .click(CoOperationPublicSectorPage.europeanCountries())
        .click(CoOperationPublicSectorPage.otherCountries())
        .click(CoOperationPublicSectorPage.submit())
        .click(CoOperationCompetitorsPage.ukRegional())
        .click(CoOperationCompetitorsPage.ukNational())
        .click(CoOperationCompetitorsPage.europeanCountries())
        .click(CoOperationCompetitorsPage.otherCountries())
        .click(CoOperationCompetitorsPage.submit())
        .click(CoOperationConsultantsPage.ukRegional())
        .click(CoOperationConsultantsPage.ukNational())
        .click(CoOperationConsultantsPage.europeanCountries())
        .click(CoOperationConsultantsPage.otherCountries())
        .click(CoOperationConsultantsPage.submit())
        .click(CoOperationInstitutionsPage.ukRegional())
        .click(CoOperationInstitutionsPage.ukNational())
        .click(CoOperationInstitutionsPage.europeanCountries())
        .click(CoOperationInstitutionsPage.otherCountries())
        .click(CoOperationInstitutionsPage.submit())
        .click(CoOperationGovernmentPage.ukRegional())
        .click(CoOperationGovernmentPage.ukNational())
        .click(CoOperationGovernmentPage.europeanCountries())
        .click(CoOperationGovernmentPage.otherCountries())
        .click(CoOperationGovernmentPage.submit())
        .click(InnovationsProtectedPatentsPage.none())
        .click(InnovationsProtectedPatentsPage.submit())
        .click(InnovationsProtectedDesignPage.lessThan40())
        .click(InnovationsProtectedDesignPage.submit())
        .click(InnovationsProtectedCopyrightPage.answer4090())
        .click(InnovationsProtectedCopyrightPage.submit())
        .click(InnovationsProtectedTrademarkPage.over90())
        .click(InnovationsProtectedTrademarkPage.submit())
        .click(InnovationsProtectedLeadTimePage.lessThan40())
        .click(InnovationsProtectedLeadTimePage.submit())
        .click(InnovationsProtectedServicesPage.none())
        .click(InnovationsProtectedServicesPage.submit())
        .click(InnovationsProtectedSecrecyPage.over90())
        .click(InnovationsProtectedSecrecyPage.submit())
        .click(CoOperationOnInnovationCompletedPage.submit())

        //Public Financial Support for Innovation
        .click(PublicFinancialSupportPage.authoritiesYes())
        .click(PublicFinancialSupportPage.centralGovernmentYes())
        .click(PublicFinancialSupportPage.euYes())
        .click(PublicFinancialSupportPage.submit())
        .click(KindFinancialCentralGovernmentSupportPage.directYes())
        .click(KindFinancialCentralGovernmentSupportPage.indirectNo())
        .click(KindFinancialCentralGovernmentSupportPage.submit())
        .click(PublicFinancialSupportForInnovationCompletedPage.submit())

        //Turnover and Exports
        .setValue(Turnover2014Page.answer(), 1703000)
        .click(Turnover2014Page.submit())
        .setValue(Turnover2016Page.answer(), 1703000)
        .click(Turnover2016Page.submit())
        .setValue(Exports2016Page.answer(), 1703000)
        .click(Exports2016Page.submit())
        .click(TurnoverAndExportsCompletedPage.submit())

        //Employees and Skills
        .setValue(Employees2014Page.answer(), 500)
        .click(Employees2014Page.submit())
        .setValue(Employees2016Page.answer(), 600)
        .click(Employees2016Page.submit())
        .setValue(EmployeesQualifications2016Page.answer(), 50)
        .setValue(EmployeesQualifications2016Page.answerOther(), 60)
        .click(EmployeesQualifications2016Page.submit())
        .click(EmployeesInHouseSkillsPage.graphicArtsLayoutAdvertising())
        .click(EmployeesInHouseSkillsPage.designOfObjectsOrServices())
        .click(EmployeesInHouseSkillsPage.multimediaWebDesignForExampleAudioGraphicsTextStillPicturesAnimationVideo())
        .click(EmployeesInHouseSkillsPage.softwareDevelopmentDatabaseManagement())
        .click(EmployeesInHouseSkillsPage.engineeringAppliedSciences())
        .click(EmployeesInHouseSkillsPage.mathematicsStatistics())
        .click(EmployeesInHouseSkillsPage.submit())
        .click(EmployeesAndSkillsCompletedPage.submit())

        //General Information
        .setValue(AdditionalCommentsPage.answer(), "Some additional comments on the survey")
        .click(AdditionalCommentsPage.submit())
        .setValue(HowLongPage.generalInformationHours(), 2)
        .setValue(HowLongPage.minutes(), 59)
        .click(HowLongPage.submit())
        .click(ApproachedTelephonePage.yes())
        .click(ApproachedTelephonePage.submit())

        .click(ConfirmationPage.submit())

        // Thank You
        .getUrl().should.eventually.contain(ThankYou.pageName);
    });
  });

});
