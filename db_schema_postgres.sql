
-- Esquema base para Postgres (adaptado desde SQLite). Ajusta tipos/constraints seg?n pol?ticas.

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(150) NOT NULL,
    specialty VARCHAR(150),
    email VARCHAR(150) NOT NULL UNIQUE,
    username VARCHAR(80) NOT NULL UNIQUE,
    password_hash VARCHAR(200) NOT NULL,
    role VARCHAR(20),
    status VARCHAR(20)
);

CREATE TABLE patients (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(150) NOT NULL,
    dni VARCHAR(20),
    age INTEGER,
    sex VARCHAR(10),
    birth_date VARCHAR(10),
    phone VARCHAR(50),
    address VARCHAR(250),
    city VARCHAR(150),
    health_insurance VARCHAR(150),
    health_insurance_number VARCHAR(100),
    first_consultation_date VARCHAR(10),
    center VARCHAR(150),
    antecedentes TEXT,
    clinica_actual TEXT,
    estudios_realizados TEXT,
    created_by_id INTEGER REFERENCES users(id),
    smoking_current BOOLEAN,
    smoking_previous BOOLEAN,
    smoking_start_age INTEGER,
    smoking_end_age INTEGER,
    smoking_cigarettes_per_day INTEGER,
    smoking_pack_years DOUBLE PRECISION,
    respiratory_conditions TEXT,
    autoimmune_conditions TEXT,
    autoimmune_other TEXT,
    systemic_symptoms TEXT,
    occupational_exposure_types TEXT,
    occupational_accident BOOLEAN,
    occupational_accident_when TEXT,
    occupational_leave_due_to_breathing BOOLEAN,
    occupational_jobs TEXT,
    occupational_years TEXT,
    domestic_exposures TEXT,
    domestic_exposures_details TEXT,
    drug_use TEXT,
    current_medications TEXT,
    previous_medications TEXT,
    pneumotoxic_drugs TEXT,
    family_history_father TEXT,
    family_history_mother TEXT,
    family_history_siblings TEXT,
    family_history_children TEXT,
    symptom_cough BOOLEAN,
    symptom_mmrc INTEGER,
    symptom_duration_months INTEGER,
    weight_kg DOUBLE PRECISION,
    height_cm DOUBLE PRECISION,
    bmi DOUBLE PRECISION,
    physical_crepitaciones_velcro BOOLEAN,
    physical_crepitaciones BOOLEAN,
    physical_roncus BOOLEAN,
    physical_wheezing BOOLEAN,
    physical_clubbing BOOLEAN,
    physical_pulmonary_hypertension_signs BOOLEAN,
    smoking_years DOUBLE PRECISION,
    created_at TEXT,
    updated_at TEXT,
    updated_by_id INTEGER,
    consent_given BOOLEAN,
    consent_date TEXT,
    diagnoses TEXT,
    notes_personal TEXT,
    notes_smoking TEXT,
    notes_autoimmune TEXT,
    notes_systemic TEXT,
    notes_exposures TEXT,
    notes_family_history TEXT,
    notes_respiratory_exam TEXT,
    family_genogram TEXT,
    family_genogram_pdf TEXT,
    email TEXT
);

CREATE TABLE consultations (
    id SERIAL PRIMARY KEY,
    patient_id INTEGER NOT NULL REFERENCES patients(id) ON DELETE CASCADE,
    date VARCHAR(20),
    notes TEXT,
    created_by_id INTEGER REFERENCES users(id),
    lab_general TEXT,
    lab_immunology TEXT,
    lab_immunology_values TEXT,
    lab_immunology_notes TEXT
);

CREATE TABLE studies (
    id SERIAL PRIMARY KEY,
    patient_id INTEGER NOT NULL REFERENCES patients(id) ON DELETE CASCADE,
    consultation_id INTEGER REFERENCES consultations(id) ON DELETE CASCADE,
    study_type VARCHAR(150),
    date VARCHAR(20),
    center VARCHAR(150),
    description TEXT,
    created_by_id INTEGER REFERENCES users(id),
    report_file TEXT,
    access_code TEXT
);

CREATE TABLE review_requests (
    id SERIAL PRIMARY KEY,
    patient_id INTEGER NOT NULL REFERENCES patients(id) ON DELETE CASCADE,
    consultation_id INTEGER REFERENCES consultations(id) ON DELETE CASCADE,
    study_id INTEGER REFERENCES studies(id) ON DELETE CASCADE,
    created_by_id INTEGER NOT NULL REFERENCES users(id),
    recipients TEXT NOT NULL,
    message TEXT,
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP,
    resolved_at TIMESTAMP
);

CREATE TABLE review_comments (
    id SERIAL PRIMARY KEY,
    review_id INTEGER NOT NULL REFERENCES review_requests(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES users(id),
    message TEXT NOT NULL,
    created_at TIMESTAMP
);

CREATE TABLE case_presentations (
    id SERIAL PRIMARY KEY,
    patient_id INTEGER UNIQUE REFERENCES patients(id) ON DELETE CASCADE,
    intro TEXT,
    physical_exam TEXT,
    respiratory_tests TEXT,
    immunology TEXT,
    exposures TEXT,
    imaging TEXT,
    notes TEXT
);

CREATE TABLE screenings (
    id SERIAL PRIMARY KEY,
    patient_id INTEGER NOT NULL REFERENCES patients(id) ON DELETE CASCADE,
    family_history BOOLEAN,
    prior_ct BOOLEAN,
    prior_comparison TEXT,
    study_center VARCHAR(200),
    study_number VARCHAR(100),
    study_date VARCHAR(20),
    findings TEXT,
    lung_rads VARCHAR(50),
    recommendation TEXT,
    conclusion TEXT,
    nccn_criteria TEXT,
    next_control_date VARCHAR(20),
    study_file TEXT,
    screening_lung BOOLEAN,
    followup_nodule BOOLEAN,
    ecog_status TEXT,
    extra_email TEXT
);

CREATE TABLE screening_followups (
    id SERIAL PRIMARY KEY,
    screening_id INTEGER NOT NULL REFERENCES screenings(id) ON DELETE CASCADE,
    study_type VARCHAR(150),
    study_center VARCHAR(200),
    study_number VARCHAR(100),
    study_date VARCHAR(20),
    findings TEXT,
    lung_rads VARCHAR(50),
    next_control_date VARCHAR(20),
    file_name VARCHAR(300),
    created_at TIMESTAMP,
    created_by_id INTEGER REFERENCES users(id),
    completed BOOLEAN DEFAULT FALSE,
    completed_at TIMESTAMP,
    status VARCHAR(20) DEFAULT 'pending'
);

CREATE TABLE control_reminders (
    id SERIAL PRIMARY KEY,
    patient_id INTEGER NOT NULL REFERENCES patients(id) ON DELETE CASCADE,
    consultation_id INTEGER REFERENCES consultations(id) ON DELETE CASCADE,
    control_date VARCHAR(20),
    extra_emails TEXT,
    created_at TIMESTAMP,
    created_by_id INTEGER REFERENCES users(id),
    completed BOOLEAN DEFAULT FALSE,
    completed_at TIMESTAMP,
    status VARCHAR(20) DEFAULT 'pending'
);

CREATE TABLE medical_resources (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    url VARCHAR(500),
    file_name VARCHAR(300),
    created_at TIMESTAMP,
    created_by_id INTEGER REFERENCES users(id),
    notes TEXT
);
