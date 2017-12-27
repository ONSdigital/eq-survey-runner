ALTER TABLE eq_session
   ADD COLUMN session_data VARCHAR;

ALTER TABLE eq_session
   ADD COLUMN created_at TIMESTAMP;

ALTER TABLE eq_session
   ADD COLUMN updated_at TIMESTAMP;
