-- ============================================================
-- 🏥 POLYCLINIC MANAGEMENT SYSTEM — SAMPLE DATA
-- ============================================================
-- Demo va test uchun sinov yozuvlari.
-- Ishga tushirish:
--   mysql -u root -p polyclinic_db < sample_data.sql
-- ============================================================

USE polyclinic_db;

-- Foreign key tekshiruvni vaqtincha o'chirib turamiz
SET FOREIGN_KEY_CHECKS = 0;

TRUNCATE TABLE payment;
TRUNCATE TABLE visit_consultation;
TRUNCATE TABLE visit_procedure;
TRUNCATE TABLE visit;
TRUNCATE TABLE patient;
TRUNCATE TABLE doctor;
TRUNCATE TABLE procedure_type;
TRUNCATE TABLE qualification;
TRUNCATE TABLE specialty;
TRUNCATE TABLE discount_category;

SET FOREIGN_KEY_CHECKS = 1;

-- ============================================================
-- 1. CHEGIRMA TOIFALARI
-- ============================================================
INSERT INTO discount_category (name, percent, description) VALUES
('Nafaqaxor',       15.00, 'Pensiya yoshidagi fuqarolar uchun'),
('Faxriy',          25.00, 'Mehnat va urush faxriylari'),
('Bola (0-7 yosh)', 20.00, '7 yoshgacha bo''lgan bolalar'),
('O''quvchi',        10.00, 'Maktab va litsey o''quvchilari uchun'),
('Talaba',          12.00, 'OTM talabalari'),
('Nogiron I',       30.00, 'I guruh nogironlari'),
('Nogiron II',      20.00, 'II guruh nogironlari'),
('Korporativ',      15.00, 'Hamkor kompaniyalar xodimlari'),
('Ko''p bolali oila', 18.00, '4 va undan ko''p bolali oilalar'),
('Standart',         0.00, 'Chegirmasiz oddiy mijoz');

-- ============================================================
-- 2. MUTAXASSISLIKLAR
-- ============================================================
INSERT INTO specialty (name, description) VALUES
('Terapiya',        'Umumiy ichki kasalliklar'),
('Kardiologiya',    'Yurak-qon tomir kasalliklari'),
('Stomatologiya',   'Tish-jag'' kasalliklari'),
('Nevrologiya',     'Asab tizimi kasalliklari'),
('Pediatriya',      'Bolalar kasalliklari'),
('Ginekologiya',    'Ayol jinsiy a''zolari kasalliklari'),
('Urologiya',       'Erkak jinsiy a''zolari va siydik yo''llari'),
('Dermatologiya',   'Teri kasalliklari'),
('Oftalmologiya',   'Ko''z kasalliklari'),
('LOR',             'Quloq, tomoq, burun kasalliklari'),
('Endokrinologiya', 'Ichki sekretsiya bezlari'),
('Travmatologiya',  'Shikastlar va sinishlar');

-- ============================================================
-- 3. SHIFOKOR MALAKALARI
-- ============================================================
INSERT INTO qualification (name, price_multiplier, description) VALUES
('Stajor',          0.80, 'Yangi boshlovchi shifokor'),
('Ikkinchi toifa',  1.00, 'Ikkinchi toifa shifokor'),
('Birinchi toifa',  1.20, 'Birinchi toifa shifokor'),
('Oliy toifa',      1.50, 'Oliy toifa, ko''p yillik tajriba'),
('Fan nomzodi',     1.80, 'Tibbiyot fanlari nomzodi'),
('Fan doktori',     2.20, 'Tibbiyot fanlari doktori, professor');

-- ============================================================
-- 4. SHIFOKORLAR
-- ============================================================
INSERT INTO doctor (full_name, specialty_id, qualification_id, consultation_price, phone, hired_at) VALUES
('Karimov Ahmad Toshpulatovich',     1, 4, 80000.00,  '+998901234567', '2018-03-15'),
('Yusupova Dilbar Olimovna',          2, 5, 120000.00, '+998901234568', '2015-09-01'),
('Rahmonov Sherzod Akmalovich',       3, 3, 90000.00,  '+998901234569', '2020-01-10'),
('Toshpulatova Madina Karimovna',     4, 4, 100000.00, '+998901234570', '2017-06-20'),
('Abdullayev Bekzod Rashidovich',     5, 3, 75000.00,  '+998901234571', '2021-02-14'),
('Sayfullayeva Nigora Toshmatovna',   6, 4, 95000.00,  '+998901234572', '2016-11-05'),
('Hakimov Olimjon Yusupovich',        7, 3, 85000.00,  '+998901234573', '2019-08-12'),
('Maxmudova Zarina Bahodirovna',      8, 2, 70000.00,  '+998901234574', '2022-04-01'),
('Norboyev Sanjar Murodovich',        9, 4, 90000.00,  '+998901234575', '2018-12-03'),
('Qodirov Asror Tursunbekovich',     10, 3, 80000.00,  '+998901234576', '2020-07-19'),
('Ergasheva Mehriniso Hamidovna',    11, 6, 150000.00, '+998901234577', '2010-05-25'),
('Toshev Jasur Komilovich',          12, 4, 100000.00, '+998901234578', '2017-10-08'),
('Ismatova Gulnora Akramovna',        1, 2, 60000.00,  '+998901234579', '2023-01-15'),
('Rasulov Otabek Sherzodovich',       2, 3, 110000.00, '+998901234580', '2019-03-22'),
('Mirzayeva Sevara Olimjonovna',      3, 4, 95000.00,  '+998901234581', '2016-08-30');

-- ============================================================
-- 5. PROTSEDURA TURLARI
-- ============================================================
INSERT INTO procedure_type (name, base_price, duration_minutes, description) VALUES
('Umumiy qon tahlili',           45000.00,  10, 'Eritrotsit, leykotsit, gemoglobin'),
('Biokimyoviy qon tahlili',      90000.00,  15, 'Glukoza, xolesterin, jigar fermentlari'),
('Siydik tahlili',               30000.00,  10, 'Siydikning umumiy ko''rinishi'),
('UZI (qorin bo''shlig''i)',     150000.00,  20, 'Jigar, taloq, oshqozon-osti, buyrak'),
('UZI (yurak / EXOKG)',         200000.00,  30, 'Yurak ekokardiografiyasi'),
('UZI (kichik tos)',            120000.00,  20, 'Bachadon, tuxumdonlar, qovuq'),
('EKG (elektrokardiogramma)',    50000.00,  15, 'Yurak elektr faolligi yozuvi'),
('Rentgen (ko''krak)',          80000.00,  10, 'Ko''krak qafasi rentgenografiyasi'),
('MRT (bosh miya)',             450000.00,  45, 'Magnit-rezonans tomografiya'),
('KT (kompyuter tomografiya)',  350000.00,  30, 'Rentgen kompyuter tomografiyasi'),
('Tish tozalash',                100000.00, 30, 'Professional tish tozalash'),
('Plomba qo''yish',              130000.00, 40, 'Karies davolash, plomba'),
('Tishni olib tashlash',         80000.00,  20, 'Oddiy tish ekstraksiyasi'),
('Endoskopiya (gastroskopiya)', 250000.00,  30, 'Oshqozon ichki ko''rinishi'),
('Spirometriya',                 60000.00,  15, 'O''pka funktsiyasini o''lchash'),
('Audiometriya',                 55000.00,  20, 'Eshitish darajasini tekshirish'),
('Ko''z bosimini o''lchash',     35000.00,  10, 'Glaukoma tekshiruvi'),
('Inyeksiya (mushak ichi)',      15000.00,  5,  'Dori muskuliga yuborish'),
('Tomchi (kapelnitsa)',         50000.00,  60, 'Vena ichi tomchi infuzion terapiya'),
('Massaj (10 daqiqa)',           40000.00,  10, 'Davo massaji');

-- ============================================================
-- 6. BEMORLAR
-- ============================================================
INSERT INTO patient (full_name, birth_date, gender, phone, address, discount_category_id) VALUES
('Aliyev Bahrom Rashidovich',         '1955-03-12', 'M', '+998991111001', 'Toshkent, Yunusobod, 5-kvartal',     1),
('Saidova Mukarram Olimovna',         '1948-07-25', 'F', '+998991111002', 'Toshkent, Mirzo Ulug''bek, 12-uy',     2),
('Karimov Davron Sherzodovich',       '2019-11-08', 'M', '+998991111003', 'Toshkent, Chilonzor, 8-mavze',         3),
('Hakimova Sevinch Akmalovna',        '2020-05-14', 'F', '+998991111004', 'Toshkent, Sergeli, 4-mavze',           3),
('Yusupov Otabek Komilovich',         '2008-09-21', 'M', '+998991111005', 'Toshkent, Olmazor, 19-uy',             4),
('Toshpulatova Madina Asrorovna',     '2003-02-17', 'F', '+998991111006', 'Toshkent, Yashnobod, 7-kvartal',       5),
('Rahmonov Jasur Bahodirovich',       '1985-06-30', 'M', '+998991111007', 'Toshkent, Mirobod, 14-uy',             10),
('Mirzayeva Nilufar Sanjarovna',      '1990-12-05', 'F', '+998991111008', 'Toshkent, Bektemir, 3-mavze',          10),
('Abdullayev Sherzod Olimjonovich',   '1972-08-19', 'M', '+998991111009', 'Toshkent, Yakkasaroy, 22-uy',          6),
('Sayfullayev Bekzod Hasanovich',     '1980-04-11', 'M', '+998991111010', 'Toshkent, Uchtepa, 9-mavze',           7),
('Norboyeva Gulchehra Nodirovna',     '1965-01-23', 'F', '+998991111011', 'Toshkent, Shayxontohur, 6-uy',          1),
('Qodirov Ravshan Tursunbekovich',    '1958-10-04', 'M', '+998991111012', 'Toshkent, Yunusobod, 11-mavze',         2),
('Ergasheva Mavluda Hamidovna',       '1995-07-15', 'F', '+998991111013', 'Toshkent, Chilonzor, 17-uy',           10),
('Toshev Asror Komilovich',           '1988-03-28', 'M', '+998991111014', 'Toshkent, Mirzo Ulug''bek, 5-mavze',    8),
('Ismatova Dilnoza Akramovna',        '2012-09-09', 'F', '+998991111015', 'Toshkent, Sergeli, 15-uy',             4),
('Rasulov Akbar Sherzodovich',        '1978-11-22', 'M', '+998991111016', 'Toshkent, Olmazor, 8-mavze',           9),
('Karimova Shahnoza Bahodirovna',     '2015-04-06', 'F', '+998991111017', 'Toshkent, Yashnobod, 20-uy',           3),
('Yusupova Charos Otabekovna',        '1992-08-13', 'F', '+998991111018', 'Toshkent, Mirobod, 11-mavze',          10),
('Saidov Sardor Olimjonovich',        '1970-05-19', 'M', '+998991111019', 'Toshkent, Bektemir, 6-uy',             10),
('Aliyeva Zilola Bahromovna',         '1996-12-31', 'F', '+998991111020', 'Toshkent, Yakkasaroy, 14-mavze',       10);

-- ============================================================
-- 7. MUROJAATLAR (VISITS)
-- ============================================================
-- Sana 2026-04 ichida tarqalgan
INSERT INTO visit (patient_id, primary_doctor_id, visit_date, diagnosis, payment_status) VALUES
( 1,  2, '2026-04-01', 'Arterial gipertenziya II daraja',         'PAID'),
( 2,  4, '2026-04-02', 'Bosh og''rig''i, migren shubhasi',         'PAID'),
( 3,  5, '2026-04-03', 'O''tkir respirator infektsiya',           'PAID'),
( 4,  5, '2026-04-04', 'Profilaktik ko''rik (chaqaloq)',          'PAID'),
( 5,  3, '2026-04-05', 'Karies, plomba kerak',                    'PAID'),
( 6,  6, '2026-04-08', 'Ginekologik profilaktika ko''rigi',       'PAID'),
( 7,  1, '2026-04-09', 'Oshqozon-ichak buzilishi',                'PAID'),
( 8, 11, '2026-04-10', 'Qandli diabet 2-tipi (kuzatuv)',          'PAID'),
( 9,  7, '2026-04-11', 'Buyrak toshlari shubhasi',                'PENDING'),
(10,  9, '2026-04-12', 'Ko''rish keskinligining pasayishi',       'PAID'),
(11,  2, '2026-04-15', 'YuIK, stenokardiya',                      'PAID'),
(12, 10, '2026-04-16', 'Yiringli otit',                           'PAID'),
(13, 14, '2026-04-17', 'Aritmiya, EKG kerak',                     'PAID'),
(14,  8, '2026-04-18', 'Allergik dermatit',                       'PAID'),
(15,  5, '2026-04-19', 'Tomoq og''rig''i, angina',                'PAID'),
(16, 12, '2026-04-22', 'Bilakdagi shikast (singan emas)',         'PAID'),
(17,  3, '2026-04-23', 'Sutda tish kariesi',                      'PAID'),
(18,  6, '2026-04-24', 'Tug''ruqdan keyingi profilaktika',         'PAID'),
(19,  1, '2026-04-25', 'Bel og''rig''i, periodik',                 'PENDING'),
(20, 11, '2026-04-26', 'Qalqonsimon bez tekshiruvi',              'PAID'),
( 1,  2, '2026-04-27', 'Gipertenziya kuzatuvi',                   'PAID'),
( 7, 14, '2026-04-28', 'EKG natijalari muhokamasi',                'PAID'),
( 8,  1, '2026-04-29', 'Diabet va gipertenziya kombinatsiyasi',   'PAID');

-- ============================================================
-- 8. MUROJAAT-PROTSEDURA (M:N) — har bir murojaatga 1-3 ta protsedura
-- ============================================================
INSERT INTO visit_procedure (visit_id, procedure_type_id, price_at_time, quantity, notes) VALUES
-- Visit 1: gipertenziya
( 1,  1,  45000.00, 1, 'Umumiy qon tahlili'),
( 1,  7,  50000.00, 1, 'EKG'),
( 1,  5, 200000.00, 1, 'EXOKG'),
-- Visit 2: bosh og'rig'i
( 2,  9, 450000.00, 1, 'Bosh miya MRT'),
-- Visit 3: ORVI
( 3,  1,  45000.00, 1, NULL),
( 3, 18,  15000.00, 2, 'Antibiotik inyeksiyasi'),
-- Visit 4: chaqaloq profilaktika (faqat konsultatsiya)
-- Visit 5: karies
( 5, 11, 100000.00, 1, NULL),
( 5, 12, 130000.00, 2, '2 ta tishga plomba'),
-- Visit 6: ginekologik
( 6,  6, 120000.00, 1, 'Kichik tos UZI'),
( 6,  3,  30000.00, 1, NULL),
-- Visit 7: oshqozon
( 7, 14, 250000.00, 1, 'Gastroskopiya'),
( 7,  2,  90000.00, 1, NULL),
-- Visit 8: diabet
( 8,  2,  90000.00, 1, 'Glukoza, HbA1c'),
( 8,  1,  45000.00, 1, NULL),
-- Visit 9: buyrak
( 9,  4, 150000.00, 1, NULL),
( 9,  3,  30000.00, 1, NULL),
-- Visit 10: ko'z
(10, 17,  35000.00, 1, NULL),
-- Visit 11: stenokardiya
(11,  7,  50000.00, 1, NULL),
(11,  5, 200000.00, 1, NULL),
(11,  2,  90000.00, 1, NULL),
-- Visit 12: otit
(12, 18,  15000.00, 3, '3 ta inyeksiya'),
-- Visit 13: aritmiya
(13,  7,  50000.00, 1, NULL),
(13,  5, 200000.00, 1, NULL),
-- Visit 14: dermatit (faqat konsultatsiya)
-- Visit 15: angina
(15,  1,  45000.00, 1, NULL),
(15, 18,  15000.00, 2, NULL),
-- Visit 16: shikast
(16,  8,  80000.00, 1, 'Bilak rentgeni'),
-- Visit 17: tish
(17, 11, 100000.00, 1, NULL),
(17, 12, 130000.00, 1, NULL),
-- Visit 18: profilaktika
(18,  1,  45000.00, 1, NULL),
-- Visit 19: bel og'rig'i
(19, 10, 350000.00, 1, 'Bel umurtqasi KT'),
(19, 20,  40000.00, 5, '5 sessiya massaj'),
-- Visit 20: qalqonsimon
(20,  2,  90000.00, 1, 'Qalqonsimon bez gormonlari'),
-- Visit 21: gipertenziya kuzatuv
(21,  7,  50000.00, 1, NULL),
-- Visit 22: EKG natijalari (faqat konsultatsiya)
-- Visit 23: diabet+gipertenziya
(23,  2,  90000.00, 1, NULL),
(23,  7,  50000.00, 1, NULL),
(23, 19,  50000.00, 1, 'Tomchi terapiya');

-- ============================================================
-- 9. MUROJAAT-KONSULTATSIYA (qo'shimcha shifokorlar konsultatsiyasi)
-- ============================================================
INSERT INTO visit_consultation (visit_id, doctor_id, price_at_time, notes) VALUES
-- Visit 1 (Aliyev): kardiolog asosiy + terapevt qo'shimcha
( 1,  1, 80000.00, 'Komorbid holat — terapevt fikri'),
-- Visit 7 (Rahmonov): terapevt asosiy + kardiolog
( 7, 14, 110000.00, 'Yurak shikoyatlari hisobga'),
-- Visit 8 (Mirzayeva, diabet): endokrinolog asosiy + kardiolog
( 8,  2, 120000.00, 'Diabet asoratlarini tekshirish'),
-- Visit 11 (Norboyeva): kardiolog + nevrolog
(11,  4, 100000.00, 'Qo''shimcha nevrologik tekshiruv'),
-- Visit 19 (Saidov, bel): terapevt + travmatolog
(19, 12, 100000.00, 'Travmatolog konsultatsiyasi'),
-- Visit 23 (kombinatsiya): terapevt + endokrinolog
(23, 11, 150000.00, 'Endokrinolog fikri');

-- ============================================================
-- 10. SUBTOTAL/DISCOUNT/TOTAL'NI YANGILASH (avtomatik trigger emas, qo'lda)
-- ============================================================
-- Har bir murojaat uchun:
--   subtotal = SUM(visit_procedure.price * qty) + primary doctor consultation
--            + SUM(visit_consultation.price)
--   discount_amount = subtotal * patient.discount_category.percent / 100
--   total_cost = subtotal - discount_amount

UPDATE visit v
JOIN (
    SELECT
        v.id AS visit_id,
        d.consultation_price * q.price_multiplier
            + COALESCE(SUM(DISTINCT vp.price_at_time * vp.quantity), 0)
            + COALESCE(SUM(DISTINCT vc.price_at_time), 0) AS calculated_subtotal
    FROM visit v
    JOIN doctor d ON v.primary_doctor_id = d.id
    JOIN qualification q ON d.qualification_id = q.id
    LEFT JOIN visit_procedure vp ON vp.visit_id = v.id
    LEFT JOIN visit_consultation vc ON vc.visit_id = v.id
    GROUP BY v.id, d.consultation_price, q.price_multiplier
) calc ON v.id = calc.visit_id
SET v.subtotal = calc.calculated_subtotal;

-- Chegirma va total
UPDATE visit v
JOIN patient p ON v.patient_id = p.id
LEFT JOIN discount_category dc ON p.discount_category_id = dc.id
SET
    v.discount_amount = ROUND(v.subtotal * COALESCE(dc.percent, 0) / 100, 2),
    v.total_cost      = ROUND(v.subtotal - (v.subtotal * COALESCE(dc.percent, 0) / 100), 2);

-- ============================================================
-- 11. TO'LOVLAR (faqat PAID statusdagilarga)
-- ============================================================
INSERT INTO payment (visit_id, amount, method, paid_at, receipt_number)
SELECT
    v.id,
    v.total_cost,
    CASE (v.id % 3)
        WHEN 0 THEN 'CASH'
        WHEN 1 THEN 'CARD'
        ELSE        'TRANSFER'
    END,
    TIMESTAMP(v.visit_date, '14:30:00'),
    CONCAT('RCP-2026-', LPAD(v.id, 6, '0'))
FROM visit v
WHERE v.payment_status = 'PAID';

-- ============================================================
-- ✅ MA'LUMOTLAR TAYYOR
-- ============================================================
-- Tekshirish:
SELECT 'Bemorlar:'        AS jadval, COUNT(*) AS soni FROM patient
UNION SELECT 'Shifokorlar:',         COUNT(*) FROM doctor
UNION SELECT 'Mutaxassisliklar:',    COUNT(*) FROM specialty
UNION SELECT 'Protsedura turlari:',  COUNT(*) FROM procedure_type
UNION SELECT 'Murojaatlar:',         COUNT(*) FROM visit
UNION SELECT 'Protsedura yozuvlari:', COUNT(*) FROM visit_procedure
UNION SELECT 'Konsultatsiyalar:',    COUNT(*) FROM visit_consultation
UNION SELECT 'To''lovlar:',           COUNT(*) FROM payment;

-- Demo so'rovlar (mijozga ko'rsatish uchun)
SELECT '═══ Bugungi daromad ═══' AS info;
SELECT * FROM v_daily_revenue LIMIT 5;

SELECT '═══ Eng faol shifokorlar ═══' AS info;
SELECT * FROM v_top_doctors LIMIT 5;
