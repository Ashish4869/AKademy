#Importing Neccesary Dependencies
from flask import Flask,jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS

#Initializing the app and configuring it with MYSQL Database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Ashishkishorekumar321@localhost/akademydb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Creating instance of objects
db = SQLAlchemy(app)
ma = Marshmallow(app)
CORS(app)


#--------------TABLE CREATION------------------

#Teachers table
class Teachers(db.Model):
    name = db.Column(db.String(30), primary_key=True)
    password = db.Column(db.String(30) , nullable = False)

    def __init__(self , name , password):
        self.name = name
        self.password = password


#Courses Table
class Courses(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    course_name = db.Column(db.String(100) , nullable = False)
    course_length = db.Column(db.String(10))
    course_image_id = db.Column(db.String(200) , nullable = False)
    course_prerequsite = db.Column(db.Text())
    sem = db.Column(db.Integer , nullable = False)
    name = db.Column(db.String(30), db.ForeignKey('teachers.name'), nullable=False) #relation to the teacher table

    def __init__(self , id , course_name , course_length  , course_image_id, course_prerequsite , sem , name):
        self.id = id
        self.course_name = course_name
        self.course_length = course_length
        self.course_image_id = course_image_id
        self.course_prerequsite = course_prerequsite
        self.sem = sem
        self.name = name


#Posts Table
class Posts(db.Model):
    post_id = db.Column(db.Integer, primary_key= True)
    post_type = db.Column(db.Integer , nullable= False)
    post_file = db.Column(db.String(300) , nullable= False)
    post_date = db.Column(db.String(20))
    post_description = db.Column(db.Text())
    id = db.Column(db.Integer, db.ForeignKey('courses.id', ondelete ='cascade'), nullable= False) #relation to the courses table table

    def __init__(self, post_id , post_type , post_file , post_date , post_description, id):
        self.post_id = post_id
        self.post_type = post_type
        self.post_file = post_file
        self.post_date = post_date
        self.post_description = post_description
        self.id = id


#Users Table
class Users(db.Model):
    uid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30) , nullable = False)
    email = db.Column(db.String(30), nullable = False)
    password = db.Column(db.String(30) , nullable = False)

    def __init__(self , uid , username , email , password):
        self.uid = uid
        self.username = username
        self.email = email
        self.password = password


#Ratings Table
class Rating(db.Model):
    rating_id = db.Column(db.Integer, primary_key=True)
    rating_value = db.Column(db.Integer , nullable = False)
    rating_feedBack = db.Column(db.Text())
    uid = db.Column(db.Integer, db.ForeignKey('users.uid'), nullable= False) #Relation to users table
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False) #Relation to Courses table

    def __init__(self , rating_id,rating_value ,rating_feedBack, uid , course_id):
        self.rating_id = rating_id
        self.rating_value = rating_value
        self.rating_feedBack = rating_feedBack
        self.uid = uid
        self.course_id = course_id


#--------------Schema Creation-----------

#Creating Teachers schema for easy retrival
class TeachersSchema(ma.Schema):
    class Meta:
        fields = ('name' , 'password')

Teacher_Schema = TeachersSchema()
Teachers_Schema = TeachersSchema(many=True)
        

#Creating Courses schema for easy retrival
class CoursesSchema(ma.Schema):
    class Meta:
        fields = ('id' , 'course_name' , 'course_length' , 'course_image_id' , 'course_prerequsite' , 'sem' , 'name')

Course_Schema = CoursesSchema()
Courses_Schema = CoursesSchema(many=True)

#Creating Posts Schema for easy retrival
class PostsSchema(ma.Schema):
    class Meta:
        fields = ('post_id' , 'post_type' , 'post_file' , 'post_date' , 'post_description' , 'id')

Post_Schema = PostsSchema()
Posts_Schema = PostsSchema(many=True)


#Creating Users schema for easy retrival
class UsersSchema(ma.Schema):
    class Meta:
        fields = ('uid' , 'username' , 'email' , 'password')

User_Schema = UsersSchema()
Users_Schema = UsersSchema(many=True)


#Creating Rating schema for easy retrival
class RatingSchema(ma.Schema):
    class Meta:
        fields = ('rating_id', 'rating_value' ,'rating_feedBack', 'uid' ,'course_id')

Rating_Schema = RatingSchema()
Ratings_Schema = RatingSchema(many = True)


#Creating RatingRewarded schema for easy retrival
class RatingAwardedSchema(ma.Schema):
    class Meta:
        fields = ('course_name', 'rating_value' ,'rating_feedBack')

RatingAwarded_Schema = RatingAwardedSchema()
RatingAwardeds_Schema = RatingAwardedSchema(many = True)


#Creating RatingRewarded schema for easy retrival
class AvgRatingSchema(ma.Schema):
    class Meta:
        fields = ('id', 'AvgRating')

AvgRating_Schema = AvgRatingSchema()
AvgRatings_Schema = AvgRatingSchema(many = True)



#------------------Routing------------------


#-------------------GETTTING DATA-------------
#gets all the courses
@app.route('/get/Courses' , methods = ['GET'])
def getCourses():
   allCourses = Courses.query.all()
   results = Courses_Schema.dump(allCourses)
   return jsonify(results)


#gets the list of all teachers from the database
@app.route('/get/Teachers' , methods = ['GET'])
def getTeachers():
   allTeachers = Teachers.query.all()
   results = Teachers_Schema.dump(allTeachers)
   return jsonify(results)

#gets the list of all users from the database
@app.route('/get/Users' , methods = ['GET'])
def getUsers():
    allUsers = Users.query.all()
    results = Users_Schema.dump(allUsers)
    return jsonify(results)
    
#gets the courses as per the sem from the database
@app.route('/get/Course/<sem>' , methods = ['GET'])
def getPostDetails(sem):
    courses = Courses.query.filter(Courses.sem == sem)
    results = Courses_Schema.dump(courses)
    return jsonify(results)


#gets the courses as per the lecturer who teaches it in particular sem
@app.route('/get/CourseByLecturer/<name>/<sem>' , methods = ['GET'])
def getCoursesByLecturer(name , sem):
    courses = Courses.query.filter(Courses.name == name , Courses.sem == sem )
    results = Courses_Schema.dump(courses)
    return jsonify(results)



#gets the details of a particular teacher (used for login)
@app.route('/get/Teacher/<name>' , methods = ['GET'])
def getTeacherDetails(name):
    teacher = Teachers.query.get(name)
    results = Teacher_Schema.dump(teacher)
    return jsonify(results)


#gets the details of particular user (used for checking uniquness in sign in , and checking for correct credentials in sign up)
@app.route('/get/User/<username>' , methods = ['GET'])
def getUserDetails(username):
    user = Users.query.filter(Users.username == username).first()
    results = User_Schema.dump(user)
    return jsonify(results)


#gets the details of all the post in the post table
@app.route('/get/Post' , methods = ['GET'])
def getPosts():
    allPosts = Posts.query.all()
    results = Posts_Schema.dump(allPosts)
    return jsonify(results)

#gets the details of the posts from a particular course
@app.route('/get/Post/<id>' , methods = ['GET'])
def getCoursePost(id):
    Post = Posts.query.filter(Posts.id == id)
    results = Posts_Schema.dump(Post)
    return jsonify(results)



#gets all the rating present in the database
@app.route('/get/Ratings' , methods = ['GET'])
def getRatings():
    allRating = Rating.query.all()
    results = Ratings_Schema.dump(allRating)
    return jsonify(results)


#gets the average of rating from a particular course
@app.route('/get/AvgRating/<id>' , methods = ['GET'])
def AvgRating(id):
    rating = Rating.query.with_entities(db.func.avg(Rating.rating_value)).filter(Rating.course_id == id)
    results = rating[0][0]
    return ({"AvgRating" : results})


#gets the highest postid from the post table
@app.route('/get/HighestPostID' , methods = ['GET'])
def getHighestPostID():
    id = Posts.query.with_entities(db.func.max(Posts.post_id))
    result = id[0][0]
    return ({"Highest_id" : result})


#gets the highest courseid from the coursetable table in 3rd sem
@app.route('/get/HighestCourseID3rdSem' , methods = ['GET'])
def getHighestCourseID3():
    id = Courses.query.with_entities(db.func.max(Courses.id)).filter(Courses.sem == 3)
    result = id[0][0]
    return ({"Highest_id" : result})

#gets the highest courseid from the coursetable table in 4th sem
@app.route('/get/HighestCourseID4thSem' , methods = ['GET'])
def getHighestCourseID4():
    id = Courses.query.with_entities(db.func.max(Courses.id)).filter(Courses.sem == 4)
    result = id[0][0]
    return ({"Highest_id" : result})

#gets the highest UID of the last user who signed up from the users table 
@app.route('/get/HighestUID' , methods = ['GET'])
def getHighestUID():
    id = Users.query.with_entities(db.func.max(Users.uid))
    result = id[0][0]
    return ({"Highest_id" : result})

#gets the no of posts from the courses selected
@app.route('/get/postCount/<id>' , methods = ['GET'])
def getpostCount(id):
    id = Posts.query.filter(Posts.id == id).count()
    print(id)
    return ({"PostCount" : id})


#gets the highest ratingID from the rating table 
@app.route('/get/HighestRatingID' , methods = ['GET'])
def getHighestRatingID():
    id = Users.query.with_entities(db.func.max(Rating.rating_id))
    result = id[0][0]
    return ({"Highest_id" : result})

#gets the rating a user gave for a particular course
@app.route('/get/RatingofCourse/<uid>/<CourseID>' , methods = ['GET'])
def getRatingofCourse(uid , CourseID):
    ratings = Rating.query.filter(Rating.uid == uid , Rating.course_id == CourseID ).first()
    results = Rating_Schema.dump(ratings)
    return jsonify(results)


#gets the rating that student as awarded
@app.route('/get/RatingAwarded/<uid>' , methods = ['GET'])
def getRatingAwarded(uid):
    ratings = db.session.query(Courses.course_name , Rating.rating_value , Rating.rating_feedBack).filter(Courses.id == Rating.course_id).filter(Rating.uid == uid).all()
    results = RatingAwardeds_Schema.dump(ratings)
    print(results)
    return jsonify(results)

#gets the rating that teacher is rewarded
@app.route('/get/RatingRewarded/<name>' , methods = ['GET'])
def getRatingReAwarded(name):
    ratings = db.session.query(Courses.course_name , Rating.rating_value , Rating.rating_feedBack).filter(Courses.id == Rating.course_id).filter(Courses.name == name).all()
    results = RatingAwardeds_Schema.dump(ratings)
    return jsonify(results)


#gets the avg of rating of all courses rating exits
@app.route('/get/AvgRating/' , methods = ['GET'])
def getAvgRating():
    ratings = db.session.query(Courses.id , db.func.round(db.func.avg(Rating.rating_value),1).label('AvgRating')).filter(Courses.id == Rating.course_id).group_by(Courses.id)
    results = AvgRatings_Schema.dump(ratings)
    return jsonify(results)







#------------------UPDATING DATA--------------------
#updates the course as per the id provided , edits the database
@app.route('/update/Course/<id>' , methods = ['PUT'])
def updateCourse(id):
    post = Courses.query.get(id)
    course_name = request.json['course_name']
    course_length = request.json['course_length']
    course_image_id = request.json['course_image_id']
    course_prerequsite = request.json['course_prerequsite']
    Sem = request.json['sem']
    Name = request.json['name']

    post.course_name = course_name
    post.course_length = course_length
    post.course_image_id = course_image_id
    post.course_prerequsite = course_prerequsite
    post.Sem = Sem
    post.Name = Name

    db.session.commit()
    return Course_Schema.jsonify(post)


@app.route('/update/Post/<id>' , methods = ['PUT'])
def UpdatePost(id):
    post = Posts.query.get(id)
    post_type = request.json['post_type']
    post_file = request.json['post_file']
    post_date = request.json['post_date']
    post_description = request.json['post_description']
    id = request.json['id']


    post.post_type = post_type
    post.post_file = post_file
    post.post_date = post_date
    post.post_description = post_description
    post.id = id

    db.session.commit()
    return Post_Schema.jsonify(post)


@app.route('/update/user/<uid>' , methods = ['PUT'])
def ChangePasswordUser(uid):
    user = Users.query.get(uid)
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']

    user.username = username
    user.email = email
    user.password = password

    db.session.commit()
    return Post_Schema.jsonify(user)


@app.route('/update/teacher/<name>' , methods = ['PUT'])
def ChangePasswordTeacher(name):
    teacher = Teachers.query.get(name)
    password = request.json['password']

    teacher.password = password
   
    db.session.commit()
    return Post_Schema.jsonify(teacher)








#---------------ADDING NEW DATA----------------
#adds a new course into the database
@app.route('/add/Course' , methods = ['POST'])
def addCourses():
    id = request.json['id']
    course_name = request.json['course_name']
    course_length = request.json['course_length']
    course_image_id = request.json['course_image_id']
    course_prerequsite = request.json['course_prerequsite']
    Sem = request.json['sem']
    Name = request.json['name']
    course = Courses(id,course_name ,course_length ,course_image_id ,course_prerequsite, Sem,Name)
    db.session.add(course)
    db.session.commit()
    return Course_Schema.jsonify(course)


#adds a new teacher to the database
@app.route('/add/Teacher' , methods = ['POST'])
def addTeacher():
    Name = request.json['name']
    Password = request.json['password']
    teacher = Teachers(Name , Password)
    db.session.add(teacher)
    db.session.commit()
    return Teacher_Schema.jsonify(teacher)

    

#adds a new users into the database
@app.route('/add/User' , methods = ['POST'])
def addUser():
    uid = request.json['uid']
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']
    user = Users(uid , username , email , password)
    db.session.add(user)
    db.session.commit()
    return User_Schema.jsonify(user)


#adds a new post into the database
@app.route('/add/Post' , methods = ['POST'])
def addPost():
    post_id = request.json['post_id']
    post_type = request.json['post_type']
    post_file = request.json['post_file']

    if post_type == 2:
        post_file = ChangeLink(post_file)

    post_date = request.json['post_date']
    post_description = request.json['post_description']
    id = request.json['id']
    post = Posts(post_id , post_type , post_file , post_date , post_description , id)
    db.session.add(post)
    db.session.commit()
    return Post_Schema.jsonify(post)


#Adds a new rating into the database
@app.route('/add/Rating' , methods = ['POST'])
def addRating():
    rating_id = request.json['rating_id']
    rating_value = request.json['rating_value']
    rating_feedBack = request.json['rating_feedBack']
    uid = request.json['uid']
    course_id = request.json['course_id']
    rating = Rating(rating_id , rating_value ,rating_feedBack, uid , course_id)
    db.session.add(rating)
    db.session.commit()
    return Rating_Schema.jsonify(rating)





#---------------DELETING DATA----------------
#deletes a Teacher record from the database
@app.route('/delete/Teacher/<Name>' , methods = ['DELETE'])
def Teacherdelete(name):
    teacher = Teachers.query.get(name)
    db.session.delete(teacher)
    db.session.commit()

    return Course_Schema.jsonify(teacher)


#deletes a course record from the database
@app.route('/delete/Course/<id>' , methods = ['DELETE'])
def coursedelete(id):
    post = Courses.query.get(id)
    db.session.delete(post)
    db.session.commit()

    return Course_Schema.jsonify(post)
    


#deletes a post record from the database based from its post id
@app.route('/delete/Post/<id>' , methods = ['DELETE'])
def PostDelete(id):
    post = Posts.query.get(id)
    db.session.delete(post)
    db.session.commit()

    return Post_Schema.jsonify(post)

#deletes all rating from the course from the database based 
@app.route('/delete/CourseRatings/<id>' , methods = ['DELETE'])
def CourseRating(id):
    rating = Rating.__table__.delete().where(Rating.course_id == id)
 
    db.session.execute(rating)
    db.session.commit()

    return Rating_Schema.jsonify(rating)









#------------HELPER FUNCTIONS-------------
#converts the normal youtube link to an embedded link
def ChangeLink(publicLink):
    linkSplit = publicLink.split('watch?v=')
    embdedLink = 'embed/'.join(linkSplit)
    embdedLink = embdedLink + '?rel=0&autoplay=1&modestbranding=1'
    return embdedLink


if __name__ == "__main__":
    app.run(debug=True)
