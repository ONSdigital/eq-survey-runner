class FeedbackForm {

  url() {
    return '/feedback';
  }

  display() {
    return '[data-qa="a-feedback-open"]';
  }

  open() {
    return '[data-qa="a-feedback-open"]';
  }

  close() {
    return '[data-qa="a-feedback-close"]';
  }

  thanks() {
    return '#feedback-thanks';
  }

  container() {
    return '#feedback-form';
  }

  submit() {
    return '[data-qa="btn-feedback-submit"]';
  }

  messageInput() {
    return '#feedback-message';
  }

  messageLabel() {
    return '[for=feedback-message]';
  }

  nameInput() {
    return '#feedback-name';
  }

  nameLabel() {
    return '[for=feedback-name]';
  }

  emailInput() {
    return '#feedback-email';
  }

  emailLabel() {
    return '[for=feedback-email]';
  }

  signOut() {
    return '[data-qa="btn-sign-out"]';
  }
}

module.exports =  new FeedbackForm();
