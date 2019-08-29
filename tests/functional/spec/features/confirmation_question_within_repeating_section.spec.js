const helpers = require('../../helpers');

const DoesAnyoneLiveHerePage = require('../../generated_pages/confirmation_question_within_repeating_section/list-collector.page');
const AddPersonPage = require('../../generated_pages/confirmation_question_within_repeating_section/list-collector-add.page');
const CarerPage = require('../../generated_pages/confirmation_question_within_repeating_section/carer-block.page');
const DateOfBirthPage = require('../../generated_pages/confirmation_question_within_repeating_section/dob-block.page');
const ConfirmDateOfBirthPage = require('../../generated_pages/confirmation_question_within_repeating_section/confirm-dob-block.page');
const SectionSummaryPage = require('../../generated_pages/confirmation_question_within_repeating_section/section-summary.page');

describe('Feature: Confirmation Question Within A Repeating Section', function () {

  describe('Given I am in a repeating section', function () {

    beforeEach('Add a person', function () {
      return helpers.openQuestionnaire('test_confirmation_question_within_repeating_section.json').then(() => {
        return browser
          .click(DoesAnyoneLiveHerePage.yes())
          .click(DoesAnyoneLiveHerePage.submit())
          .setValue(AddPersonPage.firstName(), 'John')
          .setValue(AddPersonPage.lastName(), 'Doe')
          .click(AddPersonPage.submit())
          .click(DoesAnyoneLiveHerePage.no())
          .click(DoesAnyoneLiveHerePage.submit())
          .getUrl().should.eventually.contain(DateOfBirthPage.url().split('/').slice(-1)[0]);
      });
    });

    describe('Given a confirmation question', function () {

      it('When I answer \'No\' to the confirmation question, Then I should be routed back to the source question', function () {
        return browser
          // Answer question preceding confirmation question
          .setValue(DateOfBirthPage.day(), '01')
          .setValue(DateOfBirthPage.month(), '01')
          .setValue(DateOfBirthPage.year(), '2007')
          .click(DateOfBirthPage.submit())

          // Answer 'No' to confirmation question
          .click(ConfirmDateOfBirthPage.no())
          .click(ConfirmDateOfBirthPage.submit())
          .getUrl().should.eventually.contain(DateOfBirthPage.pageName);
      });

    });

    describe('Given I have answered a confirmation question', function () {

      it('When I view the summary, Then the confirmation question should not be displayed', function () {
        return browser
          .setValue(DateOfBirthPage.day(), '01')
          .setValue(DateOfBirthPage.month(), '01')
          .setValue(DateOfBirthPage.year(), '2007')
          .click(DateOfBirthPage.submit())

          .click(ConfirmDateOfBirthPage.yes())
          .click(ConfirmDateOfBirthPage.submit())

          .getUrl().should.eventually.contain(SectionSummaryPage.pageName)
          .isExisting(SectionSummaryPage.confirmDateOfBirth()).should.eventually.be.false;
      });

    });

    describe('Given a confirmation question with a skip condition', function () {

      it('When I submit an a date of birth where the age is at least \'16\', Then I should be skipped past the confirmation question and directed to the carer question', function () {
        return browser
          .setValue(DateOfBirthPage.day(), '01')
          .setValue(DateOfBirthPage.month(), '01')
          .setValue(DateOfBirthPage.year(), '2000')
          .click(DateOfBirthPage.submit())

          .getUrl().should.eventually.contain(CarerPage.pageName)
          .getText(CarerPage.questionText()).should.eventually.contain('Does John Doe look');
      });

    });

  });

});
