const helpers = require('../../helpers');
const RadioMandatoryPage = require('../../pages/surveys/radio/radio-mandatory.page');
const RadioNonMandatoryPage = require('../../pages/surveys/radio/radio-non-mandatory.page');
const SummaryPage = require('../../pages/surveys/radio/summary.page');

describe('Component: Radio', function() {

var radio_schema = 'test_radio.json';


    describe('Optional', function() {
          beforeEach('load the survey', function() {
            return helpers.openQuestionnaire(radio_schema).then(() => {
                return browser;
                  .click(RadioMandatoryPage.none())
                  .click(RadioMandatoryPage.submit());
                  });
                });

          it('When I submit without choosing an option that I should be able to go on to the next page', function() {
             return browser
               .click(RadioNonMandatoryPage.submit())
               .getUrl().should.eventually.contain(SummaryPage.pageName);
            });

         it('When I select an optional option field and not enter any text I should still be able to move on', function() {
           return browser;
              .getUrl().should.eventually.contain(RadioNonMandatoryPage.pageName)
              .click(RadioNonMandatoryPage.other())
              .click(RadioNonMandatoryPage.submit())

              .getText(SummaryPage.radioMandatoryAnswer()).should.eventually.contain('None')
              .getText(SummaryPage.radioNonMandatoryAnswer()).should.eventually.contain('No answer provided');

            });

        it('When I select the other option then submit then return and remove other field text then it should be displayed correctly on the summary page', function() {
         return browser;
          .click(RadioNonMandatoryPage.other())
          .setValue(RadioNonMandatoryPage.otherText(), 'Hello')
          .click(RadioNonMandatoryPage.submit())

          .click(SummaryPage.previous())

          .click(RadioNonMandatoryPage.other())
          .setValue(RadioNonMandatoryPage.otherText(), '')
          .click(RadioNonMandatoryPage.submit())

          .getText(SummaryPage.radioMandatoryAnswer()).should.eventually.contain('None')
          .getText(SummaryPage.radioNonMandatoryAnswer()).should.eventually.contain('No answer provided');
          });
    });

    describe('Mandatory', function() {
      beforeEach('load the survey', function() {
        return helpers.openQuestionnaire(radio_schema).then(() => {
            return browser;
              });
            });

      it('When I submit without choosing an option that I should get an error', function() {
         return browser;
            .click(RadioMandatoryPage.submit())
            .isVisible(RadioMandatoryPage.error()).should.eventually.be.true;
        });

      it('When I submit data it should be persisted and displayed on the summary page', function() {
         return browser;
         .click(RadioMandatoryPage.bacon())
         .click(RadioMandatoryPage.submit())

         .click(RadioNonMandatoryPage.coffee())
         .click(RadioNonMandatoryPage.submit())

         .getUrl().should.eventually.contain(SummaryPage.pageName)
         .getText(SummaryPage.radioMandatoryAnswer()).should.eventually.contain('Bacon')
         .getText(SummaryPage.radioNonMandatoryAnswer()).should.eventually.contain('Coffee')
        });


      it('When I submit data and then go back and update an answer the content on thr summary screen should be correct', function() {
         return browser;
         .click(RadioMandatoryPage.eggs())
         .click(RadioMandatoryPage.submit())

         .click(RadioNonMandatoryPage.none())
         .click(RadioNonMandatoryPage.submit())

         .click(SummaryPage.previous())

         .click(RadioNonMandatoryPage.tea())
         .click(RadioNonMandatoryPage.submit())

         .getText(SummaryPage.radioMandatoryAnswer()).should.eventually.contain('Eggs')
         .getText(SummaryPage.radioNonMandatoryAnswer()).should.eventually.contain('Tea')
         });

      it('When I select the other option the text field should be viewable', function() {
         return browser;
          .click(RadioMandatoryPage.other())
          .isVisible(RadioMandatoryPage.otherText()).should.eventually.be.true;
         });


      it('When I select the other option the data entered should be displayed on the summary page', function() {
         return browser;
          .click(RadioMandatoryPage.other())
          .setValue(RadioMandatoryPage.otherText(), 'Hello')

          .click(RadioMandatoryPage.submit())
          .click(RadioNonMandatoryPage.submit())

          .click(SummaryPage.previous())

          .click(RadioNonMandatoryPage.other())
          .setValue(RadioNonMandatoryPage.otherText(), 'World')
          .click(RadioNonMandatoryPage.submit())


          .getText(SummaryPage.radioMandatoryAnswer()).should.eventually.contain('Hello')
          .getText(SummaryPage.radioNonMandatoryAnswer()).should.eventually.contain('World');
         });
    });
});
