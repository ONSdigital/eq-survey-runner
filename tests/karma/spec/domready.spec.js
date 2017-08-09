import domready from 'app/modules/domready'

describe('domready', () => {
  before('register domready functions', function() {
    this.count = 1
    domready(() => { this.count++ }) // 2
    domready(() => { this.count++ }) // 3
    domready(() => { this.count++ }) // 4
  })

  it('should execute a callback given once the dom is ready', function() {
    expect(this.count).to.equal(4)
  })
})
