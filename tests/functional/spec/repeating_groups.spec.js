const helpers = require('../helpers');

const NoOfRepeatsPage = require('../pages/surveys/repeating_groups/no-of-repeats.page.js');
const RepeatedBlockPage = require('../pages/surveys/repeating_groups/repeated-block.page.js');
const AgeBlockPage = require('../pages/surveys/repeating_groups/age-block.page.js');
const ShoeSizeBlockPage = require('../pages/surveys/repeating_groups/shoe-size-block.page.js');
const SummaryPage = require('../pages/surveys/repeating_groups/summary.page.js');

describe('Repeating Groups', function() {


  it('Given a group of questions will repeat three times, when I complete the three groups of questions, then I should see a summary page of the questions.', function() {
    return helpers.startQuestionnaire('test_repeating_and_conditional_routing.json')
    .then(() => {
      return completeRepeatingQuestions(3, 3);
    })
      .then(() => {
      return browser
          .getUrl().should.eventually.contain(SummaryPage.pageName);
    });
  });

  it('Given a group of questions will repeat two times, when I select age and shoe size, then I should see a question for age.', function() {
    return helpers.startQuestionnaire('test_repeating_and_conditional_routing.json').then(() => {
        return browser
          .setValue(NoOfRepeatsPage.answer(), 2)
          .click(NoOfRepeatsPage.submit())
          .click(RepeatedBlockPage.ageAndShoeSize())
          .click(RepeatedBlockPage.submit())

          .getUrl().should.eventually.contain('/0/' + AgeBlockPage.pageName);
    });
  });

  it('Given the number of repeats question has been set to two, when I select shoe size, then I should see a question for shoe size.', function() {
    return helpers.startQuestionnaire('test_repeating_and_conditional_routing.json').then(() => {
        return browser
          .setValue(NoOfRepeatsPage.answer(), 2)
          .click(NoOfRepeatsPage.submit())
          .click(RepeatedBlockPage.shoeSizeOnly())
          .click(RepeatedBlockPage.submit())

          .getUrl().should.eventually.contain('/0/' + ShoeSizeBlockPage.pageName);
    });
  });

  it('Given I have completed the questions to the first of two groups, when I select age and shoe size, then I should see a question for age.', function() {
    return helpers.startQuestionnaire('test_repeating_and_conditional_routing.json')
    .then(() => {
      return completeRepeatingQuestions(2, 1);
    })
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
    return helpers.startQuestionnaire('test_repeating_and_conditional_routing.json').then(() => {
        return browser
          .setValue(NoOfRepeatsPage.answer(), 2)
          .click(NoOfRepeatsPage.submit())
          .click(RepeatedBlockPage.ageAndShoeSize())
          .click(RepeatedBlockPage.submit())

          .click(ShoeSizeBlockPage.previous())

          .getUrl().should.eventually.contain('/0/' + RepeatedBlockPage.pageName);
    });
  });

  function completeRepeatingQuestions(numberOfRepeats, complete) {
    let chain = browser
      .setValue(NoOfRepeatsPage.answer(), numberOfRepeats)
      .click(NoOfRepeatsPage.submit());

    for (var i = 0; i < complete; i++) {
      chain = chain.then(() => {
        return browser
          .click(RepeatedBlockPage.ageAndShoeSize())
          .click(RepeatedBlockPage.submit())
          .setValue(AgeBlockPage.answer(), i+20)
          .click(AgeBlockPage.submit())
          .setValue(ShoeSizeBlockPage.answer(), i+8)
          .click(ShoeSizeBlockPage.submit());

      });
    }
    return chain;
  }

});

