ALTER TABLE questionnaire_state
  ADD COLUMN created_at DATETIME;

ALTER TABLE questionnaire_state
  ADD COLUMN updated_at DATETIME;

ALTER TABLE questionnaire_state
  ADD COLUMN version INT;
