SELECT
        timetable.id,
        timetable.timeschedule_id as pair,
        to_char(timeschedule.start_time, 'HH24:MI') as "start",
        to_char(timeschedule.end_time, 'HH24:MI') as "end",
        timetable.name as lesson,
        timetable.type as lesson_type,
        auditorium.cabinet,
        format('%s %s. %s.', teacher.surname, substring(teacher.name, 1, 1), substring(teacher.patronymic, 1, 1)) as "FIO",
        timetable.odd "odd / even week",
        timetable.dow as "day of week"
    FROM
        timetable
        INNER JOIN
            timeschedule on timetable.timeschedule_id = timeschedule.id
        INNER JOIN
            semester on timetable.semester_id = semester.id
        LEFT JOIN
            auditorium on timetable.auditorium_id = auditorium.id
        LEFT JOIN
            teacher on timetable.teacher_id = teacher.id
    WHERE
        (odd = TRUNC(DATE_PART('day', current_timestamp - semester.start_day) / 7)::int % 2 OR odd = 2) AND
        (dow = extract(isodow from current_date))
    ORDER BY pair;