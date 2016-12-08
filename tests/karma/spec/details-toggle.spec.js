import { applyDetailsToggle, classTrigger, classDetails, classBody, classExpandedState } from 'app/modules/details-toggle'

const strTemplate = `<div class="guidance ${classDetails}" data-show-label="Show further guidance" data-hide-label="Hide further guidance">
  <a class="guidance__link ${classTrigger} js-details-label" href="#guidance-response" id="guidance-response-link" aria-controls="guidance-response-main" aria-expanded="false">
    Show further guidance
  </a>
  <div class="guidance__main ${classBody}" id="guidance-response-main" aria-hidden="true">
    Vestibulum id ligula porta felis euismod semper. Curabitur blandit tempus porttitor. Morbi leo risus, porta ac consectetur ac, vestibulum at eros. Vivamus sagittis lacus vel augue laoreet rutrum faucibus dolor auctor. Donec sed odio dui. Aenean lacinia bibendum nulla sed consectetur.
  </div>
</div>`

let elDetails, elTrigger, elBody

describe('Details Toggle', () => {
  before('Add template to DOM', () => {
    let wrapper = document.createElement('div')
    wrapper.innerHTML = strTemplate
    elDetails = wrapper.firstChild
    document.body.appendChild(elDetails)
    let el = applyDetailsToggle(elDetails)
    ;({elTrigger, elBody} = el)
  })

  it('DOM should contain the template', () => {
    expect(document.body.contains(elDetails)).to.equal(true)
  })

  it(`Should toggle class '.${classExpandedState}' when clicked`, () => {
    elTrigger.click()
    expect(elDetails.classList.contains(classExpandedState)).to.equal(true)
    elTrigger.click()
    expect(elDetails.classList.contains(classExpandedState)).to.equal(false)
  })
})
