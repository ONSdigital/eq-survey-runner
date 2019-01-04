import {openQuestionnaire} from '../helpers/helpers.js';

const PrimaryNameBlockPage = require('../../generated_pages/repeat_until_summaries/primary-name-block.page.js');
const RepeatingAnyoneElseBlockPage = require('../../generated_pages/repeat_until_summaries/repeating-anyone-else-block.page.js');
const RepeatingNameBlockPage = require('../../generated_pages/repeat_until_summaries/repeating-name-block.page.js');
const HouseholdSummaryBlockPage = require('../../generated_pages/repeat_until_summaries/household-summary-block.page.js');
const FirstNumberBlockPage = require('../../generated_pages/repeat_until_summaries/first-number-block.page.js');
const SecondNumberBlockPage = require('../../generated_pages/repeat_until_summaries/second-number-block.page.js');
const CurrencyTotalPlaybackPage = require('../../generated_pages/repeat_until_summaries/currency-total-playback.page.js');
const MemberSummaryBlockPage = require('../../generated_pages/repeat_until_summaries/member-summary-block.page.js');
const SummaryPage = require('../../generated_pages/repeat_until_summaries/summary.page.js');
const ThankYouPage = require('../../base_pages/thank-you.page.js');

describe('Repeat Until Summaries', function() {

  beforeEach(function () {
    openQuestionnaire('test_repeat_until_summaries.json');
  });

  it('Given I complete the Household Section, When I get to see the section summary, Then I should see all answers in that section', function() {
    completeHouseholdSection();
    cy
      .then(checkHouseholdSummaryBlockPage)
      .get(HouseholdSummaryBlockPage.submit()).click();
  });

  it('Given I complete the First Member group, When I get to see the calculation summary, Then I should see the correct total for the first member', function () {
    completeHouseholdSection();
    cy.get(HouseholdSummaryBlockPage.submit()).click();
    completeMember(['Aaa']);
  });

  it('Given I complete the Second Member group, When I get to see the calculation summary, Then I should see the correct total for the second member', function () {
    completeHouseholdSection();
    cy.get(HouseholdSummaryBlockPage.submit()).click();
    completeMember(['Aaa', 'Bbb']);
  });

  it('Given I complete the Third Member group, When I get to see the calculation summary, Then I should see the correct total for the third member', function () {
    completeHouseholdSection();
    cy.get(HouseholdSummaryBlockPage.submit()).click();
    completeMember(['Aaa', 'Bbb', 'Ccc']);
  });

  it('Given I\'ve completed the Member Section, When I get to see the section summary, Then I should see the correct answers for each member', function () {
    completeHouseholdSection();
    cy.get(HouseholdSummaryBlockPage.submit()).click();
    completeMember(['Aaa', 'Bbb', 'Ccc']);
    cy
      .url().should('contain', MemberSummaryBlockPage.pageName)
      .then(checkMemberSummaryBlockPage)
      .get(MemberSummaryBlockPage.submit()).click();

  });

  it('Given I\'ve completed all Sections, When I get to see the final summary, Then I should see the correct answers for all questions', function () {
    completeHouseholdSection();
    cy.get(HouseholdSummaryBlockPage.submit()).click();
    completeMember(['Aaa', 'Bbb', 'Ccc']);

    cy
      .get(MemberSummaryBlockPage.submit()).click()
      .url().should('contain', SummaryPage.pageName)
      .then(checkHouseholdSummaryBlockPage)
      .then(checkMemberSummaryBlockPage);
  });

  it('Given I\'ve Submitted the survey, When I get to see the answers after submission, Then I should see the correct answers for all questions', function () {
    completeHouseholdSection();
    cy.get(HouseholdSummaryBlockPage.submit()).click();
    completeMember(['Aaa', 'Bbb', 'Ccc']);
    cy
      .get(MemberSummaryBlockPage.submit()).click()
      .get(SummaryPage.submit()).click()
      .url().should('contain', ThankYouPage.pageName)
      .get(ThankYouPage.viewSubmitted()).click()
      .url().should('contain', 'view-submission')
      .then(checkHouseholdSummaryBlockPage)
      .then(checkMemberSummaryBlockPage);
  });
});

function checkHouseholdSummaryBlockPage() {
  cy
    .get(HouseholdSummaryBlockPage.primaryName()).stripText().should('contain', 'Aaa')
    .get(HouseholdSummaryBlockPage.repeatingName()).stripText().should('contain', 'Bbb')
    .get(HouseholdSummaryBlockPage.repeatingName(1)).stripText().should('contain', 'Ccc');
}

function checkMemberSummaryBlockPage() {
  cy
    .get(MemberSummaryBlockPage.memberGroupTitle()).stripText().should('contain', 'Aaa')
    .get(MemberSummaryBlockPage.firstNumberQuestion()).stripText().should('contain', 'Aaa')
    .get(MemberSummaryBlockPage.firstNumberAnswer()).stripText().should('contain', '0')
    .get(MemberSummaryBlockPage.secondNumberQuestion()).stripText().should('contain', 'Aaa')
    .get(MemberSummaryBlockPage.secondNumberAnswer()).stripText().should('contain', '00')

    .get(MemberSummaryBlockPage.memberGroupTitle(1)).stripText().should('contain', 'Bbb')
    .get(MemberSummaryBlockPage.firstNumberQuestion(1)).stripText().should('contain', 'Bbb')
    .get(MemberSummaryBlockPage.firstNumberAnswer(1)).stripText().should('contain', '1')
    .get(MemberSummaryBlockPage.secondNumberQuestion(1)).stripText().should('contain', 'Bbb')
    .get(MemberSummaryBlockPage.secondNumberAnswer(1)).stripText().should('contain', '11')

    .get(MemberSummaryBlockPage.memberGroupTitle(2)).stripText().should('contain', 'Ccc')
    .get(MemberSummaryBlockPage.firstNumberQuestion(2)).stripText().should('contain', 'Ccc')
    .get(MemberSummaryBlockPage.firstNumberAnswer(2)).stripText().should('contain', '2')
    .get(MemberSummaryBlockPage.secondNumberQuestion(2)).stripText().should('contain', 'Ccc')
    .get(MemberSummaryBlockPage.secondNumberAnswer(2)).stripText().should('contain', '22');
}

function completeHouseholdSection() {
  cy
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

    .url().should('contain', HouseholdSummaryBlockPage.pageName);
}

function completeMember(memberNames) {
  memberNames.forEach((name,i) => {
    const firstNumber = String(i);
    const secondNumber = String(i) + String(i);
    cy
      .get(FirstNumberBlockPage.firstNumber()).type(firstNumber)
      .get(FirstNumberBlockPage.submit()).click()
      .get(SecondNumberBlockPage.secondNumber()).type(secondNumber)
      .get(SecondNumberBlockPage.submit()).click()

      .url().should('contain', CurrencyTotalPlaybackPage.pageName)

      .get(CurrencyTotalPlaybackPage.firstNumberAnswer(i)).stripText().should('contain', firstNumber)
      .get(CurrencyTotalPlaybackPage.firstNumberAnswerLabel(i)).stripText().should('contain', 'First value for ' + name)
      .get(CurrencyTotalPlaybackPage.secondNumberAnswer(i)).stripText().should('contain', secondNumber)
      .get(CurrencyTotalPlaybackPage.secondNumberAnswerLabel(i)).stripText().should('contain', 'Second value for ' + name)
      .get(CurrencyTotalPlaybackPage.submit()).click();
  });
}
