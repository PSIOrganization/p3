<template>
  <div class="gameform">
    <div id="formulario-persona">
      <h3>Join a Game!</h3>
      <form @submit.prevent="enviarFormulario">
        <div class="container">
          
            <div class="col-md-4">
              <div class="form-group">
                <label>Alias </label>
                <input ref="alias" v-model="participant.alias" type="text" />
              </div>
            </div>
            
            <div class="col-md-4">
              <div class="form-group">
                <label>Game ID </label>
                <input v-model="participant.game" type="text" />
              </div>
            </div>
              <div class="form-group">
                <button class="joinbutton">Join</button>
              </div>
        </div>
        <div class="container">
          <div class="row">
            <div class="col-md-12">
              <div v-if="error" class="alert alert-danger" role="alert">
                {{ error_message }}
              </div>
            </div>
          </div>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  name: "game-form",
  data() {
    return {
      participant: {
        alias: "",
        game: "",
      },
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
  },
  methods: {
    enviarFormulario() {
      // this.resetEstado();
      // // Comprobamos la presencia de errores

      // // console.log("Funcional")
      this.$emit("add-participant", this.participant);
      // this.$refs.nombre.focus();
      // Restablecemos el valor de la variables
      this.participant = {
        alias: "",
        game: "",
      };
    },
  },
};
</script>

<style scoped src="../assets/gameform.css">
/*@import '../assets/waiting.css' */
</style>
