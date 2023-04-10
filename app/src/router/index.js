import { createRouter, createWebHistory } from "vue-router";
import HomeView from "@/views/HomeView.vue"
import MeView from "@/views/MeView.vue";
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
      path: '/me',
      name: 'me',
      component: MeView
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
