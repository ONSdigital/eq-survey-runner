const helpers = require('../../../../helpers');

describe('Feature: Sum of grouped answers validation against total', function() {
  describe('Equal to', function () {
    var TotalAnswerPage = require('../../../../pages/features/grouped_validation/sum/equal-to/total-block.page');
    var BreakdownAnswerPage = require('../../../../pages/features/grouped_validation/sum/equal-to/breakdown-block.page');
    var SummaryPage = require('../../../../pages/features/grouped_validation/sum/equal-to/summary.page');

    beforeEach(function() {
        return helpers.openQuestionnaire('test_sum_equal_validation_against_total.json');
    });

    describe('Given I start a grouped answer validation survey and enter 12 into the total', function() {
      it('When I continue and enter 3 in each breakdown field, Then I should be able to get to the summary', function() {
        return browser
         .setValue(TotalAnswerPage.answer(), '12')
         .click(TotalAnswerPage.submit())
         .setValue(BreakdownAnswerPage.breakdown1(), '3')
         .setValue(BreakdownAnswerPage.breakdown2(), '3')
         .setValue(BreakdownAnswerPage.breakdown3(), '3')
         .setValue(BreakdownAnswerPage.breakdown4(), '3')
         .click(BreakdownAnswerPage.submit())
         .getUrl().should.eventually.contain(SummaryPage.pageName);
        });
     });

    describe('Given I start a grouped answer validation survey and enter 5 into the total', function() {
      it('When I continue and enter 5 into breakdown 1 and leave the others empty, Then I should be able to get to the summary', function() {
        return browser
         .setValue(TotalAnswerPage.answer(), '5')
         .click(TotalAnswerPage.submit())
         .setValue(BreakdownAnswerPage.breakdown1(), '5')
         .setValue(BreakdownAnswerPage.breakdown2(), '')
         .setValue(BreakdownAnswerPage.breakdown3(), '')
         .setValue(BreakdownAnswerPage.breakdown4(), '')
         .click(BreakdownAnswerPage.submit())
         .getUrl().should.eventually.contain(SummaryPage.pageName);
        });
     });

     describe('Given I start a grouped answer validation survey and enter 5 into the total', function() {
      it('When I continue and enter 3 in each breakdown field, Then I should see a validation error', function() {
        return browser
         .setValue(TotalAnswerPage.answer(), '5')
         .click(TotalAnswerPage.submit())
         .setValue(BreakdownAnswerPage.breakdown1(), '3')
         .setValue(BreakdownAnswerPage.breakdown2(), '3')
         .setValue(BreakdownAnswerPage.breakdown3(), '3')
         .setValue(BreakdownAnswerPage.breakdown4(), '3')
         .click(BreakdownAnswerPage.submit())
         .getText(BreakdownAnswerPage.errorNumber(1)).should.eventually.contain('Enter answers that add up to 5');
       });
     });
  });

  describe('Less than', function () {
    var TotalAnswerPage = require('../../../../pages/features/grouped_validation/sum/less-than/total-block.page');
    var BreakdownAnswerPage = require('../../../../pages/features/grouped_validation/sum/less-than/breakdown-block.page');
    var SummaryPage = require('../../../../pages/features/grouped_validation/sum/less-than/summary.page');

    beforeEach(function() {
        return helpers.openQuestionnaire('test_sum_less_validation_against_total.json');
    });

    describe('Given I start a grouped answer validation survey and enter 12 into the total', function() {
      it('When I continue and enter 2 in each breakdown field, Then I should be able to get to the summary', function() {
        return browser
         .setValue(TotalAnswerPage.answer(), '12')
         .click(TotalAnswerPage.submit())
         .setValue(BreakdownAnswerPage.breakdown1(), '2')
         .setValue(BreakdownAnswerPage.breakdown2(), '2')
         .setValue(BreakdownAnswerPage.breakdown3(), '2')
         .setValue(BreakdownAnswerPage.breakdown4(), '2')
         .click(BreakdownAnswerPage.submit())
         .getUrl().should.eventually.contain(SummaryPage.pageName);
        });
     });

    describe('Given I start a grouped answer validation survey and enter 5 into the total', function() {
      it('When I continue and enter 4 into breakdown 1 and leave the others empty, Then I should be able to get to the summary', function() {
        return browser
         .setValue(TotalAnswerPage.answer(), '5')
         .click(TotalAnswerPage.submit())
         .setValue(BreakdownAnswerPage.breakdown1(), '4')
         .setValue(BreakdownAnswerPage.breakdown2(), '')
         .setValue(BreakdownAnswerPage.breakdown3(), '')
         .setValue(BreakdownAnswerPage.breakdown4(), '')
         .click(BreakdownAnswerPage.submit())
         .getUrl().should.eventually.contain(SummaryPage.pageName);
        });
     });

     describe('Given I start a grouped answer validation survey and enter 12 into the total', function() {
      it('When I continue and enter 3 in each breakdown field, Then I should see a validation error', function() {
        return browser
         .setValue(TotalAnswerPage.answer(), '12')
         .click(TotalAnswerPage.submit())
         .setValue(BreakdownAnswerPage.breakdown1(), '3')
         .setValue(BreakdownAnswerPage.breakdown2(), '3')
         .setValue(BreakdownAnswerPage.breakdown3(), '3')
         .setValue(BreakdownAnswerPage.breakdown4(), '3')
         .click(BreakdownAnswerPage.submit())
         .getText(BreakdownAnswerPage.errorNumber(1)).should.eventually.contain('Enter answers that add up to less than £12.00');
       });
     });

     describe('Given I start a grouped answer validation survey and enter 5 into the total', function() {
      it('When I continue and enter 3 in each breakdown field, Then I should see a validation error', function() {
        return browser
         .setValue(TotalAnswerPage.answer(), '5')
         .click(TotalAnswerPage.submit())
         .setValue(BreakdownAnswerPage.breakdown1(), '3')
         .setValue(BreakdownAnswerPage.breakdown2(), '3')
         .setValue(BreakdownAnswerPage.breakdown3(), '3')
         .setValue(BreakdownAnswerPage.breakdown4(), '3')
         .click(BreakdownAnswerPage.submit())
         .getText(BreakdownAnswerPage.errorNumber(1)).should.eventually.contain('Enter answers that add up to less than £5.00');
       });
     });
   });

  describe('Less than or equal to', function () {
    var TotalAnswerPage = require('../../../../pages/features/grouped_validation/sum/less-than-equal-to/total-block.page');
    var BreakdownAnswerPage = require('../../../../pages/features/grouped_validation/sum/less-than-equal-to/breakdown-block.page');
    var SummaryPage = require('../../../../pages/features/grouped_validation/sum/less-than-equal-to/summary.page');

    beforeEach(function() {
        return helpers.openQuestionnaire('test_sum_equal_or_less_validation_against_total.json');
    });

    describe('Given I start a grouped answer validation survey and enter 12 into the total', function() {
      it('When I continue and enter 3 in each breakdown field, Then I should be able to get to the summary', function() {
        return browser
         .setValue(TotalAnswerPage.answer(), '12')
         .click(TotalAnswerPage.submit())
         .setValue(BreakdownAnswerPage.breakdown1(), '3')
         .setValue(BreakdownAnswerPage.breakdown2(), '3')
         .setValue(BreakdownAnswerPage.breakdown3(), '3')
         .setValue(BreakdownAnswerPage.breakdown4(), '3')
         .click(BreakdownAnswerPage.submit())
         .getUrl().should.eventually.contain(SummaryPage.pageName);
        });
     });

    describe('Given I start a grouped answer validation survey and enter 5 into the total', function() {
      it('When I continue and enter 5 into breakdown 1 and leave the others empty, Then I should be able to get to the summary', function() {
        return browser
         .setValue(TotalAnswerPage.answer(), '5')
         .click(TotalAnswerPage.submit())
         .setValue(BreakdownAnswerPage.breakdown1(), '5')
         .setValue(BreakdownAnswerPage.breakdown2(), '')
         .setValue(BreakdownAnswerPage.breakdown3(), '')
         .setValue(BreakdownAnswerPage.breakdown4(), '')
         .click(BreakdownAnswerPage.submit())
         .getUrl().should.eventually.contain(SummaryPage.pageName);
        });
     });

    describe('Given I start a grouped answer validation survey and enter 12 into the total', function() {
      it('When I continue and enter 2 in each breakdown field, Then I should be able to get to the summary', function() {
        return browser
         .setValue(TotalAnswerPage.answer(), '12')
         .click(TotalAnswerPage.submit())
         .setValue(BreakdownAnswerPage.breakdown1(), '2')
         .setValue(BreakdownAnswerPage.breakdown2(), '2')
         .setValue(BreakdownAnswerPage.breakdown3(), '2')
         .setValue(BreakdownAnswerPage.breakdown4(), '2')
         .click(BreakdownAnswerPage.submit())
         .getUrl().should.eventually.contain(SummaryPage.pageName);
        });
     });

    describe('Given I start a grouped answer validation survey and enter 5 into the total', function() {
      it('When I continue and enter 4 into breakdown 1 and leave the others empty, Then I should be able to get to the summary', function() {
        return browser
         .setValue(TotalAnswerPage.answer(), '5')
         .click(TotalAnswerPage.submit())
         .setValue(BreakdownAnswerPage.breakdown1(), '4')
         .setValue(BreakdownAnswerPage.breakdown2(), '')
         .setValue(BreakdownAnswerPage.breakdown3(), '')
         .setValue(BreakdownAnswerPage.breakdown4(), '')
         .click(BreakdownAnswerPage.submit())
         .getUrl().should.eventually.contain(SummaryPage.pageName);
        });
     });

    describe('Given I start a grouped answer validation survey and enter 5 into the total', function() {
      it('When I continue and enter 3 in each breakdown field, Then I should see a validation error', function() {
        return browser
         .setValue(TotalAnswerPage.answer(), '5')
         .click(TotalAnswerPage.submit())
         .setValue(BreakdownAnswerPage.breakdown1(), '3')
         .setValue(BreakdownAnswerPage.breakdown2(), '3')
         .setValue(BreakdownAnswerPage.breakdown3(), '3')
         .setValue(BreakdownAnswerPage.breakdown4(), '3')
         .click(BreakdownAnswerPage.submit())
         .getText(BreakdownAnswerPage.errorNumber(1)).should.eventually.contain('Enter answers that add up to or are less than 5');
       });
    });
  });

  describe('Multi Rule Equals', function () {
    var TotalAnswerPage = require('../../../../pages/features/grouped_validation/sum/equal-to/total-block.page');
    var BreakdownAnswerPage = require('../../../../pages/features/grouped_validation/sum/equal-to/breakdown-block.page');
    var SummaryPage = require('../../../../pages/features/grouped_validation/sum/equal-to/summary.page');

    beforeEach(function() {
        return helpers.openQuestionnaire('test_sum_multi_validation_against_total.json');
    });

    describe('Given I start a grouped answer with multi rule validation survey and enter 10 into the total', function() {
      it('When I continue and enter nothing, all zeros or 10 at breakdown level, Then I should be able to get to the summary', function() {
        return browser
         .setValue(TotalAnswerPage.answer(), '10')
         .click(TotalAnswerPage.submit())
         .click(BreakdownAnswerPage.submit())
         .getUrl().should.eventually.contain(SummaryPage.pageName)

         .click(SummaryPage.previous())
         .setValue(BreakdownAnswerPage.breakdown1(), '0')
         .setValue(BreakdownAnswerPage.breakdown2(), '0')
         .setValue(BreakdownAnswerPage.breakdown3(), '0')
         .setValue(BreakdownAnswerPage.breakdown4(), '0')
         .click(BreakdownAnswerPage.submit())
         .getUrl().should.eventually.contain(SummaryPage.pageName)

         .click(SummaryPage.previous())
         .setValue(BreakdownAnswerPage.breakdown1(), '1')
         .setValue(BreakdownAnswerPage.breakdown2(), '2')
         .setValue(BreakdownAnswerPage.breakdown3(), '3')
         .setValue(BreakdownAnswerPage.breakdown4(), '4')
         .click(BreakdownAnswerPage.submit())
         .getUrl().should.eventually.contain(SummaryPage.pageName);
        });
     });

    describe('Given I start a grouped answer with multi rule validation survey and enter 10 into the total', function() {
      it('When I continue and enter less between 1 - 9 or greater than 10, Then it should error', function() {
        return browser
         .setValue(TotalAnswerPage.answer(), '10')
         .click(TotalAnswerPage.submit())
         .setValue(BreakdownAnswerPage.breakdown1(), '1')
         .click(BreakdownAnswerPage.submit())

         .getText(BreakdownAnswerPage.errorNumber(1)).should.eventually.contain('Enter answers that add up to 10')

         .setValue(BreakdownAnswerPage.breakdown2(), '2')
         .setValue(BreakdownAnswerPage.breakdown3(), '3')
         .setValue(BreakdownAnswerPage.breakdown4(), '5')
         .click(BreakdownAnswerPage.submit())
         .getText(BreakdownAnswerPage.errorNumber(1)).should.eventually.contain('Enter answers that add up to 10');
        });
     });
  });
});
