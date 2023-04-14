import { createRouter, createWebHistory } from "vue-router";
import HomeView from "@/views/HomeView.vue"
import AthleteView from "@/views/AthleteView.vue";
import PageNotFound from "@/views/PageNotFound.vue";
import AuthStrava from "@/views/AuthStrava.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
      meta: { requiresAuth: false },
    },
    {
      path: '/athlete/:slug',
      name: 'athlete',
      component: AthleteView
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
