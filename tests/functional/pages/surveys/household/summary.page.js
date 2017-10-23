// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<
const QuestionPage = require('../question.page');

class SummaryPage extends QuestionPage {

  constructor() {
    super('summary');
  }

  firstName() { return '#first-name-answer'; }

  firstNameEdit() { return '[data-qa="first-name-edit"]'; }

  middleNames() { return '#middle-names-answer'; }

  middleNamesEdit() { return '[data-qa="middle-names-edit"]'; }

  lastName() { return '#last-name-answer'; }

  lastNameEdit() { return '[data-qa="last-name-edit"]'; }

  householdCompositionAddAnother() { return '#household-composition-add-another-answer'; }

  householdCompositionAddAnotherEdit() { return '[data-qa="household-composition-add-another-edit"]'; }

  whoIsRelated() { return '#who-is-related-answer'; }

  whoIsRelatedEdit() { return '[data-qa="who-is-related-edit"]'; }

  whatIsYourAge() { return '#what-is-your-age-answer'; }

  whatIsYourAgeEdit() { return '[data-qa="what-is-your-age-edit"]'; }

  whatIsYourShoeSize() { return '#what-is-your-shoe-size-answer'; }

  whatIsYourShoeSizeEdit() { return '[data-qa="what-is-your-shoe-size-edit"]'; }

}
module.exports = new SummaryPage();
