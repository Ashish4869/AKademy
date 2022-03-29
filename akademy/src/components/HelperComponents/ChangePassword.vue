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
        <h1 style="margin-left: 30%">Change Password</h1>
      </div>

      <!------------- Change Password -------------->
      <div class="form-control">
        <label for="Enter New Password">Enter New Password</label>
        <input
          id="NewPassword"
          name="NewPassword"
          type="text"
          v-model="this.newPassword"
        />
      </div>

      <div class="form-control">
        <label for="PasswordConfirmation">Re Enter the New Password</label>
        <input
          id="PasswordConfirmation"
          name="PasswordConfirmation"
          type="text"
          v-model="this.ConfirmPassword"
        />
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
      value: 0,
      newPassword: '',
      ConfirmPassword: '',
    };
  },

  methods: {
    //closes the pop up
    confirmError() {
      this.inputIsInValid = false;
    },

    //clears the values and sets the value to what it was initially
    close() {
      this.newPassword = '';
      this.ConfirmPassword = '';

      this.$store.commit('SetFormActivity', {
        value: false,
      });
    },

    //validation return inside a function
    inputValidation() {
      if (this.newPassword == '' || this.ConfirmPassword == '') {
        return true;
      } else return false;
    },

    //checks few conditions and edits the password
    submitForm() {
      if (this.inputValidation()) {
        this.inputIsInValid = true;
        console.log('hello');
      } else {
        if (this.newPassword != this.ConfirmPassword) {
          this.value = 1;
          this.$emit('showError', this.value);
        } else if (
          this.newPassword == this.$store.state.CurrentPassword ||
          this.ConfirmPassword == this.$store.state.CurrentPassword
        ) {
          this.value = 2;
          this.$emit('showError', this.value);
        } else {
          if (this.$store.state.isTeacher == true) {
            this.AddingTeacherChangedPasswordToDatabase();
          } else {
            this.AddingUserChangedPasswordToDatabase();
          }
        }

        this.close();
      }
    },

    AddingUserChangedPasswordToDatabase() {
      fetch(
        `http://localhost:5000/update/user/${this.$store.state.CurrentUserUID}`,
        {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            uid: this.$store.state.CurrentUserUID,
            username: this.$store.state.CurrentUser,
            email: this.$store.state.CurrentEmail,
            password: this.ConfirmPassword,
          }),
        }
      )
        .then((resp) => resp.json())
        .then(() => {
          this.value = 0;
          this.$emit('showError', this.value);
          this.close();
        })
        .catch((error) => {
          console.log(error);
        });
    },

    AddingTeacherChangedPasswordToDatabase() {
      //Adds password to database
      //Adds password to database
      fetch(
        `http://localhost:5000/update/teacher/${this.$store.state.CurrentUser}`,
        {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            name: this.$store.state.CurrentUser,
            password: this.ConfirmPassword,
          }),
        }
      )
        .then((resp) => resp.json())
        .then(() => {
          this.value = 0;
          this.$emit('showError', this.value);
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
  left: 57%;
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
.hideForm {
  visibility: hidden;
}
.displayForm {
  visibility: visible;
}

.form-control {
  margin: 1rem 0;
}
</style>
