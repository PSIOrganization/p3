import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import {createStore} from 'vuex'

import './assets/main.css'

const app = createApp(App)

const store = createStore({
    state(){
        return{
            uuidp: ''
        }
    },
    mutations: {
        storeparticipant(state, {uuidp}){
            state.uuidp = uuidp
        }
    }
})

app.use(router)
app.use(store)

app.mount('#app')

import '../node_modules/bootstrap/dist/js/bootstrap.js'
import '../node_modules/bootstrap/dist/css/bootstrap.min.css'

// store.commit('storeparticipant',{
//     'uuidp': 'value'
// });