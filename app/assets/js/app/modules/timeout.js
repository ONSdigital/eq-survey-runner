import domready from './domready'
import dialog from './dialog'
import fetch from './fetch'
import LoaderBtn from './loader-btn'
import { padStart } from 'lodash'

class TimeoutUI {
  constructor(timePrompt, timeLimit) {
    this.el = document.querySelector('.js-timeout')
    this.circleEl = document.querySelector('.js-timeout-circle')
    this.timeTextEl = document.querySelector('.js-timeout-time')
    this.timePrompt = timePrompt
    this.timeLimit = timeLimit

    if (!this.el || !this.circleEl || !this.timeTextEl) return false

    this.circleElRadius = this.circleEl.getAttribute('r')
    this.strokeWidth = this.circleEl.getAttribute('stroke-width')
    this.timeStartCountdown = this.getTimeNow()

    this.reset()
  }

  getTimeNow() {
    return parseInt(new Date().getTime() / 1000)
  }

  onTick() {
    let countDown = this.timeLimit - (this.getTimeNow() - this.timeStartCountdown)
    if (countDown <= this.timePrompt) {
      this.draw(countDown)
    }

    return countDown
  }

  draw(time) {
    const date = new Date(null)
    date.setSeconds(time)
    const mins = padStart(date.getUTCMinutes(), 2, '0')
    const seconds = padStart(date.getUTCSeconds(), 2, '0')
    const angle = (360 - (360 / (this.timePrompt / time))) / (57.5 / this.circleElRadius)

    this.timeTextEl.innerHTML = `${mins}:${seconds}`

    if (angle > 0) {
      // adjust for stroke, but add a couple of px to account for stroke radius
      this.circleEl.style.strokeDasharray = `${Math.max(0, (angle - (this.strokeWidth / 2)) + 2)}, 1000`
      this.circleEl.getBoundingClientRect()
    }

    if (time < 10) {
      this.el.classList.add('is-warning')
    }
  }

  reset() {
    this.timeStartCountdown = this.getTimeNow()
    this.circleEl.style.strokeDasharray = '0, 1000'
    this.circleEl.getBoundingClientRect()
  }
}

domready(() => {
  const sessionTimeout = window.__EQ_SESSION_TIMEOUT__
  const promptTime = window.__EQ_SESSION_TIMEOUT_PROMPT__
  const sessionExpiredUrl = window.__EQ_SESSION_EXPIRED_URL__
  const expireSessionUrl = window.__EQ_EXPIRE_SESSION_URL__
  const sessionContinueUrl = window.__EQ_SESSION_CONTINUE_URL__

  const continueBtn = new LoaderBtn('.js-timeout-continue')
  const saveBtn = document.querySelector('.js-timeout-save')

  const continueRetryLimit = 5
  let continueRetryCount = continueRetryLimit

  const timeoutUI = new TimeoutUI(promptTime, sessionTimeout)

  // bail if there's no timeout or the DOM elements aren't there
  if (!sessionTimeout || !timeoutUI.el) return

  const handleContinue = (e) => {
    e.preventDefault()
    fetch(sessionContinueUrl)
      .then(() => {
        dialog.hide()
        continueBtn.reset()
        continueRetryCount = continueRetryLimit
        timeoutUI.reset()
      }).catch(() => {
        // if error retry 5 times
        if (continueRetryCount-- > 0) {
          window.setTimeout(() => {
            handleContinue(e)
          }, 1000)
        } else {
          continueBtn.reset()
          continueRetryCount = continueRetryLimit
        }
      })
  }

  const handleSave = (e) => {
    e.preventDefault()
    document.querySelector('.js-btn-save').click()
    return false
  }

  // intercept and override ESC key closing dialog
  document.addEventListener('keydown', (e) => {
    if (e.which === 27) { // ESC Key
      e.preventDefault()
      e.stopImmediatePropagation()
      handleContinue(e)
    }
  }, false)

  continueBtn.addEventListener('click', handleContinue)
  saveBtn.addEventListener('click', handleSave)

  // must be initialised after the keydown listener
  dialog.init()

  let timeoutInterval = window.setInterval((a) => {
    let countDown = timeoutUI.onTick()
    if (countDown < 1) {
      window.clearInterval(timeoutInterval)
      fetch(expireSessionUrl, { method: 'POST' })
        .then(() => {
          window.location = sessionExpiredUrl
        })
    }

    if (countDown < promptTime) {
      dialog.show()
    }
  }, 1000)
})
