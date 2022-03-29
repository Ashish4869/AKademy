<template>
  <the-header></the-header>
  <!-- POST PAGE LAYOUT -->

  <button
    class="createCourseButton"
    v-if="this.$store.state.isTeacher"
    @click="activatePostForm()"
  >
    <i class="fas fa-plus-circle"> Create Posts</i>
  </button>

  <!-- Add Post component -->
  <add-post
    v-if="this.$store.state.isFormActive"
    @refresh-posts="ShowPopandGetCourse"
  ></add-post>

  <!-- Add rating component -->
  <add-rating
    v-if="this.$store.state.isRatingFormActive"
    @refresh-rating="ShowPopUpforRating"
  ></add-rating>

  <!-- Shows no posts image if there is no post -->
  <div v-if="this.coursePosts.length == 0">
    <img class="NoPostsFound" src="@/assets/NODATA.png" alt="" />

    <p
      style="
        margin-left: 40%;
        font-size: 32px;
        font-style: sans-serif;
        color: #f8f8ff;
      "
    >
      No Posts in this course...
    </p>
  </div>

  <ul style="list-style: none">
    <!--Course Items Displayed -->
    <li v-for="(post, index) in coursePosts" :key="post.post_id">
      <post-card>
        <button
          class="modButton1"
          v-if="this.$store.state.isTeacher"
          @click="
            editPost(
              post.post_id,
              post.post_date,
              post.post_description,
              post.post_type,
              post.post_file
            )
          "
        >
          Edit
        </button>

        <button
          class="modButton2"
          v-if="this.$store.state.isTeacher"
          @click="DeletePost(post.post_id)"
        >
          Delete
        </button>
        <header class="CourseTitle">
          <h4>
            <strong
              >{{ this.$store.state.SelectedCourseInstructor }} @
              {{ post.post_date }}</strong
            >
          </h4>
        </header>
        <p class="DescriptionStyle">{{ post.post_description }}</p>

        <!-- Makes the resource available on a click -->
        <button
          class="ViewResourceButton"
          @click="setIndex(index)"
          v-if="currentIndex != index"
        >
          View Resource
        </button>

        <!-- Hides the Resource on click and prevent more than one resource from showing  -->
        <button
          class="ViewResourceButton"
          @click="HideIndex()"
          v-if="currentIndex === index"
        >
          Hide Resource
        </button>

        <!-- if current post is selected and is a link, show it -->
        <div
          class="ShowLink"
          v-if="currentIndex === index && post.post_type === 1"
        >
          <p class="postTypeText">
            Link to the site :
            <a
              :href="post.post_file"
              target="_blank"
              style="text-decoration: none"
              >{{ post.post_file }}</a
            >
          </p>
        </div>

        <!-- if current post is selected and is a video, show it -->
        <div
          class="ShowVideo"
          v-if="currentIndex === index && post.post_type === 2"
        >
          <iframe
            width="560"
            height="315"
            :src="post.post_file"
            title="YouTube video player"
            frameborder="0"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowfullscreen
          ></iframe>
        </div>

        <!-- if current post is selected and is a pdf, show it -->
        <div
          class="ShowPdf"
          v-if="currentIndex === index && post.post_type === 3"
        >
          <p class="postTypeText">
            PDF:
            <a
              :href="post.post_file"
              target="_blank"
              style="text-decoration: none"
              >{{ post.post_file }}</a
            >
          </p>
        </div>
      </post-card>
    </li>
  </ul>
  <button
    v-if="this.$store.state.isTeacher == false"
    class="RateUs"
    @click="OpenRatingForm"
  >
    <i class="far fa-thumbs-up"></i> Rate this Course
  </button>

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
import PostCard from '../components/ui/PostCard.vue';
import AddPosts from '../components/HelperComponents/AddPosts.vue';
import TheHeader from '../components/nav/TheHeader.vue';
import AddRating from '../components/HelperComponents/AddRating.vue';
import BaseDialog from '../components/ui/BaseDialouge.vue';
export default {
  components: {
    'post-card': PostCard,
    'add-post': AddPosts,
    TheHeader,
    AddRating,
    BaseDialog,
  },

  data() {
    return {
      // index for the current post selected
      currentIndex: -1,
      //The array of objects that we will get from database
      coursePosts: {},

      inputIsInValid: false,
      popUpTitle: '',
      popUpMessage: '',
    };
  },

  methods: {
    // makes the index -1 so that none of the posts are open
    HideIndex() {
      this.currentIndex = -1;
    },

    //sets the current index to do the post clicked on
    setIndex(index) {
      this.currentIndex = index;
    },
    //USED TO ACTIVATE THE POST FORM
    activatePostForm() {
      this.$store.commit('SetFormActivity', {
        value: true,
      });

      //Gets the highest post ID so that we can use to add new posts
      fetch('http://localhost:5000/get/HighestPostID', {
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

    //DELETES THE POST
    DeletePost(postId) {
      console.log(postId);
      this.DeletePostFromDataBase(postId);
    },

    //Edits the selected post
    editPost(postId, postDate, postDescription, postType, postFile) {
      //sets the values of the selected coruse in vuex
      this.$store.commit('setPostEdit', {
        postIndex: postId,
        postDate: postDate,
        postDescription: postDescription,
        postType: postType,
        link: postFile,
      });

      //Opens the form
      this.$store.commit('SetFormActivity', {
        value: true,
      });

      //sets the bool for editing the post
      this.$store.commit('SetIsEditPost', {
        value: true,
      });
    },

    //gets the data from the database
    getCoursePosts() {
      //gets the data from the database as per the course selected in landing page
      fetch(
        `http://localhost:5000/get/Post/${this.$store.state.SelectedCourseID}`,
        {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          },
        }
      )
        .then((resp) => resp.json())
        .then((data) => {
          this.coursePosts = data;
          console.log(this.coursePosts);
        })
        .catch((error) => {
          console.log(error);
        });
    },

    //showes messages and refreshes data
    ShowPopandGetCourse(edit) {
      if (edit === 1) {
        this.ShowUpdatePopUp();
      } else if (edit === 0) {
        this.ShowAddedPopUp();
      }

      this.getCoursePosts();
    },

    //showes messages and refreshes data
    ShowPopUpforRating(messageNumber) {
      if (messageNumber === 1) {
        this.ShowRatingAdded();
      } else if (messageNumber === 0) {
        this.ErrorAddingRating();
      }
    },

    //Deletes the post from the database
    DeletePostFromDataBase(postId) {
      fetch(`http://localhost:5000/delete/Post/${postId}`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
        },
      })
        .then(() => {
          this.ShowPopUp('Post Deleted', 'Successfully Deleted The Post!');
          this.getCoursePosts();
        })
        .catch((error) => {
          console.log(error);
        });
    },

    OpenRatingForm() {
      this.$store.state.isRatingFormActive = true;
      console.log((this.$store.state.isRatingFormActive = true));

      //Gets the highest rating ID so that we can use to add new rating
      fetch('http://localhost:5000/get/HighestRatingID', {
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

    //Shows the pop up with the arguments passed in the function
    ShowPopUp(popUpTitle, popUpMessage) {
      this.popUpTitle = popUpTitle;
      this.popUpMessage = popUpMessage;
      this.inputIsInValid = true;
    },

    //shows pop up that course is updated
    ShowUpdatePopUp() {
      this.popUpTitle = 'Post Updated';
      this.popUpMessage = 'Post has been succesfully updated!';
      this.inputIsInValid = true;
    },

    ShowAddedPopUp() {
      this.popUpTitle = 'Post Added';
      this.popUpMessage = 'Your Post has been succesfully added!';
      this.inputIsInValid = true;
    },

    ShowRatingAdded() {
      this.popUpTitle = 'Rating Added';
      this.popUpMessage = 'Thank You for leaving a rating!';
      this.inputIsInValid = true;
    },

    ErrorAddingRating() {
      this.popUpTitle = 'ERROR';
      this.popUpMessage = 'You cannot add Multiple rating for the same course!';
      this.inputIsInValid = true;
    },

    //closes the popup
    confirmError() {
      this.inputIsInValid = false;
    },
  },

  //this function is called when the component is created
  created() {
    this.getCoursePosts();
  },
};
</script>
<style scoped>
header.CourseTitle {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #f8f8ff;
  text-align: left;
}
.DescriptionStyle {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #f8f8ff;
  text-align: left;
  position: relative;
  bottom: 10px;
}
.postTypeText {
  color: #f8f8ff;
}
.ViewResourceButton {
  cursor: pointer;
  position: relative;
  right: 1%;
  padding: 10px;
  border-radius: 20px;
  border: 1px solid #f8f8ff;
  background-color: #171717;
  color: white;
}
.ViewResourceButton:hover {
  background-color: #000000;
  border-color: #ffffff;
}
.PostContent {
  text-align: left;
  font-size: 28px;
  font-family: Avenir, Helvetica, Arial, sans-serif;
  color: #2c3e50;
}
.CourseSelectButton {
  padding: 10px 20px;
  border-radius: 10px;
  border: 1px solid #000000;
}
.fade-button-enter-from,
.fade-button-leave-to {
  opacity: 0;
}

.fade-button-enter-active {
  transition: opacity 0.2s ease-out;
}

.fade-button-leave-active {
  transition: opacity 0.2s ease-in;
}

.fade-button-enter-to,
.fade-button-leave-from {
  opacity: 1;
}

.course-fade-enter-from {
  opacity: 0;
  transform: translateY(-30px);
}
.course-fade-enter-active {
  transition: all 0.3s ease-out;
}
.course-fade-enter-to {
  opacity: 1;
  transform: translateY(0);
}
.course-fade-leave-from {
  opacity: 1;
  transform: translateY(0);
}
.course-fade-leave-active {
  transition: all 0.3s ease-in;
}

.course-fade-leave-to {
  opacity: 0;
  transform: translateY(30px);
}
.RateUs {
  position: absolute;
  position: fixed;
  bottom: 10px;
  right: 5px;
  padding: 15px 35px;
  font-size: 18px;
  border-radius: 30px;
  border: 1px solid #000000;
  background-color: #dc143c;
  color: #f8f8ff;
}

.ShowVideo {
  margin-top: 30px;
}
button.createCourseButton {
  background-color: #dc143c;
  color: #f8f8ff;
  font-size: 20px;
  font-family: serif;
  position: relative;
  left: 83%;
  top: 110px;
  position: fixed;
  padding: 1rem 3rem;
  clear: both;
  display: inline-block;
  overflow: hidden;
  white-space: nowrap;
  border: 1px solid #f8f8ff;
  cursor: pointer;
  border-radius: 20px;
}
.modButton1 {
  position: relative;
  left: 60%;
  padding: 10px 40px;
  border: 1px solid crimson;
  cursor: pointer;
  border-radius: 20px;
  background-color: #171717;
  color: #f8f8ff;
}
.modButton2 {
  position: relative;
  left: 65%;
  background-color: #ffffff;
  color: crimson;
  border: 1px solid crimson;
  padding: 10px 30px;
  border-radius: 20px;
  cursor: pointer;
}

.NoPostsFound {
  margin-left: 30%;
  margin-top: 100px;
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
