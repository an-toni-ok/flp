import { createApp } from 'vue';
import './style.css';
import App from './App.vue';
import router from '../router/routes';
import { createPinia } from 'pinia';
import { library } from '@fortawesome/fontawesome-svg-core';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { fas } from '@fortawesome/free-solid-svg-icons';
import { far } from '@fortawesome/free-regular-svg-icons';
import VueKonva from 'vue-konva';
import PrimeVue from 'primevue/config';

library.add(fas);
library.add(far);
const pinia = createPinia();

createApp(App).component('font-awesome-icon', FontAwesomeIcon).use(router).use(pinia).use(VueKonva).use(PrimeVue).mount('#app');