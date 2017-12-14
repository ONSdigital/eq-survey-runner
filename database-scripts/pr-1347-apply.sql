ALTER TABLE questionnaire_state
  ADD COLUMN created_at TIMESTAMP;

ALTER TABLE questionnaire_state
  ADD COLUMN updated_at TIMESTAMP;

ALTER TABLE questionnaire_state
  ADD COLUMN version INT;
