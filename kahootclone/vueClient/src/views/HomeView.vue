<template>
    <main>
    <div id="gameForm">
      <gameForm
        :error="error"
        :error_message="error_message"
        @add-participant="addParticipant"
      />
    </div>
    </main>
  
</template>

<script>
import GameForm from "../components/GameForm.vue";
const myVar = import.meta.env.VITE_DJANGOURL;
export default {
  components: {
    GameForm,
  },
  data() {
    return {
      myVar: myVar,
      error: false,
      error_message: "",
    };
  },
  methods: {
    async addParticipant(participant) {
      console.log(participant);
      const url = `${this.myVar}participant/`;
      const response = await fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(participant),
      });
      this.status = response.status;
      // console.log(response.status);

      if (response.status == 201) {
        // commit participant uuidp to store
        // console.log(participant_response.uuidP)
        const participant_response = await response.json();
        this.$store.commit("store_participant", {
          uuidp: participant_response.uuidP,
        });
        this.$router.push({
          name: "waitingGame",
          params: { gameId: participant.game },
        });
      } else if (response.status == 403) {
        const error_response = await response.json();
        console.log("Error");
        this.error = true;
        this.error_message = error_response;
      } else {
        console.log("Error");
        this.error = true;
      }
    },
  },
};
</script>

