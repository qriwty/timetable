DROP FUNCTION IF EXISTS get_timetable(time_swing varchar, dat_of_week varchar);

CREATE OR REPLACE FUNCTION get_timetable(time_swing varchar(10) default 'current',
                                         day_of_week varchar(10) default 'current')
    RETURNS TABLE (
        pair INT,
        start_time text,
        end_time text,
        lesson varchar,
        lesson_type varchar,
        cabinet varchar
    ) AS $$
    DECLARE
        current_dow INT;
        week_swing INT;
    BEGIN
        IF day_of_week = 'current' THEN
            current_dow := extract(isodow from current_date);
        ELSE
            current_dow := day_of_week::INT;
        END IF;
        IF time_swing = 'current' THEN
           week_swing := 0;
        ELSE
            week_swing := time_swing::INT;
        END IF;
        RETURN QUERY
            SELECT
                timetable.timeschedule_id as pair,
                to_char(timeschedule.start_time, 'HH24:MI') as "start",
                to_char(timeschedule.end_time, 'HH24:MI') as "end",
                timetable.name as lesson,
                timetable.type as lesson_type,
                auditorium.cabinet
            FROM
                timetable
                INNER JOIN
                    timeschedule on timetable.timeschedule_id = timeschedule.id
                INNER JOIN
                    semester on timetable.semester_id = semester.id
                LEFT JOIN
                    auditorium on timetable.auditorium_id = auditorium.id
            WHERE
                (odd = TRUNC(DATE_PART('day', current_timestamp - semester.start_day) + extract(isodow from semester.start_day) / 7 + 1 + week_swing)::int % 2 OR odd = 2) AND
                (dow = current_dow)
            ORDER BY pair;
    END;
$$ LANGUAGE plpgsql;

SELECT * FROM get_timetable('0', 'current');
