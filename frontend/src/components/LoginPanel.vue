<script setup>
import { ref } from "vue";
import router from "../router";
import { useUsersStore } from "../stores/users";

const usernameModel = ref("");
const passwordModel = ref("");

const { loginUser } = useUsersStore();

const login = async () => {
  try {
    await loginUser(usernameModel.value, passwordModel.value);
    router.push("dashboard");
  } catch (error) {
    console.log(error);
    alert("Invalid username and/or password");
  }
};
</script>

<template>
  <main>
    <form @submit.prevent="login">
      <h1>Please sign in</h1>
      <div>
        <input
          id="floatingInput"
          type="text"
          required
          placeholder="Username"
          v-model="usernameModel"
        />
      </div>
      <div>
        <input
          id="floatingPassword"
          type="password"
          required
          placeholder="Password"
          v-model="passwordModel"
        />
      </div>

      <button type="submit">Sign in</button>
    </form>
    <button @click="router.push('register')">Create an account</button>
  </main>
</template>
