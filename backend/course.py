@app.route('/courses', methods=['GET', 'POST'])
def courses():
    conn = get_db_connection()
    cur = conn.cursor()

    if request.method == 'POST':
        student_email = request.form['student_email']
        course_code = request.form['course_code']
        course_rev = request.form['course_rev']
        exam_type = request.form['exam_type']
        new_grade = request.form['grade']
        print(student_email, course_code, course_rev, exam_type, new_grade)

        if new_grade == '':
            new_grade = None

        if new_grade is None:
            cur.execute(
                'UPDATE grades SET grade_score = NULL WHERE grade_student_epita_email_ref = %s AND grade_course_code_ref = %s AND grade_course_rev_ref = %s AND grade_exam_type_ref = %s',
                (student_email, course_code, course_rev, exam_type))
        else:
            cur.execute('REPLACE INTO grades (grade_student_epita_email_ref, grade_course_code_ref, grade_course_rev_ref, grade_exam_type_ref, grade_score) VALUES (%s, %s, %s, %s, %s)',
                        (student_email, course_code, course_rev, exam_type, new_grade))

        conn.commit()
        flash('Grades updated successfully!')
        return redirect(url_for('courses'))

    # 查询所有课程
    cur.execute('SELECT course_code, course_rev, course_name FROM courses ORDER BY course_code, course_rev')
    courses = cur.fetchall()
    print(courses)

    # 查询所有学生和他们的成绩
    cur.execute('''
        SELECT s.student_epita_email, c.course_code, c.course_rev, g.grade_exam_type_ref, g.grade_score
        FROM students s
        LEFT JOIN grades g ON s.student_epita_email = g.grade_student_epita_email_ref
        LEFT JOIN courses c ON g.grade_course_code_ref = c.course_code AND g.grade_course_rev_ref = c.course_rev
        ORDER BY s.student_epita_email, c.course_code, c.course_rev, g.grade_exam_type_ref
    ''')
    grades = cur.fetchall()
    print(grades)

    conn.close()
    return render_template('courses.html', grades=grades, courses=courses)
