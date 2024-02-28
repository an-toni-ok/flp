import { createRouter, createWebHashHistory } from "vue-router";

import Planning from "../src/components/Planning/Planning.vue";
import Tutorial from "../src/components/Tutorial.vue";
import Methodology from "../src/components/Methodology.vue"
import Contact from "../src/components/Contact.vue";

const router = createRouter({
    history: createWebHashHistory(),
    routes: [
        {
            path: "/",
            name: "index",
            component: Planning,
        },
        {
            path: "/tutorial",
            name: "tutorial",
            component: Tutorial,
        },
        {
            path: "/methodik",
            name: "methodik",
            component: Methodology,
        },
        {
            path: "/kontakt",
            name: "kontakt",
            component: Contact,
        }
    ]
});

export default router;