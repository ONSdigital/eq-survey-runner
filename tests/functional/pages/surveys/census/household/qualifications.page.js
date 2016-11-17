import QuestionPage from '../../question.page'

class QualificationsPage extends QuestionPage {

  click5OrMoreGcsesGradesAStarToCOrOLevelsPassesOrCsesGrade1SchoolCertificateOneALevel2To3AsLevelsOrVcesHigherDiploma() {
    browser.element('[id="qualifications-answer-1"]').click()
    return this
  }

  click1To4GcsesOrOLevelsOrCsesAnyGradesEntryLevelFoundationDiploma() {
    browser.element('[id="qualifications-answer-2"]').click()
    return this
  }

  click2OrMoreALevels4OrMoreAsLevelsOrVcesHigherSchoolCertificateAdvancedDiploma() {
    browser.element('[id="qualifications-answer-3"]').click()
    return this
  }

  clickApprenticeshipTradeAdvancedFoundationOrModern() {
    browser.element('[id="qualifications-answer-4"]').click()
    return this
  }

  clickNvqLevelOneFoundationGnvqBasicSkills() {
    browser.element('[id="qualifications-answer-5"]').click()
    return this
  }

  clickNvqLevelTwoIntermediateGnvqCityAndGuildsCraftBtecFirstRsaDiploma() {
    browser.element('[id="qualifications-answer-6"]').click()
    return this
  }

  clickNvqLevelThreeAdvancedGnvqCityAndGuildsAdvancedCraftOncOndBtecNationalRsaAdvancedDiploma() {
    browser.element('[id="qualifications-answer-7"]').click()
    return this
  }

  clickNvqLevelFourToFiveHncHndRsaHigherDiplomaBtecHigherFoundationDegree() {
    browser.element('[id="qualifications-answer-8"]').click()
    return this
  }

  clickOtherVocationalOrWorkRelatedQualifications() {
    browser.element('[id="qualifications-answer-9"]').click()
    return this
  }

  clickUndergraduateDegree() {
    browser.element('[id="qualifications-answer-10"]').click()
    return this
  }

  clickPostgraduateCertificateDiploma() {
    browser.element('[id="qualifications-answer-11"]').click()
    return this
  }

  clickMastersDegree() {
    browser.element('[id="qualifications-answer-12"]').click()
    return this
  }

  clickDoctorateDegreeForExamplePhd() {
    browser.element('[id="qualifications-answer-13"]').click()
    return this
  }

  clickProfessionalQualificationForExampleTeachingNursingAccountancy() {
    browser.element('[id="qualifications-answer-14"]').click()
    return this
  }

  clickForeignQualificationsUkEquivalentNotKnown() {
    browser.element('[id="qualifications-answer-15"]').click()
    return this
  }

  clickNoQualifications() {
    browser.element('[id="qualifications-answer-16"]').click()
    return this
  }

  setQualificationsAnswer(value) {
    browser.setValue('[name="qualifications-answer"]', value)
    return this
  }

  getQualificationsAnswer(value) {
    return browser.element('[name="qualifications-answer"]').getValue()
  }

  clickMoreThanFiveGcsesGradesAStarToCOrOLevelsPassesOrCsesGrade1SchoolCertificateOneALevelTwoToThreeAsLevelsOrVcesIntermediateOrNationalWelshBaccalaureateLevelTwo() {
    browser.element('[id="qualifications-welsh-answer-1"]').click()
    return this
  }

  clickOneToFourGcsesOrOLevelsOrCsesAnyGradesEntryLevelFoundationWelshBaccalaureateLevelOne() {
    browser.element('[id="qualifications-welsh-answer-2"]').click()
    return this
  }

  clickMoreThanTwoALevelsMoreThanFourAsLevelsOrVcesHigherSchoolCertificateAdvancedWelshBaccalaureateLevelThree() {
    browser.element('[id="qualifications-welsh-answer-3"]').click()
    return this
  }

  clickApprenticeshipFoundationModernOrHigher() {
    browser.element('[id="qualifications-welsh-answer-4"]').click()
    return this
  }

  clickNvqLevelOneFoundationGnvqEssentialOrKeySkills() {
    browser.element('[id="qualifications-welsh-answer-5"]').click()
    return this
  }

  clickNvqLevelTwoIntermediateGnvqCityAndGuildsCraftBtecFirstRsaDiploma() {
    browser.element('[id="qualifications-welsh-answer-6"]').click()
    return this
  }

  clickNvqLevelThreeAdvancedGnvqCityAndGuildsAdvancedCraftOncOndBtecNationalRsaAdvancedDiploma() {
    browser.element('[id="qualifications-welsh-answer-7"]').click()
    return this
  }

  clickNvqLevelFourToFiveHncHndRsaHigherDiplomaBtecHigher() {
    browser.element('[id="qualifications-welsh-answer-8"]').click()
    return this
  }

  clickOtherVocationalOrWorkRelatedQualifications() {
    browser.element('[id="qualifications-welsh-answer-9"]').click()
    return this
  }

  clickUndergraduateDegree() {
    browser.element('[id="qualifications-welsh-answer-10"]').click()
    return this
  }

  clickPostgraduateCertificateDiploma() {
    browser.element('[id="qualifications-welsh-answer-11"]').click()
    return this
  }

  clickMastersDegree() {
    browser.element('[id="qualifications-welsh-answer-12"]').click()
    return this
  }

  clickDoctorateDegreeForExamplePhd() {
    browser.element('[id="qualifications-welsh-answer-13"]').click()
    return this
  }

  clickProfessionalQualificationForExampleTeachingNursingAccountancy() {
    browser.element('[id="qualifications-welsh-answer-14"]').click()
    return this
  }

  clickForeignQualificationsUkEquivalentNotKnown() {
    browser.element('[id="qualifications-welsh-answer-15"]').click()
    return this
  }

  clickNoQualifications() {
    browser.element('[id="qualifications-welsh-answer-16"]').click()
    return this
  }

  setQualificationsWelshAnswer(value) {
    browser.setValue('[name="qualifications-welsh-answer"]', value)
    return this
  }

  getQualificationsWelshAnswer(value) {
    return browser.element('[name="qualifications-welsh-answer"]').getValue()
  }

}

export default new QualificationsPage()
