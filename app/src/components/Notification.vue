<script setup>
import Modal from './Modal.vue';

const props = defineProps({
    notificationActive: {
        type: Boolean,
        required: true,
    },
    message: {
        type: String,
        required: true,
    }
});

const emit = defineEmits(['close']);

const closeButtonClick = () => {
    emit('close');
};

</script>

<template>
    <Modal @close="closeButtonClick" :modalActive="notificationActive">
        <p>{{ message }}</p>
        <div class="modal-footer">
            <button @click="closeButtonClick" class="planning-button modal-button">Schließen</button>
        </div>
    </Modal>
</template>