from ssms.db import get_db, get_results

# 1. 综合排名
# tested
def avg_coursetype(sid):
	db = get_db()
	cur = db.cursor()
	cur.execute('select avg(gpa) gpa, coursetype, sum(coursepoint) coursepoint from course, studentCourse where sid = ? and course.cid = studentCourse.cid group by coursetype', (sid))
	avg_coursetype = get_results(cur)
	return avg_coursetype
	
# tested	
def total_point(sid):
	db = get_db()
	cur = db.cursor()
	cur.execute('select sum(coursepoint) totalpoint from course, studentCourse where sid = ? and course.cid = studentCourse.cid', (sid))
	total_point = get_results(cur)
	return total_point

# tested	
def total_avg_gpa(sid):
	db = get_db()
	cur = db.cursor()
	cur.execute('select sum(sc)/sum(coursepoint) avggpa from (select gpa*coursepoint sc, coursepoint from course, studentCourse where sid = ? and course.cid = studentCourse.cid) as s', (sid))
	total_avg_gpa = get_results(cur)
	return total_avg_gpa

# 2. 综合排名变化趋势
# tested
def courseterm_rank(sid):
	db = get_db()
	cur = db.cursor()
	cur.execute('select courseterm, rank() over(order by avggpa desc) totalrank from (select sum(sc)/sum(coursepoint) avggpa, courseterm from (select gpa*coursepoint sc, coursepoint, courseterm from course, studentCourse where sid = ? and course.cid = studentCourse.cid) as s group by courseterm) as c', (sid))
	total_avg_gpa = get_results(cur)
	return courseterm_rank
	
# 3. 个人成绩分布图
# tested
def score_distribution(sid):
	db = get_db()
	cur = db.cursor()
	cur.execute('select count(*) 小于60 from course, studentCourse where sid = ? and course.cid = studentCourse.cid and score < 60', (sid))
	score_distribution = get_results(cur)
	cur.execute('select count(*) 60至70 from course, studentCourse where sid = ? and course.cid = studentCourse.cid and score >= 60 and score < 70', (sid))
	score_distribution.extend(get_results(cur))
	cur.execute('select count(*) 70至80 from course, studentCourse where sid = ? and course.cid = studentCourse.cid and score >= 70 and score < 80', (sid))
	score_distribution.extend(get_results(cur))
	cur.execute('select count(*) 80至90 from course, studentCourse where sid = ? and course.cid = studentCourse.cid and score >= 80 and score < 90', (sid))
	score_distribution.extend(get_results(cur))
	cur.execute('select count(*) 90至100 from course, studentCourse where sid = ? and course.cid = studentCourse.cid and score >= 90', (sid))
	score_distribution.extend(get_results(cur))
	return score_distribution
	
# 4. 优势学科
# tested	
def top_subject(sid):
	db = get_db()
	cur = db.cursor()
	cur.execute('select score, gpa, course.cid cid from course, studentCourse where sid = ? and course.cid = studentCourse.cid order by gpa desc limit 3', (sid))
	top_subject = get_results(cur)
	return top_subject

# 5. 劣势学科
# tested
def worst_subject(sid):
	db = get_db()
	cur = db.cursor()
	cur.execute('select score, gpa, course.cid cid from course, studentCourse where sid = ? and course.cid = studentCourse.cid order by gpa limit 3', (sid))
	worse_subject = get_results(cur)
	return worse_subject
	
# 指定课程平均分 表
# tested
def course_avg(cid):
	db = get_db()
	cur = db.cursor()
	cur.execute('select avg(score) avg from studentCourse where cid = ?', (cid))
	course_avg = get_results(cur)
	return course_avg
	
# 指定课程总人数 表
# tested
def course_count(cid):
	db = get_db()
	cur = db.cursor()
	cur.execute('select count(*) count from studentCourse where cid = ?', (cid))
	course_count = get_results(cur)
	return course_count
	
# 指定课程学生排名 表
# tested
def student_rank(cid, sid):
	db = get_db()
	cur = db.cursor()
	cur.execute('select rank() over(order by score desc) rnk from (select * from studentCourse where cid = ?) as s where sid = ?', (cid, sid))
	student_rank = get_results(cur)
	return student_rank

# 6. 成绩分布	图
# tested
def course_score(cid):
	db = get_db()
	cur = db.cursor()
	cur.execute('select score from studentCourse where cid = ?', (cid))
	course_score = get_results(cur)
	return course_score

# 6. 成绩分布	表
# tested
def course_info(cid):
	db = get_db()
	cur = db.cursor()
	cur.execute('select avg(score) avg, max(score) max, count(score > 85 or null)/ count(*) good from studentCourse where cid = ?', (cid))
	course_info = get_results(cur)
	return course_info
