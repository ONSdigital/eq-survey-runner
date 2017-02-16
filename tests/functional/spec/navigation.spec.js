import chai from 'chai'
import landingPage from '../pages/landing.page'
import PercentagePage from '../pages/surveys/percentage/percentage.page'
import SummaryPage from '../pages/summary.page'
import {
  openQuestionnaire,
  setMobileViewport,
  openMobileNavigation,
  closeMobileNavigation,
  isViewSectionsVisible
} from '../helpers'

const expect = chai.expect

describe('Navigation', function() {
  it('Given a page with navigation, a user on mobile should be able to access it via the associated button', function() {
    let navIsVisible
    // Given
    setMobileViewport()
    openQuestionnaire('test_navigation.json')
    // When
    navIsVisible = openMobileNavigation()
    // Then
    expect(navIsVisible).to.be.true
  })

  it('Given a page with navigation, a user on mobile who has the navigation visible should be able to close it by tapping the close button', function() {
    let navIsNotVisible
    // When
    navIsNotVisible = closeMobileNavigation()
    // Then
    expect(navIsNotVisible).to.be.true
  })

  it('Given survey launched on mobile device, When on Introduction page, Then view sections link should not be displayed.', function() {
    // Given
    setMobileViewport()

    // When
    openQuestionnaire('test_repeating_household.json')

    // Then
    expect(isViewSectionsVisible()).to.be.false
  })

  it('Given survey launched on mobile device, When on Thank-You page, Then view sections link should not be displayed.', function() {
    // Given
    setMobileViewport()
    openQuestionnaire('test_percentage.json')

    // When
    expect(isViewSectionsVisible()).to.be.true
    PercentagePage.submit()
    SummaryPage.submit()

    // Then
    expect(isViewSectionsVisible()).to.be.false
  })
})
