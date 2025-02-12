

-- Создание базы данных
CREATE DATABASE admissions_system;



-- Таблица студентов
CREATE TABLE Recommended_Students (
    id SERIAL PRIMARY KEY, 
    name VARCHAR(100) NOT NULL,
    photo_base64 TEXT NOT NULL, --сохранение фото в формате в base64
    status VARCHAR(50) DEFAULT 'unconfirmed' --если получится так,что STATUS не был указан,то автоматически ставится 'unconfirmed'
    created_at TIMESTAMP DEFAULT NOW()
);

-- Таблица экзаменов
CREATE TABLE Exams (
    id SERIAL PRIMARY KEY,
    subject VARCHAR(255) NOT NULL, -- название предмета 
    date DATE NOT NULL, --дата проведения экзамена
    max_score INT NOT NULL, -- максимальный балл
    pass_score INT NOT NULL -- пороговый балл
);

-- Таблица результатов экзаменов
CREATE TABLE Exam_Results (
    id SERIAL PRIMARY KEY,
    student_id INT REFERENCES students(id) ON DELETE CASCADE, --Поле связывает результат экзамена с конкретным студентом через внешний ключ
    exam_id INT REFERENCES exams(id) ON DELETE CASCADE, -- тоже самое что и со студентами
    score INT NOT NULL, --результат экзамена 
    created_at TIMESTAMP DEFAULT NOW() -- время создания записи студентов
);

-- Таблица неподтвержденных студентов
CREATE TABLE Failed_Students (
    id SERIAL PRIMARY KEY,
    student_id INT REFERENCES students(id) ON DELETE CASCADE, --Поле связывает результат экзамена с конкретным студентом через внешний ключ
    reason TEXT NOT NULL, -- причина почему студент не был подтвержден
    created_at TIMESTAMP DEFAULT NOW()
);
