<script setup>
import { ref } from "vue";
import router from "../router";
import { useUsersStore } from "../stores/users";

const usernameModel = ref("");
const passwordModel = ref("");
const confirmPasswordModel = ref("");
const writeScopeModel = ref(false);

const { registerUser } = useUsersStore();

const register = async () => {
  if (passwordModel.value !== confirmPasswordModel.value) {
    alert("Passwords do not match");
    return;
  }

  try {
    await registerUser(
      usernameModel.value,
      passwordModel.value,
      writeScopeModel.value
    );
  } catch (error) {
    if (error.response.status === 400) {
      alert("Username already exists");
    } else {
      console.log(error.response.status);
      alert("Something went wrong");
    }
  }
};
</script>

<template>
  <main>
    <form @submit.prevent="register">
      <h1>Please sign up</h1>
      <div>
        <input
          type="text"
          required
          placeholder="Username"
          v-model="usernameModel"
        />
      </div>
      <div>
        <input
          type="password"
          required
          placeholder="Password"
          v-model="passwordModel"
        />
      </div>
      <div>
        <input
          type="password"
          required
          placeholder="Confirm Password"
          v-model="confirmPasswordModel"
        />
      </div>

      <div>
        <input type="checkbox" id="checkbox" v-model="writeScopeModel" />
        <label for="checkbox">I'm a writer</label>
      </div>
      <button type="submit">Sign up</button>
    </form>
    <button @click="router.push('/')">Already have an account? Sign in</button>
  </main>
</template>
