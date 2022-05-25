import { useSessionStorage } from "@vueuse/core";
import axios from "axios";
import { defineStore } from "pinia";
import { useUsersStore } from "./users";
const API_URL = import.meta.env.VITE_API_URL;

export const usePostsStore = defineStore("posts", {
  state: () => ({
    posts: useSessionStorage("posts", []),
  }),
  actions: {
    async getPosts() {
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
      const { newPost } = await axios.post(
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
      this.posts.push(newPost);
    },
  },
});
