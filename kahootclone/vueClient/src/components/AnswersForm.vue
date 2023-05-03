<template>
  <div class="answersform">
    <div id="formulario-persona">
      <div class="row2" v-for="answer in answers" :key="answer.value">
        <form @submit.prevent="enviarFormulario(answer.value)">
          <button :class="answer.class"></button>
        </form>
      </div>
      <div class="container">
        <div class="row">
          <div class="col-md-12">
            <div v-if="error" class="alert alert-danger" role="alert">
              {{ error_message }}
            </div>
            <div v-if="info">
              {{ info_message }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "game-form",
  data() {
    return {
      answers: [
        {
          value: 0,
          class: "answer1",
        },
        {
          value: 1,
          class: "answer2",
        },
        {
          value: 2,
          class: "answer3",
        },
        {
          value: 3,
          class: "answer4",
        },
      ],
    };
  },
  props: {
    error: {
      type: Boolean,
      default: false,
    },
    error_message: {
      type: String,
      default: "",
    },
    info: {
      type: Boolean,
      default: false,
    },
    info_message: {
      type: String,
      default: "",
    },
  },
  methods: {
    enviarFormulario(answerNo) {
      // this.resetEstado();
      // // // Comprobamos la presencia de errores

      // this.form_value = event.target.value;
      // // // console.log("Funcional")
      this.$emit("add-guess", answerNo);
      // // this.$refs.nombre.focus();
      // // Restablecemos el valor de la variables
      // console.log(answerNo);
    },
  },
};
</script>

<style scoped src="../assets/answersform.css">
/*@import '../assets/answersform.css' */
</style>
