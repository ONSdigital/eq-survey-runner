const helpers = require('../../helpers');

const BusinessChanges = require('../../pages/surveys/ukis/business-changes.page.js');
const ConstrainingInnovationReferendum = require('../../pages/surveys/ukis/constraining-innovation-referendum.page.js');
const ConstraintsOnInnovationCompleted = require('../../pages/surveys/ukis/constraints-on-innovation-completed.page.js');
const InternalInvestmentRD = require('../../pages/surveys/ukis/internal-investment-r-d.page.js');
const AcquisitionInternalInvestmentRD = require('../../pages/surveys/ukis/acquisition-internal-investment-r-d.page.js');
const InvestmentAdvancedMachinery = require('../../pages/surveys/ukis/investment-advanced-machinery.page.js');
const InvestmentExistingKnowledgeInnovation = require('../../pages/surveys/ukis/investment-existing-knowledge-innovation.page.js');
const InvestmentTrainingInnovative = require('../../pages/surveys/ukis/investment-training-innovative.page.js');
const InvestmentDesignFutureInnovation = require('../../pages/surveys/ukis/investment-design-future-innovation.page.js');
const InvestmentIntroductionInnovations = require('../../pages/surveys/ukis/investment-introduction-innovations.page.js');
const IntroducingSignificantlyImprovedGoods = require('../../pages/surveys/ukis/introducing-significantly-improved-goods.page.js');
const IntroduceSignificantlyImprovement = require('../../pages/surveys/ukis/introduce-significantly-improvement.page.js');
const ProcessImproved = require('../../pages/surveys/ukis/process-improved.page.js');
const ConstraintsInnovationActivities = require('../../pages/surveys/ukis/constraints-innovation-activities.page.js');
const NotNecessaryPossible = require('../../pages/surveys/ukis/not-necessary-possible.page.js');
const PublicFinancialSupport = require('../../pages/surveys/ukis/public-financial-support.page.js');

describe('Example Test', function() {

  it('Given I have selected Yes to 2.1, When I do not answer 6.13, Then I will be routed to Section 7', function() {
    return helpers.startQuestionnaire('1_0001.json').then(() => {
        return browser

        .click(helpers.navigationLink('Business Strategy & Practices'))
        .getUrl().should.eventually.contain(BusinessChanges.pageName)
        .click(BusinessChanges.yes())
        .click(BusinessChanges.submit())

        .click(helpers.navigationLink('Constraints on Innovation'))
        .then(() => {
            return helpers.pressSubmit(12);
        })
        .getUrl().should.eventually.contain(ConstrainingInnovationReferendum.pageName)
        .click(ConstrainingInnovationReferendum.submit())

        .getUrl().should.eventually.contain(ConstraintsOnInnovationCompleted.pageName);
    });
  });

  it('Given I have selected Yes to 3.1, When I am answering question 6.13 , Then I will be routed to section 7', function() {
    return helpers.startQuestionnaire('1_0001.json').then(() => {
        return browser

        .click(helpers.navigationLink('Innovation Investment'))

        // when
        .getUrl().should.eventually.contain(InternalInvestmentRD.pageName)
        .click(InternalInvestmentRD.yes())
        .click(InternalInvestmentRD.submit())

        .click(helpers.navigationLink('Constraints on Innovation'))
        .then(() => {
            return helpers.pressSubmit(12);
        })

        // then
        .getUrl().should.eventually.contain(ConstrainingInnovationReferendum.pageName)
        .click(ConstrainingInnovationReferendum.medium())
        .click(ConstrainingInnovationReferendum.submit())

        .getUrl().should.eventually.contain(ConstraintsOnInnovationCompleted.pageName);
    });
  });

  it('Given I have selected Yes to 3.4, When I am answering question 6.13 , Then I will be routed to section 7', function() {
    return helpers.startQuestionnaire('1_0001.json').then(() => {
        return browser

        .click(helpers.navigationLink('Innovation Investment'))
        .getUrl().should.eventually.contain(InternalInvestmentRD.pageName)
        .click(InternalInvestmentRD.submit())

        // when
        .getUrl().should.eventually.contain(AcquisitionInternalInvestmentRD.pageName)
        .click(AcquisitionInternalInvestmentRD.yes())
        .click(AcquisitionInternalInvestmentRD.submit())

        .click(helpers.navigationLink('Constraints on Innovation'))
        .then(() => {
            return helpers.pressSubmit(12);
        })

        // then
        .getUrl().should.eventually.contain(ConstrainingInnovationReferendum.pageName)
        .click(ConstrainingInnovationReferendum.medium())
        .click(ConstrainingInnovationReferendum.submit())

        .getUrl().should.eventually.contain(ConstraintsOnInnovationCompleted.pageName);
    });
  });

  it('Given I have selected Yes to 3.6, When I am answering question 6.13 , Then I will be routed to section 7', function() {
    return helpers.startQuestionnaire('1_0001.json').then(() => {
        return browser

        .click(helpers.navigationLink('Innovation Investment'))
        .getUrl().should.eventually.contain(InternalInvestmentRD.pageName)
        .click(InternalInvestmentRD.submit())
        .click(AcquisitionInternalInvestmentRD.submit())

        // when
        .getUrl().should.eventually.contain(InvestmentAdvancedMachinery.pageName)
        .click(InvestmentAdvancedMachinery.yes())
        .click(InvestmentAdvancedMachinery.submit())

        .click(helpers.navigationLink('Constraints on Innovation'))
        .then(() => {
            return helpers.pressSubmit(12);
        })

        // then
        .getUrl().should.eventually.contain(ConstrainingInnovationReferendum.pageName)
        .click(ConstrainingInnovationReferendum.medium())
        .click(ConstrainingInnovationReferendum.submit())

        .getUrl().should.eventually.contain(ConstraintsOnInnovationCompleted.pageName);
    });
  });

  it('Given I have selected Yes to 3.9, When I am answering question 6.13 , Then I will be routed to section 7', function() {
    return helpers.startQuestionnaire('1_0001.json').then(() => {
        return browser

        .click(helpers.navigationLink('Innovation Investment'))
        .getUrl().should.eventually.contain(InternalInvestmentRD.pageName)
        .then(() => {
            return helpers.pressSubmit(3);
        })

        // when
        .getUrl().should.eventually.contain(InvestmentExistingKnowledgeInnovation.pageName)
        .click(InvestmentExistingKnowledgeInnovation.yes())
        .click(InvestmentExistingKnowledgeInnovation.submit())

        .click(helpers.navigationLink('Constraints on Innovation'))
        .then(() => {
            return helpers.pressSubmit(12);
        })

        // then
        .getUrl().should.eventually.contain(ConstrainingInnovationReferendum.pageName)
        .click(ConstrainingInnovationReferendum.medium())
        .click(ConstrainingInnovationReferendum.submit())

        .getUrl().should.eventually.contain(ConstraintsOnInnovationCompleted.pageName);
    });
  });

  it('Given I have selected Yes to 3.11, When I am answering question 6.13 , Then I will be routed to section 7', function() {
    return helpers.startQuestionnaire('1_0001.json').then(() => {
        return browser

        .click(helpers.navigationLink('Innovation Investment'))
        .getUrl().should.eventually.contain(InternalInvestmentRD.pageName)
        .then(() => {
            return helpers.pressSubmit(4);
        })

        // when
        .getUrl().should.eventually.contain(InvestmentTrainingInnovative.pageName)
        .click(InvestmentTrainingInnovative.yes())
        .click(InvestmentTrainingInnovative.submit())

        .click(helpers.navigationLink('Constraints on Innovation'))
        .then(() => {
            return helpers.pressSubmit(12);
        })

        // then
        .getUrl().should.eventually.contain(ConstrainingInnovationReferendum.pageName)
        .click(ConstrainingInnovationReferendum.medium())
        .click(ConstrainingInnovationReferendum.submit())

        .getUrl().should.eventually.contain(ConstraintsOnInnovationCompleted.pageName);
    });
  });

  it('Given I have selected Yes to 3.13, When I am answering question 6.13 , Then I will be routed to section 7', function() {
    return helpers.startQuestionnaire('1_0001.json').then(() => {
        return browser

        .click(helpers.navigationLink('Innovation Investment'))
        .getUrl().should.eventually.contain(InternalInvestmentRD.pageName)
        .then(() => {
            return helpers.pressSubmit(5);
        })

        // when
        .getUrl().should.eventually.contain(InvestmentDesignFutureInnovation.pageName)
        .click(InvestmentDesignFutureInnovation.yes())
        .click(InvestmentDesignFutureInnovation.submit())

        .click(helpers.navigationLink('Constraints on Innovation'))
        .then(() => {
            return helpers.pressSubmit(12);
        })

        // then
        .getUrl().should.eventually.contain(ConstrainingInnovationReferendum.pageName)
        .click(ConstrainingInnovationReferendum.medium())
        .click(ConstrainingInnovationReferendum.submit())

        .getUrl().should.eventually.contain(ConstraintsOnInnovationCompleted.pageName);
    });
  });

  it('Given I have selected Yes to 3.15, When I am answering question 6.13 , Then I will be routed to section 7', function() {
    return helpers.startQuestionnaire('1_0001.json').then(() => {
        return browser

        .click(helpers.navigationLink('Innovation Investment'))
        .getUrl().should.eventually.contain(InternalInvestmentRD.pageName)
        .then(() => {
            return helpers.pressSubmit(6);
        })

        // when
        .getUrl().should.eventually.contain(InvestmentIntroductionInnovations.pageName)
        .click(InvestmentIntroductionInnovations.yes())
        .click(InvestmentIntroductionInnovations.submit())

        .click(helpers.navigationLink('Constraints on Innovation'))
        .then(() => {
            return helpers.pressSubmit(12);
        })

        // then
        .getUrl().should.eventually.contain(ConstrainingInnovationReferendum.pageName)
        .click(ConstrainingInnovationReferendum.medium())
        .click(ConstrainingInnovationReferendum.submit())

        .getUrl().should.eventually.contain(ConstraintsOnInnovationCompleted.pageName);
    });
  });

  it('Given I have selected Yes to 4.1, When I am answering question 6.13 , Then I will be routed to section 7', function() {
    return helpers.startQuestionnaire('1_0001.json').then(() => {
        return browser

        .click(helpers.navigationLink('Goods and Services Innovation'))

        // when
        .getUrl().should.eventually.contain(IntroducingSignificantlyImprovedGoods.pageName)
        .click(IntroducingSignificantlyImprovedGoods.yes())
        .click(IntroducingSignificantlyImprovedGoods.submit())

        .click(helpers.navigationLink('Constraints on Innovation'))
        .then(() => {
            return helpers.pressSubmit(12);
        })

        // then
        .getUrl().should.eventually.contain(ConstrainingInnovationReferendum.pageName)
        .click(ConstrainingInnovationReferendum.medium())
        .click(ConstrainingInnovationReferendum.submit())

        .getUrl().should.eventually.contain(ConstraintsOnInnovationCompleted.pageName);
    });
  });

  it('Given I have selected Yes to 4.3, When I am answering question 6.13 , Then I will be routed to section 7', function() {
    return helpers.startQuestionnaire('1_0001.json').then(() => {
        return browser

        .click(helpers.navigationLink('Goods and Services Innovation'))
        .click(IntroducingSignificantlyImprovedGoods.submit())

        // when
        .getUrl().should.eventually.contain(IntroduceSignificantlyImprovement.pageName)
        .click(IntroduceSignificantlyImprovement.yes())
        .click(IntroduceSignificantlyImprovement.submit())

        .click(helpers.navigationLink('Constraints on Innovation'))
        .then(() => {
            return helpers.pressSubmit(12);
        })

        // then
        .getUrl().should.eventually.contain(ConstrainingInnovationReferendum.pageName)
        .click(ConstrainingInnovationReferendum.medium())
        .click(ConstrainingInnovationReferendum.submit())

        .getUrl().should.eventually.contain(ConstraintsOnInnovationCompleted.pageName);
    });
  });

  it('Given I have selected Yes to 5.1, When I am answering question 6.13 , Then I will be routed to section 7', function() {
    return helpers.startQuestionnaire('1_0001.json').then(() => {
        return browser

        .click(helpers.navigationLink('Process Innovation'))

        // when
        .getUrl().should.eventually.contain(ProcessImproved.pageName)
        .click(ProcessImproved.yes())
        .click(ProcessImproved.submit())

        .click(helpers.navigationLink('Constraints on Innovation'))
        .then(() => {
            return helpers.pressSubmit(12);
        })

        // then
        .getUrl().should.eventually.contain(ConstrainingInnovationReferendum.pageName)
        .click(ConstrainingInnovationReferendum.medium())
        .click(ConstrainingInnovationReferendum.submit())

        .getUrl().should.eventually.contain(ConstraintsOnInnovationCompleted.pageName);
    });
  });

  it('Given I have selected Yes to 6.1, When I am answering question 6.13 , Then I will be routed to section 7', function() {
    return helpers.startQuestionnaire('1_0001.json').then(() => {
        return browser

        .click(helpers.navigationLink('Constraints on Innovation'))

        // when
        .getUrl().should.eventually.contain(ConstraintsInnovationActivities.pageName)
        .click(ConstraintsInnovationActivities.abandonedAnswserYes())

        .then(() => {
            return helpers.pressSubmit(12);
        })

        // then
        .getUrl().should.eventually.contain(ConstrainingInnovationReferendum.pageName)
        .click(ConstrainingInnovationReferendum.medium())
        .click(ConstrainingInnovationReferendum.submit())

        .getUrl().should.eventually.contain(ConstraintsOnInnovationCompleted.pageName);
    });
  });

  it('Given I have a combination of NO and not selected answers to questions 2.1, 3.1, 3.4, 3.6, 3.9, 3.11, 3.13, 3.15, 4.1, 4.3, 5.1 6.1, When I am answering question 6.13, Then I WILL see question 6.14 and then be routed to section 10', function() {
    return helpers.startQuestionnaire('1_0001.json').then(() => {
        return browser

        // when 2..
        .click(helpers.navigationLink('Business Strategy & Practices'))
        .getUrl().should.eventually.contain(BusinessChanges.pageName)
        .click(BusinessChanges.no())
        .click(BusinessChanges.submit())

        // when 3..
        .click(helpers.navigationLink('Innovation Investment'))
        .getUrl().should.eventually.contain(InternalInvestmentRD.pageName)
        .click(InternalInvestmentRD.no())
        .then(() => {
            return helpers.pressSubmit(3);
        })
        .getUrl().should.eventually.contain(InvestmentExistingKnowledgeInnovation.pageName)
        .click(InvestmentExistingKnowledgeInnovation.no())
        .then(() => {
            return helpers.pressSubmit(3);
        })
        .getUrl().should.eventually.contain(InvestmentIntroductionInnovations.pageName)
        .click(InvestmentIntroductionInnovations.no())
        .click(InvestmentIntroductionInnovations.submit())

        // when 4..
        .click(helpers.navigationLink('Goods and Services Innovation'))
        .click(IntroducingSignificantlyImprovedGoods.submit())
        .getUrl().should.eventually.contain(IntroduceSignificantlyImprovement.pageName)
        .click(IntroduceSignificantlyImprovement.no())
        .click(IntroduceSignificantlyImprovement.submit())

        // when 5.1
        .click(helpers.navigationLink('Process Innovation'))
        .getUrl().should.eventually.contain(ProcessImproved.pageName)
        .click(ProcessImproved.no())
        .click(ProcessImproved.submit())

        // when 6..
        .click(helpers.navigationLink('Constraints on Innovation'))
        .getUrl().should.eventually.contain(ConstraintsInnovationActivities.pageName)
        .then(() => {
            return helpers.pressSubmit(12);
        })

        // when 6.13
        .getUrl().should.eventually.contain(ConstrainingInnovationReferendum.pageName)
        .click(ConstrainingInnovationReferendum.medium())
        .click(ConstrainingInnovationReferendum.submit())

        // then
        .getUrl().should.eventually.contain(NotNecessaryPossible.pageName);
    });
  });

  it('Given I have not selected answers to questions 2.1, 3.1, 3.4, 3.6, 3.9, 3.11, 3.13, 3.15, 4.1, 4.3, 5.1 6.1, When I am answering question 6.13, Then I WILL see question 6.14 and then be routed to section 10', function() {
    return helpers.startQuestionnaire('1_0001.json').then(() => {
        return browser

        // **** Attempt 6.13 without answering anything else ****
         // when 6.13
        .click(helpers.navigationLink('Constraints on Innovation'))
        .getUrl().should.eventually.contain(ConstraintsInnovationActivities.pageName)
        .then(() => {
            return helpers.pressSubmit(12);
        })

        .getUrl().should.eventually.contain(ConstrainingInnovationReferendum.pageName)
        .click(ConstrainingInnovationReferendum.medium())
        .click(ConstrainingInnovationReferendum.submit())

        // then
        .getUrl().should.eventually.contain(NotNecessaryPossible.pageName)
        .click(NotNecessaryPossible.submit())
        .click(ConstraintsOnInnovationCompleted.submit())
        .getUrl().should.eventually.contain(PublicFinancialSupport.pageName)

        // **** Attempt 6.13 with non response submissions on anything else ****
        // when 2..
        .click(helpers.navigationLink('Business Strategy & Practices'))
        .getUrl().should.eventually.contain(BusinessChanges.pageName)
        .click(BusinessChanges.submit())

        // when 3..
        .click(helpers.navigationLink('Innovation Investment'))
        .getUrl().should.eventually.contain(InternalInvestmentRD.pageName)
        .then(() => {
            return helpers.pressSubmit(7);
        })

        // when 4..
        .click(helpers.navigationLink('Goods and Services Innovation'))
        .getUrl().should.eventually.contain(IntroducingSignificantlyImprovedGoods.pageName)
        .then(() => {
            return helpers.pressSubmit(2);
        })
        // when 5.1
        .click(helpers.navigationLink('Process Innovation'))
        .getUrl().should.eventually.contain(ProcessImproved.pageName)
        .click(ProcessImproved.submit())

        // when 6...
        .click(helpers.navigationLink('Constraints on Innovation'))
        .getUrl().should.eventually.contain(ConstraintsInnovationActivities.pageName)
        .then(() => {
            return helpers.pressSubmit(12);
        })

         // when 6.13
        .getUrl().should.eventually.contain(ConstrainingInnovationReferendum.pageName)
        .click(ConstrainingInnovationReferendum.medium())
        .click(ConstrainingInnovationReferendum.submit())

        // then
        .getUrl().should.eventually.contain(NotNecessaryPossible.pageName)
        .click(NotNecessaryPossible.submit())
        .click(ConstraintsOnInnovationCompleted.submit())
        .getUrl().should.eventually.contain(PublicFinancialSupport.pageName);
    });
  });

});
