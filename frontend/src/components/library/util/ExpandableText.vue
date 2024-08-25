<script setup>
import { computed, ref } from 'vue';
import { IconButton } from '@/components/library/buttons';
import { IconArrowDown } from '@/components/icons';
const props = defineProps({
    text: {
        type: String,
        required: true
    },
    help_text: {
        type: String,
        required: true
    }
})

const dropdown_open = ref(false)
const show_dropdown = computed(() => {
        return props.text.length > 30
    },
)

const formatted_techs = computed(() => {
        if (dropdown_open.value) {
            return props.text
        }
        if (props.text.length < 30) {
            return props.text
        }
        return props.text.slice(0, 26) + "..."
    },
)
</script>

<template>
    <div 
        class="tech-display-container" 
        :class="{ 'open' : dropdown_open }" >
        <p>{{ formatted_techs }}</p>
        <IconButton v-if="show_dropdown"
            :text="props.help_text"
            tooltip-position="top"
            :borders="false"
            @click="dropdown_open = !dropdown_open">
            <IconArrowDown />
        </IconButton>
    </div>
</template>

<style scoped>
.tech-display-container {
    display: flex;
    align-items: center;
    justify-content: space-between;
    max-width: 15rem;
}

.tech-display-container > p {
    max-width: 12.5rem;
    text-wrap: wrap;
    word-wrap: break-word;
    text-align: left;
    padding-block: 0.25rem;
}

.tech-display-container > button > * {
    transform: rotate(0deg);
    transition: 200ms;
}

.open > button > * {
    transform: rotate(180deg);
    transition: 200ms;
}
</style>