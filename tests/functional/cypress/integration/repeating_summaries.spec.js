import {openQuestionnaire} from '../helpers/helpers.js'

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
          .get(PrimaryNameBlockPage.primaryName()).type('Aaa')
      .get(PrimaryNameBlockPage.submit()).click()
      .get(RepeatingAnyoneElseBlockPage.yes()).click()
      .get(RepeatingAnyoneElseBlockPage.submit()).click()

      .get(RepeatingNameBlockPage.repeatingName()).type('Bbb')
      .get(RepeatingNameBlockPage.submit()).click()
      .get(RepeatingAnyoneElseBlockPage.yes()).click()
      .get(RepeatingAnyoneElseBlockPage.submit()).click()

      .get(RepeatingNameBlockPage.repeatingName()).type('Ccc')
      .get(RepeatingNameBlockPage.submit()).click()
      .get(RepeatingAnyoneElseBlockPage.no()).click()
      .get(RepeatingAnyoneElseBlockPage.submit()).click()

      .url().should('contain', HouseholdSummaryBlockPage.pageName)

      .then(checkHouseholdSummaryBlockPage)
      .get(HouseholdSummaryBlockPage.submit()).click();
  });

  it("Given I complete the First Member group, When I get to see the calculation summary, Then I should see the correct total for the first member", function () {

      .get(FirstNumberBlockPage.firstNumber()).type('1')
      .get(FirstNumberBlockPage.submit()).click()
      .get(SecondNumberBlockPage.secondNumber()).type('10')
      .get(SecondNumberBlockPage.submit()).click()

      .url().should('contain', CurrencyTotalPlaybackPage.pageName)

      .get(CurrencyTotalPlaybackPage.firstNumberAnswer()).stripText().should('contain', "1")
      .get(CurrencyTotalPlaybackPage.firstNumberAnswerLabel()).stripText().should('contain', "First value for Aaa")
      .get(CurrencyTotalPlaybackPage.secondNumberAnswer()).stripText().should('contain', "10")
      .get(CurrencyTotalPlaybackPage.secondNumberAnswerLabel()).stripText().should('contain', "Second value for Aaa")
      .get(CurrencyTotalPlaybackPage.submit()).click();
  });

  it("Given I complete the Second Member group, When I get to see the calculation summary, Then I should see the correct total for the second member", function () {

      .get(FirstNumberBlockPage.firstNumber()).type('2')
      .get(FirstNumberBlockPage.submit()).click()
      .get(SecondNumberBlockPage.secondNumber()).type('20')
      .get(SecondNumberBlockPage.submit()).click()

      .url().should('contain', CurrencyTotalPlaybackPage.pageName)

      .get(CurrencyTotalPlaybackPage.firstNumberAnswer(1)).stripText().should('contain', "2")
      .get(CurrencyTotalPlaybackPage.firstNumberAnswerLabel(1)).stripText().should('contain', "First value for Bbb")
      .get(CurrencyTotalPlaybackPage.secondNumberAnswer(1)).stripText().should('contain', "20")
      .get(CurrencyTotalPlaybackPage.secondNumberAnswerLabel(1)).stripText().should('contain', "Second value for Bbb")
      .get(CurrencyTotalPlaybackPage.submit()).click();
  });

  it("Given I complete the Third Member group, When I get to see the calculation summary, Then I should see the correct total for the third member", function () {

      .get(FirstNumberBlockPage.firstNumber()).type('3')
      .get(FirstNumberBlockPage.submit()).click()
      .get(SecondNumberBlockPage.secondNumber()).type('30')
      .get(SecondNumberBlockPage.submit()).click()

      .url().should('contain', CurrencyTotalPlaybackPage.pageName)

      .get(CurrencyTotalPlaybackPage.firstNumberAnswer(2)).stripText().should('contain', "3")
      .get(CurrencyTotalPlaybackPage.firstNumberAnswerLabel(2)).stripText().should('contain', "First value for Ccc")
      .get(CurrencyTotalPlaybackPage.secondNumberAnswer(2)).stripText().should('contain', "30")
      .get(CurrencyTotalPlaybackPage.secondNumberAnswerLabel(2)).stripText().should('contain', "Second value for Ccc")
      .get(CurrencyTotalPlaybackPage.submit()).click();

  });

  it("Given I've completed the Member Section, When I get to see the section summary, Then I should see the correct answers for each member", function () {
          .url().should('contain', MemberSummaryBlockPage.pageName)
      .then(checkMemberSummaryBlockPage)
      .get(MemberSummaryBlockPage.submit()).click();

  });

  it("Given I've completed all Sections, When I get to see the final summary, Then I should see the correct answers for all questions", function () {
          .url().should('contain', SummaryPage.pageName)
      .then(checkHouseholdSummaryBlockPage)
      .then(checkMemberSummaryBlockPage);
  });

  it("Given I've Submitted the survey, When I get to see the answers after submission, Then I should see the correct answers for all questions", function () {
          .get(SummaryPage.submit()).click()
      .url().should('contain', ThankYouPage.pageName)
      .get(ThankYouPage.viewSubmitted()).click()
      .url().should('contain', 'view-submission')
      .then(checkHouseholdSummaryBlockPage)
      .then(checkMemberSummaryBlockPage);
  });
});

function checkHouseholdSummaryBlockPage() {

    .get(HouseholdSummaryBlockPage.primaryName()).stripText().should('contain', "Aaa")
    .get(HouseholdSummaryBlockPage.repeatingName()).stripText().should('contain', "Bbb")
    .get(HouseholdSummaryBlockPage.repeatingName(1)).stripText().should('contain', "Ccc");
}

function checkMemberSummaryBlockPage() {

    .get(MemberSummaryBlockPage.memberGroupTitle()).stripText().should('contain', "Aaa")
    .get(MemberSummaryBlockPage.firstNumberQuestion()).stripText().should('contain', "Aaa")
    .get(MemberSummaryBlockPage.firstNumberAnswer()).stripText().should('contain', "1")
    .get(MemberSummaryBlockPage.secondNumberQuestion()).stripText().should('contain', "Aaa")
    .get(MemberSummaryBlockPage.secondNumberAnswer()).stripText().should('contain', "10")

    .get(MemberSummaryBlockPage.memberGroupTitle(1)).stripText().should('contain', "Bbb")
    .get(MemberSummaryBlockPage.firstNumberQuestion(1)).stripText().should('contain', "Bbb")
    .get(MemberSummaryBlockPage.firstNumberAnswer(1)).stripText().should('contain', "2")
    .get(MemberSummaryBlockPage.secondNumberQuestion(1)).stripText().should('contain', "Bbb")
    .get(MemberSummaryBlockPage.secondNumberAnswer(1)).stripText().should('contain', "20")

    .get(MemberSummaryBlockPage.memberGroupTitle(2)).stripText().should('contain', "Ccc")
    .get(MemberSummaryBlockPage.firstNumberQuestion(2)).stripText().should('contain', "Ccc")
    .get(MemberSummaryBlockPage.firstNumberAnswer(2)).stripText().should('contain', "3")
    .get(MemberSummaryBlockPage.secondNumberQuestion(2)).stripText().should('contain', "Ccc")
    .get(MemberSummaryBlockPage.secondNumberAnswer(2)).stripText().should('contain', "30");
}
