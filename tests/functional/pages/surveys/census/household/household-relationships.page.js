// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class HouseholdRelationshipsPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('household-relationships')
  }

  clickHouseholdRelationshipsAnswerHusbandOrWife(instance = 0) {
    browser.selectByValue('[id="household-relationships-answer-' + instance + '"]', 'Husband or wife')
    return this
  }

  clickHouseholdRelationshipsAnswerSameSexCivilPartner(instance = 0) {
    browser.selectByValue('[id="household-relationships-answer-' + instance + '"]', 'Same-sex civil partner')
    return this
  }

  clickHouseholdRelationshipsAnswerPartner(instance = 0) {
    browser.selectByValue('[id="household-relationships-answer-' + instance + '"]', 'Partner')
    return this
  }

  clickHouseholdRelationshipsAnswerGrandparent(instance = 0) {
    browser.selectByValue('[id="household-relationships-answer-' + instance + '"]', 'Grandparent')
    return this
  }

  clickHouseholdRelationshipsAnswerMotherOrFather(instance = 0) {
    browser.selectByValue('[id="household-relationships-answer-' + instance + '"]', 'Mother or father')
    return this
  }

  clickHouseholdRelationshipsAnswerStepMotherOrStepFather(instance = 0) {
    browser.selectByValue('[id="household-relationships-answer-' + instance + '"]', 'Step-mother or step-father')
    return this
  }

  clickHouseholdRelationshipsAnswerSonOrDaughter(instance = 0) {
    browser.selectByValue('[id="household-relationships-answer-' + instance + '"]', 'Son or daughter')
    return this
  }

  clickHouseholdRelationshipsAnswerStepChild(instance = 0) {
    browser.selectByValue('[id="household-relationships-answer-' + instance + '"]', 'Step-child')
    return this
  }

  clickHouseholdRelationshipsAnswerBrotherOrSister(instance = 0) {
    browser.selectByValue('[id="household-relationships-answer-' + instance + '"]', 'Brother or sister')
    return this
  }

  clickHouseholdRelationshipsAnswerStepBrotherOrStepSister(instance = 0) {
    browser.selectByValue('[id="household-relationships-answer-' + instance + '"]', 'Step–brother or step–sister')
    return this
  }

  clickHouseholdRelationshipsAnswerGrandchild(instance = 0) {
    browser.selectByValue('[id="household-relationships-answer-' + instance + '"]', 'Grandchild')
    return this
  }

  clickHouseholdRelationshipsAnswerRelationOther(instance = 0) {
    browser.selectByValue('[id="household-relationships-answer-' + instance + '"]', 'Relation - other')
    return this
  }

  clickHouseholdRelationshipsAnswerUnrelatedIncludingFosterChild(instance = 0) {
    browser.selectByValue('[id="household-relationships-answer-' + instance + '"]', 'Unrelated (including foster child)')
    return this
  }

}

export default new HouseholdRelationshipsPage()
