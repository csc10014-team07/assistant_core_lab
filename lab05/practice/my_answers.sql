
-- Q1: All columns of all students
SELECT *
FROM students;

-- Q2: Name and year of every student
SELECT name, year
FROM students;

-- Q3: Names of CS students
SELECT name
FROM students
WHERE program = 'CS';

-- Q4: Name and year of students in year 3 or higher
SELECT name, year
FROM students
WHERE year >= 3;

-- Q5: Student names from Z to A
SELECT name
FROM students
ORDER BY name DESC;

-- Q6: Title and credits of 4-credit courses, sorted by title
SELECT title, credits
FROM courses
WHERE credits = 4
ORDER BY title;

-- Q7: How many students?
SELECT COUNT(*)
FROM students;

-- Q8: Number of students per program, sorted by program
SELECT program, COUNT(*)
FROM students
GROUP BY program
ORDER BY program;

-- Q9: Average grade in CSC10004, rounded to 2 decimals
SELECT ROUND(AVG(grade), 2)
FROM enrollments
WHERE course_code = 'CSC10004';

-- Q10: Student ID and course code of enrollments without a grade
SELECT student_id, course_code
FROM enrollments
WHERE grade IS NULL
ORDER BY student_id;

-- Q11: Name and grade of graded students in CSC10014, by name
SELECT s.name, e.grade
FROM enrollments e
JOIN students s ON s.id = e.student_id
WHERE e.course_code = 'CSC10014'
  AND e.grade IS NOT NULL
ORDER BY s.name;

-- Q12: Each course title with the number of enrolled students,
-- most first, then by title
SELECT c.title, COUNT(e.student_id)
FROM courses c
JOIN enrollments e ON e.course_code = c.code
GROUP BY c.code, c.title
ORDER BY COUNT(e.student_id) DESC, c.title;

-- Q13: Names of students with a grade below 5
SELECT DISTINCT s.name
FROM students s
JOIN enrollments e ON e.student_id = s.id
WHERE e.grade < 5
ORDER BY s.name;

-- Q14: Each student's name and total credits enrolled,
-- most first, then by name
SELECT s.name, SUM(c.credits) AS credits
FROM enrollments e
JOIN students s ON s.id = e.student_id
JOIN courses c ON c.code = e.course_code
GROUP BY s.name
ORDER BY credits DESC, s.name;

-- Q15: Names of students not enrolled in CSC10014
SELECT s.name
FROM students s
LEFT JOIN enrollments e
    ON e.student_id = s.id
    AND e.course_code = 'CSC10014'
WHERE e.student_id IS NULL
ORDER BY s.name;
