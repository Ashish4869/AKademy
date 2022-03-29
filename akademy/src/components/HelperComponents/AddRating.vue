<template>
  <section>
    <div class="backgroundBlur"></div>
    <!-- THIS IS USED TO GENERATE BACK GROUND BLUR EFFECT -->
    <base-dialog v-if="inputIsInValid" title="Invalid Input">
      <template #header>
        <h3 class="PopUpTitle">
          <strong>ERROR </strong>
        </h3>
      </template>
      <template #default>
        <p class="PopUpMessage">PLEASE FILL ALL THE FIELDS</p>
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
      <!---------------FORM-------------------->
      <div class="formHeader">
        <!-- HEADRER OF THE FORM -->
        <h1 style="margin-left: 30%">RATING</h1>
      </div>

      <!------------- RATING  -------------->
      <div class="form-control">
        <label>Give Your Rating</label>
        <ul>
          <li
            :class="RatingStatus[1] ? 'active' : 'notActive'"
            @mouseover="showRating(1)"
          >
            <label for="rating_1"><i class="fas fa-star"></i></label
            ><input type="radio" name="ratings" id="rating_1" value="1" />
          </li>
          <li
            :class="RatingStatus[2] ? 'active' : 'notActive'"
            @mouseover="showRating(2)"
          >
            <label for="rating_2"><i class="fas fa-star"></i></label
            ><input type="radio" name="ratings" id="rating_2" value="2" />
          </li>
          <li
            :class="RatingStatus[3] ? 'active' : 'notActive'"
            @mouseover="showRating(3)"
          >
            <label for="rating_3"><i class="fas fa-star"></i></label
            ><input type="radio" name="ratings" id="rating_3" value="3" />
          </li>
          <li
            :class="RatingStatus[4] ? 'active' : 'notActive'"
            @mouseover="showRating(4)"
          >
            <label for="rating_4"><i class="fas fa-star"></i></label
            ><input type="radio" name="ratings" id="rating_4" value="4" />
          </li>
          <li
            :class="RatingStatus[5] ? 'active' : 'notActive'"
            @mouseover="showRating(5)"
          >
            <label for="rating_5"><i class="fas fa-star"></i></label
            ><input type="radio" name="ratings" id="rating_5" value="5" />
          </li>
        </ul>
      </div>

      <div class="form-control">
        <label for="Feedback">Feedback</label>
        <textarea
          rows="5"
          cols="71"
          name="Feedback"
          placeholder=" PLease give your constructive feedback here..."
          v-model="this.RatingFeedBack"
        >
        </textarea>
      </div>

      <!-- SUBMIT AND UPDATE BUTTON TOGGLES BASED ON EDIT MODE -->
      <button class="submit" type="submit">SUBMIT</button>
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
      RatingStatus: { 1: false, 2: false, 3: false, 4: false, 5: false },
      RatingFeedBack: '',
      value: 0,
    };
  },

  methods: {
    confirmError() {
      this.inputIsInValid = false;
    },

    close() {
      this.RatingFeedBack = '';
      for (let i = 1; i <= 5; i++) this.RatingStatus[i] = false;

      this.$store.commit('SetRatingFormActivity', {
        value: false,
      });
    },
    //validation return inside a function
    inputValidation() {
      if (this.RatingStatus[1] == 0 || this.RatingFeedBack == '') {
        return true;
      } else return false;
    },

    submitForm() {
      if (this.inputValidation()) {
        this.inputIsInValid = true;
      } else {
        //saving the rating value before the user can change it
        let rating = 0;
        for (let i = 1; i <= 5; i++)
          if (this.RatingStatus[i] == true) {
            rating++;
          }
        this.CheckAddRatingToDatabase(rating);
      }
    },

    setPrevOn(value) {
      for (let i = 1; i <= value; i++) this.RatingStatus[i] = true;
    },

    setNextOff(value) {
      for (let i = value + 1; i < 6; i++) this.RatingStatus[i] = false;
    },

    showRating(value) {
      this.setPrevOn(value);
      this.setNextOff(value);
    },

    CheckAddRatingToDatabase(rating) {
      //Gets whether the rating exits or not
      fetch(
        `http://localhost:5000/get/RatingofCourse/${this.$store.state.CurrentUserUID}/${this.$store.state.SelectedCourseID}`,
        {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          },
        }
      )
        .then((resp) => resp.json())
        .then((data) => {
          if (Object.keys(data).length != 0) {
            this.value = 0;
            this.$emit('refresh-rating', this.value);
            this.close();
          } else {
            this.AddRatingToDatabase(rating);
          }
        })
        .catch((error) => {
          console.log(error);
        });
    },

    AddRatingToDatabase(rating) {
      let ratingID = this.$store.state.Highest_Id + 1;

      //Adds rating to database
      fetch('http://localhost:5000/add/Rating', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          rating_id: ratingID,
          rating_value: rating,
          rating_feedBack: this.RatingFeedBack,
          uid: this.$store.state.CurrentUserUID,
          course_id: this.$store.state.SelectedCourseID,
        }),
      })
        .then((resp) => resp.json())
        .then(() => {
          this.value = 1;
          this.$emit('refresh-rating', this.value);
          this.close();
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
  right: 50px;
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
  margin-top: 100px;
  margin-left: 460px;
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
  margin: 1rem 0;
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

/* CSS for RATING STAR */
input[type='radio'] {
  display: none;
}

ul {
  padding: 0;
  margin: 0px 0px 0px 100px;
}

ul li {
  list-style-type: none;
  display: inline-block;
  margin: 10px;
  color: grey;
  font-size: 50px !important;
}

ul li:hover {
  color: yellow;
}

.active {
  color: yellow;
}

.notActive {
  color: grey;
}
</style>
