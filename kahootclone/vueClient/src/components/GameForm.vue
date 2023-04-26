<template>
    <div id="formulario-persona">
        <h3>Join a Game!</h3>
        <form @submit.prevent="enviarFormulario">
            <div class="container">
                <div class="row">
                    <div class="col-md-4">
                        <div class="form-group">
                            <label>Alias </label>
                            <input 
                                ref="alias"
                                v-model="participant.alias" 
                                type="text" 
                            />
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="form-group">
                            <label>Game ID </label>
                            <input 
                                v-model="participant.game" 
                                type="text" 
                            />
                        </div>
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-4">
                        <div class="form-group">
                            <button class="btn btn-primary">Join</button>
                        </div>
                    </div>
                </div>
            </div>
            <div class="container">
    	        <div class="row">
                    <div class="col-md-12">
                        <div v-if="error" class="alert alert-danger" role="alert">
                            Yay
                        </div>
                    </div>
                </div>
            </div>
        </form>
    </div>
</template>

<script>
    export default {
        name: 'game-form',
        data() {
            return {
                participant: {
                    alias: '',
                    game: '',
                },
                error: false,
            }
        },
        props: {
            error: false,
        },
        methods: {
            enviarFormulario() {
                this.resetEstado();
                // // Comprobamos la presencia de errores

                // // console.log("Funcional")
                this.$emit('add-participant', this.participant);
                // this.$refs.nombre.focus();
                // Restablecemos el valor de la variables
                this.participant = {
                    alias: '',
                    game: '',
                }
            },
            resetEstado() {
                this.error = false;
            }
        },
    }
</script>

<style scoped>
    form {
        margin-bottom: 2rem;
    }
</style>
    