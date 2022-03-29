<template>
  <!-- HEADER -->
  <header class="mainHeader">
    <img
      src="../assets/AKademy.png"
      style="position: relative; left: 45%"
      alt=""
    />
  </header>

  <!--- END OF HEADER -->

  <!-- FLEX BOX -->
  <div class="row">
    <!-- RIGHT COLUMN (LOGIN-FORM)-->
    <div class="col1">
      <button
        class="switchButtonType"
        @click="toggleAuthMode()"
        value=""
        v-if="IsStudent"
      >
        {{ IsSignIn ? 'Sign Up ' : 'Sign In' }}
      </button>

      <h1 class="signIn">
        {{ logType ? 'SIGN IN' : 'SIGN UP' }}
      </h1>

      <!-- SIGN IN FORM -->
      <base-dialog v-if="inputIsInValid" title="Invalid Input">
        <template #header>
          <h3 class="PopUpTitle">
            <strong>{{ this.popUpTitle }}</strong>
          </h3>
        </template>
        <template #default>
          <p class="PopUpMessage">{{ this.popUpMessage }}</p>
        </template>
        <template #actions>
          <button @click="confirmError(this.IsStudent)" class="dialogButton">
            OK
          </button>
        </template>
      </base-dialog>

      <form
        @submit.prevent="submitData()"
        class="logInputDataForm"
        v-if="IsSignIn"
      >
        <div :class="{ invalid: Validity.username === 'invalid' }">
          <label for="username" class="logFormLabel1">USERNAME</label>
          <input
            type="text"
            class="logFormInput1"
            placeholder=" Username..."
            v-model.trim="username"
            @blur="validateInput('username', username)"
          />
        </div>
        <p v-if="Validity.username === 'invalid'" class="errorText">
          Please Enter A User Name...
        </p>
        <div
          class="input2"
          :class="{ invalid: Validity.password === 'invalid' }"
        >
          <label for="password" class="logFormLabel2">PASSWORD</label>
          <input
            type="password"
            class="logFormInput2"
            placeholder=" Password..."
            v-model.trim="password"
            @blur="validateInput('password', password)"
          />
        </div>
        <p v-if="Validity.password === 'invalid'" class="errorText">
          Please Enter A Password...
        </p>
        <button class="signInButton">
          {{ buttonText ? 'Sign In' : 'Sign Up' }}
        </button>
      </form>
      <!-- END OF SIGN IN FORM -->

      <!-- SIGN UP FORM -->
      <form @submit.prevent="submitData()" class="logInputDataForm" v-else>
        <div :class="{ invalid: Validity.username === 'invalid' }">
          <label for="username" class="logFormLabel1">USERNAME</label>
          <input
            type="text"
            class="logFormInput1"
            placeholder=" Username..."
            v-model.trim="username"
            @blur="validateInput('username', username)"
          />
          <p v-if="Validity.username === 'invalid'" class="errorText">
            Please Enter A User Name...
          </p>
        </div>
        <div :class="{ invalid: Validity.email === 'invalid' }">
          <label for="email" class="logFormLabel3">EMAIL</label>
          <input
            type="email"
            class="logFormInput3"
            placeholder=" Email..."
            v-model.trim="email"
            @blur="validateInput('email', email)"
          />
          <p v-if="Validity.email === 'invalid'" class="errorText">
            Please Enter A Email Name...
          </p>
        </div>
        <div
          class="input2"
          :class="{ invalid: Validity.password === 'invalid' }"
        >
          <label for=" Password" class="logFormLabel2">PASSWORD</label>
          <input
            type="password"
            class="logFormInput2"
            placeholder=" Password..."
            v-model="password"
            @blur="validateInput('password', password)"
          />
          <p v-if="Validity.password === 'invalid'" class="errorText">
            Please Enter A Password...
          </p>
        </div>

        <button class="createAccountButton" style="margin-top: 80px">
          Create Account
        </button>
      </form>
      <!-- END OF SIGN UP FORM -->

      <div class="authData">
        {{
          IsStudent
            ? 'Do You Have Student Account? If Not Sign Up!'
            : 'If You Are A Teacher Then Sign In!'
        }}
      </div>
    </div>
    <!-- END OF RIGHT COLUMN -->

    <!-- LEFT COLUMN (STUDENT/TEACHER)IMAGE -->
    <div class="col2">
      <div>
        <!--test code 2-->
        <i
          class="far fa-check-circle fa-3x checkMark1"
          :class="{ checkopacity: IsStudent }"
        ></i>
        <!-- test code 2-->
        <i
          class="far fa-check-circle fa-3x checkMark2"
          :class="{ checkopacity: !IsStudent }"
        ></i>
      </div>

      <button @click="toggleCategory1()" class="teacherButton">
        <img
          :src="require('@/assets/teacher.png')"
          class="teacherButtonImage"
          alt="teacher_image"
        />
      </button>

      <button @click="toggleCategory2()" class="studentButton">
        <img
          :src="require('@/assets/student.png')"
          class="studentButtonImage"
          alt="student_image"
        />
      </button>
    </div>
  </div>
  <!-- END OF FLEX BOX -->
  <div></div>
</template>

<!-- SCRIPT -->
<script>
import BaseDialog from '../components/ui/BaseDialouge.vue';
export default {
  components: {
    'base-dialog': BaseDialog,
  },
  data() {
    return {
      popUpMessage: '',
      popUpTitle: '',
      category: '',
      logType: true,
      username: '',
      email: '',
      password: '',
      buttonText: true,
      IsSignIn: true,
      //test code 1
      IsStudent: true,
      hover: false,
      Validity: { username: 'pending', email: 'pending', password: 'pending' },
      inputIsInValid: false,
      FetchedData: {},
      numberOfStudentFields: 4,
      numberOfTeacherFields: 2,
      canRoute: false,
    };
  },

  methods: {
    //Toggle Between SignIn and SignUp
    toggleAuthMode() {
      this.IsSignIn = !this.IsSignIn;
      this.logType = !this.logType;
      this.buttonText = !this.buttonText;
      this.username = '';
      this.password = '';
      this.email = '';
      this.Validity.username = 'pending';
      this.Validity.email = 'pending';
      this.Validity.password = 'pending';
    },

    //Toggle From Teacher To Student
    toggleCategory1() {
      this.IsSignIn = true;
      this.logType = true;
      this.buttonText = true;
      if (this.IsStudent === true) this.IsStudent = !this.IsStudent;
      this.username = '';
      this.password = '';
      this.email = '';
      this.Validity.username = 'pending';
      this.Validity.email = 'pending';
      this.Validity.password = 'pending';
    },

    //Toggle From Student To Teacher
    toggleCategory2() {
      if (this.IsStudent === false) this.IsStudent = !this.IsStudent;
      if (this.authType === false) this.authType = true;
      this.username = '';
      this.password = '';
      this.email = '';
      this.Validity.username = 'pending';
      this.Validity.email = 'pending';
      this.Validity.password = 'pending';
    },

    //This Function Is For Individual Field Currently Applied On Username Of SignUp
    validateInput(inputField, field) {
      if (field === '') this.Validity[inputField] = 'invalid';
      else this.Validity[inputField] = 'valid';
    },

    //Submitting SignIn Form
    //Add Your Cases Depending On The Return Value From The JSON File
    submitData() {
      //check if the input in input field is not empty before querying the database
      if (this.IsSignIn == true) {
        if (this.username === '' || this.password === '') {
          this.ShowPopUp('ERROR', 'Please Enter all the fields.');
        } else {
          this.inputIsInValid = false;
        }
      } else if (this.IsSignIn == false) {
        if (this.username === '' || this.password === '' || this.email === '') {
          this.ShowPopUp('ERROR', 'Please Enter all the fields.');
        } else {
          this.inputIsInValid = false;
        }
      }

      //if student has submitted details via sign in
      if (
        this.IsStudent == true &&
        this.logType == true &&
        this.inputIsInValid == false
      ) {
        this.verifyWithDatabase(this.numberOfStudentFields, 'User');
      }

      //if student has submitted details via sign up
      if (
        this.IsStudent == true &&
        this.logType == false &&
        this.inputIsInValid == false
      ) {
        this.verifyandInsertIntoDatabase();
      }

      //if teacher has submitted details via sign in
      if (
        this.IsStudent == false &&
        this.logType == true &&
        this.inputIsInValid == false
      ) {
        this.verifyWithDatabase(this.numberOfTeacherFields, 'Teacher');
      }
    },

    //queries the database and adds the data if no issues found
    verifyandInsertIntoDatabase() {
      fetch(`http://localhost:5000/get/User/${this.username}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      })
        .then((resp) => resp.json())
        .then((data) => {
          this.FetchedData = data;
          console.log(this.FetchedData);

          //checking if the data fetched from database matches with the entered data in input fields.
          if (
            Object.keys(this.FetchedData).length === this.numberOfStudentFields
          ) {
            this.ShowPopUp(
              'ERROR',
              'That username is already taken. Please choose another one.'
            );
            this.ClearInputFields();
          } else {
            //inserting the user input into the database
            let userid = this.$store.state.Highest_Id + 1;
            fetch('http://localhost:5000/add/User', {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
              },
              body: JSON.stringify({
                uid: userid,
                username: this.username,
                email: this.email,
                password: this.password,
              }),
            })
              .then((resp) => resp.json())
              .then(() => {
                this.ShowPopUp(
                  'Account Created',
                  'You have Successfully Created a Account!'
                );
                this.toggleAuthMode();
              })
              .catch((error) => {
                console.log(error);
              });
          }
        })
        .catch((error) => {
          console.log(error);
        });
    },

    //Checks if the values in the database matches with that of the input field
    verifyWithDatabase(len, route) {
      fetch(`http://localhost:5000/get/${route}/${this.username}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      })
        .then((resp) => resp.json())
        .then((data) => {
          this.FetchedData = data;
          console.log(this.FetchedData);

          //checking if the data fetched from database matches with the entered data in input fields.
          if (Object.keys(this.FetchedData).length === len) {
            if (this.FetchedData.password === this.password) {
              this.ShowPopUp('Logged In', 'You have logged in Sucessfully!');

              //Can route to landing
              this.canRoute = true;

              this.ClearInputFields();
            } else {
              this.ShowPopUp('Error', 'Your password is incorrect.');
            }
          } else {
            this.ShowPopUp('Error', 'Your username or password is incorrect.');
          }
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

    //clears the input field of the form
    ClearInputFields() {
      this.username = '';
      this.email = '';
      this.password = '';
    },

    //Okay Button To Close The Dialog Window
    confirmError(isStudent) {
      this.inputIsInValid = false;

      //route only in the case the login was successfull
      console.log(isStudent);
      console.log(this.canRoute);

      //route to page if canRoute is true and get the data as per the status bool
      if (this.canRoute === true && isStudent === true) {
        this.$store.commit('SetCurrentUser', {
          value: this.FetchedData.username,
        });

        this.$store.commit('SetUserUID', {
          value: this.FetchedData.uid,
        });

        this.$store.commit('SetIsTeacher', {
          value: false,
        });

        this.$router.push('/Landing');
      } else if (this.canRoute === true && isStudent === false) {
        this.$store.commit('SetCurrentUser', {
          value: this.FetchedData.name,
        });

        this.$store.commit('SetIsTeacher', {
          value: true,
        });

        //Route to landing page
        this.$router.push('/Landing');
      }
    },
  },

  //This function is called when this component is created
  created() {
    this.canRoute = false;

    //getting the Highest UID in the table so that we can increment
    // and store that value when a new account is created.
    fetch('http://localhost:5000/get/HighestUID', {
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
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Dancing+Script&family=Nunito:wght@700&family=Poppins&family=Shadows+Into+Light&family=Ubuntu:wght@500&display=swap');
.mainHeader {
  background-color: #171717;
  border-radius: 0 0 5px 5px;
  border: 3px solid #dc143c;
  padding-bottom: 10px;
}
.brandName {
  position: relative;
  left: 45%;
  bottom: 10px;
  font-size: 24px;
  font-weight: 900;
  display: inline-block;
  font-family: 'Poppins', sans-serif;
  border: 1px solid crimson;
  border-radius: 15px;
}
.row {
  display: flex;
  flex-direction: row-reverse;
}
.col1 {
  flex: 60%;
  padding: 10px;
  height: 100vh; /* Should be removed. Only for demonstration */
  background-color: #dc143c;
  border-radius: 2px 0 0 1px;
  background-image: url('../assets/background_doodle.png');
}
.col2 {
  flex: 40%;
  padding: 10px;
  height: 100vh; /* Should be removed. Only for demonstration */
  background-color: #171717;
  border-radius: 0 2px 0 0;
}
.invalid input {
  border: 1px solid #dc143c;
}
.invalid label {
  color: #f8f8ff;
}
button.teacherButton {
  border-radius: 20px;
  background-color: transparent;
  border: 1px solid #dc143c;
  position: relative;
  top: 10px;
  left: 250px;
  transition: transform 1s;
  cursor: pointer;
}
button.teacherButton:hover {
  transform: scale(1.1);
}
.teacherButtonImage {
  width: 310px;
  height: 220px;
}
button.studentButton {
  border-radius: 20px;
  background-color: transparent;
  border: 1px solid #dc143c;
  position: relative;
  top: 40px;
  left: 50px;
  transition: transform 1s;
  cursor: pointer;
}
button.studentButton:hover {
  transform: scale(1.1);
}
.studentButtonImage {
  width: 280px;
  height: 230px;
}

.signIn {
  font-family: 'Poppins', sans-serif;
  font-size: 64px;
  text-align: center;
  margin-top: 60px;
  text-shadow: 0px 4px 3px rgba(0, 0, 0, 0.4), 0px 8px 13px rgba(0, 0, 0, 0.1),
    0px 18px 23px rgba(0, 0, 0, 0.1);
}
.logFormLabel1 {
  font-family: 'Nunito', sans-serif;
  font-size: 32px;
  font-weight: 900;
}
.logFormLabel2 {
  font-family: 'Nunito', sans-serif;
  font-size: 30px;
  margin-top: 50px !important;
}

.logFormLabel3 {
  font-family: 'Nunito', sans-serif;
  font-size: 30px;
  margin-top: 90px !important;
  margin-right: 100px;
}
.logInputDataForm {
  margin-top: 40px;
  text-align: center;
}
.logFormInput1 {
  font-family: 'Nunito', sans-serif;
  font-size: 30px;
  background-color: transparent;
  border-radius: 10px;
  width: 40%;
  border: 3px solid #000000;
  margin-left: 20px;
}
.logFormInput2 {
  font-family: 'Nunito', sans-serif;
  font-size: 30px;
  background-color: transparent;
  border-radius: 10px;
  width: 40%;
  border: 3px solid #000000;
  margin-left: 20px;
  margin-top: 10px;
}
.logFormInput3 {
  font-family: 'Nunito', sans-serif;
  font-size: 30px;
  background-color: transparent;
  border-radius: 10px;
  width: 40%;
  border: 3px solid #000000;
  margin-top: 20px;
}
.input2 {
  position: relative;
  margin-bottom: 30px;
  top: 20px;
}
.input3 {
  position: relative;
  top: 40px;
  right: 80px;
}
.signInButton {
  padding: 10px 40px;
  background-color: #000000;
  color: #ffffff;
  cursor: pointer;
  font-size: 26px;
  border-radius: 10px;
  margin-top: 40px;
  font-family: 'Nunito', sans-serif;
  border: 5px solid #000000;
}
.signInButton:hover {
  border: 1px solid #ffffff;
}
.createAccountButton {
  padding: 10px 40px;
  background-color: #000000;
  color: #ffffff;
  cursor: pointer;
  font-size: 26px;
  border-radius: 10px;
  position: relative;
  bottom: 60px;
  font-family: 'Nunito', sans-serif;
  border: 5px solid #000000;
}
.createAccountButton:hover {
  border: 1px solid #ffffff;
}
.switchButtonType {
  padding: 10px 40px;
  background-color: transparent;
  color: #000000;
  cursor: pointer;
  font-size: 26px;
  border-radius: 10px;
  margin-top: 40px;
  font-family: 'Nunito', sans-serif;
  border: 2px solid #1b1b1b;
  position: relative;
  left: 80%;
  bottom: 30px;
}
.switchButtonType:hover {
  background-color: #171717;
  color: #f8f8ff;
  border: 2px solid #f8f8ff;
}
.checkMark1 {
  position: relative;
  top: 60px;
  left: 505px;
  color: #dc143c !important;
}
.checkMark2 {
  position: relative;
  top: 340px;
  left: 220px;
  color: #dc143c !important;
}
.checkopacity {
  opacity: 0;
}

.errorText {
  margin-left: 75px;
  margin-top: 10px;
  color: #f8f8ff;
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
.authData {
  font-family: 'Poppins', sans-serif;
  position: relative;
  top: 60px;
  left: 26%;
  font-size: 24px;
  color: #f8f8ff;
}
</style>
