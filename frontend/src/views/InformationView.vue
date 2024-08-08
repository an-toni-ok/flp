<script setup>
import TextView from './TextView.vue';

const text = [
    "Lorem ipsum dolor sit amet consectetur adipisicing elit. Ex, magnam nobis deleniti voluptate sunt culpa explicabo quisquam, sed laborum laudantium, debitis obcaecati adipisci laboriosam sapiente corporis vel? Suscipit, minima quos.",
    "Lorem ipsum dolor sit amet consectetur adipisicing elit. Ex, magnam nobis deleniti voluptate sunt culpa explicabo quisquam, sed laborum laudantium, debitis obcaecati adipisci laboriosam sapiente corporis vel? Suscipit, minima quos."
]
</script>

<template>
    <TextView
        title="Informationen"
        :text-array="text" />
</template>

<style>
</style>