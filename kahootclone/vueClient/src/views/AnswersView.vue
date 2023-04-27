<template>
    <div id="answersForm">
        <answersForm @add-guess="addGuess"/>
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
          message: '',
        }
      },
      created() {
      },
      methods: {
        // ajax function every 2 seconds to get game
        // if game is started, redirect to game view
        // if game is not started, do nothing
        // if game is not found, redirect to home view
        async addGuess(participant) {
          console.log(participant);
          const url = `${this.myVar}participant/`;
          const response = await fetch(url, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(participant),
          });

          this.status = response.status;
          if (response.status == 201) {
            this.$router.push({ name: 'waitingGame', params: { gameId: participant.game } });
          } else if (response.status == 403) {
            this.error = true;
            this.error_message = 'Game not found';
          } else {
            console.log('Error');
            this.error = true;
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
  