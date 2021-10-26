DROP TABLE IF EXISTS semester, timeSchedule, auditorium, teacher, timetable;


create table semester (
    id serial primary key,
    start_day date,
    end_day date
);

INSERT INTO semester (start_day, end_day) VALUES ('01.09.2021', '31.12.2021');


create table timeSchedule (
    id serial primary key,
    start_time time,
    end_time time
);

INSERT INTO
    timeSchedule (start_time, end_time)
    VALUES
           ('08:00', '09:35'),
           ('09:50', '11:25'),
           ('11:40', '13:15'),
           ('13:30', '15:05');


create table auditorium (
    id serial primary key,
    cabinet char(15),
    building char(15)
);

INSERT INTO
    auditorium (cabinet, building)
    VALUES
           ('233г', 'ГУК'),
           ('201ф', 'ИКС'),
           ('909ф', 'ИКС'),
           ('203ф', 'ИКС'),
           ('607ф', 'ИКС'),
           ('311ф', 'ИКС'),
           ('707ф', 'ИКС'),
           ('109а', 'АДМИН'),
           ('02a', 'АДМИН'),
           ('2в', 'ВСТАВКА');


create table teacher (
    id serial primary key,
    name char(20),
    surname char(20),
    patronymic char(20),
    phone char(20),
    email char(20),
    auditorium_id integer REFERENCES auditorium (id),
    description char(20)
);

INSERT INTO
    teacher (surname, name, patronymic, phone, email, auditorium_id, description)
    VALUES
           ('Годовиченко', 'Николай', 'Анатольевич', '+380', '@gmail', (SELECT id from auditorium WHERE cabinet = '909ф'), 'Хороший');


create table timetable (
    id serial primary key,
    timeSchedule_id integer REFERENCES timeSchedule (id),
    name char(20),
    dow integer CHECK (dow >= 0 AND dow <= 7),
    odd integer CHECK (odd >= 0 AND odd <= 2),
    type char(20),
    auditorium_id integer REFERENCES auditorium (id),
    teacher_id integer REFERENCES teacher (id),
    semester_id integer REFERENCES semester (id)
);

INSERT INTO
    timetable (dow, timeSchedule_id, name, odd, type, auditorium_id, teacher_id, semester_id)
    VALUES
            (1, 1, 'Укр', 1, 'лекция', (SELECT id from auditorium WHERE cabinet = '233г'), (SELECT id from teacher WHERE email = '@gmail'), 1),
            (1, 2, 'Вышмат', 2, 'лекция', (SELECT id from auditorium WHERE cabinet = '201ф'), (SELECT id from teacher WHERE email = '@gmail'), 1),
            (1, 3, 'ООП', 2, 'лекция', (SELECT id from auditorium WHERE cabinet = '909ф'), (SELECT id from teacher WHERE email = '@gmail'), 1),
            (1, 4, 'Веб', 2, 'лекция', (SELECT id from auditorium WHERE cabinet = '203ф'), (SELECT id from teacher WHERE email = '@gmail'), 1);

INSERT INTO
    timetable (dow, timeSchedule_id, name, odd, type, auditorium_id, teacher_id, semester_id)
    VALUES
            (2, 1, 'Базы данных', 2, 'лаба', (SELECT id from auditorium WHERE cabinet = '607ф'), (SELECT id from teacher WHERE email = '@gmail'), 1),
            (2, 2, 'Конфликт', 0, '', (SELECT id from auditorium WHERE cabinet = '2в'), (SELECT id from teacher WHERE email = '@gmail'), 1),
            (2, 3, 'Вышмат', 2, 'практика', (SELECT id from auditorium WHERE cabinet = '311ф'), (SELECT id from teacher WHERE email = '@gmail'), 1),
            (2, 4, 'Физ-ра', 2, '', (SELECT id from auditorium WHERE cabinet = ''), (SELECT id from teacher WHERE email = '@gmail'), 1);

INSERT INTO
    timetable (dow, timeSchedule_id, name, odd, type, auditorium_id, teacher_id, semester_id)
    VALUES
           (3, 1, 'Конфликт', 1, '', (SELECT id from auditorium WHERE cabinet = '2в'), (SELECT id from teacher WHERE email = '@gmail'), 1),
           (3, 2, 'Экология', 2, 'лекция', (SELECT id from auditorium WHERE cabinet = '214гук'), (SELECT id from teacher WHERE email = '@gmail'), 1),
           (3, 3, 'Алгоритмы', 2, 'лекция', (SELECT id from auditorium WHERE cabinet = '707ф'), (SELECT id from teacher WHERE email = '@gmail'), 1),
           (3, 4, 'Базы данных', 2, 'лекция', (SELECT id from auditorium WHERE cabinet = '707ф'), (SELECT id from teacher WHERE email = '@gmail'), 1);

INSERT INTO
    timetable (dow, timeSchedule_id, name, odd, type, auditorium_id, teacher_id, semester_id)
    VALUES
           (4, 2, 'Веб', 1, 'лаба', (SELECT id from auditorium WHERE cabinet = '909ф'), (SELECT id from teacher WHERE email = '@gmail'), 1),
           (4, 3, 'Укр', 2, 'практика', (SELECT id from auditorium WHERE cabinet = '201ф'), (SELECT id from teacher WHERE email = '@gmail'), 1);

INSERT INTO
    timetable (dow, timeSchedule_id, name, odd, type, auditorium_id, teacher_id, semester_id)
    VALUES
           (5, 1, 'ООП', 2, 'лаба', (SELECT id from auditorium WHERE cabinet = '909ф'), (SELECT id from teacher WHERE email = '@gmail'), 1),
           (5, 2, 'Экология', 1, 'практика', (SELECT id from auditorium WHERE cabinet = '02а'), (SELECT id from teacher WHERE email = '@gmail'), 1),
           (5, 3, 'Алгоритмы', 0, 'лаба', (SELECT id from auditorium WHERE cabinet = '109а'), (SELECT id from teacher WHERE email = '@gmail'), 1),
           (5, 4, 'Физ-ра', 2, '', (SELECT id from auditorium WHERE cabinet = ''), (SELECT id from teacher WHERE email = '@gmail'), 1);
