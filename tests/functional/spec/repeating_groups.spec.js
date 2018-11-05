const helpers = require('../helpers');

const NoOfRepeatsPage = require('../generated_pages/repeating_and_conditional_routing/no-of-repeats.page.js');
const RepeatedBlockPage = require('../generated_pages/repeating_and_conditional_routing/repeated-block.page.js');
const AgeBlockPage = require('../generated_pages/repeating_and_conditional_routing/age-block.page.js');
const ShoeSizeBlockPage = require('../generated_pages/repeating_and_conditional_routing/shoe-size-block.page.js');
const SummaryPage = require('../generated_pages/repeating_and_conditional_routing/summary.page.js');

describe('Repeating Groups', function() {

  beforeEach(function() {
    return helpers.startQuestionnaire('test_repeating_and_conditional_routing.json');
  });

  it('Given a group of questions will repeat three times, when I complete the three groups of questions, then I should see a summary page of the questions.', function() {
    return completeRepeatingQuestions(3, 3)
      .then(() => {
        return browser
          .getUrl().should.eventually.contain(SummaryPage.pageName);
      });
  });

  it('Given a group of questions will repeat two times, when I select age and shoe size, then I should see a question for age.', function() {
      return browser
        .setValue(NoOfRepeatsPage.answer(), 2)
        .click(NoOfRepeatsPage.submit())
        .click(RepeatedBlockPage.ageAndShoeSize())
        .click(RepeatedBlockPage.submit())

        .getUrl().should.eventually.contain('/0/' + AgeBlockPage.pageName);
  });

  it('Given the number of repeats question has been set to two, when I select shoe size, then I should see a question for shoe size.', function() {
      return browser
        .setValue(NoOfRepeatsPage.answer(), 2)
        .click(NoOfRepeatsPage.submit())
        .click(RepeatedBlockPage.shoeSizeOnly())
        .click(RepeatedBlockPage.submit())

        .getUrl().should.eventually.contain('/0/' + ShoeSizeBlockPage.pageName);
  });

  it('Given I have completed the questions to the first of two groups, when I select age and shoe size, then I should see a question for age.', function() {
      return completeRepeatingQuestions(2, 1)
        .then(() => {
          return browser
              .click(RepeatedBlockPage.ageAndShoeSize())
              .click(RepeatedBlockPage.submit())
              .getUrl().should.eventually.contain('/1/' + AgeBlockPage.pageName);
        });
  });

  it('Given I have completed the questions to the first of two groups, when I select shoe size, then I should see a question for shoe size.', function() {
    return helpers.startQuestionnaire('test_repeating_and_conditional_routing.json')
      .then(() => {
        return completeRepeatingQuestions(2, 1);
      })
      .then(() => {
        return browser
          .click(RepeatedBlockPage.shoeSizeOnly())
          .click(RepeatedBlockPage.submit())
          .getUrl().should.eventually.contain('/1/' + ShoeSizeBlockPage.pageName);
    });
  });

  it('Given I am on the second question in the second group, when I go to the previous page, then I should see the first question for second group.', function() {
      return browser
        .setValue(NoOfRepeatsPage.answer(), 2)
        .click(NoOfRepeatsPage.submit())
        .click(RepeatedBlockPage.ageAndShoeSize())
        .click(RepeatedBlockPage.submit())

        .click(ShoeSizeBlockPage.previous())

        .getUrl().should.eventually.contain('/0/' + RepeatedBlockPage.pageName);
  });

  it('Given I go through the whole survey, I should see a summary of all the repeating groups', function() {
      return completeRepeatingQuestions(3, 3)
        .then(() => {
          return browser
            .getUrl().should.eventually.contain(SummaryPage.pageName)
            .getText(SummaryPage.whatIsYourAge(0)).should.eventually.contain(20)
            .getText(SummaryPage.whatIsYourAge(1)).should.eventually.contain(21)
            .getText(SummaryPage.whatIsYourAge(2)).should.eventually.contain(22)
            .getText(SummaryPage.whatIsYourShoeSize(0)).should.eventually.contain(8)
            .getText(SummaryPage.whatIsYourShoeSize(1)).should.eventually.contain(9)
            .getText(SummaryPage.whatIsYourShoeSize(2)).should.eventually.contain(10);
        });
  });

  function completeRepeatingQuestions(numberOfRepeats, complete) {
    let chain = browser
      .setValue(NoOfRepeatsPage.answer(), numberOfRepeats)
      .click(NoOfRepeatsPage.submit());

    for (let i = 0; i < complete; i++) {
      chain = chain.then(() => {
        return browser
          .click(RepeatedBlockPage.ageAndShoeSize())
          .click(RepeatedBlockPage.submit())
          .setValue(AgeBlockPage.whatIsYourAge(), i+20)
          .click(AgeBlockPage.submit())
          .setValue(ShoeSizeBlockPage.whatIsYourShoeSize(), i+8)
          .click(ShoeSizeBlockPage.submit());

      });
    }
    return chain;
  }

});

