<script setup>
const props = defineProps({
    modalActive: {
        type: Boolean,
        required: true,
    }
});

const emit = defineEmits(['close']);

const closeButtonClick = () => {
    emit('close');
}

</script>

<template>
    <Transition name="modal-animation">
        <div v-show="modalActive" class="modal">
            <Transition name="modal-animation-inner">
                <div v-show="modalActive" class="modal-inner">
                    <font-awesome-icon @click="closeButtonClick" class="close-icon" icon="fa-solid fa-circle-xmark" />
                    <slot />
                    <!--Modal Content-->
                </div>
            </Transition>
        </div>
    </Transition>
</template>

<style lang="scss" scoped >
.modal-animation-enter-active,
.modal-animation-leave-active {
    transition: opacity 0.3s cubic-bezier(0.52, 0.2, 0.19, 1.02);
}

.modal-animation-enter-from,
.modal-animation-leave-to {
    opacity: 0;
}

.modal-animation-inner-enter-active {
    transition: all 0.3s cubic-bezier(0.52, 0.2, 0.19, 1.02) 0.15s;
}

.modal-animation-inner-leave-active {
    transition: all 0.3s cubic-bezier(0.52, 0.2, 0.19, 1.02);
}

.modal-animation-inner-enter-from {
    opacity: 0;
    transform: scale(0.8);
}

.modal-animation-inner-leave-to {
    transform: scale(0.8);
}

.modal {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    width: 100vw;
    position: fixed;
    top: 0;
    left: 0;
    background-color: rgba(255, 255, 255, 0.7);
    z-index: 5;
    overflow: auto;

    .modal-inner {
        -webkit-box-shadow: inset 0px 0px 0px 1px black;
        -moz-box-shadow: inset 0px 0px 0px 1px black;
        box-shadow: inset 0px 0px 0px 1px black;
        position: relative;
        width: max-content;
        background-color: white;
        padding: 45px 16px;
        overflow: auto;
    }
}

.close-icon {
    position: absolute;
    top: 15px;
    right: 15px;
    font-size: 20px;
    cursor: pointer;

    &:hover {
        color: var(--tha-red);
    }
}
</style>