const helpers = require('../helpers');

const HouseholdCompositionPage = require('../generated_pages/repeating_household/household-composition.page.js');
const RepeatingBlock1Page = require('../generated_pages/repeating_household/repeating-block-1.page.js');
const RepeatingBlock2Page = require('../generated_pages/repeating_household/repeating-block-2.page.js');
const RepeatingBlock3Page = require('../generated_pages/repeating_household/repeating-block-3.page.js');
const SummaryPage = require('../generated_pages/repeating_household/summary.page.js');

describe('Household Repeating', function() {

  it('Given I enter one name, when I navigate through the subsequent group, I should see the name on each block.', function() {
    return helpers.startQuestionnaire('test_repeating_household.json').then(() => {
        return browser
          .setValue(HouseholdCompositionPage.firstName(),'Alpha')
          .setValue(HouseholdCompositionPage.lastName(),'One')
          .click(HouseholdCompositionPage.submit())
          .getText(RepeatingBlock1Page.displayedDescription()).should.eventually.contain("Alpha One")
          .setValue(RepeatingBlock1Page.whatIsYourAge(),'99')
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
          .setValue(RepeatingBlock1Page.whatIsYourAge(),'60')
          .click(RepeatingBlock1Page.submit())
          .getText(RepeatingBlock2Page.displayedName()).should.eventually.contain("Alpha One")
          .setValue(RepeatingBlock2Page.whatIsYourShoeSize(),'10')
          .click(RepeatingBlock2Page.submit())
          .getText(RepeatingBlock3Page.questionText()).should.eventually.contain("60")
          .getText(RepeatingBlock3Page.questionText()).should.eventually.contain("10")
          .click(RepeatingBlock3Page.yes())
          .click(RepeatingBlock3Page.submit())

          .getText(RepeatingBlock1Page.displayedDescription()).should.eventually.contain("Bravo Two")
          .setValue(RepeatingBlock1Page.whatIsYourAge(),'50')
          .click(RepeatingBlock1Page.submit())
          .getText(RepeatingBlock2Page.displayedName()).should.eventually.contain("Bravo Two")
          .setValue(RepeatingBlock2Page.whatIsYourShoeSize(),'11')
          .click(RepeatingBlock2Page.submit())
          .getText(RepeatingBlock3Page.questionText()).should.eventually.contain("50")
          .getText(RepeatingBlock3Page.questionText()).should.eventually.contain("11")
          .click(RepeatingBlock3Page.yes())
          .click(RepeatingBlock3Page.submit())

          .getText(RepeatingBlock1Page.displayedDescription()).should.eventually.contain("Charlie Three")
          .setValue(RepeatingBlock1Page.whatIsYourAge(),'40')
          .click(RepeatingBlock1Page.submit())
          .getText(RepeatingBlock2Page.displayedName()).should.eventually.contain("Charlie Three")
          .setValue(RepeatingBlock2Page.whatIsYourShoeSize(),'12')
          .click(RepeatingBlock2Page.submit())
          .getText(RepeatingBlock3Page.questionText()).should.eventually.contain("40")
          .getText(RepeatingBlock3Page.questionText()).should.eventually.contain("12")
          .click(RepeatingBlock3Page.yes())
          .click(RepeatingBlock3Page.submit())

          .then(checkSummaryBlockPage);
    });
  });
});


function checkSummaryBlockPage() {
  return browser
    .getUrl().should.eventually.contain(SummaryPage.pageName)

    .getText(SummaryPage.multipleQuestionsGroupTitle()).should.eventually.contain("Group 1")

    .getText(SummaryPage.firstName()).should.eventually.contain("Alpha")
    .getText(SummaryPage.middleNames()).should.eventually.contain("No answer provided")
    .getText(SummaryPage.lastName()).should.eventually.contain("One")

    .getText(SummaryPage.repeatingGroupTitle()).should.eventually.contain("Alpha One")
    .getText(SummaryPage.whatIsYourAge()).should.eventually.contain("60")
    .getText(SummaryPage.whatIsYourShoeSize()).should.eventually.contain("10")
    .getText(SummaryPage.confirmAnswer()).should.eventually.contain("Yes")

    .getText(SummaryPage.repeatingGroupTitle(1)).should.eventually.contain("Bravo Two")
    .getText(SummaryPage.whatIsYourAge(1)).should.eventually.contain("50")
    .getText(SummaryPage.whatIsYourShoeSize(1)).should.eventually.contain("11")
    .getText(SummaryPage.confirmAnswer(1)).should.eventually.contain("Yes")

    .getText(SummaryPage.repeatingGroupTitle(2)).should.eventually.contain("Charlie Three")
    .getText(SummaryPage.whatIsYourAge(2)).should.eventually.contain("40")
    .getText(SummaryPage.whatIsYourShoeSize(2)).should.eventually.contain("12")
    .getText(SummaryPage.confirmAnswer(2)).should.eventually.contain("Yes");
}
