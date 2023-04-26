<template>
  <div class="about">
    <h1>You're in!</h1>
    <br>
    <h3>Game with pin: {{ gameId }}</h3>
    <br>
    <h3>Waiting for the game to start...</h3>
    <br>
    <h3>State: {{ gameState }}</h3>
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
      }
    },
    created() {
      this.gameId = this.$route.params.gameId;
    },
    mounted() {
      setInterval(this.getGame, 2000);
    },
    // mounted: {
    //   // this.getGame();
    //   // setInterval(this.getGame, 2000);
    // },
    methods: {
      // ajax function every 2 seconds to get game
      // if game is started, redirect to game view
      // if game is not started, do nothing
      // if game is not found, redirect to home view
      async getGame() {
        const url = `${this.myVar}games/${this.gameId}/`;
        console.log(url)
        const response = await fetch(url, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json; charset=UTF-8',
          },
        });
        if (response.status == 200) {
          this.gameState = response.status;
          // if (game.started) {
          //   this.$router.push({ name: 'game', params: { gameId: this.gameId } });
          // }
        }
      },
    }
  }
</script>

<style>
@media (min-width: 1024px) {
  .about {
    min-height: 100vh;
    align-items: center;
  }
}
</style>
