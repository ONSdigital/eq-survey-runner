      class Navigation {

        navigateToInnovationActivitiesBusinessStrategyandPractices() {
          browser.element('//a[contains(@href, \'business-strategy-practices/0/business-changes\')]').click()
          return this
        }

        navigateToInnovationInvestment() {
          browser.element('//a[contains(@href, \'innovation-investment/0/internal-investment-r-d\')]').click()
          return this
        }

        navigateToGoodsandServicesInnovation() {
          browser.element('//a[contains(@href, \'goods-services-innovation/0/introducing-significantly-improved-goods\')]').click()
          return this
        }

        navigateToProcessInnovation() {
          browser.element('//a[contains(@href, \'process-innovation/0/process-improved\')]').click()
          return this
        }

        navigateToPublicFinancialSupportforInnovation() {
          browser.element('//a[contains(@href, \'public-financial-support-for-innovation/0/public-financial-support\')]').click()
          return this
        }

        navigateToConstraintsonInnovation() {
          browser.element('//a[contains(@href, \'constraints-on-innovation/0/constraints-innovation-activities\')]').click()
          return this
        }

        navigateToFactorsAffectingInnovation() {
          browser.element('//a[contains(@href, \'context-for-innovation-section-64-group-64/0/context-for-innovation-block-52\')]').click()
          return this
        }

        navigateToInformationNeededforInnovation() {
          browser.element('//a[contains(@href, \'context-for-innovation-section-77-group-77/0/context-for-innovation-block-65\')]').click()
          return this
        }

        navigateToCooperationonInnovation() {
          browser.element('//a[contains(@href, \'context-for-innovation-section-94-group-94/0/context-for-innovation-block-78\')]').click()
          return this
        }
    }

      export default new Navigation()
