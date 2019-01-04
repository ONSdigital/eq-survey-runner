import {openQuestionnaire} from '../../../helpers/helpers.js';

const NumberOfEmployeesTotalBlockPage = require('../../../../generated_pages/confirmation_question/number-of-employees-total-block.page.js');
const ConfirmZeroEmployeesBlockPage = require('../../../../generated_pages/confirmation_question/confirm-zero-employees-block.page.js');
const SummaryPage = require('../../../../generated_pages/confirmation_question/summary.page.js');

describe('Feature: Routing incompletes block if routing backwards', function() {

  describe('Given I have a confirmation Question', function() {

    before('Get to summary', function () {
      openQuestionnaire('test_confirmation_question.json')
        .get(NumberOfEmployeesTotalBlockPage.numberOfEmployeesTotal()).type(0)
        .get(NumberOfEmployeesTotalBlockPage.submit()).click()
        .get(ConfirmZeroEmployeesBlockPage.yes()).click()
        .get(ConfirmZeroEmployeesBlockPage.submit()).click()
        .url().should('contain', SummaryPage.pageName);
    });

    it('When I use browser back button and change confirmation to no then Summary should not be available', function () {
      cy
        .go('back')
        .navigationLink('Summary').should('be.visible')
        .get(ConfirmZeroEmployeesBlockPage.no()).click()
        .get(ConfirmZeroEmployeesBlockPage.submit()).click()
        .navigationLink('Summary').should('not.be.visible');
    });

  });
});
