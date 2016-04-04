import domready from 'app/modules/domready'

describe('domready', () => {
  let count = 1
  domready(() => { count++ }) // 2
  domready(() => { count++ }) // 3
  domready(() => { count++ }) // 4

  it('should execute a callback given once the dom is ready', () => {
    expect(count).to.equal(4)
  })
})
