class FeedbackForm {

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
    return '#feedback-message-label';
  }

  nameInput() {
    return '#feedback-name';
  }

  nameLabel() {
    return '#feedback-name-label';
  }

  emailInput() {
    return '#feedback-email';
  }

  emailLabel() {
    return '#feedback-email-label';
  }
}

module.exports =  new FeedbackForm();
