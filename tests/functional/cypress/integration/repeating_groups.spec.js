import {openQuestionnaire} from '../helpers/helpers.js'

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
                  .url().should('contain', SummaryPage.pageName);
      });
  });

  it('Given a group of questions will repeat two times, when I select age and shoe size, then I should see a question for age.', function() {
              .get(NoOfRepeatsPage.answer()).type(2)
        .get(NoOfRepeatsPage.submit()).click()
        .get(RepeatedBlockPage.ageAndShoeSize()).click()
        .get(RepeatedBlockPage.submit()).click()

        .url().should('contain', '/0/' + AgeBlockPage.pageName);
  });

  it('Given the number of repeats question has been set to two, when I select shoe size, then I should see a question for shoe size.', function() {
              .get(NoOfRepeatsPage.answer()).type(2)
        .get(NoOfRepeatsPage.submit()).click()
        .get(RepeatedBlockPage.shoeSizeOnly()).click()
        .get(RepeatedBlockPage.submit()).click()

        .url().should('contain', '/0/' + ShoeSizeBlockPage.pageName);
  });

  it('Given I have completed the questions to the first of two groups, when I select age and shoe size, then I should see a question for age.', function() {
      return completeRepeatingQuestions(2, 1)
        .then(() => {
                        .get(RepeatedBlockPage.ageAndShoeSize()).click()
              .get(RepeatedBlockPage.submit()).click()
              .url().should('contain', '/1/' + AgeBlockPage.pageName);
        });
  });

  it('Given I have completed the questions to the first of two groups, when I select shoe size, then I should see a question for shoe size.', function() {
    return helpers.startQuestionnaire('test_repeating_and_conditional_routing.json')
      .then(() => {
        return completeRepeatingQuestions(2, 1);
      })
      .then(() => {
                  .get(RepeatedBlockPage.shoeSizeOnly()).click()
          .get(RepeatedBlockPage.submit()).click()
          .url().should('contain', '/1/' + ShoeSizeBlockPage.pageName);
    });
  });

  it('Given I am on the second question in the second group, when I go to the previous page, then I should see the first question for second group.', function() {
              .get(NoOfRepeatsPage.answer()).type(2)
        .get(NoOfRepeatsPage.submit()).click()
        .get(RepeatedBlockPage.ageAndShoeSize()).click()
        .get(RepeatedBlockPage.submit()).click()

        .get(ShoeSizeBlockPage.previous()).click()

        .url().should('contain', '/0/' + RepeatedBlockPage.pageName);
  });

  it('Given I go through the whole survey, I should see a summary of all the repeating groups', function() {
      return completeRepeatingQuestions(3, 3)
        .then(() => {
                      .url().should('contain', SummaryPage.pageName)
            .get(SummaryPage.whatIsYourAge(0)).stripText().should('contain', 20)
            .get(SummaryPage.whatIsYourAge(1)).stripText().should('contain', 21)
            .get(SummaryPage.whatIsYourAge(2)).stripText().should('contain', 22)
            .get(SummaryPage.whatIsYourShoeSize(0)).stripText().should('contain', 8)
            .get(SummaryPage.whatIsYourShoeSize(1)).stripText().should('contain', 9)
            .get(SummaryPage.whatIsYourShoeSize(2)).stripText().should('contain', 10);
        });
  });

  function completeRepeatingQuestions(numberOfRepeats, complete) {
    let chain = browser
      .get(NoOfRepeatsPage.answer()).type(numberOfRepeats)
      .get(NoOfRepeatsPage.submit()).click();

    for (let i = 0; i < complete; i++) {
      chain = chain.then(() => {
                  .get(RepeatedBlockPage.ageAndShoeSize()).click()
          .get(RepeatedBlockPage.submit()).click()
          .get(AgeBlockPage.whatIsYourAge()).type(i+20)
          .get(AgeBlockPage.submit()).click()
          .get(ShoeSizeBlockPage.whatIsYourShoeSize()).type(i+8)
          .get(ShoeSizeBlockPage.submit()).click();

      });
    }
    return chain;
  }

});

