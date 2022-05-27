import { useSessionStorage } from "@vueuse/core";
import axios from "axios";
import { defineStore } from "pinia";
import { useUsersStore } from "./users";
const API_URL = import.meta.env.VITE_API_URL;

export const usePostsStore = defineStore("posts", {
  state: () => ({
    posts: useSessionStorage("posts", []),
    updatingToggle: false, // toggle to watch for updates
  }),
  actions: {
    async fetchPosts() {
      const { token } = useUsersStore();
      const { data } = await axios.get(`${API_URL}/posts`, {
        headers: {
          Authorization: "Bearer " + token,
        },
      });
      this.posts = data;
    },
    async createPost(title, content) {
      console.log(`title = ${title}`);
      console.log(`content = ${content}`);

      const { token } = useUsersStore();
      await axios.post(
        `${API_URL}/posts`,
        {
          title: title,
          content: content,
        },
        {
          headers: {
            Authorization: "Bearer " + token,
          },
        }
      );
      this.updatingToggle = !this.updatingToggle;
    },
  },
  getters: {
    dateSortedPosts(state) {
      if (state.posts.length < 2) {
        return [...state.posts];
      }
      return [...state.posts].sort((a, b) => {
        return b.creation_date - a.creation_date;
      });
    },
    voteSortedPosts(state) {
      if (state.posts.length < 2) {
        return [...state.posts];
      }
      return [...state.posts].sort((a, b) => {
        return b.votes - a.votes;
      });
    },
  },
});
