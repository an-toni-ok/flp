<script setup>
const props = defineProps({
    name: {
        type: String,
        required: true
    },
    opened: {
        type: Boolean,
        required: true
    }
})
</script>

<template>
    <li>
        <a class="nav-link" href="">
            <!-- Icon goes here -->
            <slot></slot>
            <span v-show="opened">{{ name }}</span>
        </a>
    </li>
</template>

<style scoped>
.nav-link {
    text-decoration: none;
    color: var(--color-text-primary);
    display: flex;
    justify-content: flex-start;
    gap: 15px;
    align-items: center;
    margin-bottom: calc(var(--default-padding) / 2);
    padding: var(--default-padding) var(--base-padding-width);
}

.nav-link > * {
    height: 1rem;
}

.nav-link > span {
    font-size: 1rem;
    line-height: 1;
    padding-right: calc(0.5 * var(--nav-padding));
}

.nav-link:hover,
.nav-link:focus {
    border-top: 1px solid var(--color-border);
    border-bottom: 1px solid var(--color-border);
    padding-top: calc(var(--default-padding) - 1px);
    padding-bottom: calc(var(--default-padding) - 1px);
}

.nav-link:hover > *,
.nav-link:focus > * {
    fill: var(--color-brand);
}

.nav-link:hover > span,
.nav-link:focus > * {
    text-decoration: underline;
    text-decoration-color: var(--color-brand);
}
</style>