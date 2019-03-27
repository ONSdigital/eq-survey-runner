const helpers = require('../helpers');
const ageBlock = require('../generated_pages/variants_question/age-block.page.js');
const ageConfirmationBlock = require('../generated_pages/variants_question/age-confirmation-block.page.js');
const basicVariantsSummary = require('../generated_pages/variants_question/basic-variants-summary.page.js');
const currencyBlock = require('../generated_pages/variants_question/currency-block.page.js');
const currencySectionSummary = require('../generated_pages/variants_question/currency-section-summary.page.js');
const firstNumberBlock = require('../generated_pages/variants_question/first-number-block.page.js');
const nameBlock = require('../generated_pages/variants_question/name-block.page.js');
const proxyBlock = require('../generated_pages/variants_question/proxy-block.page.js');
const secondNumberBlock = require('../generated_pages/variants_question/second-number-block.page.js');

describe('QuestionVariants', function() {

  beforeEach(function() {
    return helpers.openQuestionnaire('test_variants_question.json');
  });

  it('Given I am completing the survey, then the correct questions are shown based on my previous answers', function () {
    return browser
      .setValue(nameBlock.firstName(), 'Guido')
      .setValue(nameBlock.lastName(), 'van Rossum')
      .click(nameBlock.submit())

      .getText(proxyBlock.questionText()).should.eventually.contain('Are you Guido van Rossum?')

      .click(proxyBlock.proxy())
      .click(proxyBlock.submit())

      .getText(ageBlock.questionText()).should.eventually.contain('What age is Guido van Rossum')

      .setValue(ageBlock.age(), 63)
      .click(ageBlock.submit())

      .getText(ageConfirmationBlock.questionText()).should.eventually.contain('Guido van Rossum is over 16?')

      .click(ageConfirmationBlock.ageConfirmYes())
      .click(ageConfirmationBlock.submit())

      .getText(basicVariantsSummary.ageQuestion()).should.eventually.contain('What age is Guido van Rossum')
      .getText(basicVariantsSummary.ageAnswer()).should.eventually.contain('63')

      .click(basicVariantsSummary.submit())

      .click(currencyBlock.gbp())
      .click(currencyBlock.submit())

      .getText(firstNumberBlock.firstNumberLabel()).should.eventually.contain('First answer in GBP')

      .setValue(firstNumberBlock.firstNumber(), 123)
      .click(firstNumberBlock.submit())

      .setValue(secondNumberBlock.secondNumber(), 321)
      .click(secondNumberBlock.submit())

      .getText(currencySectionSummary.currencyAnswer()).should.eventually.contain('Sterling')
      .getText(currencySectionSummary.firstNumberAnswer()).should.eventually.contain('£')

      .click(currencySectionSummary.currencyAnswerEdit())
      .click(currencyBlock.usd())
      .click(currencyBlock.submit())

      .getText(currencySectionSummary.firstNumberAnswer()).should.eventually.contain('$');

    });
});


