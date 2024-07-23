<script setup>
import { computed, ref } from 'vue';
import IconArrowDown from '../icons/IconArrowDown.vue';
import IconButtonTable from '../Buttons/IconButtonTable.vue';
import ExpandableText from './ExpandableText.vue';

const props = defineProps({
    machine: {
        required: true,
    },
})

// const tech_open = ref(false)
// const show_tech_dropdown = computed(() => {
//         return props.machine.set_technologies.join(", ").length > 30
//     },
// )

// const formatted_techs = computed(() => {
//         var tech_text = props.machine.set_technologies.join(", ")
//         if (tech_open.value) {
//             return tech_text
//         }
//         if (tech_text.length < 30) {
//             return tech_text
//         }
//         return tech_text.slice(0, 26) + "..."
//     },
// )
</script>

<template>
    <tr>
        <td>
            <ExpandableText 
                help_text="Show all technologies"
                :text="machine.machine_type" />
        </td>
        <td>{{ machine.machine_hourly_cost }}</td>
        <td>{{ machine.investion_cost }}</td>
        <td>{{ machine.additional_machine_time }}</td>
        <td>{{ machine.breite }}</td>
        <td>{{ machine.laenge }}</td>
        <td>
            <ExpandableText 
                help_text="Show all technologies"
                :text="machine.set_technologies.join(', ')" />
        </td>
        <!-- <td>{{ machine.set_technologies }}</td> -->
        <td class="action">
            <div class="center">
                <slot></slot>
            </div>
        </td>
    </tr>
</template>

<style scoped>
.action {
    white-space: nowrap;
    width: fit-content;
}

.center {
    display: flex;
    justify-content: center;
}

tr > td {
    text-align: right;
}

tr > td:nth-child(1) {
    text-align: left;
    max-width: 30ch;
    word-wrap: break-word;
}
</style>