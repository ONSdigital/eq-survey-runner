// >>> WARNING THIS PAGE WAS AUTO-GENERATED - DO NOT EDIT!!! <<<

import MultipleChoiceWithOtherPage from '../../multiple-choice.page'

class HouseholdRelationshipsPage extends MultipleChoiceWithOtherPage {

  constructor() {
    super('household-relationships')
  }

  setHouseholdRelationshipsAnswerHusbandOrWife(instance = 0) {
    browser.selectByValue('[name="household-relationships-answer-' + instance + '"]', 'Husband or wife')
    return this
  }

  setHouseholdRelationshipsAnswerSameSexCivilPartner(instance = 0) {
    browser.selectByValue('[name="household-relationships-answer-' + instance + '"]', 'Same-sex civil partner')
    return this
  }

  setHouseholdRelationshipsAnswerPartner(instance = 0) {
    browser.selectByValue('[name="household-relationships-answer-' + instance + '"]', 'Partner')
    return this
  }

  setHouseholdRelationshipsAnswerGrandparent(instance = 0) {
    browser.selectByValue('[name="household-relationships-answer-' + instance + '"]', 'Grandparent')
    return this
  }

  setHouseholdRelationshipsAnswerMotherOrFather(instance = 0) {
    browser.selectByValue('[name="household-relationships-answer-' + instance + '"]', 'Mother or father')
    return this
  }

  setHouseholdRelationshipsAnswerStepMotherOrStepFather(instance = 0) {
    browser.selectByValue('[name="household-relationships-answer-' + instance + '"]', 'Step-mother or step-father')
    return this
  }

  setHouseholdRelationshipsAnswerSonOrDaughter(instance = 0) {
    browser.selectByValue('[name="household-relationships-answer-' + instance + '"]', 'Son or daughter')
    return this
  }

  setHouseholdRelationshipsAnswerStepChild(instance = 0) {
    browser.selectByValue('[name="household-relationships-answer-' + instance + '"]', 'Step-child')
    return this
  }

  setHouseholdRelationshipsAnswerBrotherOrSister(instance = 0) {
    browser.selectByValue('[name="household-relationships-answer-' + instance + '"]', 'Brother or sister')
    return this
  }

  setHouseholdRelationshipsAnswerStepBrotherOrStepSister(instance = 0) {
    browser.selectByValue('[name="household-relationships-answer-' + instance + '"]', 'Step–brother or step–sister')
    return this
  }

  setHouseholdRelationshipsAnswerGrandchild(instance = 0) {
    browser.selectByValue('[name="household-relationships-answer-' + instance + '"]', 'Grandchild')
    return this
  }

  setHouseholdRelationshipsAnswerRelationOther(instance = 0) {
    browser.selectByValue('[name="household-relationships-answer-' + instance + '"]', 'Relation - other')
    return this
  }

  setHouseholdRelationshipsAnswerUnrelatedIncludingFosterChild(instance = 0) {
    browser.selectByValue('[name="household-relationships-answer-' + instance + '"]', 'Unrelated (including foster child)')
    return this
  }

}

export default new HouseholdRelationshipsPage()
