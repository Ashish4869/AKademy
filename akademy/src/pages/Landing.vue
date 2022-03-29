<template>
  <the-header></the-header>
  <div></div>
  <section class="landingPage">
    <img src="../assets/MainHeader.png" alt="MainHeader" class="mainHeader" />
    <img
      src="../assets/landing.png"
      alt="landingPageImage"
      class="landingImage"
    />
    <img src="../assets/logo.gif" alt="mainLogo" class="MainLogo" />
    <div class="socialIcons">
      <i class="fab fa-github fa-3x ic1"></i>
      <i class="fab fa-linkedin-in fa-3x ic2"></i>
      <i class="fab fa-discord fa-3x ic3"></i>
    </div>
    <div class="footer">
      <p>Ⓒ 2022 Akademy</p>
    </div>
  </section>
</template>

<script>
import TheHeader from '../components/nav/TheHeader.vue';

export default {
  components: {
    TheHeader,
  },
  data() {
    return {};
  },

  //used to set the profile bool to false when we load the landing page
  created() {
    this.$store.commit('SetProfileActivity', { value: false });
  },
};
</script>

<style scoped>
img {
  margin-left: 400px;
}
.landingPage {
  background-color: #171717 !important;
}
.mainHeader {
  position: relative;
  right: 25%;
}
.landingImage {
  position: relative;
  right: 30%;
  bottom: 20px;
}
.MainLogo {
  position: absolute;
  left: 25%;
  bottom: 10%;
  height: 500px;
}
.socialIcons {
  position: absolute;
  left: 73%;
  bottom: 1px;
  color: #d12749;
}
.ic1 {
  margin: 15px;
}
.ic1:hover {
  color: #f70838;
}
.ic2 {
  margin: 15px;
}
.ic2:hover {
  color: #f70838;
}
.ic3 {
  margin: 15px;
}
.ic3:hover {
  color: #f70838;
}
.footer {
  padding: 2px;
  text-align: center;
  background-color: #dc143c;
  color: #f8f8ff;
}
</style>
