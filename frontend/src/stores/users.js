import axios from "axios";
import { defineStore } from "pinia";
const API_URL = import.meta.env.VITE_API_URL;

export const useUsersStore = defineStore("user", {
  state: () => ({
    username: String,
    scope: String,
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
      this.scope = data.scope;

      // store token in session storage
      sessionStorage.token = data.token;
    },
  },
});
