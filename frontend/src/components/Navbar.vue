<script setup>
import { ref } from 'vue';
import { NavLink } from '@/components/library/links';
import { IconButton } from '@/components/library/buttons'
import { IconLogo, IconArrowsRight, IconHistory, IconInformation, IconPlanning, IconMethods, IconContact } from '@/components/icons';

const opened = ref(false);
</script>

<template>
    <nav class="nav-spacing">
        <ul class="links">
            <NavLink name="Planung" :opened="opened" location="/">
                <IconPlanning />
            </NavLink>
            <NavLink name="Verlauf" :opened="opened" location="/history">
                <IconHistory />
            </NavLink>
            <NavLink name="Informationen" :opened="opened" location="/info">
                <IconInformation />
            </NavLink>
            <NavLink name="Methodik" :opened="opened" location="/methodik">
                <IconMethods />
            </NavLink>
            <NavLink name="Kontakt" :opened="opened" location="/contact">
                <IconContact />
            </NavLink>
        </ul>
        <div class="interaction">
            <IconLogo />
            <IconButton
                @click="opened = !opened" 
                :class="opened ? 'rotate' : ''"
                :no-border="true"
                text="Expand the navigation."
                tooltip-position="right"
                :borders="false"
                :small="true">
                <IconArrowsRight />
            </IconButton>
        </div>
    </nav>
</template>

<style scoped>
@import '@/assets/base.css';

.rotate {
    transform: rotate(180deg);
}

nav {
    height: 100%;
    display: inline-flex;
    flex-direction: column;
    justify-content: space-between;
    --nav-padding: 25px;
    border-right: 1px solid var(--color-border);
    align-self: flex-start;
    padding: var(--top-padding-width) 0;
}

.links {
    padding: 0;
    margin: 0;
}

.links > li {
    list-style-type: none;
}

.interaction {
    display: inline-flex;
    flex-direction: column;
    justify-content: flex-start;
    gap: var(--nav-padding);
    /* padding: 0 calc(var(--default-padding) * 2); */

    padding: 0 var(--base-padding-width);
    align-self: flex-start;
}

.interaction > :deep(button) {
    width: 20px;
    height: 20px;
}
</style>
