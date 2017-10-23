const helpers = require('../../helpers');

const IntroducingSignificantlyImprovedGoodsPage = require('../../pages/surveys/ukis/introducing-significantly-improved-goods.page.js');
const IntroduceSignificantlyImprovementPage = require('../../pages/surveys/ukis/introduce-significantly-improvement.page.js');
const EntityMainlyDevelopedThese = require('../../pages/surveys/ukis/entity-mainly-developed-these.page.js');
const NewGoodsServicesInnovations = require('../../pages/surveys/ukis/new-goods-services-innovations.page.js');
const GoodsServicesInnovationsNew = require('../../pages/surveys/ukis/goods-services-innovations-new.page.js');
const PercentageTurnover2016 = require('../../pages/surveys/ukis/percentage-turnover-2016.page.js');
const GoodsAndServicesInnovationCompleted = require('../../pages/surveys/ukis/goods-and-services-innovation-completed.page.js');

describe('Example Test', function() {

  it('Given I am answering question 4.1 under 4. Goods and Services Innovation block, When no response or No is selected, Then I am routed to question 4.3', function() {
    return helpers.startQuestionnaire('1_0001.json').then(() => {
        return browser

        .click(helpers.navigationLink('Goods and Services Innovation'))
        .getUrl().should.eventually.contain(IntroducingSignificantlyImprovedGoodsPage.pageName)

        // when submit without a response
        .click(IntroducingSignificantlyImprovedGoodsPage.submit())
        .getUrl().should.eventually.contain(IntroduceSignificantlyImprovementPage.pageName)
        .click(IntroduceSignificantlyImprovementPage.previous())

        // when No selected
        .click(IntroducingSignificantlyImprovedGoodsPage.no())
        .click(IntroducingSignificantlyImprovedGoodsPage.submit())
        .getUrl().should.eventually.contain(IntroduceSignificantlyImprovementPage.pageName);
    });
  });

  it('Given the Goods and Services Innovation block, When I answer No to question 4.1 and Yes to question 4.3, Then I will see questions 4.5, 4.6 & 4.7', function() {
    return helpers.startQuestionnaire('1_0001.json').then(() => {
        return browser

        .click(helpers.navigationLink('Goods and Services Innovation'))
        .getUrl().should.eventually.contain(IntroducingSignificantlyImprovedGoodsPage.pageName)
        // When
        .click(IntroducingSignificantlyImprovedGoodsPage.no())
        .click(IntroducingSignificantlyImprovedGoodsPage.submit())
        .click(IntroduceSignificantlyImprovementPage.yes())
        .click(IntroduceSignificantlyImprovementPage.submit())
        .click(EntityMainlyDevelopedThese.submit())
        // Then
        .getUrl().should.eventually.contain(NewGoodsServicesInnovations.pageName)
        .click(NewGoodsServicesInnovations.submit())
        .getUrl().should.eventually.contain(GoodsServicesInnovationsNew.pageName)
        .click(GoodsServicesInnovationsNew.submit())
        .getUrl().should.eventually.contain(PercentageTurnover2016.pageName)
        .click(PercentageTurnover2016.submit());
    });
  });

  it('Given the Goods and Services Innovation block, When I answer No to question 4.1 and no response or No to question 4.3, Then I will NOT see questions 4.5, 4.6 & 4.7', function() {
    return helpers.startQuestionnaire('1_0001.json').then(() => {
        return browser

        .click(helpers.navigationLink('Goods and Services Innovation'))
        .getUrl().should.eventually.contain(IntroducingSignificantlyImprovedGoodsPage.pageName)
        // When
        .click(IntroducingSignificantlyImprovedGoodsPage.no())
        .click(IntroducingSignificantlyImprovedGoodsPage.submit())

        .click(IntroduceSignificantlyImprovementPage.submit())
        // Then
        .getUrl().should.eventually.contain(GoodsAndServicesInnovationCompleted.pageName)
        .click(GoodsAndServicesInnovationCompleted.previous())
        // When
        .click(IntroduceSignificantlyImprovementPage.no())
        .click(IntroduceSignificantlyImprovementPage.submit())
        // Then
        .getUrl().should.eventually.contain(GoodsAndServicesInnovationCompleted.pageName);

    });
  });

  it('Given I am answering question 4.1 under 4. Goods and Services Innovation block, When I do not select a response for 4.1 and answer Yes for 4.3, Then I will see questions 4.5, 4.6 & 4.7', function() {
    return helpers.startQuestionnaire('1_0001.json').then(() => {
        return browser

        .click(helpers.navigationLink('Goods and Services Innovation'))
        .getUrl().should.eventually.contain(IntroducingSignificantlyImprovedGoodsPage.pageName)
        // When
        .click(IntroducingSignificantlyImprovedGoodsPage.submit())
        .click(IntroduceSignificantlyImprovementPage.yes())
        .click(IntroduceSignificantlyImprovementPage.submit())
        .click(EntityMainlyDevelopedThese.submit())
        // Then
        .getUrl().should.eventually.contain(NewGoodsServicesInnovations.pageName)
        .click(NewGoodsServicesInnovations.submit())
        .getUrl().should.eventually.contain(GoodsServicesInnovationsNew.pageName)
        .click(GoodsServicesInnovationsNew.submit())
        .getUrl().should.eventually.contain(PercentageTurnover2016.pageName)
        .click(PercentageTurnover2016.submit());
    });
  });

  it('Given I am answering question 4.1 under 4. Goods and Services Innovation block, When I do not select a response for 4.1 and I do not answer 4.3, Then I will NOT see questions 4.5, 4.6 & 4.7', function() {
    return helpers.startQuestionnaire('1_0001.json').then(() => {
        return browser

        .click(helpers.navigationLink('Goods and Services Innovation'))
        .getUrl().should.eventually.contain(IntroducingSignificantlyImprovedGoodsPage.pageName)
        // When
        .click(IntroducingSignificantlyImprovedGoodsPage.submit())
        .click(IntroduceSignificantlyImprovementPage.submit())
        // Then
        .getUrl().should.eventually.contain(GoodsAndServicesInnovationCompleted.pageName)

    });
  });

});
