CREATE TABLE IF NOT EXISTS refresh_tokens (digest TEXT PRIMARY KEY, subject TEXT NOT NULL, expires INTEGER NOT NULL);
CREATE INDEX IF NOT EXISTS refresh_tokens_subject ON refresh_tokens(subject);
