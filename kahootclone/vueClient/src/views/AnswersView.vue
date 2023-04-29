<template>
  <div id="answersForm">
    <h1>{{ answerMessage }}</h1>
    <answersForm :error="error" 
                  :error_message="error_message" 
                  :info="info"
                  :info_message="info_message"
                  @add-guess="addGuess"/>
    <button v-if="returnButton" @click="returnToHome">Return to Home</button>
  </div>
</template>
  
  <script>
    import AnswersForm from '../components/AnswersForm.vue';
    const myVar = import.meta.env.VITE_DJANGOURL;
    export default {
      components: {
        AnswersForm,
      },
      data() {
        return {
          myVar: myVar,
          gameId: '',
          gameState: null,
          answerMessage: '',
          error: false,
          error_message: '',
          info: false,
          info_message: '',
          returnButton: false,
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
            if (this.gameState == 3) {
              this.answerMessage = `Question ${game.questionNo + 1}`;
            } else if (this.gameState == 4) {
              this.answerMessage = `Waiting for next question...`;
            } else if (this.gameState == 5) {
              this.answerMessage = `That's the end!`;
              this.returnButton = true;
            }
          }
        },
        async addGuess(answerNo) {
          // console.log(answerNo);
          const guess_dict = {
            'game': this.gameId,
            'answer': answerNo,
            'uuidp': this.$store.state.uuidp,
          }
          const url = `${this.myVar}guess/`;
          const response = await fetch(url, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json; charset=UTF-8',
            },
            body: JSON.stringify(guess_dict),
          });

          this.status = response.status;
          const response_json = await response.json();
          if (response.status == 201) {
            this.error = false;
            this.info = true;
            // console.log(response_json.answer)
            this.info_message = `Your answer has been selected!`;
            // console.log(this.info_message)
          } else if (response.status == 403) {
            this.info = false
            this.error = true;
            this.error_message = response_json;
          } else {
            console.log('Error');
            this.info = false;
            this.error = true;
          }
      },
      returnToHome() {
        this.$router.push({ name: 'joinGame' });
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
  