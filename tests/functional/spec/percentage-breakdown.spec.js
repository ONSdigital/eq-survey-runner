import {getRandomString, openQuestionnaire} from '../helpers'
import totalBreakdownPage from '../pages/surveys/total-breakdown/total-breakdown.page'


describe('Percentage breakdown question', function() {

  it('Given four percentage fields, When I enter 25 in each field, Then total should be 100', function() {
    // Given
    openQuestionnaire('test_total_breakdown.json')

    // When
    totalBreakdownPage.setPercentage(1, '25')
                      .setPercentage(2, '25')
                      .setPercentage(3, '25')
                      .setPercentage(4, '25')

    // Then
    expect(totalBreakdownPage.getTotal()).to.equal('100')
  })

  it('Given four percentage fields, When I enter non integer value into a field, Then total should ignore the non integer value', function() {
    // Given
    openQuestionnaire('test_total_breakdown.json')

    // When
    totalBreakdownPage.setPercentage(1, 'twenty five')
                      .setPercentage(2, '25')
                      .setPercentage(3, '25')
                      .setPercentage(4, '25')

    // Then
    expect(totalBreakdownPage.getTotal()).to.equal('75')
  })

  it('Given four percentage fields, When I enter a negative value into a field, Then total should ignore the negative value', function() {
    // Given
    openQuestionnaire('test_total_breakdown.json')

    // When
    totalBreakdownPage.setPercentage(1, '-50')
                      .setPercentage(2, '25')
                      .setPercentage(3, '25')
                      .setPercentage(4, '25')

    // Then
    expect(totalBreakdownPage.getTotal()).to.equal('75')
  })

  it('Given four percentage fields, When I enter a values totalling > 100, Then total should display the value', function() {
    // Given
    openQuestionnaire('test_total_breakdown.json')

    // When
    totalBreakdownPage.setPercentage(1, '50')
                      .setPercentage(2, '50')
                      .setPercentage(3, '50')
                      .setPercentage(4, '50')

    // Then
    expect(totalBreakdownPage.getTotal()).to.equal('200')
  })

  it('Given four percentage fields, When I enter non-integer values into each field, Then total should be 0', function() {
    // Given
    openQuestionnaire('test_total_breakdown.json')

    // When
    totalBreakdownPage.setPercentage(1, 'total')
                      .setPercentage(2, 'should')
                      .setPercentage(3, 'be')
                      .setPercentage(4, 'zero')

    // Then
    expect(totalBreakdownPage.getTotal()).to.equal('0')
  })

  it('Given four percentage fields, When total is < 100, Then total field should be highlighted', function() {
    // Given
    openQuestionnaire('test_total_breakdown.json')

    // When
    totalBreakdownPage.setPercentage(1, '20')
                      .setPercentage(2, '20')
                      .setPercentage(3, '20')
                      .setPercentage(4, '20')

    // Then
    expect(totalBreakdownPage.isTotalHighlighted()).to.be.true
  })

  it('Given four percentage fields, When total is > 100, Then total field should be highlighted', function() {
    // Given
    openQuestionnaire('test_total_breakdown.json')

    // When
    totalBreakdownPage.setPercentage(1, '100')
                      .setPercentage(2, '100')
                      .setPercentage(3, '100')
                      .setPercentage(4, '100')

    // Then
    expect(totalBreakdownPage.isTotalHighlighted()).to.be.true
  })

  it('Given four percentage fields, When total == 100, Then total field should NOT be highlighted', function() {
    // Given
    openQuestionnaire('test_total_breakdown.json')

    // When
    totalBreakdownPage.setPercentage(1, '25')
                      .setPercentage(2, '25')
                      .setPercentage(3, '25')
                      .setPercentage(4, '25')

    // Then
    expect(totalBreakdownPage.isTotalHighlighted()).to.be.false
  })

  it('Given four percentage fields, When floating point numbers entered, Then total should be integer', function() {
    // Given
    openQuestionnaire('test_total_breakdown.json')

    // When
    totalBreakdownPage.setPercentage(1, '1.234')
                      .setPercentage(2, '2.345')
                      .setPercentage(3, '3.456')
                      .setPercentage(4, '4.567')

    // Then
    expect(totalBreakdownPage.getTotal()).to.equal('10')
  })

  it('Given a total field, When I navigate away then come back, Then total value should be preserved', function() {
    // Given
    openQuestionnaire('test_total_breakdown.json')

    // When
    totalBreakdownPage.setPercentage(1, '50')
                      .setPercentage(2, '10')
                      .setPercentage(3, '10')
                      .setPercentage(4, '10')
                      .submit()

    totalBreakdownPage.previous()

    // Then
    expect(totalBreakdownPage.getTotal()).to.equal('80')
  })

  it('Given a total field, When I enter values that total > 100 and submit, Then an error should be displayed', function() {
    // Given
    openQuestionnaire('test_total_breakdown.json')

    // When
    totalBreakdownPage.setPercentage(1, '100')
                      .setPercentage(2, '100')
                      .setPercentage(3, '100')
                      .setPercentage(4, '100')
                      .submit()

    // Then
    expect(totalBreakdownPage.errorExists()).to.be.true
  })

  it('Given a total field, When question loads, Then total field should initially be read only', function() {
    // Given
    openQuestionnaire('test_total_breakdown.json')

    // Then
    expect(totalBreakdownPage.isTotalReadOnly()).to.be.true
  })

})
