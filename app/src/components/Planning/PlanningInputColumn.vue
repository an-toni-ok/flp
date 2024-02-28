<script setup>
import { computed } from "vue";
import { usePlanningStore } from "../../../store/planning";
import InputNumber from 'primevue/inputnumber';

const store = usePlanningStore();

const emit = defineEmits(['add', 'remove', 'push', 'pop']);

const addRow = () => {
  emit('add');
};

const removeRow = () => {
  emit('remove');
};

const arrayPush = () => {
  emit('push');
};

const arrayPop = () => {
  emit('pop');
};

const props = defineProps({
  title: {
    type: String,
    required: false,
  },
  type: {
    type: String,
    required: true,
  },
  list: {
    type: Array,
    required: false,
  },
  value: {
    type: String,
    required: false,
  },
  isArray: {
    type: Boolean,
    required: false,
    default: false
  },
  object: {
    type: Object,
    required: false,
  },
  selectList: {
    type: Array,
    required: false,
  },
  selectValue: {
    type: String,
    required: false,
  },
  placeholder: {
    type: String,
    required: false,
  },
  isPlaceholder: {
    type: Boolean,
    required: false,
    default: false,
  },
  isOutputMachine: {
    type: Boolean,
    required: false,
    default: false,
  },
  unit: {
    type: String,
    required: false,
  },
  longTextfield: {
    type: Boolean,
    required: false,
  },
  min: {
    type: Number,
    required: false,
  },
  max: {
    type: Number,
    required: false,
  },
});

const suffix = computed(() => " ".concat(props.unit));

const isOrder = computed(() => {
  if (props.value === "order") {
    return true;
  };
  return false;
});

const fractionDigits = computed(() => {
  if (props.value === "index") {
    return 0;
  } else {
    return 1;
  }
});
</script>

<template>
  <div class="input-column">
    <div v-if="props.title !== '' " class="input-title">
      <p>{{ props.title }}<span v-if="props.type !== 'button'">:</span></p>
      <input v-if="props.type === 'checkbox' && props.object !== undefined" type="checkbox"
        id="checkbox" v-model="props.object[props.value]" />
    </div>
    <div v-for="(item, index) in props.list" :key="item.id" class="input-element">
      <p v-if="props.type === 'output'" class="output-text-field" :class="{ order: isOrder, placeholder: props.isPlaceholder }">
        <span v-if="props.isArray == true">
          <span v-for="(arrayValue, arrayIndex) in item[props.value]">{{ arrayValue }}<span
              v-if="item[props.value].length !== arrayIndex + 1">, </span></span>
        </span>
        <span v-else> {{ store.formatNumber(item[props.value], props.unit) }} </span>
      </p>
      <div v-if="props.type === 'select'">
        <select v-model="item[props.value]" class="input-select" required>
          <option value="" disabled selected hidden>
            {{ props.placeholder }}
          </option>
          <option v-for="item in props.selectList" :key="item.id">
            {{ item }}
          </option>
        </select>
      </div>
      <div v-if="props.type === 'selectArray'" class="select-array-column">
        <div v-for="(arrayValue, arrayIndex) in item[props.value]" :key="arrayValue.id">
          <select v-model="item[props.value][arrayIndex]" class="input-select array-select" required>
            <option value="" disabled selected hidden>
              {{ props.placeholder }}
            </option>
            <option v-for="selectOption in props.selectList" :key="item.id" :value="selectOption">
              {{ selectOption }}
            </option>
          </select>
        </div>
        <div class="round-button-container">
          <button v-if="item[props.value].length < 10" class="round-button column-round-button" @click="arrayPush">
            <span class="round-button-text">+</span>
          </button>
          <button v-if="item[props.value].length > 1" class="round-button column-round-button" @click="arrayPop">
            <span class="round-button-text">-</span>
          </button>
        </div>
      </div>
      <div v-if="props.type === 'inputText'">
        <input class="input-field" v-model="item[value]" :class="{ long: props.longTextfield }"
          :placeholder="props.placeholder" />
      </div>
      <div v-if="props.type === 'inputNumber'">
        <InputNumber v-model="item[value]" :pt="{
          input: { class: 'input-field' }
        }" :placeholder="props.placeholder" :suffix="suffix" :max-fraction-digits="fractionDigits" :min="props.min" :max="props.max" ></InputNumber>
      </div>
      <div v-if="props.type === 'inputCurrency'">
        <InputNumber v-model="item[value]" :pt="{
          input: { class: 'input-field' }
        }" mode="currency" currency="EUR" locale="de-DE"
          :placeholder="props.placeholder" :min="props.min" :max="props.max"/>
      </div>
      <div v-if="props.type === 'button'" class="round-button-container">
        <button v-if="props.list.length === index + 1 || props.isPlaceholder" class="round-button" @click="addRow">
          <span class="round-button-text">+</span>
        </button>
        <button v-if="(props.list.length === index + 1 && index > 0) || (props.isOutputMachine && !props.isPlaceholder && props.list.length === 1)" class="round-button" @click="removeRow">
          <span class="round-button-text">-</span>
        </button>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.order {
  width: 1.5em;
  text-align: center;
}

.column-round-button {
  margin-left: 5px;
  margin-right: 5px;
}

.long {
  width: 28.5em;
}

.select-array-column {
  display: flex;
  flex-direction: column;
  justify-content: space-evenly;

  .array-select {
    margin-bottom: 15px;
  }
}

.placeholder {
  color: gray;
}

input[type="checkbox"] {
  width: 20px !important;
  height: 20px !important;
  margin-left: 15px;
  -webkit-appearance: none;
  -moz-appearance: none;
  -o-appearance: none;
  appearance: none;
  outline: 1px solid black;
  box-shadow: none;
  font-size: 1.1em;
  text-align: center;
  line-height: 1em;
  background: white;
}

input[type='checkbox']:checked:after {
  content: '✔';
  color: var(--tha-red)
}

</style>