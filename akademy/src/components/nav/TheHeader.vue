<template>
  <header>
    <!-- link to the home page -->
    <h1 @click="SetNavBar">
      <router-link to="/Landing" class="brandName">AKademy</router-link>
    </h1>
    <nav>
      <ul v-if="this.$store.state.InCourse === false">
        <!-- link to the Oddsem data -->
        <li @click="SetNavBar">
          <router-link to="/OddSem" class="navItem1">3rd Sem</router-link>
        </li>
        <!-- link to the even sem data -->
        <li @click="SetNavBar">
          <router-link to="/EvenSem" class="navItem2">4th Sem</router-link>
        </li>
      </ul>
      <!-- if we are in a course , display its name -->
      <ul v-if="this.$store.state.InCourse === true" class="courseHeader">
        <li>
          <h3>{{ this.$store.state.SelectedCourseName }}</h3>
        </li>
      </ul>
    </nav>

    <!-- display the use who has logged in the righ side of he nav bar -->
    <div class="navItem3" @click="goProfile">
      <h2>
        {{
          this.$store.state.isInProfilePage
            ? 'Log Out'
            : this.$store.state.CurrentUser
        }}
      </h2>
    </div>
  </header>
</template>

<script>
export default {
  data() {
    return {};
  },
  methods: {
    //sets the nav bar to show sems when we click on the AKademy link
    SetNavBar() {
      this.$store.commit('IsInCourse', { value: false });
      this.$store.commit('SetProfileActivity', { value: false });
    },

    // should change this later
    goProfile() {
      //if we are in profile page
      if (this.$store.state.isInProfilePage) {
        this.$router.push('/');
      } else {
        //if we are not in profile page
        this.$router.push('/Profile');
        this.$store.commit('SetProfileActivity', { value: true });
        this.$store.commit('IsInCourse', { value: false });
      }
    },
  },
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Dancing+Script&family=Nunito:wght@700&family=Poppins&family=Shadows+Into+Light&family=Ubuntu:wght@500&display=swap');

header {
  height: 5rem;
  background-color: #dc143c;
  /* margin: 0 10%; */
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.courseHeader {
  margin-left: 100px;
  color: #f8f8ff;
  font-family: 'Poppins', sans-serif;
}
.brandName {
  position: relative;
  left: 30px;
  text-decoration: none;
  border: 1px solid #171717;
  padding: 10px;
  border-radius: 10px;
  color: #f8f8ff;
}

ul {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  justify-self: center;
  align-items: center;
}

li {
  margin: 0 1rem;
}

a {
  text-decoration: none;
  color: #333;
  font-weight: bold;
  border-bottom: 2px solid transparent;
  padding-bottom: 0.25rem;
}

button {
  font: inherit;
  cursor: pointer;
  padding: 0.5rem 1.5rem;
  border: 1px solid #380500;
  background-color: transparent;
  color: #000000;
  border-radius: 30px;
}

button:hover,
button:active {
  /* background-color: #f0d5ff; */
}
.navItem1 {
  font-size: 24px;
  position: relative;
  right: 10px;
  border: 1px solid #171717;
  padding: 10px;
  border-radius: 10px;
  color: #f8f8ff;
}
.navItem2 {
  font-size: 24px;
  position: relative;
  left: 50px;
  border: 1px solid #171717;
  padding: 10px;
  border-radius: 10px;
  color: #f8f8ff;
}

.navItem3 {
  cursor: pointer;
  font-size: 24px;
  color: #f8f8ff;
  margin-right: 20px;
}

.navItem3:hover {
  color: #171717;
}

.brandName:focus {
  color: #171717;
}
.navItem1:focus {
  color: #171717;
}
.navItem2:focus {
  color: #171717;
}

a:hover {
  border-color: #f8f8ff;
}

a.router-link-active {
  color: #171717;
  border-color: #f8f8ff;
}
</style>
