import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "joinGame",
      component: HomeView,
    },
    {
      path: "/game/:gameId",
      name: "waitingGame",
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import("../views/WaitingView.vue"),
    },
    {
      path: "/game/:gameId/start",
      name: "answersQuestion",
      component: () => import("../views/AnswersView.vue"),
    },
    {
      path: "/:pathMatch(.*)*",
      name: "notFound",
      component: () => import("../views/NotFoundView.vue"),
    },
  ],
});

export default router;
