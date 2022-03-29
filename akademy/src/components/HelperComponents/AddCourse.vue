<template>
  <section>
    <div class="backgroundBlur"></div>
    <!-- THIS IS USED TO GENERATE BACK GROUND BLUR EFFECT -->
    <base-dialog v-if="true" title="Invalid Input">
      <template #header>
        <h3 class="PopUpTitle">
          <strong>ERROR </strong>
        </h3>
      </template>
      <template #default>
        <p class="PopUpMessage">PLEASE FILL ALL THE DETAILS</p>
        <!-- <p>Please Enter Valid Input</p> -->
      </template>
      <template #actions>
        <button @click="confirmError" class="dialogButton">OK</button>
      </template>
    </base-dialog>
    <form
      @submit.prevent="submitForm"
      :class="inputIsInValid ? 'hideForm' : 'displayForm'"
    >
      <!---------------FORM----------->
      <div class="formHeader">
        <!-- HEADRER OF THE FORM -->
        <h1 style="margin-left: 30%">
          {{ this.$store.state.isEdit ? 'EDIT' : 'ENTER' }} Course Details
        </h1>
      </div>

      <div class="form-control">
        <label for="courseTitle">Course Tile</label>
        <input
          id="courseTitle"
          name="courseTitle"
          type="text"
          v-model="$store.state.courseTitle"
          placeholder="ex: Data Structures And Algorithm"
        />
      </div>

      <div class="form-control">
        <label for="courseBannerUrl">Course Image Url</label>
        <input
          id="courseBannerUrl"
          name="courseBannerUrl"
          type="text"
          v-model="$store.state.imageUrl"
          placeholder="ex: https://image.com"
        />
      </div>
      <div class="form-control">
        <label for="courseLength">Course Length</label>
        <input
          id="courseLength"
          name="courseLength"
          type="text"
          v-model="$store.state.courseLength"
          placeholder="number of hrs (ex: 40)"
        />
      </div>
      <div class="form-control">
        <label for="prerequisite">Prerequiste</label>
        <input
          id="prerequisite"
          name="prerequisite"
          type="text"
          v-model="$store.state.prerequisite"
          placeholder="ex: Personal Interest"
        />
      </div>
      <!-- SUBMIT AND UPDATE BUTTON TOGGLES BASED ON EDIT MODE -->
      <button class="submit" type="submit">
        {{ this.$store.state.isEdit ? 'UPDATE' : 'SUBMIT' }}
      </button>
      <!-- CLOSE BUTTON -->
      <button class="close" type="button" @click="close">
        <i class="fas fa-times"></i> CLOSE
      </button>
    </form>
  </section>
</template>

<script>
import BaseDialogue from '../ui/BaseDialouge.vue';
export default {
  components: {
    'base-dialog': BaseDialogue,
  },
  data() {
    return {
      inputIsInValid: false,
      isEdit: -1,
    };
  },
  methods: {
    close() {
      this.$store.state.editCourseIndex = 0;
      this.$store.state.sem = 0;
      this.$store.state.isEdit = false; //CLOSE FUNCTION RESETING EVERYTHING TO AVOID
      this.clearInputCache();
      this.$store.commit('SetFormActivity', {
        value: false,
      });
    },
    //validation return inside a function
    inputValidation() {
      if (
        this.$store.state.courseTitle === '' ||
        this.$store.state.imageUrl === '' ||
        this.$store.state.courseLength === '' ||
        this.$store.state.prerequisite === ''
      ) {
        return true;
      } else return false;
    },
    //resets the the values
    clearInputCache() {
      this.$store.state.instructorName = '';
      this.$store.state.courseTitle = '';
      this.$store.state.imageUrl = '';
      this.$store.state.courseLength = '';
      this.$store.state.prerequisite = '';
    },
    submitForm() {
      //if we are editing the course
      if (this.$store.state.isEdit) {
        if (this.inputValidation()) {
          this.inputIsInValid = true;
        } else {
          this.EditCourseFromDatabase();
          this.close();
        }
      }
      //we are adding a new course
      else {
        if (this.inputValidation()) {
          this.inputIsInValid = true;
        } else {
          this.AddCourseToDataBase();
          this.close();
        }
      }
    },

    //Shows the pop up with the arguments passed in the function
    SetPopUp(popUpTitle, popUpMessage) {
      this.popUpTitle = popUpTitle;
      this.popUpMessage = popUpMessage;
    },

    //closing the pop up message
    confirmError() {
      this.inputIsInValid = false;
    },

    AddCourseToDataBase() {
      //calculate the sem from the courseid
      let Currentsem = this.$store.state.Highest_Id;
      let RemainSem = Currentsem % 1000;
      Currentsem = (Currentsem - RemainSem) / 1000;
      let Highest_Id = this.$store.state.Highest_Id + 1;

      //adds course into the database
      fetch('http://localhost:5000/add/Course', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          id: Highest_Id,
          course_name: this.$store.state.courseTitle,
          course_length: this.$store.state.courseLength,
          course_image_id: this.$store.state.imageUrl,
          course_prerequsite: this.$store.state.prerequisite,
          sem: Currentsem,
          name: this.$store.state.CurrentUser,
        }),
      })
        .then((resp) => resp.json())
        .then(() => {
          this.close();
          this.isEdit = 0;
          this.$emit('refresh-courses', this.isEdit);
        })
        .catch((error) => {
          console.log(error);
        });
    },

    //Edits the course in the database
    EditCourseFromDatabase() {
      let Currentsem = this.$store.state.Highest_Id;
      let RemainSem = Currentsem % 1000;
      Currentsem = (Currentsem - RemainSem) / 1000;

      fetch(
        `http://localhost:5000/update/Course/${this.$store.state.CourseID}`,
        {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            id: this.$store.state.CourseID,
            course_name: this.$store.state.courseTitle,
            course_length: this.$store.state.courseLength,
            course_image_id: this.$store.state.imageUrl,
            course_prerequsite: this.$store.state.prerequisite,
            sem: Currentsem,
            name: this.$store.state.CurrentUser,
          }),
        }
      )
        .then((resp) => resp.json())
        .then(() => {
          this.close();
          this.isEdit = 1;
          this.$emit('refresh-courses', this.isEdit);
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },
};
</script>

<style scoped>
.formHeader {
  background-color: crimson;
  position: relative;
  bottom: 80px;
  right: 80px;
  width: 150%;
  padding: 20px 0 10px 0;
}
div.backgroundBlur {
  position: fixed;
  top: 0;
  left: 0;
  height: 100vh;
  width: 100%;
  background-color: rgba(0, 0, 0, 0.75);
  z-index: 10;
}
form {
  margin: 2rem auto;
  max-width: 40rem;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(255, 255, 255, 0.26);
  padding: 3rem 3rem 2rem 3rem;
  background-color: #ffffff;
  position: fixed;
  top: 3vh;
  width: 80%;
  z-index: 100;
  overflow: hidden;
}
.form-control {
  margin: 0.5rem 0;
}
label {
  font-weight: bold;
  font-size: 24px;
}
input {
  display: block;
  width: 100%;
  font: inherit;
  margin-top: 0.5rem;
  padding: 10px;
}
button.submit {
  margin-top: 5px;
  padding: 10px 30px;
  border-radius: 5px;
  background-color: #dc143c;
  border: 1px solid #000000;
  color: #f8f8ff;
}
button.close {
  position: relative;
  left: 60%;
  padding: 10px 30px;
  border-radius: 5px;
  background-color: #dc143c;
  border: 1px solid #000000;
  color: #f8f8ff;
}
.dialogButton {
  font-family: 'Poppins', sans-serif;
  font-size: 20px;
  text-align: center;
  background-color: #000000;
  color: white;
  padding: 1rem;
  cursor: pointer;
  border-radius: 13px;
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
.hideForm {
  visibility: hidden;
}
.displayForm {
  visibility: visible;
}
</style>
