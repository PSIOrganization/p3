<template>
    <div id="formulario-persona">
        <h3>Question number _____ [poner]</h3>
        <form @submit.prevent="enviarFormulario">
            <div class="row2" v-for="answer in answers" :key="answer.value">
                <button type="submit" @click="enviarFormulario(answer.value)">{{ answer.text }}</button>
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
</template>

<script>
    export default {
        name: 'game-form',
        data() {
            return {
                answers: [
                    {
                        value: 0,
                        text: '1'
                    },
                    {
                        value: 1,
                        text: '2'
                    },
                    {
                        value: 2,
                        text: '3'
                    },
                    {
                        value: 3,
                        text: '4'
                    },
                ],
                answerNo: '',
                error: false,
                error_message: '',
            }
        },
        props: {
            error: false,
            error_message: '',
        },
        methods: {
            enviarFormulario(answerNo) {
                // this.resetEstado();
                // // // Comprobamos la presencia de errores

                // this.form_value = event.target.value;
                // // // console.log("Funcional")
                // this.$emit('add-guess', answerNo);
                // // this.$refs.nombre.focus();
                // // Restablecemos el valor de la variables
                // this.participant = {
                //     alias: '',
                //     game: '',
                // }
                console.log(answerNo);
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
    