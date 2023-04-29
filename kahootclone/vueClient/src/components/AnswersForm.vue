<template>
    <div id="formulario-persona">
        <div class="row2" v-for="answer in answers" :key="answer.value">
            <form @submit.prevent="enviarFormulario(answer.value)">
                <button class="btn btn-primary">{{ answer.text }}</button>
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
            }
        },
        props: {
            error: false,
            error_message: '',
            info: false,
            info_message: '',
        },
        methods: {
            enviarFormulario(answerNo) {
                // this.resetEstado();
                // // // Comprobamos la presencia de errores

                // this.form_value = event.target.value;
                // // // console.log("Funcional")
                this.$emit('add-guess', answerNo);
                // // this.$refs.nombre.focus();
                // // Restablecemos el valor de la variables
                // console.log(answerNo);
            },
        },
    }
</script>

<style scoped>
    form {
        margin-bottom: 2rem;
    }
</style>
    