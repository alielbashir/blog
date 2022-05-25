import axios from "axios";
import { defineStore } from "pinia";
const API_URL = import.meta.env.VITE_API_URL;

export const usePostsStore = defineStore("posts", {
  state: () => ({
    posts: [],
  }),
  actions: {
    async getPosts() {
      const { data } = await axios.get(`${API_URL}/posts`, {
        headers: {
          Authorization: "Bearer " + sessionStorage.token,
        },
      });
      this.posts = data;
    },
    async createPost(title, content) {
      const { newPost } = await axios.post(
        `${API_URL}/posts`,
        {
          title: title,
          content: content,
        },
        {
          headers: {
            Authorization: "Bearer " + sessionStorage.token,
          },
        }
      );
      this.posts.push(newPost);
    },
  },
});
