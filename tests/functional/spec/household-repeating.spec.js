const helpers = require('../helpers');

const HouseholdCompositionPage = require('../pages/surveys/household/household-composition.page.js');
const RepeatingBlock1Page = require('../pages/surveys/household/repeating-block-1.page.js');
const RepeatingBlock2Page = require('../pages/surveys/household/repeating-block-2.page.js');
const RepeatingBlock3Page = require('../pages/surveys/household/repeating-block-3.page.js');
const SummaryPage = require('../pages/surveys/household/summary.page.js');

describe('Household Repeating', function() {

  it('Given I enter one name, when I navigate through the subsequent group, I should see the name on each block.', function() {
    return helpers.startQuestionnaire('test_repeating_household.json').then(() => {
        return browser
          .setValue(HouseholdCompositionPage.firstName(),'Alpha')
          .setValue(HouseholdCompositionPage.lastName(),'One')
          .click(HouseholdCompositionPage.submit())
          .getText(RepeatingBlock1Page.displayedDescription()).should.eventually.contain("Alpha One")
          .setValue(RepeatingBlock1Page.answer(),'99')
          .click(RepeatingBlock1Page.submit())
          .getText(RepeatingBlock2Page.displayedName()).should.eventually.contain("Alpha One");
    });
  });

  it('Given I enter multiple names, when I navigate through the subsequent groups, I should the names on their respective blocks.', function() {
    return helpers.startQuestionnaire('test_repeating_household.json').then(() => {
        return browser
          .setValue(HouseholdCompositionPage.firstName(),'Alpha')
          .setValue(HouseholdCompositionPage.lastName(),'One')
          .click(HouseholdCompositionPage.addPerson())
          .setValue(HouseholdCompositionPage.firstName('_1'),'Bravo')
          .setValue(HouseholdCompositionPage.lastName('_1'),'Two')
          .click(HouseholdCompositionPage.addPerson())
          .setValue(HouseholdCompositionPage.firstName('_2'),'Charlie')
          .setValue(HouseholdCompositionPage.lastName('_2'),'Three')
          .click(HouseholdCompositionPage.submit())

          .getText(RepeatingBlock1Page.displayedDescription()).should.eventually.contain("Alpha One")
          .setValue(RepeatingBlock1Page.answer(),'60')
          .click(RepeatingBlock1Page.submit())
          .getText(RepeatingBlock2Page.displayedName()).should.eventually.contain("Alpha One")
          .setValue(RepeatingBlock2Page.answer(),'10')
          .click(RepeatingBlock2Page.submit())
          .getText(RepeatingBlock3Page.questionText()).should.eventually.contain("60")
          .getText(RepeatingBlock3Page.questionText()).should.eventually.contain("10")
          .click(RepeatingBlock3Page.yes())
          .click(RepeatingBlock3Page.submit())

          .getText(RepeatingBlock1Page.displayedDescription()).should.eventually.contain("Bravo Two")
          .setValue(RepeatingBlock1Page.answer(),'50')
          .click(RepeatingBlock1Page.submit())
          .getText(RepeatingBlock2Page.displayedName()).should.eventually.contain("Bravo Two")
          .setValue(RepeatingBlock2Page.answer(),'11')
          .click(RepeatingBlock2Page.submit())
          .getText(RepeatingBlock3Page.questionText()).should.eventually.contain("50")
          .getText(RepeatingBlock3Page.questionText()).should.eventually.contain("11")
          .click(RepeatingBlock3Page.yes())
          .click(RepeatingBlock3Page.submit())

          .getText(RepeatingBlock1Page.displayedDescription()).should.eventually.contain("Charlie Three")
          .setValue(RepeatingBlock1Page.answer(),'40')
          .click(RepeatingBlock1Page.submit())
          .getText(RepeatingBlock2Page.displayedName()).should.eventually.contain("Charlie Three")
          .setValue(RepeatingBlock2Page.answer(),'12')
          .click(RepeatingBlock2Page.submit())
          .getText(RepeatingBlock3Page.questionText()).should.eventually.contain("40")
          .getText(RepeatingBlock3Page.questionText()).should.eventually.contain("12")
          .click(RepeatingBlock3Page.yes())
          .click(RepeatingBlock3Page.submit())

          .getUrl().should.eventually.contain(SummaryPage.pageName);
    });
  });

});

