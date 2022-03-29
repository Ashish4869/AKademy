import { createRouter, createWebHistory } from 'vue-router';

import EvenSem from './pages/EvenSem.vue';
import OddSem from './pages/OddSem.vue';
import Landing from './pages/Landing.vue';
import Login from './pages/Login.vue';
import Posts from './pages/Posts.vue';
import Profile from './pages/Profile.vue';

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: Login },
    { path: '/Landing', component: Landing },
    { path: '/OddSem', component: OddSem },
    { path: '/EvenSem', component: EvenSem },
    { path: '/posts/:id', name: 'posts', component: Posts, props: true },
    { path: '/Profile', component: Profile },
  ],
});

export default router;
