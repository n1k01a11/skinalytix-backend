-- ============================================================
-- MODULE 1 — Authentication / Users
-- ============================================================
CREATE TABLE users (
    user_id         SERIAL PRIMARY KEY,
    full_name       VARCHAR(150) NOT NULL,
    email           VARCHAR(150) UNIQUE NOT NULL,
    password_hash   VARCHAR(255) NOT NULL,
    age             INTEGER NOT NULL,
    sex             VARCHAR(30),
    created_at      TIMESTAMP DEFAULT NOW()
);

-- ============================================================
-- MODULE 3 — Skin Analysis (camera capture + AI result)
-- ============================================================
CREATE TABLE skin_analyses (
    analysis_id         SERIAL PRIMARY KEY,
    user_id             INTEGER REFERENCES users(user_id) ON DELETE CASCADE,
    image_path           TEXT,                     -- path/URL to stored captured photo
    ai_detected_concerns  JSONB,                    -- e.g. ["Acne", "Dark spots", "Uneven texture"]
    analyzed_at          TIMESTAMP DEFAULT NOW()
);

-- ============================================================
-- MODULE 4 — Skin Consultation (8-section form)
-- Stored as JSONB: one row per submission, keyed by section.
-- Simpler than 30+ normalized columns, and maps 1:1 to the
-- `answers` map already used in the Flutter ConsultationController.
-- ============================================================
CREATE TABLE consultations (
    consultation_id  SERIAL PRIMARY KEY,
    user_id          INTEGER REFERENCES users(user_id) ON DELETE CASCADE,
    analysis_id      INTEGER REFERENCES skin_analyses(analysis_id) ON DELETE SET NULL,
    responses        JSONB NOT NULL,   -- { "fullName": "...", "concerns": [...], "severity": "Severe", ... }
    submitted_at     TIMESTAMP DEFAULT NOW()
);

-- ============================================================
-- MODULE 5 — Combined Skin Profile
-- A snapshot generated after AI + consultation are both done —
-- this is what the recommendation engine reads from.
-- ============================================================
CREATE TABLE skin_profiles (
    profile_id        SERIAL PRIMARY KEY,
    user_id           INTEGER REFERENCES users(user_id) ON DELETE CASCADE,
    analysis_id       INTEGER REFERENCES skin_analyses(analysis_id) ON DELETE SET NULL,
    consultation_id   INTEGER REFERENCES consultations(consultation_id) ON DELETE SET NULL,
    skin_type         VARCHAR(50),
    concerns          JSONB,          -- merged AI + self-reported concerns
    sensitivity       VARCHAR(100),
    sun_exposure      VARCHAR(50),
    primary_goal      VARCHAR(100),
    severity          VARCHAR(20),     -- Mild / Moderate / Severe / Not sure
    created_at        TIMESTAMP DEFAULT NOW()
);

-- ============================================================
-- MODULE 10 — OTC Product Management (admin side)
-- ============================================================
CREATE TABLE products (
    product_id             SERIAL PRIMARY KEY,
    brand                  VARCHAR(100) NOT NULL,
    product_name           VARCHAR(150) NOT NULL,
    category               VARCHAR(50) NOT NULL,      -- Cleanser, Toner, Serum, Moisturizer, Sunscreen, etc.
    skin_types             JSONB,            -- ["Oily", "Combination"]
    skin_concerns          JSONB,            -- ["Acne", "Dark spots"] -- identified/reported concerns, not diagnoses
    key_ingredients        JSONB,            -- ["Niacinamide", "Vitamin E"]
    usage_instructions     TEXT,
    time_of_use            JSONB,            -- e.g. ["AM"], ["PM"], or ["AM", "PM"] for both
    product_notes          TEXT,             -- e.g. "Similar key ingredients to another product; further comparison may be needed"
    recommendation_status  VARCHAR(20) DEFAULT 'active',  -- active / redundant / discontinued
    created_at             TIMESTAMP DEFAULT NOW()
);

-- ============================================================
-- MODULE 6/7 — Recommendations & Referrals
-- ============================================================
CREATE TABLE recommendations (
    recommendation_id SERIAL PRIMARY KEY,
    user_id           INTEGER REFERENCES users(user_id) ON DELETE CASCADE,
    profile_id        INTEGER REFERENCES skin_profiles(profile_id) ON DELETE SET NULL,
    product_ids       JSONB,            -- [12, 15, 20] -> product_id references
    routine_explanation TEXT,
    generated_at      TIMESTAMP DEFAULT NOW()
);

CREATE TABLE referrals (
    referral_id       SERIAL PRIMARY KEY,
    user_id           INTEGER REFERENCES users(user_id) ON DELETE CASCADE,
    profile_id        INTEGER REFERENCES skin_profiles(profile_id) ON DELETE SET NULL,
    reason            TEXT,             -- e.g. "Severity: Severe — outside OTC scope"
    referred_at       TIMESTAMP DEFAULT NOW()
);

-- ============================================================
-- MODULE 9 — Admin users (separate from consumer `users` table)
-- ============================================================
CREATE TABLE admin_users (
    admin_id      SERIAL PRIMARY KEY,
    username      VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role          VARCHAR(30) DEFAULT 'admin'
);