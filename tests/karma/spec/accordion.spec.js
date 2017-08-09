import {forEach} from 'lodash'
import accordion, {classAccordion,
                   classAccordionContent,
                   classAccordionBody,
                   classAccordionCloseAll,
                   classAccordionOpenAll,
                   classAccordionTitle,
                   classClose,
                   classExpanded,
                   classHidden,
                   classPreview
                  } from 'app/modules/accordion'

const strTemplate = `
<div class="${classAccordion}">
  <div class="accordion__controls">
    <button class="${classAccordionOpenAll} ${classHidden}" aria-hidden="true">Open all</button>
    <button class="${classAccordionCloseAll} ${classHidden}" aria-hidden="true">Close all</button>
  </div>
  <dl class="${classAccordionContent}">

    <dt class="${classAccordionTitle}" data-js-accordion-event-label="First Item">
      <span>First Item</span><span class="${classPreview}">Preview</span><span class="${classClose}">Close</span>
    </dt>
    <dd class="${classAccordionBody}">
      First item content
    </dd>

    <dt class="${classAccordionTitle}" data-js-accordion-event-label="Second Item">
      <spanSecond Item</span><span class="${classPreview}">Preview</span><span class="${classClose}">Close</span>
    </dt>
    <dd class="${classAccordionBody}">
      Second item content
    </dd>
  </dl>
</div>
`

let elTemplate

describe('Accordion;', function() {
  before('Add template to DOM and stub analytics', function() {
    let wrapper = document.createElement('div')
    wrapper.innerHTML = strTemplate
    elTemplate = wrapper
    document.body.appendChild(elTemplate)

    accordion((event, attr) => {
      this.lastEvent = attr
      this.lastEvent.name = event
    })
  })

  it('DOM should contain the template', function() {
    expect(document.body.contains(elTemplate)).to.equal(true)
  })

  describe('When the accordion attaches to the DOM,', function() {

    describe('Elements marked as content,', function() {
      it('Should be assigned the "tablist" role', function() {
        testAttributeValueEquals(classAccordionContent, 'role', 'tablist')
      })

      it('Should have an aria-multiselectable attribute set to true', function() {
        testAttributeValueEquals(classAccordionContent, 'aria-multiselectable', 'true')
      })
    })

    describe('Elements marked as a title', function() {
      it('Should be assigned the "tab" role', function() {
        testAttributeValueEquals(classAccordionTitle, 'role', 'tab')
      })

      it('Should have an aria-expanded attribute set to false', function() {
        testAttributeValueEquals(classAccordionTitle, 'aria-expanded', 'false')
      })

      it('Should have an aria-selected attribute set to false', function() {
        testAttributeValueEquals(classAccordionTitle, 'aria-selected', 'false')
      })
    })

    describe('Elements marked as a body', function() {
      it('Should be assigned the "tabpanel" role', function() {
        testAttributeValueEquals(classAccordionBody, 'role', 'tabpanel')
      })

      it('Should have an aria-hidden attribute set to true', function() {
        testAttributeValueEquals(classAccordionBody, 'aria-hidden', 'true')
      })
    })

  })

  describe('When the first title is clicked', function() {
    before('Click the first title', function() {
      this.titles = document.getElementsByClassName(classAccordionTitle)
      this.titles[0].click()
    })

    it('should publish the open question event', function() {
      expect(this.lastEvent.name).to.equal('send')
      expect(this.lastEvent.eventCategory).to.equal('Preview Survey')
      expect(this.lastEvent.eventAction).to.equal('Open question')
      expect(this.lastEvent.eventLabel).to.equal('First Item')
    })

    it('should have an aria-expanded attribute set to true', function() {
      expect(this.titles[0].getAttribute('aria-expanded')).to.equal('true')
    })

    it('should have an aria-selected attribute set to true', function() {
      expect(this.titles[0].getAttribute('aria-selected')).to.equal('true')
    })

    describe('the associated body', function() {
      before('get the associated body', function() {
        this.body = document.getElementById(this.titles[0].getAttribute('aria-controls'))
      })

      it('should have an aria-hidden attribute set to false', function() {
        expect(this.body.getAttribute('aria-hidden')).to.equal('false')
      })

      it('should not have the hidden class', function() {
        expect(this.body.classList.contains(classHidden)).to.be.false
      })
    })

    describe('and the first title is clicked again,', () => {
      before('Click the first title, again', function() {
        this.titles[0].click()
      })

      it('should publish the close question event', function() {
        expect(this.lastEvent.name).to.equal('send')
        expect(this.lastEvent.eventCategory).to.equal('Preview Survey')
        expect(this.lastEvent.eventAction).to.equal('Close question')
        expect(this.lastEvent.eventLabel).to.equal('First Item')
      })

      it('should have an aria-expanded attribute set to false', function() {
        expect(this.titles[0].getAttribute('aria-expanded')).to.equal('false')
      })

      it('should have an aria-selected attribute set to false', function() {
        expect(this.titles[0].getAttribute('aria-selected')).to.equal('false')
      })

      describe('the associated body', function() {
        before('get the associated body', function() {
          this.body = document.getElementById(this.titles[0].getAttribute('aria-controls'))
        })

        it('should have an aria-hidden attribute set to true', function() {
          expect(this.body.getAttribute('aria-hidden')).to.equal('true')
        })

        it('should have the hidden class', function() {
          expect(this.body.classList.contains(classHidden)).to.be.false
        })
      })
    })

  })

  describe('When open all is clicked,', () => {
    before("Click open all", function() {
      this.openAlls = document.getElementsByClassName(classAccordionOpenAll)
      this.openAlls[0].click()
    })

    it('all Open all buttons should have the hidden class', function() {
      for (let i=0; i < this.openAlls.length; i++) {
        expect(this.openAlls[i].classList.contains(classHidden)).to.be.true
      }
    })

    it('all Open all buttons should have an aria-hidden attribute set to true', () => {
      testAttributeValueEquals(classAccordionOpenAll, 'aria-hidden', 'true')
    })

    it('all Close all buttons should not have the hidden class', () => {
      const closeAlls = document.getElementsByClassName(classAccordionCloseAll)

      for (let i=0; i < closeAlls.length; i++) {
        expect(closeAlls[i].classList.contains(classHidden)).to.be.false
      }
    })

    it('all Close all buttons should still have an aria-hidden attribute set to true', () => {
      // Assumption here is that close all (and open all) aren't particularly
      // useful to screen reader users
      testAttributeValueEquals(classAccordionCloseAll, 'aria-hidden', 'true')
    })

    it('All titles should have an aria-expanded attribute set to true', function() {
      testAttributeValueEquals(classAccordionTitle, 'aria-expanded', 'true')
    })

    it('All titles should have an aria-selected attribute set to true', function() {
      testAttributeValueEquals(classAccordionTitle, 'aria-selected', 'true')
    })

    it('All bodys should not have the hidden class', () => {
      const bodys = document.getElementsByClassName(classAccordionBody)

      for (let i=0; i < bodys.length; i++) {
        expect(bodys[i].classList.contains(classHidden)).to.be.false
      }
    })

    it('All bodys should have an aria-hidden attribute set to false', () => {
      testAttributeValueEquals(classAccordionBody, 'aria-hidden', 'false')
    })

    describe("and a Title is clicked", () => {
      before("Click the first title", function() {
        this.titles = document.getElementsByClassName(classAccordionTitle)
        this.titles[0].click()
      })

      it('all Open all buttons should not have the hidden class', function() {
        for (let i=0; i < this.openAlls.length; i++) {
          expect(this.openAlls[i].classList.contains(classHidden)).to.be.false
        }
      })

      it('all Open all buttons should have an aria-hidden attribute set to true', function() {
        testAttributeValueEquals(classAccordionOpenAll, 'aria-hidden', 'true')
      })

      it('all Close all buttons should have the hidden class', function() {
        const closeAlls = document.getElementsByClassName(classAccordionCloseAll)

        for (let i=0; i < closeAlls.length; i++) {
          expect(closeAlls[i].classList.contains(classHidden)).to.be.true
        }
      })
    })
  })


})

function testAttributeValueEquals(className, attribute, value) {
  const elements = document.getElementsByClassName(className)

  for (let i=0; i < elements.length; i++) {
    expect(elements[i].getAttribute(attribute)).to.equal(value)
  }
}
