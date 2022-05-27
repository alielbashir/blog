import axios from "axios";
import { defineStore } from "pinia";
import { useSessionStorage } from "@vueuse/core";

const API_URL = import.meta.env.VITE_API_URL;

export const useUsersStore = defineStore("user", {
  state: () => ({
    username: useSessionStorage("username", ""),
    isWriter: useSessionStorage("isWriter", false),
    token: useSessionStorage("token", ""),
  }),
  actions: {
    async loginUser(username, password) {
      // FIXME: should i try catch here or only in function consumers?
      if (password === 0) {
        alert("Passwords do not match");
        return;
      }

      const { data } = await axios.post(`${API_URL}/users/login`, {
        username: username,
        password: password,
      });

      this.username = data.username;
      this.isWriter = data.scope === "write";
      this.token = data.token;
    },
    logoutUser() {
      this.username = "";
      this.isWriter = false;
      this.token = "";
      console.log("state reset for user");
    },
    async registerUser(username, password, writeScope) {
      await axios.post(`${API_URL}/users/register`, {
        username: username,
        password: password,
        scope: writeScope ? "write" : "read",
      });
    },
  },
});
