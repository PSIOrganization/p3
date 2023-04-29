<template>
  <div id="lobby">
    <h1>You're in!</h1>
    <br>
    <h3>Game with pin: {{ gameId }}</h3>
    <br>
    <h3>{{ message }}</h3>
    <br>
  </div>
</template>

<script>
  const myVar = import.meta.env.VITE_DJANGOURL;
  export default {
    data() {
      return {
        myVar: myVar,
        gameId: '',
        gameState: null,
        message: '',
        myInterval: null,
      }
    },
    created() {
      this.gameId = this.$route.params.gameId;
    },
    mounted() {
      this.myInterval = setInterval(this.getGame, 500);
    },
    beforeUnmount() {
      clearInterval(this.myInterval);
    },
    // beforeRouteLeave() {
    //   clearInterval(this.myInterval);
    // },
    methods: {
      // ajax function every 2 seconds to get game
      // if game is started, redirect to game view
      // if game is not started, do nothing
      // if game is not found, redirect to home view
      async getGame() {
        const url = `${this.myVar}games/${this.gameId}/`;
        console.log(url)
        // console.log(this.$store.state.uuidp) lo tenemos
        const response = await fetch(url, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json; charset=UTF-8',
          },
        });
        const game = await response.json();
        if (response.status == 200) {
          // console.log(game);
          this.gameState = game.state;
          if (this.gameState == 1) {
            this.message = 'Waiting for the game to start...';
          }
          else if (this.gameState == 2) {
            this.message = 'Game will start soon...';
            
          } else if (this.gameState == 3) {
            // console.log(game.questionNo)
            this.$router.push({ name: 'answersQuestion', params: { gameId: this.gameId } });
          }
        }
      },
    }
  }
</script>

<style>
@media (min-width: 1024px) {
  #lobby {
    min-height: 100vh;
    align-items: center;
  }
}
</style>
