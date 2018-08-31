const helpers = require('../helpers');

const PrimaryNamePage = require('../pages/surveys/routing_repeat_until/primary-name-block.page.js');
const RepeatingNamePage = require('../pages/surveys/routing_repeat_until/repeating-name-block.page.js');
const RepeatingAnyoneElsePage = require('../pages/surveys/routing_repeat_until/repeating-anyone-else-block.page.js');
const SexPage = require('../pages/surveys/routing_repeat_until/sex-block.page.js');
const SummaryPage = require('../pages/surveys/routing_repeat_until/summary.page.js');

describe('Routing Repeat Until', function() {

  it('Given the test_routing_repeat_until survey is selected when one additional member is entered we are asked about the the sex of them and the primary member', function() {

    return helpers.openQuestionnaire('test_routing_repeat_until.json').then(() => {

      return browser
        .setValue(PrimaryNamePage.answer(), 'Bob')
        .click(PrimaryNamePage.submit())

        .click(RepeatingAnyoneElsePage.yes())
        .click(RepeatingAnyoneElsePage.submit())

        .setValue(RepeatingNamePage.answer(), 'Alice')
        .click(RepeatingNamePage.submit())

        .click(RepeatingAnyoneElsePage.no())
        .click(RepeatingAnyoneElsePage.submit())

        .getText(SexPage.questionText()).should.eventually.contain('Bob')
        .click(SexPage.male())
        .click(SexPage.submit())

        .getText(SexPage.questionText()).should.eventually.contain('Alice')
        .click(SexPage.female())
        .click(SexPage.submit())

        .getUrl().should.eventually.contain(SummaryPage.pageName)
        .click(SummaryPage.submit());
    });
  });

  it('Given the test_routing_repeat_until survey is selected when multiple additional members are entered we are asked about the sex of all of them and the primary member', function() {

    return helpers.openQuestionnaire('test_routing_repeat_until.json').then(() => {

      return browser
        .setValue(PrimaryNamePage.answer(), 'Bob')
        .click(PrimaryNamePage.submit())

        .click(RepeatingAnyoneElsePage.yes())
        .click(RepeatingAnyoneElsePage.submit())

        .setValue(RepeatingNamePage.answer(), 'Alice')
        .click(RepeatingNamePage.submit())

        .click(RepeatingAnyoneElsePage.yes())
        .click(RepeatingAnyoneElsePage.submit())

        .setValue(RepeatingNamePage.answer(), 'John')
        .click(RepeatingNamePage.submit())

        .click(RepeatingAnyoneElsePage.no())
        .click(RepeatingAnyoneElsePage.submit())

        .getText(SexPage.questionText()).should.eventually.contain('Bob')
        .click(SexPage.male())
        .click(SexPage.submit())

        .getText(SexPage.questionText()).should.eventually.contain('Alice')
        .click(SexPage.female())
        .click(SexPage.submit())

        .getText(SexPage.questionText()).should.eventually.contain('John')
        .click(SexPage.male())
        .click(SexPage.submit())

        .getUrl().should.eventually.contain(SummaryPage.pageName)
        .click(SummaryPage.submit());
    });
  });

  it('Given the test_routing_repeat_until survey is selected when no additional members are entered we are asked about the sex of the primary member', function() {

    return helpers.openQuestionnaire('test_routing_repeat_until.json').then(() => {

      return browser
        .setValue(PrimaryNamePage.answer(), 'Bob')
        .click(PrimaryNamePage.submit())

        .click(RepeatingAnyoneElsePage.no())
        .click(RepeatingAnyoneElsePage.submit())

        .getText(SexPage.questionText()).should.eventually.contain('Bob')
        .click(SexPage.male())
        .click(SexPage.submit())

        .getUrl().should.eventually.contain(SummaryPage.pageName)
        .click(SummaryPage.submit());
    });
  });

});

