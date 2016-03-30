import { applyDetailsToggle, classTrigger, classDetails, classMain, classExpandedState } from 'app/modules/details-toggle'

const strTemplate = `<div class="guidance ${classDetails}" data-show-label="Show further guidance" data-hide-label="Hide further guidance">
  <a class="guidance__link ${classTrigger}" href="#guidance-response" id="guidance-response-link" aria-controls="guidance-response-main" aria-expanded="false"><span class="u-vh">Click here to </span><span class="js-details-label">Show further guidance</span>
  </a>
  <div class="guidance__main ${classMain}" id="guidance-response-main" tabIndex="0" aria-hidden="true">
    Vestibulum id ligula porta felis euismod semper. Curabitur blandit tempus porttitor. Morbi leo risus, porta ac consectetur ac, vestibulum at eros. Vivamus sagittis lacus vel augue laoreet rutrum faucibus dolor auctor. Donec sed odio dui. Aenean lacinia bibendum nulla sed consectetur.
  </div>
</div>`

let elTemplate

describe('Details Toggle', () => {
  before('Add template to DOM', () => {
    let wrapper = document.createElement('div')
    wrapper.innerHTML = strTemplate
    elTemplate = wrapper
    document.body.appendChild(elTemplate)
  })

  it('DOM should contain the template', () => {
    expect(document.body.contains(elTemplate)).to.equal(true)
  })

  it(`Should toggle class '.${classExpandedState}' when clicked`, () => {
    applyDetailsToggle(elTemplate)
    const elTrigger = elTemplate.parentElement.getElementsByClassName(classTrigger)[0]
    elTrigger.click()
    expect(elTemplate.classList.contains(classExpandedState)).to.equal(true)
    elTrigger.click()
    expect(elTemplate.classList.contains(classExpandedState)).to.equal(false)
  })
})
