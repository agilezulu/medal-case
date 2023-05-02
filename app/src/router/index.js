import { createRouter, createWebHistory } from "vue-router";
import HomeView from "@/views/HomeView.vue"
import AthleteView from "@/views/AthleteView.vue";
import MeView from "@/views/MeView.vue";
import AboutView from "@/views/AboutView.vue";
import PageNotFound from "@/views/PageNotFound.vue";
import AuthStrava from "@/views/AuthStrava.vue";

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
      meta: { requiresAuth: false },
    },
    {
      path: '/about',
      name: 'about',
      component: AboutView,
      meta: { requiresAuth: false },
    },
    {
      path: '/athlete/:slug',
      name: 'athlete',
      component: AthleteView,
      meta: { requiresAuth: false },
    },
    {
      path: '/me',
      name: 'me',
      component: MeView,
      meta: { requiresAuth: true },
    },
    {
      path: "/exchange_token",
      name: "AuthStrava",
      component: AuthStrava,
      meta: { requiresAuth: false },
    },
    {
      path: "/:catchAll(.*)*",
      name: "PageNotFound",
      component: PageNotFound,
      meta: { requiresAuth: false },
    }
  ]
})

export default router
