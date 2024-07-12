<script setup>
defineProps(['active'])

import IconLogo from './icons/IconLogo.vue';
import IconArrowsRight from './icons/IconArrowsRight.vue';
import IconHistory from './icons/IconHistory.vue';
import IconInformation from './icons/IconInformation.vue';
import IconPlanning from './icons/IconPlanning.vue';
import IconMethods from './icons/IconMethods.vue';
import IconContact from './icons/IconContact.vue';
import { ref } from 'vue';

const opened = ref(false);

</script>

<template>
    <nav class="nav-spacing">
        <ul class="links">
            <li>
                <a class="nav-link" href="">
                    <IconPlanning />
                    <span v-show="opened">Planung</span>
                </a>
            </li>
            <li>
                <a class="nav-link" href="">
                    <IconHistory />
                    <span v-show="opened">Verlauf</span>
                </a>
            </li>
            <li>
                <a class="nav-link" href="">
                    <IconInformation />
                    <span v-show="opened">Informationen</span>
                </a>
            </li>
            <li>
                <a class="nav-link" href="">
                    <IconMethods />
                    <span v-show="opened">Methodik</span>
                </a>
            </li>
            <li>
                <a class="nav-link" href="">
                    <IconContact />
                    <span v-show="opened">Kontakt</span>
                </a>
            </li>
        </ul>
        <div class="interaction">
            <IconLogo />
            <IconArrowsRight 
                @click="opened = !opened" 
                :class="opened ? 'rotate' : ''" />
        </div>
    </nav>
</template>

<style scoped>
@import '@/assets/base.css';

.rotate {
    transform: rotate(180deg);
}

nav {
    height: 100vh;
    display: inline-flex;
    flex-direction: column;
    justify-content: space-between;
    --nav-padding: 25px;
    padding: 0 var(--nav-padding);
    border-right: 1px solid var(--color-border);
    align-self: flex-start;
}

.links {
    padding: 0;
    margin: 0;
}

.links > li {
    list-style-type: none;
}

.nav-link {
    text-decoration: none;
    color: var(--color-text-primary);
    display: inline-flex;
    justify-content: flex-start;
    gap: 15px;
    align-items: center;
    margin-top: var(--nav-padding);
}

.nav-link > svg {
    height: 20px;
}

.nav-link > span {
    line-height: 1;
    padding-right: calc(0.5 * var(--nav-padding));
}

.nav-link:hover > span {
    border-bottom: 1px solid var(--color-brand);
}

.nav-link:hover > svg {
    fill: var(--color-brand);
}

.interaction {
    display: inline-flex;
    flex-direction: column;
    justify-content: flex-start;
    gap: var(--nav-padding);
    margin-bottom: var(--nav-padding);
    align-self: flex-start;
}

.interaction > svg {
    width: 20px;
}
</style>
