<template>
  <router-view></router-view>
</template>

<style>
* {
  box-sizing: border-box;
}

html {
  font-family: sans-serif;
}

body {
  margin: 0;
  overflow-x: hidden;
  background-color: #171717;
}
/* --Scroll Bar-- */

/* width */

::-webkit-scrollbar {
  width: 10px;
}

/* Track */

::-webkit-scrollbar-track {
  box-shadow: inset 0 0 5px #dc143c;
  border-radius: 5px;
  background-clip: content-box;
}

/* Handle */

::-webkit-scrollbar-thumb {
  background: #dc143c;
  border-radius: 5px;
}

/* Handle on hover */

::-webkit-scrollbar-thumb:hover {
  background: #dc143c;
}

/* --End Of Scroll Bar-- */
</style>
