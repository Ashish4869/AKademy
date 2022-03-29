<template>
  <section>
    <div class="backgroundBlur"></div>
    <!--- ERROR COMPONENT ------------>
    <base-dialog v-if="inputIsInValid" title="Invalid Input">
      <template #header>
        <h3 class="PopUpTitle">
          <strong>ERROR</strong>
        </h3>
      </template>
      <template #default>
        <p class="PopUpMessage">PLEASE FILL ALL THE DETAILS</p>
      </template>
      <template #actions>
        <button @click="confirmError" class="dialogButton">OK</button>
      </template>
    </base-dialog>
    <!--------------- ERROR COMPONENT ----------------->
    <!--------------- FORM ------------------------>
    <!-- IF INPUT IS INVALID FORM GETS HIDDEN ELSE IT IS SHOWN -->
    <form
      @submit.prevent="submitForm"
      :class="inputIsInValid ? 'hideForm' : 'displayForm'"
    >
      <div class="formHeader">
        <!-- HEADRER OF THE FORM -->
        <h1 style="margin-left: 30%">
          {{ this.$store.state.isPostEdit ? 'EDIT' : 'ENTER' }} Post Details
        </h1>
      </div>
      <!-- POST DESCRIPTION INPUT -->
      <div class="form-control">
        <label for="postDescription">Post Description</label>
        <input
          id="postDescription"
          name="postDescription"
          type="text"
          placeholder="Describe your post here"
          v-model="this.$store.state.postDescription"
        />
      </div>

      <div>
        <label for="Post" class="PostLabel">Post</label><br />
        <button
          type="button"
          :class="
            this.$store.state.postType == 1
              ? 'postTypeBtnActive'
              : 'postTypeBtnDeactive'
          "
          class="linkBtn"
          @click="openPostUrlInput(1)"
        >
          Link
        </button>
        <button
          type="button"
          :class="
            this.$store.state.postType == 2
              ? 'postTypeBtnActive'
              : 'postTypeBtnDeactive'
          "
          class="videoBtn"
          @click="openPostUrlInput(2)"
        >
          Video
        </button>
        <button
          type="button"
          :class="
            this.$store.state.postType == 3
              ? 'postTypeBtnActive'
              : 'postTypeBtnDeactive'
          "
          class="pdfBtn"
          @click="openPostUrlInput(3)"
        >
          Pdf
        </button>
      </div>
      <!-- BASED ON THE ABOVE BUTTON PARTICULAR DIV TAG WILL BE SHOWED -->
      <!-- openPostUrl HAS ALL THE TOGGLEING FEATURES -->
      <div v-if="this.$store.state.postType == 1" class="postUrl">
        <p>Enter The Link :</p>
        <input
          type="text"
          placeholder="Enter the link of a site eg : Blog etc"
          v-model="this.$store.state.link"
        />
      </div>
      <div v-if="this.$store.state.postType == 2" class="postUrl">
        <p>Enter The Video :</p>
        <input
          type="text"
          placeholder="Enter the Youtube link."
          v-model="this.$store.state.link"
        />
      </div>
      <div v-if="this.$store.state.postType == 3" class="postUrl">
        <p>Enter The Pdf :</p>
        <input
          type="text"
          placeholder="Enter the link of the pdf"
          v-model="this.$store.state.link"
        />
      </div>
      <hr />
      <!-- SUBMIT AND UPDATE BUTTON TOGGLES BASED ON EDITPOSTMODE MODE -->
      <button class="submit" type="submit">
        {{ this.$store.state.isPostEdit ? 'UPDATE' : 'SUBMIT' }}
      </button>
      <!-- CLOSE BUTTON -->
      <button class="close" type="button" @click="close">
        <i class="fas fa-times"></i> CLOSE
      </button>
    </form>
  </section>
  <!------------- FORM ---------------------------->
</template>
<script>
import BaseDialogue from '../../components/ui/BaseDialouge.vue';
export default {
  components: {
    'base-dialog': BaseDialogue,
  },
  data() {
    return {
      inputIsInValid: false,
      value: 0,
    };
  },
  methods: {
    //used to close the form
    //clears all the caches of the input field (check clearPostInputCache function)
    //deactivates the edit mode
    close() {
      this.$store.state.editPostIndex = 0;
      this.$store.state.isPostEdit = false;
      this.clearPostInputCache();
      this.$store.commit('SetFormActivity', {
        value: false,
      });
    },

    //Used to open input for specific url upload
    //it also assigns the values for the globally definbed postType
    openPostUrlInput(type) {
      if (type == 1) {
        this.$store.commit('setPostType', {
          value: 1,
        });
      } else if (type == 2) {
        this.$store.commit('setPostType', {
          value: 2,
        });
      } else if (type == 3) {
        this.$store.commit('setPostType', {
          value: 3,
        });
      }
    },
    //basic input validation function accessed by submitForm function
    inputValidation() {
      if (
        this.$store.state.postType === 0 ||
        this.$store.state.postDescription === '' ||
        this.$store.state.link === ''
      ) {
        return true;
      } else return false;
    },
    //clears the input field cache accessed by both close and submit form fuction
    clearPostInputCache() {
      this.$store.state.postType = -1;
      this.$store.state.postDescription = '';
      this.$store.state.postDate = '';
      this.$store.state.link = '';
    },
    //submit form function
    //basically two cases (submit/update)
    //update when edit button is pressed
    //else normal submit method
    submitForm() {
      if (this.$store.state.isPostEdit) {
        if (this.inputValidation()) {
          this.inputIsInValid = true;
        } else {
          this.EditPostFromDataBase();
        }
      } else {
        if (this.inputValidation()) {
          this.inputIsInValid = true;
        } else {
          this.AddPostToDataBase();
        }
      }
    },
    //used to close the error dialogue box
    confirmError() {
      this.inputIsInValid = false;
    },

    //Adds a new post into the database
    AddPostToDataBase() {
      let dateObj = new Date();
      let date = dateObj.toString().split(' ').slice(1, 4).join(' ');
      let Highest_Id = this.$store.state.Highest_Id + 1;

      fetch('http://localhost:5000/add/Post', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          post_id: Highest_Id,
          post_type: this.$store.state.postType,
          post_file: this.$store.state.link,
          post_date: date,
          post_description: this.$store.state.postDescription,
          id: this.$store.state.SelectedCourseID,
        }),
      })
        .then((resp) => resp.json())
        .then(() => {
          this.close();
          this.value = 0;
          this.$emit('refresh-posts', this.value);
        })
        .catch((error) => {
          console.log(error);
        });
    },

    //Edits the current selected post
    EditPostFromDataBase() {
      fetch(
        `http://localhost:5000/update/Post/${this.$store.state.PostIndex}`,
        {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            post_id: this.$store.state.PostIndex,
            post_type: this.$store.state.postType,
            post_file: this.$store.state.link,
            post_date: this.$store.state.postDate,
            post_description: this.$store.state.postDescription,
            id: this.$store.state.SelectedCourseID,
          }),
        }
      )
        .then((resp) => resp.json())
        .then(() => {
          this.close();
          this.value = 1;
          this.$emit('refresh-posts', this.value);
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },
};
</script>

<style scoped>
div.backgroundBlur {
  position: fixed;
  top: 0;
  left: 0;
  height: 100vh;
  width: 100%;
  background-color: rgba(0, 0, 0, 0.75);
  z-index: 10;
}
.formHeader {
  background-color: crimson;
  position: relative;
  bottom: 70px;
  right: 80px;
  /* padding: 20px 80px 0 10px; */
  width: 150%;
  padding: 20px 0 10px 0;
}

form {
  margin: 3rem auto;
  max-width: 40rem;
  border-radius: 12px;
  /* box-shadow: 0 2px 8px rgba(0, 0, 0, 0.26); */
  box-shadow: 0 2px 8px rgba(255, 255, 255, 0.26);
  padding: 2rem 3rem 2rem 3rem;
  background-color: #ffffff;
  position: fixed;
  left: 30%;
  bottom: 80px;
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
  margin: 0.5rem 0;
  padding: 10px;
}
button.submit {
  /* margin-top: 5px; */
  position: relative;
  top: 10px;
  padding: 15px 40px;
  border-radius: 5px;
  border: 1px solid #000000;
  background-color: #dc143c;
  color: #f8f8ff;
  font-size: 18px;
}
button.close {
  position: relative;
  left: 43%;
  top: 10px;
  padding: 15px 40px;
  border-radius: 5px;
  border: 1px solid #000000;
  background-color: #dc143c;
  color: #f8f8ff;
  font-size: 18px;
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
.postUrl {
  font-weight: bold;
  font-size: 24px;
}
.linkBtn {
  padding: 10px 40px;
  border: 1px solid #dc143c;
  border-radius: 20px;
  font-size: 20px;
  font-family: sans-serif;
}
.pdfBtn {
  margin-left: 10px;
  padding: 10px 40px;
  border: 1px solid #dc143c;
  border-radius: 20px;
  font-size: 20px;
  font-family: sans-serif;
}
.videoBtn {
  margin-left: 10px;
  padding: 10px 40px;
  border: 1px solid #dc143c;
  border-radius: 20px;
  font-size: 20px;
  font-family: sans-serif;
}
.postTypeBtnActive {
  background-color: #dc143c;
  color: #f8f8ff;
}
.postTypeBtnDeactive {
  background-color: #ffffff;
}
</style>
