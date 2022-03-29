import { createStore } from 'vuex';

const store = createStore({
  state() {
    return {
      //Course Related info
      SelectedCourseName: '',
      SelectedCourseID: '',
      InCourse: false,
      SelectedCourseInstructor: '',

      //User logged info
      CurrentUser: '',
      isTeacher: false,
      CurrentUserUID: -1,

      //Courses related info
      isEdit: false, //VARIBALE WHICH TOGGLES THE EDIT MODE
      // editCourseIndex: 0, //INDEX OF THE COURSE TO BE EDITED
      CourseID: -1,
      courseTitle: '', //THESE VALUES ARE GLOBALIZED BECAUSE THEY ARE USED AT DISPLAYING
      instructorName: '', //VALUES AT THE INPUT FIELD DURING EDIT MODE
      imageUrl: '',
      courseLength: '',
      prerequisite: '',

      //Posts Related Variables
      isPostEdit: false,

      //Current post to edit details
      PostIndex: 0,
      editcourseTitle: '',
      postDate: '',
      postDescription: '',
      postType: 0,
      link: '',

      Highest_Id: -1,

      //Form Activity
      isFormActive: false,
      isRatingFormActive: false,

      //Prfile Page related variables
      isInProfilePage: false,
      CurrentPassword: '',
      CurrentEmail: '',
    };
  },
  mutations: {
    //Toggles bettween sem nav bar and name of the Course
    IsInCourse(state, payload) {
      state.InCourse = payload.value;
    },

    //Sets the current user
    SetCurrentUser(state, payload) {
      state.CurrentUser = payload.value;
    },

    SetUserUID(state, payload) {
      state.CurrentUserUID = payload.value;
    },

    //Set the value of this teacher
    SetIsTeacher(state, payload) {
      state.isTeacher = payload.value;
    },

    SetIsEditPost(state, payload) {
      state.isPostEdit = payload.value;
    },

    SetFormActivity(state, payload) {
      state.isFormActive = payload.value;
    },

    SetRatingFormActivity(state, payload) {
      state.isRatingFormActive = payload.value;
    },

    SetProfileActivity(state, payload) {
      state.isInProfilePage = payload.value;
    },

    setHighestID(state, payload) {
      state.Highest_Id = payload.value;
    },

    setPostEdit(state, payload) {
      state.PostIndex = payload.postIndex;
      state.postDate = payload.postDate;
      state.postDescription = payload.postDescription;
      state.postType = payload.postType;
      state.link = payload.link;
    },

    setAddPostdata(state, payload) {
      state.PostIndex = payload.postIndex;
      state.postDate = payload.postDate;
      state.postDescription = payload.postDescription;
      state.postType = payload.postType;
      state.link = payload.postlink;
    },

    //When the edit button is pressed all the info of the current post and send it here
    setCourseEditRelatedInfo(state, payload) {
      state.CourseID = payload.id;
      state.courseTitle = payload.courseName;
      state.courseLength = payload.courseLength;
      state.imageUrl = payload.courseImage;
      state.prerequisite = payload.coursePrerequisite;
    },

    setCourseIsEdit(state, payload) {
      state.isEdit = payload.value;
    },

    setPostType(state, payload) {
      state.postType = payload.value;
    },
    //All course related info are fetched and set here
    SetCourseRelatedInfo(state, payload) {
      state.SelectedCourseID = payload.CourseID;
      state.SelectedCourseName = payload.CourseName;
      state.SelectedCourseInstructor = payload.Instructor;
      state.InCourse = payload.inCourse;
    },

    //Profile related
    SetCurrentPassword(state, payload) {
      state.CurrentPassword = payload.value;
    },

    SetCurrentEmail(state, payload) {
      state.CurrentEmail = payload.value;
    },
  },
});

export default store;
