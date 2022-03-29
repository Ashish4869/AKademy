<template>
  <the-header></the-header>

  <!-- Change Password Component -->
  <change-password
    v-if="this.$store.state.isFormActive"
    @showError="SetPopUp"
  ></change-password>

  <!-- Profile Heading -->
  <div class="ProfileHeading">
    <h1><strong>Your Profile</strong></h1>
  </div>

  <!-- Profile Details Card -->
  <div class="ProfileDetailsCard">
    <div class="ParentProFileFlex">
      <div
        class="ProfileDetailLabels"
        :style="{ padding: this.$store.state.isTeacher ? '40px' : '0px' }"
      >
        <h2>Name :</h2>
        <h2 v-if="this.$store.state.isTeacher == false">Email :</h2>
        <h2>Password :</h2>
      </div>
      <div
        class="ProfileDetailValues"
        :style="{ padding: this.$store.state.isTeacher ? '40px' : '0px' }"
      >
        <h2>
          {{
            this.$store.state.isTeacher
              ? this.UserInfo.name
              : this.UserInfo.username
          }}
        </h2>
        <h2 v-if="this.$store.state.isTeacher == false">
          {{ this.UserInfo.email }}
        </h2>
        <h2>{{ this.showPassword ? this.UserInfo.password : '**********' }}</h2>
      </div>
    </div>

    <!-- Change Password and show passowrd buttons -->
    <div class="ButtonsFlex">
      <button class="ChangePassword" @click="ShowForm">Change Password</button>
      <h2 class="ShowPassword" @click="PasswordHideShow">
        {{ this.showPassword ? 'Hide Password' : 'Show Password' }} &nbsp;
        <i v-if="this.showPassword == false" class="fas fa-eye"></i>
        <i v-if="this.showPassword == true" class="far fa-eye-slash"></i>
      </h2>
    </div>
  </div>

  <!-- Shows no rating image if no rating could be found -->
  <div class="Rating" v-if="this.ratingData.length == 0">
    <img class="NoRatingFound" src="@/assets/NODATA.png" alt="" />

    <p
      style="
        margin-left: 40%;
        font-size: 32px;
        font-style: sans-serif;
        color: #f8f8ff;
      "
    >
      No Ratings to display...
    </p>
  </div>

  <!-- Rating Heading -->
  <div v-if="this.ratingData.length != 0" class="RatingHeading">
    <h1>
      <strong
        >Ratings you have
        {{ this.$store.state.isTeacher ? 'Received' : 'Given' }}</strong
      >
    </h1>
  </div>

  <!-- Rating Table Flexbox -->
  <div v-if="this.ratingData.length != 0" class="RatingTableParentFlexBox">
    <div class="RatingTableHeader">
      <h2>Course Name</h2>
      <h2>Rating</h2>
      <h2>Feedback</h2>
    </div>

    <div class="RatingTableValues">
      <ul v-for="(rating, index) in ratingData" :key="index">
        <li class="TableValues">
          <h5>{{ rating.course_name }}</h5>
          <h5>{{ rating.rating_value }} &nbsp; <i class="fas fa-star"></i></h5>
          <h5>{{ rating.rating_feedBack }}</h5>
        </li>
      </ul>
    </div>
  </div>

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
import TheHeader from '../components/nav/TheHeader.vue';
import BaseDialog from '../components/ui/BaseDialouge.vue';
import ChangePassword from '../components/HelperComponents/ChangePassword.vue';

export default {
  components: {
    TheHeader,
    BaseDialog,
    ChangePassword,
  },
  data() {
    return {
      UserInfo: {},
      showPassword: false,

      inputIsInValid: false,
      popUpTitle: '',
      popUpMessage: '',

      ratingData: {},
    };
  },

  methods: {
    //Gets the data of the user is logged in
    getUserLoggedIn() {
      //if the user is a teacher
      if (this.$store.state.isTeacher) {
        fetch(
          `http://localhost:5000//get/Teacher/${this.$store.state.CurrentUser}`,
          {
            method: 'GET',
            headers: {
              'Content-Type': 'application/json',
            },
          }
        )
          .then((resp) => resp.json())
          .then((data) => {
            this.UserInfo = data;
            console.log(this.UserInfo);
          })
          .catch((error) => {
            console.log(error);
          });
      } else {
        //if the user is student
        fetch(
          `http://localhost:5000/get/User/${this.$store.state.CurrentUser}`,
          {
            method: 'GET',
            headers: {
              'Content-Type': 'application/json',
            },
          }
        )
          .then((resp) => resp.json())
          .then((data) => {
            this.UserInfo = data;
            console.log(this.UserInfo);
          })
          .catch((error) => {
            console.log(error);
          });
      }
    },

    //Gets the ratings related to the user
    GetRatings() {
      //if the user is teacher
      if (this.$store.state.isTeacher) {
        fetch(
          `http://localhost:5000/get/RatingRewarded/${this.$store.state.CurrentUser}`,
          {
            method: 'GET',
            headers: {
              'Content-Type': 'application/json',
            },
          }
        )
          .then((resp) => resp.json())
          .then((data) => {
            this.ratingData = data;
            console.log(this.ratingData);
          })
          .catch((error) => {
            console.log(error);
          });
      } else {
        //if the user is a student
        fetch(
          `http://localhost:5000/get/RatingAwarded/${this.$store.state.CurrentUserUID}`,
          {
            method: 'GET',
            headers: {
              'Content-Type': 'application/json',
            },
          }
        )
          .then((resp) => resp.json())
          .then((data) => {
            this.ratingData = data;
            console.log(this.ratingData);
          })
          .catch((error) => {
            console.log(error);
          });
      }
    },

    //Hides and Shows the password
    PasswordHideShow() {
      this.showPassword = !this.showPassword;
    },

    //closes the popup
    confirmError() {
      this.inputIsInValid = false;
    },

    //Shows the popup
    ShowForm() {
      this.$store.commit('SetFormActivity', {
        value: true,
      });

      this.$store.commit('SetCurrentPassword', {
        value: this.UserInfo.password,
      });

      this.$store.commit('SetCurrentEmail', {
        value: this.UserInfo.email,
      });
    },

    //shows the popup
    ShowPop(PopUpTitle, PopUpMessage) {
      this.popUpTitle = PopUpTitle;
      this.popUpMessage = PopUpMessage;
      this.inputIsInValid = true;
    },

    //sets the values for the pop based on the value passed from the child
    SetPopUp(value) {
      if (value == 1) {
        this.ShowPop('ERROR', 'The password in both the fields dont match!');
      } else if (value == 2) {
        this.ShowPop(
          'ERROR',
          'Your new password cant be the same as the old password!'
        );
      } else if (value == 0) {
        this.ShowPop('SUCCESS', 'Your password has been successfully changed!');
        this.getUserLoggedIn();
      }
    },
  },

  //This function is called once the component is renderd on screen
  created() {
    // the data from the database is acquired and passed to for v-for
    this.getUserLoggedIn();

    //get the rating
    this.GetRatings();
  },
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Dancing+Script&family=Nunito:wght@700&family=Poppins&family=Shadows+Into+Light&family=Ubuntu:wght@500&display=swap');

.ProfileHeading {
  margin-left: 700px;
}

h1,
h2 {
  color: #f8f8ff;
  font-family: 'Poppins', sans-serif;
}

h5 {
  padding: 20px;
  width: 355px;
  text-align: center;
  padding-right: 10px;
}

.ProfileDetailsCard {
  margin-left: 450px;
  background-color: #dc143c;
  width: 700px;
  height: 250px;
  border-radius: 20px;
}

.ProfileDetailLabels {
  display: flex;
  padding: 30px;
  flex-direction: column;
  align-items: center;
}

.ProfileDetailValues {
  display: flex;
  padding: 30px;
  flex-direction: column;
  align-items: center;
}
.ParentProFileFlex {
  display: flex;
  justify-content: space-evenly;
}
.ButtonsFlex {
  margin-top: 50px;
  display: flex;
  justify-content: space-around;
  flex-direction: row;
}

.ShowPassword {
  cursor: pointer;
}

.ChangePassword {
  padding: 10px 30px;
  background-color: #000000;
  color: #ffffff;
  cursor: pointer;
  font-size: 24px;
  border-radius: 10px;
  font-family: 'Poppins', sans-serif;
  border: 5px solid #000000;
}

.ChangePassword:hover {
  border: 1px solid #ffffff;
}

.NoRatingFound {
  margin-left: 30%;
}

.Rating {
  margin-top: 200px;
}
/* CSS FOR TABLE */
.RatingHeading {
  margin-left: 600px;
  margin-top: 200px;
}

.RatingTableParentFlexBox {
  display: flex;
  flex-direction: column;
}

.RatingTableHeader {
  display: flex;
  justify-content: space-around;
  flex-direction: row;
  width: 1100px;
  margin-left: 250px;
  background-color: #dc143c;
  padding: 10px 50px 10px 50px;
  border-radius: 20px;
}

.RatingTableValues {
  display: flex;
  justify-content: space-between;
  align-content: center;
  flex-wrap: wrap;
  flex-direction: row;
  width: 1100px;
  margin-left: 220px;
}

/* CSS FOR TABLE CONTENTS */

ul li {
  list-style-type: none;
  margin-top: 20px;
  color: #f8f8ff;
  font-size: 26px !important;
  border: 4px solid #dc143c;
  border-radius: 20px;
}
.TableValues {
  display: flex;
  justify-content: space-around;
  width: 1095px;
}

/* CSS FOR POP UP */
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
