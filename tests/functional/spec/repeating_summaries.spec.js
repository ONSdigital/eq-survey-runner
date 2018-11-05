const helpers = require('../helpers');

const PrimaryNameBlockPage = require('../generated_pages/repeat_until_summaries/primary-name-block.page.js');
const RepeatingAnyoneElseBlockPage = require('../generated_pages/repeat_until_summaries/repeating-anyone-else-block.page.js');
const RepeatingNameBlockPage = require('../generated_pages/repeat_until_summaries/repeating-name-block.page.js');
const HouseholdSummaryBlockPage = require('../generated_pages/repeat_until_summaries/household-summary-block.page.js');
const FirstNumberBlockPage = require('../generated_pages/repeat_until_summaries/first-number-block.page.js');
const SecondNumberBlockPage = require('../generated_pages/repeat_until_summaries/second-number-block.page.js');
const CurrencyTotalPlaybackPage = require('../generated_pages/repeat_until_summaries/currency-total-playback.page.js');
const MemberSummaryBlockPage = require('../generated_pages/repeat_until_summaries/member-summary-block.page.js');
const SummaryPage = require('../generated_pages/repeat_until_summaries/summary.page.js');
const ThankYouPage = require('../base_pages/thank-you.page.js');

describe('Repeat Until Summaries', function() {

  before("Launch Survey", function () {
    return helpers.openQuestionnaire('test_repeat_until_summaries.json');
  });

  it('Given I complete the Household Section, When I get to see the section summary, Then I should see all answers in that section', function() {
    return browser
      .setValue(PrimaryNameBlockPage.primaryName(), 'Aaa')
      .click(PrimaryNameBlockPage.submit())
      .click(RepeatingAnyoneElseBlockPage.yes())
      .click(RepeatingAnyoneElseBlockPage.submit())

      .setValue(RepeatingNameBlockPage.repeatingName(), 'Bbb')
      .click(RepeatingNameBlockPage.submit())
      .click(RepeatingAnyoneElseBlockPage.yes())
      .click(RepeatingAnyoneElseBlockPage.submit())

      .setValue(RepeatingNameBlockPage.repeatingName(), 'Ccc')
      .click(RepeatingNameBlockPage.submit())
      .click(RepeatingAnyoneElseBlockPage.no())
      .click(RepeatingAnyoneElseBlockPage.submit())

      .getUrl().should.eventually.contain(HouseholdSummaryBlockPage.pageName)

      .then(checkHouseholdSummaryBlockPage)
      .click(HouseholdSummaryBlockPage.submit());
  });

  it("Given I complete the First Member group, When I get to see the calculation summary, Then I should see the correct total for the first member", function () {
    return browser

      .setValue(FirstNumberBlockPage.firstNumber(), '1')
      .click(FirstNumberBlockPage.submit())
      .setValue(SecondNumberBlockPage.secondNumber(), '10')
      .click(SecondNumberBlockPage.submit())

      .getUrl().should.eventually.contain(CurrencyTotalPlaybackPage.pageName)

      .getText(CurrencyTotalPlaybackPage.firstNumberAnswer()).should.eventually.contain("1")
      .getText(CurrencyTotalPlaybackPage.firstNumberAnswerLabel()).should.eventually.contain("First value for Aaa")
      .getText(CurrencyTotalPlaybackPage.secondNumberAnswer()).should.eventually.contain("10")
      .getText(CurrencyTotalPlaybackPage.secondNumberAnswerLabel()).should.eventually.contain("Second value for Aaa")
      .click(CurrencyTotalPlaybackPage.submit());
  });

  it("Given I complete the Second Member group, When I get to see the calculation summary, Then I should see the correct total for the second member", function () {
    return browser

      .setValue(FirstNumberBlockPage.firstNumber(), '2')
      .click(FirstNumberBlockPage.submit())
      .setValue(SecondNumberBlockPage.secondNumber(), '20')
      .click(SecondNumberBlockPage.submit())

      .getUrl().should.eventually.contain(CurrencyTotalPlaybackPage.pageName)

      .getText(CurrencyTotalPlaybackPage.firstNumberAnswer(1)).should.eventually.contain("2")
      .getText(CurrencyTotalPlaybackPage.firstNumberAnswerLabel(1)).should.eventually.contain("First value for Bbb")
      .getText(CurrencyTotalPlaybackPage.secondNumberAnswer(1)).should.eventually.contain("20")
      .getText(CurrencyTotalPlaybackPage.secondNumberAnswerLabel(1)).should.eventually.contain("Second value for Bbb")
      .click(CurrencyTotalPlaybackPage.submit());
  });

  it("Given I complete the Third Member group, When I get to see the calculation summary, Then I should see the correct total for the third member", function () {
    return browser

      .setValue(FirstNumberBlockPage.firstNumber(), '3')
      .click(FirstNumberBlockPage.submit())
      .setValue(SecondNumberBlockPage.secondNumber(), '30')
      .click(SecondNumberBlockPage.submit())

      .getUrl().should.eventually.contain(CurrencyTotalPlaybackPage.pageName)

      .getText(CurrencyTotalPlaybackPage.firstNumberAnswer(2)).should.eventually.contain("3")
      .getText(CurrencyTotalPlaybackPage.firstNumberAnswerLabel(2)).should.eventually.contain("First value for Ccc")
      .getText(CurrencyTotalPlaybackPage.secondNumberAnswer(2)).should.eventually.contain("30")
      .getText(CurrencyTotalPlaybackPage.secondNumberAnswerLabel(2)).should.eventually.contain("Second value for Ccc")
      .click(CurrencyTotalPlaybackPage.submit());

  });

  it("Given I've completed the Member Section, When I get to see the section summary, Then I should see the correct answers for each member", function () {
    return browser
      .getUrl().should.eventually.contain(MemberSummaryBlockPage.pageName)
      .then(checkMemberSummaryBlockPage)
      .click(MemberSummaryBlockPage.submit());

  });

  it("Given I've completed all Sections, When I get to see the final summary, Then I should see the correct answers for all questions", function () {
    return browser
      .getUrl().should.eventually.contain(SummaryPage.pageName)
      .then(checkHouseholdSummaryBlockPage)
      .then(checkMemberSummaryBlockPage);
  });

  it("Given I've Submitted the survey, When I get to see the answers after submission, Then I should see the correct answers for all questions", function () {
    return browser
      .click(SummaryPage.submit())
      .getUrl().should.eventually.contain(ThankYouPage.pageName)
      .click(ThankYouPage.viewSubmitted())
      .getUrl().should.eventually.contain('view-submission')
      .then(checkHouseholdSummaryBlockPage)
      .then(checkMemberSummaryBlockPage);
  });
});

function checkHouseholdSummaryBlockPage() {
  return browser

    .getText(HouseholdSummaryBlockPage.primaryName()).should.eventually.contain("Aaa")
    .getText(HouseholdSummaryBlockPage.repeatingName()).should.eventually.contain("Bbb")
    .getText(HouseholdSummaryBlockPage.repeatingName(1)).should.eventually.contain("Ccc");
}

function checkMemberSummaryBlockPage() {
  return browser

    .getText(MemberSummaryBlockPage.memberGroupTitle()).should.eventually.contain("Aaa")
    .getText(MemberSummaryBlockPage.firstNumberQuestion()).should.eventually.contain("Aaa")
    .getText(MemberSummaryBlockPage.firstNumberAnswer()).should.eventually.contain("1")
    .getText(MemberSummaryBlockPage.secondNumberQuestion()).should.eventually.contain("Aaa")
    .getText(MemberSummaryBlockPage.secondNumberAnswer()).should.eventually.contain("10")

    .getText(MemberSummaryBlockPage.memberGroupTitle(1)).should.eventually.contain("Bbb")
    .getText(MemberSummaryBlockPage.firstNumberQuestion(1)).should.eventually.contain("Bbb")
    .getText(MemberSummaryBlockPage.firstNumberAnswer(1)).should.eventually.contain("2")
    .getText(MemberSummaryBlockPage.secondNumberQuestion(1)).should.eventually.contain("Bbb")
    .getText(MemberSummaryBlockPage.secondNumberAnswer(1)).should.eventually.contain("20")

    .getText(MemberSummaryBlockPage.memberGroupTitle(2)).should.eventually.contain("Ccc")
    .getText(MemberSummaryBlockPage.firstNumberQuestion(2)).should.eventually.contain("Ccc")
    .getText(MemberSummaryBlockPage.firstNumberAnswer(2)).should.eventually.contain("3")
    .getText(MemberSummaryBlockPage.secondNumberQuestion(2)).should.eventually.contain("Ccc")
    .getText(MemberSummaryBlockPage.secondNumberAnswer(2)).should.eventually.contain("30");
}
