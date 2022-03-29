<template>
  <the-header></the-header>
  <!-- gets the data from the flask server in the form of a json 
  and is v-for upon to render the cards as per the id -->
  <section>
    <div
      v-if="this.semData.length != 0 && this.$store.state.isTeacher"
      style="font-size: 32px; font-style: sans-serif; color: #f8f8ff"
    >
      <strong>Courses You Teach</strong>
    </div>
    <!-- BUTTON TO CREATE A COURSE -->
    <button
      class="createCourseButton"
      v-if="this.$store.state.isTeacher"
      @click="activateForm()"
    >
      <i class="fas fa-plus-circle"> Create Course</i>
    </button>

    <div v-if="this.semData.length == 0">
      <img class="noCourseFound" src="@/assets/NODATA.png" alt="" />

      <p
        style="
          margin-left: 10%;
          font-size: 32px;
          font-style: sans-serif;
          color: #f8f8ff;
        "
      >
        You dont have any courses in this sem..
      </p>
    </div>

    <add-course
      v-if="this.$store.state.isFormActive"
      @refresh-courses="ShowPopandGetCourse"
    ></add-course>

    <ul
      v-for="course in semData"
      :key="course.id"
      :id="course.id"
      :title="course.course_name"
      :image="course.course_image_id"
      :prerequisite="course.course_prerequsite"
    >
      <!-- BUTTON TO EDIT THE COURSE -->
      <button
        class="modButton1"
        v-if="this.$store.state.isTeacher"
        @click="
          editCourse(
            course.id,
            course.course_name,
            course.course_length,
            course.course_image_id,
            course.course_prerequsite
          )
        "
      >
        Edit
      </button>
      <!-- BUTTON TO DELETE THE COURSE -->
      <button
        class="modButton2"
        v-if="this.$store.state.isTeacher"
        @click="removeCourse(course.id)"
      >
        Delete
      </button>

      <div class="course__data">
        <div class="course__image">
          <img :src="course.course_image_id" :alt="title" />
        </div>
        <div class="course__text">
          <h3>{{ course.course_name }}</h3>
          <div class="Instructor">
            <!-- this gives the badge look from the badge component  -->
            <base-badge
              mode="highlight"
              :no-margin-left="true"
              class="Instructor"
            >
              <h4>
                {{ course.name }}
              </h4>
            </base-badge>
            <!-- Rating of the course is put in this badge look -->
            <base-badge
              mode="highlight"
              :no-margin-left="true"
              class="Instructor"
            >
              <h4>
                {{
                  RatingData[course.id] == undefined
                    ? 'No Rating'
                    : RatingData[course.id]
                }}&nbsp; <i class="fas fa-star"></i>
              </h4>
            </base-badge>
          </div>
          <p>
            <strong>Course Length :</strong>
            {{ course.course_length }} hrs
          </p>
          <p>
            <strong>Course Prerequiste</strong> :
            {{ course.course_prerequsite }}
          </p>
        </div>
      </div>
      <div class="course__actions">
        <button
          @click="
            SetRouteDestination(course.id, course.course_name, course.name)
          "
        >
          Go to Course
        </button>
      </div>
    </ul>
  </section>

  <!-- POP UP MESSAGE -->
  <base-dialog v-if="this.inputIsInValid" title="Invalid Input">
    <template #header>
      <h3 class="PopUpTitle">
        <strong>{{ this.popUpTitle }}</strong>
      </h3>
    </template>
    <template #default>
      <p class="PopUpMessage">{{ this.popUpMessage }}</p>
      <!-- <p>Please Enter Valid Input</p> -->
    </template>
    <template #actions>
      <button @click="confirmError" class="dialogButton">OK</button>
    </template>
  </base-dialog>
</template>

<script>
import AddCourse from '../components/HelperComponents/AddCourse.vue';
import TheHeader from '../components/nav/TheHeader.vue';
import BaseDialog from '../components/ui/BaseDialouge.vue';

export default {
  components: {
    'add-course': AddCourse, //ADD COURSE COMPONENT
    TheHeader,
    BaseDialog,
  },
  data() {
    return {
      semData: {},
      avgRatingData: {},
      RatingData: {},
      inputIsInValid: false,
      popUpTitle: '',
      popUpMessage: '',
    };
  },

  methods: {
    // the data of the courses from the database is acquired and passed to for v-for
    getCourses() {
      fetch('http://localhost:5000/get/Course/4', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      })
        .then((resp) => resp.json())
        .then((data) => {
          this.semData = data;
          console.log(this.semData);
        })
        .catch((error) => {
          console.log(error);
        });
    },

    //Gets the courses the logged in teacher teaches
    getCoursesTeacher() {
      fetch(
        `http://localhost:5000/get/CourseByLecturer/${this.$store.state.CurrentUser}/4`,
        {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          },
        }
      )
        .then((resp) => resp.json())
        .then((data) => {
          this.semData = data;
          console.log(this.semData);
        })
        .catch((error) => {
          console.log(error);
        });
    },

    //Gets the avg rating of all the courses
    GetAvgRating() {
      fetch('http://localhost:5000/get/AvgRating/', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      })
        .then((resp) => resp.json())
        .then((data) => {
          this.avgRatingData = data;
          console.log(this.avgRatingData);
          this.getvalues();
        })
        .catch((error) => {
          console.log(error);
        });
    },

    //makes the values of the avg rating form the database more accesible for the v-for
    getvalues() {
      for (let i = 0; i < Object.keys(this.avgRatingData).length; i++) {
        this.RatingData[this.avgRatingData[i].id] =
          this.avgRatingData[i].AvgRating;
      }

      console.log(this.RatingData);
    },

    //showes messages and refreshes data
    ShowPopandGetCourse(edit) {
      if (edit === 1) {
        this.ShowUpdatePopUp();
      } else if (edit === 0) {
        this.ShowAddedPopUp();
      }

      this.getCoursesTeacher();
    },

    //FUNCTION WHICH TOGGLE OPENS THE FORM
    activateForm() {
      this.$store.commit('SetFormActivity', {
        value: true,
      });

      //gets the highest course no , which can be incremented and addded as the new course id
      fetch('http://localhost:5000/get/HighestCourseID4thSem', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      })
        .then((resp) => resp.json())
        .then((data) => {
          this.$store.commit('setHighestID', {
            value: data.Highest_id,
          });

          console.log(this.$store.state.Highest_Id);
        })
        .catch((error) => {
          console.log(error);
        });
    },

    //FUNCTION WHICH DELETES THE COURSE BASED ON THE INDEX
    removeCourse(courseID) {
      this.GetPostCount(courseID);
    },

    //Stores the values of the course which the user pressses edit on vuex and open the form
    editCourse(
      id,
      course_name,
      course_length,
      course_image_id,
      course_prerequsite
    ) {
      //stores the selected course values in vuex
      this.$store.commit('setCourseEditRelatedInfo', {
        id: id,
        courseName: course_name,
        courseLength: course_length,
        courseImage: course_image_id,
        coursePrerequisite: course_prerequsite,
      });

      //Opens up the form
      this.$store.commit('SetFormActivity', {
        value: true,
      });

      //Notifies that the form is for edit
      this.$store.commit('setCourseIsEdit', {
        value: true,
      });
    },

    //Sets link of the route and stores some important values in vuex
    SetRouteDestination(courseId, courseName, courseInstructor) {
      this.$store.commit('SetCourseRelatedInfo', {
        CourseID: courseId,
        CourseName: courseName,
        Instructor: courseInstructor,
        inCourse: true,
      });
      this.$router.push('/posts/' + courseId);
    },

    //Gets the number of posts that the selected course has
    GetPostCount(CourseID) {
      fetch(`http://localhost:5000/get/postCount/${CourseID}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      })
        .then((resp) => resp.json())
        .then((data) => {
          if (data.PostCount != 0) {
            this.ShowPopUp(
              'ERROR',
              'Please Delete the posts in the course to be able to delete the course.'
            );
          } else {
            console.log('courseID');
            this.DeleteRatingInCourse(CourseID);
          }
        })
        .catch((error) => {
          console.log(error);
        });
    },

    //Deletes the rating from the course
    DeleteRatingInCourse(courseID) {
      fetch(`http://localhost:5000/delete/CourseRatings/${courseID}`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
        },
      })
        .then(() => {
          alert('Deleting course ...... Please wait');
          this.DeleteCourseFromDataBase(courseID);
        })
        .catch((error) => {
          console.log(error);
        });
    },

    //Deletes the course from the database
    DeleteCourseFromDataBase(courseID) {
      fetch(`http://localhost:5000/delete/Course/${courseID}`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
        },
      })
        .then(() => {
          this.ShowPopUp('Course Deleted', 'Successfully Deleted The course!');
          this.getCoursesTeacher();
        })
        .catch((error) => {
          console.log(error);
        });
    },

    //Shows the pop up with the arguments passed in the function
    ShowPopUp(popUpTitle, popUpMessage) {
      this.popUpTitle = popUpTitle;
      this.popUpMessage = popUpMessage;
      this.inputIsInValid = true;
    },

    //shows pop up that course is updated
    ShowUpdatePopUp() {
      this.popUpTitle = 'Course Updated';
      this.popUpMessage = 'Course has been succesfully updated!';
      this.inputIsInValid = true;
    },

    //shows pop up that course is Added
    ShowAddedPopUp() {
      this.popUpTitle = 'Course Added';
      this.popUpMessage = 'Your Course has been succesfully added!';
      this.inputIsInValid = true;
    },

    //closes the popup
    confirmError() {
      this.inputIsInValid = false;
    },
  },

  // the created function is called when the component is rendered on screen
  //and thats when we query the database for data to render
  created() {
    if (this.$store.state.isTeacher) {
      this.getCoursesTeacher();
    } else {
      this.getCourses();
    }

    this.GetAvgRating();
    //sets the navbar to normal
    this.$store.commit('IsInCourse', { value: false });
  },
};
</script>

<style scoped>
section {
  margin: 2rem auto;
  max-width: 40rem;
}

ul {
  list-style: none;
  margin: 2rem auto;
  padding: 0;
  max-width: 40rem;
  margin: 1.5rem auto;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.26);
  background-color: #dc143c;
  border-radius: 20px;
  padding: 1rem;
  border-radius: 20px;
  color: #f8f8ff;
}

.course__data {
  display: flex;
}

.course__image {
  margin-right: 1rem;
}

.course__image img {
  height: 10rem;
  width: 10rem;
  object-fit: cover;
}

.course__text h3 {
  margin: 0 0 0.5rem 0;
}

.course__text h4 {
  margin: 0;
}

.course__actions {
  text-align: center;
  color: white;
}

.link_style {
  text-decoration: none;
  color: white;
}

.Instructor {
  margin-bottom: 2.2rem;
}

button {
  font: inherit;
  cursor: pointer;
  background-color: #171717;
  color: white;
  border: 1px solid #f8f8ff;
  padding: 0.5rem 1.5rem;
  border-radius: 30px;
}

button:hover,
button:active {
  background-color: #000000;
  border-color: #ffffff;
}
button.createCourseButton {
  background-color: #dc143c;
  color: #f8f8ff;
  font-size: 20px;
  font-family: serif;
  position: relative;
  left: 81%;
  top: 100px;
  position: fixed;
  padding: 1rem 3rem;
  clear: both;
  display: inline-block;
  overflow: hidden;
  white-space: nowrap;
}
.modButton1 {
  position: relative;
  left: 60%;
  padding: 10px 40px;
}
.modButton2 {
  position: relative;
  left: 65%;
  background-color: #ffffff;
  color: crimson;
  border: 1px solid crimson;
  padding: 10px 30px;
}
.noCourseFound {
  margin-left: 0%;
}

.dialogButton {
  font-family: 'Poppins', sans-serif;
  font-size: 20px;
  text-align: center;
  background-color: #171717;
  color: #f8f8ff;
  padding: 1rem;
  cursor: pointer;
  border-radius: 13px;
  padding: 10px 50px;
}
.PopUpTitle {
  font-family: 'Poppins', sans-serif;
  font-size: 40px;
  text-align: center;
}
.PopUpMessage {
  font-family: 'Poppins', sans-serif;
  font-size: 25px;
  margin-top: 25px;
  text-align: center;
}
</style>
