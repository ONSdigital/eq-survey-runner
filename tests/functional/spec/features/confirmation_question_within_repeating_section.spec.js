const helpers = require('../../helpers');

const DoesAnyoneLiveHerePage = require('../../generated_pages/confirmation_question_within_repeating_section/list-collector.page');
const AddPersonPage = require('../../generated_pages/confirmation_question_within_repeating_section/list-collector-add.page');
const CarerPage = require('../../generated_pages/confirmation_question_within_repeating_section/carer-block.page');
const DateOfBirthPage = require('../../generated_pages/confirmation_question_within_repeating_section/dob-block.page');
const ConfirmDateOfBirthPage = require('../../generated_pages/confirmation_question_within_repeating_section/confirm-dob-block.page');
const SectionSummaryPage = require('../../generated_pages/confirmation_question_within_repeating_section/section-summary.page');

describe('Feature: Confirmation Question Within A Repeating Section', function () {
  let browser;

  describe('Given I am in a repeating section', function () {

    beforeEach('Add a person', function () {
      browser = helpers.openQuestionnaire('test_confirmation_question_within_repeating_section.json').then(openBrowser => browser = openBrowser);
      $(DoesAnyoneLiveHerePage.yes()).click();
      $(DoesAnyoneLiveHerePage.submit()).click();
      $(AddPersonPage.firstName()).setValue('John');
      $(AddPersonPage.lastName()).setValue('Doe');
      $(AddPersonPage.submit()).click();
      $(DoesAnyoneLiveHerePage.no()).click();
      $(DoesAnyoneLiveHerePage.submit()).click();
      expect(browser.getUrl()).to.contain(DateOfBirthPage.url().split('/').slice(-1)[0]);
    });

    describe('Given a confirmation question', function () {

      it('When I answer \'No\' to the confirmation question, Then I should be routed back to the source question', function () {
          // Answer question preceding confirmation question
          $(DateOfBirthPage.day()).setValue('01');
          $(DateOfBirthPage.month()).setValue('01');
          $(DateOfBirthPage.year()).setValue('2007');
          $(DateOfBirthPage.submit()).click();

          // Answer 'No' to confirmation question
          $(ConfirmDateOfBirthPage.no()).click();
          $(ConfirmDateOfBirthPage.submit()).click();
          expect(browser.getUrl()).to.contain(DateOfBirthPage.pageName);
      });

    });

    describe('Given I have answered a confirmation question', function () {

      it('When I view the summary, Then the confirmation question should not be displayed', function () {
          $(DateOfBirthPage.day()).setValue('01');
          $(DateOfBirthPage.month()).setValue('01');
          $(DateOfBirthPage.year()).setValue('2007');
          $(DateOfBirthPage.submit()).click();

          $(ConfirmDateOfBirthPage.yes()).click();
          $(ConfirmDateOfBirthPage.submit()).click();

          expect(browser.getUrl()).to.contain(SectionSummaryPage.pageName);
          expect($(SectionSummaryPage.confirmDateOfBirth()).isExisting()).to.be.false;
      });

    });

    describe('Given a confirmation question with a skip condition', function () {

      it('When I submit an a date of birth where the age is at least \'16\', Then I should be skipped past the confirmation question and directed to the carer question', function () {
          $(DateOfBirthPage.day()).setValue('01');
          $(DateOfBirthPage.month()).setValue('01');
          $(DateOfBirthPage.year()).setValue('2000');
          $(DateOfBirthPage.submit()).click();

          expect(browser.getUrl()).to.contain(CarerPage.pageName);
          expect($(CarerPage.questionText()).getText()).to.contain('Does John Doe look');
      });

    });

  });

});
