import chai from 'chai'
import {
  startQuestionnaire,
  setMobileViewport,
  openMobileNavigation,
  closeMobileNavigation
} from '../helpers'

const expect = chai.expect

describe('Navigation', function() {
  it('Given a page with navigation, a user on mobile should be able to access it via the associated button', function() {
    let navIsVisible
    // Given
    setMobileViewport()
    startQuestionnaire('test_navigation.json')
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
})
