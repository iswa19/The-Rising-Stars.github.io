from Project_2_CMS import app
from flask import render_template ,redirect, request,session,flash,url_for
from .data import USERS,STUDENTS

@app.route("/login/" , methods=['GET', 'POST'])
def login():

    if 'username' in session:
        return redirect("/")

    if request.method == 'POST':
        user_creds = request.form.to_dict()

        username_found = False
        for user in USERS:
            if user['username'] == user_creds['username']:
                username_found = True
                if user['password'] == user_creds['password']:
                    session['username'] = user['username']
                    session['subject'] = user['subject']
                    session['job_title'] = user['job_title']
                    flash('Logged in successfully')
                    return redirect("/")
                else:
                    flash('invalid password or you choice wrong subject')
                    return redirect("/login")

        if not username_found:
            flash('User does not exist')
            return redirect("/login")



    return render_template("login.html", students=STUDENTS)

@app.route("/register", methods=['POST', 'GET'])
def register():

      if request.method == 'POST':
          new_user = request.form.to_dict()

          if new_user['password'] != new_user['c-password']:
              flash('Password do not match')
              return redirect("/register")

          for user in USERS:
              if user['username'] == new_user['username']:
                  flash('User already exits')
                  return redirect("/register")

          USERS.append(new_user)
          {
          "username" : new_user["username"],
          "password": new_user["password"],
           "subject": new_user["subject"],
           "job_title": new_user["job_title"]
          }
          flash('account created successfully')
          return redirect("/login")

      return render_template('register.html', students=STUDENTS)

@app.route("/")
def index():

     if 'username' not in session:
         return redirect("/login")

     for student in STUDENTS:
         if student['subject'] == session['subject']:
             student_list = student
             break

     return render_template('index.html' ,student_list=student_list)

@app.route("/logout")
def logout():
  if 'username' in session :
      session.pop('username')
      return redirect("/login")

@app.route("/<roll_no>/detail")
def detail(roll_no):

 return render_template('detail.html', roll_no=roll_no , students=STUDENTS)

@app.route("/<roll_no>/<quiz_no>/delete")
def delete(roll_no,quiz_no):

    for student in STUDENTS:
        if student['subject'] == session['subject']:
            for info in student["student-info"]:
                if info['roll-no'] == roll_no:
                    for quiz in info['Quiz']:
                        if quiz['quiz-no'] == quiz_no:
                            quiz.delete(quiz_no)
                            flash('Quiz deleted suuccessfully')
                            return redirect(url_for('detail', roll_no=roll_no, quiz_no=quiz_no))

    return redirect(url_for('detail', roll_no=roll_no, quiz_no=quiz_no))


@app.route("/<roll_no>/add",methods=['GET', 'POST'] )
def add(roll_no):

    if request.method == 'POST':
        new_quiz = request.form.to_dict()

        if new_quiz['obtain-marks'] > new_quiz['total-marks']:
            flash('you enter invalid marks!')
            return redirect(url_for('detail', roll_no=roll_no))

        for student in STUDENTS:
            if student['subject'] == session['subject']:
                for info in student["student-info"]:
                    if info['roll-no'] == roll_no:
                        for quiz in info['Quiz']:
                            if (quiz['quiz-no'] == new_quiz['quiz-no']) or (quiz['topic'] == new_quiz['topic']):
                                flash('Quiz already exist')
                                return redirect(url_for('detail', roll_no=roll_no))

                        info['Quiz'].append(new_quiz)
                        {
                                    "quiz-no": new_quiz["quiz-no"],
                                    "topic": new_quiz["topic"],
                                    "status": new_quiz["status"],
                                    "total-marks": new_quiz["total-marks"],
                                    "obtain-marks": new_quiz["obtain-marks"],
                        }
                        flash('Quiz added successfully')
                        return redirect(url_for('detail', roll_no=roll_no))



    return render_template('add_form.html', roll_no=roll_no ,students=STUDENTS)

@app.route("/<roll_no>/update", methods=['GET', 'POST'] )
def update(roll_no):

    if request.method == 'POST':
        update_quiz = request.form.to_dict()

        if update_quiz['obtain-marks'] > update_quiz['total-marks']:
            flash('you enter invalid marks!')
            return redirect(url_for('detail', roll_no=roll_no))

        for student in STUDENTS:
            if student['subject'] == session['subject']:
                for info in student["student-info"]:
                    if info['roll-no'] == roll_no:
                        for quiz in info['Quiz']:
                            if (quiz['quiz-no'] == update_quiz['quiz-no']) or (quiz['topic'] == update_quiz['topic']):
                                flash('Quiz already exist')
                                return redirect(url_for('detail',roll_no=roll_no))
                            else:
                                quiz.update({"quiz-no": update_quiz['quiz-no'], "topic": update_quiz['topic'],"status": update_quiz['status'],"total-marks": update_quiz['total-marks'],"obtain-marks": update_quiz['obtain-marks']})
                                flash('quiz updated successfully')
                                return redirect(url_for('detail',roll_no=roll_no))

    return render_template('update.html', roll_no=roll_no ,students=STUDENTS)












