-- ============================================================
-- 🏥 POLYCLINIC MANAGEMENT SYSTEM — MySQL 8 Schema
-- ============================================================
-- Bu skript ER diagramma asosida qurilgan.
-- Ishga tushirish: mysql -u root -p < database_schema.sql
-- ============================================================

DROP DATABASE IF EXISTS polyclinic_db;
CREATE DATABASE polyclinic_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE polyclinic_db;

-- ============================================================
-- 1. CHEGIRMA TOIFALARI
-- ============================================================
CREATE TABLE discount_category (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    name            VARCHAR(50) NOT NULL UNIQUE COMMENT 'Nafaqaxor, Faxriy, Bola',
    percent         DECIMAL(5,2) NOT NULL CHECK (percent >= 0 AND percent <= 100),
    description     TEXT,
    is_active       BOOLEAN NOT NULL DEFAULT TRUE,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    INDEX idx_discount_active (is_active)
) ENGINE=InnoDB COMMENT='Chegirma toifalari (nafaqaxor, faxriy va h.k.)';

-- ============================================================
-- 2. MUTAXASSISLIK
-- ============================================================
CREATE TABLE specialty (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    name            VARCHAR(100) NOT NULL UNIQUE COMMENT 'Kardiologiya, Terapiya...',
    description     TEXT,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB COMMENT='Mutaxassisliklar lug''ati';

-- ============================================================
-- 3. SHIFOKOR MALAKASI (KATEGORIYA)
-- ============================================================
CREATE TABLE qualification (
    id                  INT AUTO_INCREMENT PRIMARY KEY,
    name                VARCHAR(50) NOT NULL UNIQUE COMMENT 'Oliy, Birinchi, Ikkinchi',
    price_multiplier    DECIMAL(4,2) NOT NULL DEFAULT 1.00 COMMENT 'Narxga koeffitsient',
    description         TEXT
) ENGINE=InnoDB COMMENT='Shifokor malaka darajalari';

-- ============================================================
-- 4. SHIFOKORLAR
-- ============================================================
CREATE TABLE doctor (
    id                      INT AUTO_INCREMENT PRIMARY KEY,
    full_name               VARCHAR(150) NOT NULL,
    specialty_id            INT NOT NULL,
    qualification_id        INT NOT NULL,
    consultation_price      DECIMAL(10,2) NOT NULL CHECK (consultation_price >= 0),
    phone                   VARCHAR(20),
    is_active               BOOLEAN NOT NULL DEFAULT TRUE,
    hired_at                DATE,
    created_at              TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at              TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_doctor_specialty
        FOREIGN KEY (specialty_id) REFERENCES specialty(id)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_doctor_qualification
        FOREIGN KEY (qualification_id) REFERENCES qualification(id)
        ON DELETE RESTRICT ON UPDATE CASCADE,

    INDEX idx_doctor_specialty (specialty_id),
    INDEX idx_doctor_active (is_active),
    INDEX idx_doctor_name (full_name)
) ENGINE=InnoDB COMMENT='Shifokorlar';

-- ============================================================
-- 5. BEMORLAR
-- ============================================================
CREATE TABLE patient (
    id                      INT AUTO_INCREMENT PRIMARY KEY,
    full_name               VARCHAR(150) NOT NULL,
    birth_date              DATE NOT NULL,
    gender                  ENUM('M', 'F') NOT NULL,
    phone                   VARCHAR(20) NOT NULL UNIQUE,
    address                 VARCHAR(255),
    discount_category_id    INT NULL,
    created_at              TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at              TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_patient_discount
        FOREIGN KEY (discount_category_id) REFERENCES discount_category(id)
        ON DELETE SET NULL ON UPDATE CASCADE,

    INDEX idx_patient_phone (phone),
    INDEX idx_patient_name (full_name),
    INDEX idx_patient_discount (discount_category_id)
) ENGINE=InnoDB COMMENT='Bemorlar';

-- ============================================================
-- 6. PROTSEDURA TURLARI (LUG'AT)
-- ============================================================
CREATE TABLE procedure_type (
    id                  INT AUTO_INCREMENT PRIMARY KEY,
    name                VARCHAR(150) NOT NULL COMMENT 'UZI, Qon tahlili, EKG...',
    base_price          DECIMAL(10,2) NOT NULL CHECK (base_price >= 0),
    duration_minutes    INT DEFAULT 15,
    description         TEXT,
    is_active           BOOLEAN NOT NULL DEFAULT TRUE,
    created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    INDEX idx_procedure_active (is_active),
    INDEX idx_procedure_name (name)
) ENGINE=InnoDB COMMENT='Tibbiy protseduralar/xizmatlar lug''ati';

-- ============================================================
-- 7. MUROJAATLAR (VISITS)
-- ============================================================
CREATE TABLE visit (
    id                  INT AUTO_INCREMENT PRIMARY KEY,
    patient_id          INT NOT NULL,
    primary_doctor_id   INT NOT NULL,
    visit_date          DATE NOT NULL,
    diagnosis           TEXT,
    subtotal            DECIMAL(10,2) NOT NULL DEFAULT 0 COMMENT 'Chegirmagacha',
    discount_amount     DECIMAL(10,2) NOT NULL DEFAULT 0,
    total_cost          DECIMAL(10,2) NOT NULL DEFAULT 0 COMMENT 'Yakuniy summa',
    payment_status      ENUM('PENDING', 'PAID', 'CANCELLED') NOT NULL DEFAULT 'PENDING',
    notes               TEXT,
    created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_visit_patient
        FOREIGN KEY (patient_id) REFERENCES patient(id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_visit_doctor
        FOREIGN KEY (primary_doctor_id) REFERENCES doctor(id)
        ON DELETE RESTRICT ON UPDATE CASCADE,

    INDEX idx_visit_date (visit_date),
    INDEX idx_visit_patient (patient_id),
    INDEX idx_visit_doctor (primary_doctor_id),
    INDEX idx_visit_status (payment_status)
) ENGINE=InnoDB COMMENT='Bemor murojaatlari';

-- ============================================================
-- 8. MUROJAAT-PROTSEDURA (M:N)
-- ============================================================
CREATE TABLE visit_procedure (
    id                  INT AUTO_INCREMENT PRIMARY KEY,
    visit_id            INT NOT NULL,
    procedure_type_id   INT NOT NULL,
    price_at_time       DECIMAL(10,2) NOT NULL COMMENT 'Tarix uchun shu paytdagi narx',
    quantity            INT NOT NULL DEFAULT 1 CHECK (quantity > 0),
    notes               TEXT,
    created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_vp_visit
        FOREIGN KEY (visit_id) REFERENCES visit(id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_vp_procedure
        FOREIGN KEY (procedure_type_id) REFERENCES procedure_type(id)
        ON DELETE RESTRICT ON UPDATE CASCADE,

    INDEX idx_vp_visit (visit_id),
    INDEX idx_vp_procedure (procedure_type_id)
) ENGINE=InnoDB COMMENT='Murojaatga biriktirilgan protseduralar';

-- ============================================================
-- 9. MUROJAAT-KONSULTATSIYA (M:N)
-- ============================================================
CREATE TABLE visit_consultation (
    id                  INT AUTO_INCREMENT PRIMARY KEY,
    visit_id            INT NOT NULL,
    doctor_id           INT NOT NULL,
    price_at_time       DECIMAL(10,2) NOT NULL,
    notes               TEXT,
    created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_vc_visit
        FOREIGN KEY (visit_id) REFERENCES visit(id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_vc_doctor
        FOREIGN KEY (doctor_id) REFERENCES doctor(id)
        ON DELETE RESTRICT ON UPDATE CASCADE,

    INDEX idx_vc_visit (visit_id),
    INDEX idx_vc_doctor (doctor_id)
) ENGINE=InnoDB COMMENT='Murojaatdagi qo''shimcha shifokor konsultatsiyalari';

-- ============================================================
-- 10. TO'LOVLAR
-- ============================================================
CREATE TABLE payment (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    visit_id        INT NOT NULL UNIQUE COMMENT 'Bir murojaatga bir to''lov',
    amount          DECIMAL(10,2) NOT NULL CHECK (amount >= 0),
    method          ENUM('CASH', 'CARD', 'TRANSFER') NOT NULL DEFAULT 'CASH',
    paid_at         TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    receipt_number  VARCHAR(50) UNIQUE,

    CONSTRAINT fk_payment_visit
        FOREIGN KEY (visit_id) REFERENCES visit(id)
        ON DELETE CASCADE ON UPDATE CASCADE,

    INDEX idx_payment_date (paid_at),
    INDEX idx_payment_method (method)
) ENGINE=InnoDB COMMENT='To''lov qaydlari';

-- ============================================================
-- 📊 FOYDALI VIEW'LAR (HISOBOTLAR UCHUN)
-- ============================================================

-- Kunlik daromad
CREATE OR REPLACE VIEW v_daily_revenue AS
SELECT
    visit_date,
    COUNT(*) AS visit_count,
    SUM(subtotal) AS gross_revenue,
    SUM(discount_amount) AS total_discounts,
    SUM(total_cost) AS net_revenue
FROM visit
WHERE payment_status = 'PAID'
GROUP BY visit_date
ORDER BY visit_date DESC;

-- Eng faol shifokorlar
CREATE OR REPLACE VIEW v_top_doctors AS
SELECT
    d.id,
    d.full_name,
    s.name AS specialty,
    COUNT(v.id) AS total_visits,
    SUM(v.total_cost) AS total_revenue
FROM doctor d
LEFT JOIN specialty s ON d.specialty_id = s.id
LEFT JOIN visit v ON v.primary_doctor_id = d.id AND v.payment_status = 'PAID'
GROUP BY d.id, d.full_name, s.name
ORDER BY total_visits DESC;

-- Bemor tarixi
CREATE OR REPLACE VIEW v_patient_history AS
SELECT
    p.id AS patient_id,
    p.full_name AS patient_name,
    v.id AS visit_id,
    v.visit_date,
    d.full_name AS doctor_name,
    s.name AS specialty,
    v.diagnosis,
    v.total_cost,
    v.payment_status
FROM patient p
JOIN visit v ON v.patient_id = p.id
JOIN doctor d ON v.primary_doctor_id = d.id
JOIN specialty s ON d.specialty_id = s.id
ORDER BY v.visit_date DESC;

-- ============================================================
-- ✅ SCHEMA TAYYOR
-- ============================================================
-- Tekshirish:
--   USE polyclinic_db;
--   SHOW TABLES;
--   DESCRIBE visit;
-- ============================================================
