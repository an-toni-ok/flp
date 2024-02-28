<script setup>
import { computed, onMounted, onUnmounted, ref } from "vue";
import { useAreaStore } from "../../../store/areas";
import { useCanvasStore } from "../../../store/canvas";
import PlanningInputColumn from "./PlanningInputColumn.vue";
import PlanningTooltip from "./PlanningTooltip.vue";
import Modal from "../Modal.vue";
import Notification from "../Notification.vue";
import OutOfBoundsError from "../../class/OutofBoundsError";
import IntersectionError from "../../class/IntersectionError";

const areaStore = useAreaStore();
const canvasStore = useCanvasStore();

const areas = ref(areaStore.areas);
const restrictedAreas = ref(areaStore.restrictedAreas);
const areaRects = ref([]);
const restrictedAreaRects = ref([]);
const areaRectRefs = ref([]);
const areaTextRefs = ref([]);
const groupRefs = ref([]);
const draggingGroup = ref();
const modalActive = ref(false);
const modalHeaderText = ref("");
const modalConfirmText = ref("");
const modalAreaIndex = ref([{ index: 1 }]);
const notificationActive = ref(false);
const notificationMessage = ref("");
const stage = ref();
const rectLayer = ref();
const tooltipText = ref("");
const tooltipVisible = ref(false);
const tooltipPos = ref({ x: 0, y: 0 });
const inputColumns = areaStore.areaInputColumns;
const CANVAS_SIZE = canvasStore.CANVAS_SIZE;
let draggedNode;
let editedNode;
let editedNodeIndex;
let editedNodeGroupIndex;
let beforeDragPos = { x: 0, y: 0 };
let startPos = { x: 0, y: 0 };
let allStartPos = [];
let currentModalType = {};

// List for selecting an area when creating a restricted area
const areaIndexList = computed(() => {
  const indexList = [];
  for (const [index] of areas.value.entries()) {
    indexList.push(index + 1);
  };
  return indexList;
});

// Set canvas size
const configKonva = {
  width: CANVAS_SIZE.width,
  height: CANVAS_SIZE.height,
};

const modalTypes = {
  newArea: {
    headerText: "Neue Freifläche erstellen",
    confirmText: "Freifläche erstellen",
  },
  editArea: {
    headerText: "Freifläche bearbeiten",
    confirmText: "Änderungen übernehmen"
  },
  newRestrictedArea: {
    headerText: "Neue Sperrfläche erstellen",
    confirmText: "Sperrfläche erstellen"
  },
  editRestrictedArea: {
    headerText: "Sperrfläche bearbeiten",
    confirmText: "Änderungen übernehmen"
  }
};

// Return an empty space for the modal
const emptySpace = () => {
  return [{
    width: null,
    height: null
  }];
};

const modalSpace = ref(emptySpace());

// Show or hide the modal
const toggleModal = (type) => {
  // Show notification with error message when the user tries to
  // add a restricted area and no area exists
  if (type === modalTypes.newRestrictedArea && !areas.value.length) {
    notificationMessage.value = "Ohne eine Freifläche kann keine Sperrfläche erstellt werden!";
    toggleNotification();
    return;
  };

  modalActive.value = !modalActive.value;
  let sleepTime = 0;

  if (!modalActive.value) {
    sleepTime = 300;
  };

  if (type !== undefined) {
    modalHeaderText.value = type.headerText;
    modalConfirmText.value = type.confirmText;
  };

  setTimeout(() => {
    let editedSpace = null;

    if (type === modalTypes.editArea) {
      editedSpace = areas.value[editedNodeIndex];
    } else if (type === modalTypes.editRestrictedArea) {
      editedSpace = restrictedAreas.value[editedNodeGroupIndex][editedNodeIndex];
    };

    if (editedSpace !== null) {
      modalSpace.value = [{
        width: editedSpace.width,
        height: editedSpace.height
      }];
    } else {
      modalSpace.value = emptySpace();
    };

    currentModalType = type;
  }, sleepTime);
};

const toggleNotification = () => {
  notificationActive.value = !notificationActive.value;
};

// Check if a konva node is in a vue ref array, and if so return its index
const isNodeInRefArray = (node, refArray) => {
  let nodeIndex = null;
  for (const [index, ref] of refArray.value.entries()) {
    const refNode = ref.getNode();
    if (node === refNode) {
      nodeIndex = index;
      break;
    };
  };
  return nodeIndex;
};

// Set y position of the new area so it appears under the lowest area
const newArea = (width, height) => {
  const index = areas.value.length - 1;
  let yPos = 0;
  let xPos = 0;

  if (index > -1) {
    for (const space of areas.value) {
      if (space.y + space.height > yPos) {
        xPos = space.x;
        yPos = space.y + space.height;
      };
    };
  };

  return {
    x: xPos,
    y: yPos,
    width: width,
    height: height
  };
};

// Create a numbered rectangle to represent an area on the canvas
const createAreaRect = async (space, index) => {
  const width = space.width * canvasStore.areaPixelsPerMeter;
  const height = space.height * canvasStore.areaPixelsPerMeter;
  let text = index;
  if(height < 30) {
    text = "";
  };

  return {
    groupConfig: {
      x: space.x * canvasStore.areaPixelsPerMeter,
      y: space.y * canvasStore.areaPixelsPerMeter,
      width: width,
      height: height,
      draggable: true,
      name: 'group'
    },
    rectConfig: {
      width: width,
      height: height,
      fill: '#f30147',
      stroke: 'black',
      strokeWidth: 2,
      draggable: false,
    },
    textConfig: {
      x: 0,
      y: 0,
      width: width,
      height: height,
      text: text,
      fontFamily: 'Calibri',
      fontSize: 30,
      align: 'center',
      verticalAlign: 'middle',
    }
  };
};

// Load rectangles of areas and restricted areas to render them on the canvas
const loadRectangles = async () => {
  for (const [areaIndex, space] of areas.value.entries()) {
    areaRects.value.push(await (createAreaRect(space, areaIndex + 1)));

    restrictedAreaRects.value.push([]);

    for (const restrictedArea of restrictedAreas.value[areaIndex]) {
      restrictedAreaRects.value[areaIndex].push(await (canvasStore.createRestrictedAreaRect(restrictedArea, canvasStore.areaPixelsPerMeter, true)));
    };
  };
};

// Add new area to the canvas
const addArea = async (size) => {
  await (updateCanvas());
  const space = newArea(size.width, size.height);
  areas.value.push(space);
  restrictedAreas.value.push([]);

  await (createAreaRect(space, areaRects.value.length + 1).then((value) => {
    areaRects.value.push(value);
  }));

  await (constructGroups()).then(async () => {
    await (scaleCanvas());
  });
};

// Update the size of an area
const editArea = async (size, index) => {
  await (updateCanvas());
  const space = areas.value[index];
  // Size in pixels
  const nodeSize = {
    width: size.width * canvasStore.areaPixelsPerMeter,
    height: size.height * canvasStore.areaPixelsPerMeter
  };
  const rectRefNode = areaRectRefs.value[index].getNode();
  const textRefNode = areaTextRefs.value[index].getNode();
  const groupRefNode = groupRefs.value[index].getNode();
  const deltaX = nodeSize.width - groupRefNode.width();
  const deltaY = nodeSize.height - groupRefNode.height();

  // Push/Pull areas right of or below the edited area and
  // resize the edited area
  await (new Promise((resolve, reject) => {
    for (const [groupIndex, group] of groupRefs.value.entries()) {
      const node = group.getNode();
      const absolutePos = node.getAbsolutePosition();

      const groupSpace = areas.value[groupIndex];
      const newXPos = absolutePos.x + deltaX;
      const newYPos = absolutePos.y + deltaY;

      if (checkRight(space, groupSpace)) {
        groupSpace.x = newXPos / canvasStore.areaPixelsPerMeter;
        node.x(newXPos);
      };

      if (checkBelow(space, groupSpace)) {
        groupSpace.y = newYPos / canvasStore.areaPixelsPerMeter;
        node.y(newYPos);
      };
    };
    space.width = size.width;
    space.height = size.height;

    groupRefNode.size(nodeSize);
    rectRefNode.size(nodeSize);
    textRefNode.size(nodeSize);

    resolve();
  }));

  await (scaleCanvas());

  // Throw error if restricted areas inside the area don't fit any longer
  await (checkInsideArea(index));

  // Throw error if areas intersect because of repositioning
  const groupArr = stage.value.getNode().find('.group');
  await (updateAllStartPos());
  const checkedDirection = await (checkAllPositions(groupArr, CANVAS_SIZE));
  if (checkedDirection !== 'both') {
    throw new IntersectionError("Freiflächen");
  };

  await (updateCanvas());
};

// Delete the edited area
const deleteArea = async () => {
  areas.value.splice(editedNodeIndex, 1);
  restrictedAreas.value.splice(editedNodeIndex, 1);

  toggleModal();
  await (updateCanvas()).then(() => {
    scaleCanvas();
  });
};

// Check if any restricted area inside an area is outside of its bounds,
// and throw an error if that should be true
// This is a necessary check if the size of an area is reduced
const checkInsideArea = async (groupIndex) => {
  const groupNode = groupRefs.value[groupIndex].getNode();
  const restrictedNodes = groupNode.find(".restrictedArea");
  const boundingRect = canvasStore.nodeWithAbsolutePosition(groupNode);

  for (const node of restrictedNodes) {
    const absoluteNode = canvasStore.nodeWithAbsolutePosition(node);
    if (!canvasStore.isInBounds(absoluteNode, boundingRect)) {
      throw new OutOfBoundsError("Sperrfläche");
    };
  };
};

// Throw error if restricted area doesn't fit in it's bounding area,
// or if restricted areas inside the bounding area intersect
const checkRestrictedArea = async (groupIndex, index) => {
  let node = null;
  const groupNode = groupRefs.value[groupIndex].getNode();
  const restrictedNodes = groupNode.find(".restrictedArea");

  if (index === undefined) {
    node = restrictedNodes[restrictedNodes.length - 1];
  } else {
    node = restrictedNodes[index];
  };

  const absoluteNode = canvasStore.nodeWithAbsolutePosition(node);
  const boundingRect = canvasStore.nodeWithAbsolutePosition(groupNode);

  if (!canvasStore.isInBounds(absoluteNode, boundingRect)) {
    throw new OutOfBoundsError("Sperrfläche");
  } else {
    const checkedDirection = await (canvasStore.checkPosition(node, node.absolutePosition(), restrictedNodes, boundingRect));

    if (checkedDirection !== 'both') {
      throw new IntersectionError("Sperrflächen");
    };
  };
};

// Add new restricted area to an area
const addRestrictedArea = async (size, groupIndex) => {
  const space = { x: 0, y: 0, width: size.width, height: size.height };
  restrictedAreas.value[groupIndex].push(space);

  await (updateCanvas());
  await (checkRestrictedArea(groupIndex));
};

// Update the size of a restricted area
const editRestrictedArea = async (size, groupIndex, index) => {
  await (updateCanvas());
  const area = restrictedAreas.value[groupIndex][index];
  area.width = size.width;
  area.height = size.height;

  await (updateCanvas());
  await (checkRestrictedArea(groupIndex, index));
};

// Delete the edited restricted area
const deleteRestrictedArea = async () => {
  restrictedAreas.value[editedNodeGroupIndex].splice(editedNodeIndex, 1);

  toggleModal();
  await (updateCanvas());
};

const updateLineGuides = (e) => {
  const node = e.target;
  // Do nothing if all areas are being dragged
  if (node.hasName("draggingGroup")) {
    return;
  };

  const stageNode = stage.value.getNode();
  const nodeArr = stageNode.find('.group');

  if (node.hasName("restrictedArea")) {
    const restrictedNodeArr = stageNode.find('.restrictedArea');
    for (const restrictedNode of restrictedNodeArr) {
      nodeArr.push(restrictedNode);
    };
  };

  canvasStore.updateLineGuides(node, nodeArr);
};

// Check if rectangle 2 is above rectangle 1
const checkAbove = (r1, r2) => {
  return (
    r2.y + r2.height <= r1.y &&
    r2.x <= r1.x + r1.width &&
    r2.x + r2.width >= r1.x
  );
};

// Check if rectangle 2 below rectangle 1
const checkBelow = (r1, r2) => {
  return (
    r2.y >= r1.y + r1.height &&
    r2.x <= r1.x + r1.width &&
    r2.x + r2.width >= r1.x
  );
};

// Check if rectangle 2 is to the right of rectangle 1
const checkRight = (r1, r2) => {
  return (
    r2.x >= r1.x + r1.width &&
    r2.y <= r1.y + r1.height &&
    r2.y + r2.height >= r1.y
  );
};

// Check if rectangle 2 is to the left of rectangle 1
const checkLeft = (r1, r2) => {
  return (
    r2.x + r2.width <= r1.x &&
    r2.y <= r1.y + r1.height &&
    r2.y + r2.height >= r1.y
  );
};

// Determine the appropriate scaling and adjust the current scaling
// of the canvas accordingly, based on the size and position of the canvas nodes
const scaleCanvas = async () => {
  // Check if the scale is too small
  while (!allInCanvas()) {
    if (canvasStore.currentScale >= canvasStore.CANVAS_SCALES.length - 1) {
      throw new OutOfBoundsError("Freifläche");
    };
    await (updateCanvas(canvasStore.currentScale + 1));

    if (draggedNode !== undefined) {
      draggedNode.stopDrag();
    };
  };

  // Check if the scale is too large
  while (couldFitSmallerScale()) {
    await (updateCanvas(canvasStore.currentScale - 1));

    if (draggedNode !== undefined) {
      draggedNode.stopDrag();
    };
  };
};

// Check if all group nodes are fully inside the canvas
const allInCanvas = () => {
  for (const group of groupRefs.value) {
    const absoluteNode = canvasStore.nodeWithAbsolutePosition(group.getNode());
    if (!canvasStore.isInBounds(absoluteNode, CANVAS_SIZE)) {
      return false;
    };
  };

  return true;
};

// Take a rectangle and scale, return same rectangle in that scale
const scaleNode = (node, scale) => {
  const ratio = (1 / canvasStore.areaPixelsPerMeter) * canvasStore.CANVAS_SCALES[scale];

  return {
    x: node.x * ratio,
    y: node.y * ratio,
    width: node.width * ratio,
    height: node.height * ratio
  };
};

// Check if all group nodes could fit in the next smaller scale of the canvas
const couldFitSmallerScale = () => {
  if (canvasStore.currentScale <= 0) {
    return false;
  };

  for (const group of groupRefs.value) {
    const absoluteNode = canvasStore.nodeWithAbsolutePosition(group.getNode());
    const scaledNode = scaleNode(absoluteNode, canvasStore.currentScale - 1);

    if (!canvasStore.isInBounds(scaledNode, CANVAS_SIZE)) {
      return false;
    };
  };
  return true;
};

// Check for all nodes in an array if their new position is allowed and return allowed direction
const checkAllPositions = async (nodeArr, boundingRect) => {
  let allowedArr = [];

  for (const [index, node] of nodeArr.entries()) {
    allowedArr.push(await (canvasStore.checkPosition(node, allStartPos[index], nodeArr, boundingRect)));
  };

  if (
    allowedArr.includes(null) ||
    (allowedArr.includes("horizontal") &&
      allowedArr.includes("vertical"))
  ) {
    return null;
  } else if (allowedArr.includes("horizontal")) {
    return "horizontal";
  } else if (allowedArr.includes("vertical")) {
    return "vertical";
  } else if (allowedArr.includes("both")) {
    return "both";
  };
};

const updateAllStartPos = async () => {
  allStartPos = [];
  for (const group of groupRefs.value) {
    allStartPos.push(group.getNode().absolutePosition());
  };
};

// Show a modal for editing an area when doubleclicking on one
const areaDoubleClick = (e) => {
  editedNode = e.target;
  editedNodeIndex = isNodeInRefArray(editedNode, areaTextRefs);
  toggleModal(modalTypes.editArea);
};

// Show a modal for editing a restricted area when doubleclicking on one
const restrictedAreaDoubleClick = (e) => {
  editedNode = e.target;
  for (const [groupIndex, group] of groupRefs.value.entries()) {
    const areas = group.getNode().find(".restrictedArea");
    for (const [areaIndex, area] of areas.entries()) {
      if (e.target === area) {
        editedNodeGroupIndex = groupIndex;
        editedNodeIndex = areaIndex;
      };
    };
  };
  toggleModal(modalTypes.editRestrictedArea);
};

const handleDragstart = (e) => {
  draggedNode = e.target;
  startPos = e.target.absolutePosition();
  beforeDragPos.x = startPos.x;
  beforeDragPos.y = startPos.y;

  if (canvasStore.dragAll && !e.target.hasName("restrictedArea")) {
    updateAllStartPos();
  } else {
    allStartPos = [];
  };

  hideTooltip();
};

// Check if the new position of the dragged node is allowed
// and if not reset the position
const handleDragmove = async (e) => {
  const node = e.target;
  const groupArr = stage.value.getNode().find('.group');
  const oldStartPos = startPos;
  let newStartPos = oldStartPos;

  // If dragging all areas
  if (canvasStore.dragAll && !node.hasName("restrictedArea")) {
    await (checkAllPositions(groupArr, CANVAS_SIZE)).then(async (allowedDirection) => {
      if (allowedDirection !== null) {

        switch (allowedDirection) {
          case "both":
            newStartPos.x = node.x();
            newStartPos.y = node.y();
            break;
          case "horizontal":
            newStartPos.x = node.x();
            node.y(oldStartPos.y);
            break;
          case "vertical":
            node.x(oldStartPos.x);
            newStartPos.y = node.y();
        };

        for (const group of groupArr) {
          await (canvasStore.setPosition(group, oldStartPos, allowedDirection, groupArr, areas.value, canvasStore.areaPixelsPerMeter, true));
        };

      } else {
        node.x(oldStartPos.x);
        node.y(oldStartPos.y);
      };

      updateAllStartPos();
    });
    // If dragging a single area
  } else if (!node.hasName("restrictedArea")) {
    await (canvasStore.checkPosition(node, oldStartPos, groupArr, CANVAS_SIZE)).then(async (allowedDirection) => {
      newStartPos = await (canvasStore.setPosition(node, oldStartPos, allowedDirection, groupArr, areas.value, canvasStore.areaPixelsPerMeter));
    });
    // If dragging a restricted area
  } else {
    const groupNode = node.findAncestor('.group');
    const boundingRect = canvasStore.nodeWithAbsolutePosition(groupNode);
    const groupNodeIndex = isNodeInRefArray(groupNode, groupRefs);
    const nodeArr = groupNode.find('.restrictedArea');
    const spaceArr = restrictedAreas.value[groupNodeIndex];

    await (canvasStore.checkPosition(node, oldStartPos, nodeArr, boundingRect)).then(async (allowedDirection) => {
      newStartPos = await (canvasStore.setPosition(node, oldStartPos, allowedDirection, nodeArr, spaceArr, canvasStore.areaPixelsPerMeter));
    });
  };

  startPos = newStartPos;

  scaleCanvas();
};

// After dragging a single area around snap areas together if possible
const handleDragend = async (e) => {
  // Don't do anything if there is only one area of if a restricted area is being dragged
  if (
    areas.value.length <= 1 ||
    groupRefs.value.length === 0 ||
    e.target.hasName("restrictedArea")
  ) {
    return;
  };

  const node = e.target;
  const absoluteNode = canvasStore.nodeWithAbsolutePosition(node);
  let closestPosition = null;

  // Look for areas directly above, below, to the right and to the left
  // of the dragged rectangle
  await (new Promise((resolve, reject) => {
    groupRefs.value.forEach((group) => {
      const groupNode = group.getNode();
      // Don't check position with itself
      if (node === groupNode) {
        return;
      };

      const position = { distance: null, isHorizontal: false };
      const absoluteGroup = canvasStore.nodeWithAbsolutePosition(groupNode);

      if (checkAbove(absoluteNode, absoluteGroup)) {
        position.distance = (absoluteGroup.y + absoluteGroup.height) - absoluteNode.y;
      } else if (checkBelow(absoluteNode, absoluteGroup)) {
        position.distance = absoluteGroup.y - (absoluteNode.y + absoluteNode.height);
      } else if (checkLeft(absoluteNode, absoluteGroup)) {
        position.distance = (absoluteGroup.x + absoluteGroup.width) - absoluteNode.x;
        position.isHorizontal = true;
      } else if (checkRight(absoluteNode, absoluteGroup)) {
        position.distance = absoluteGroup.x - (absoluteNode.x + absoluteNode.width);
        position.isHorizontal = true;
      };

      // Find closest possible snapping position
      if (position.distance !== null) {
        if (closestPosition === null) {
          closestPosition = position;
        } else if (Math.abs(closestPosition.distance) > Math.abs(position.distance)) {
          closestPosition = position;
        };
      };
    });
    resolve();
  })).then(() => {
    // Snap positions of the dragged area if possible, otherwise reset 
    // position of the area to the position prior to dragging it
    const groupIndex = isNodeInRefArray(node, groupRefs);
    const space = areas.value[groupIndex];

    if (closestPosition === null) {
      node.absolutePosition(beforeDragPos);
    } else if (closestPosition.isHorizontal) {
      node.x(node.x() + closestPosition.distance);
    } else {
      node.y(node.y() + closestPosition.distance);
    };

    space.x = node.x() / canvasStore.areaPixelsPerMeter;
    space.y = node.y() / canvasStore.areaPixelsPerMeter;
  });
};

const handleModalConfirm = async () => {
  const space = modalSpace.value[0];

  const startAreas = JSON.parse(JSON.stringify(areas.value));
  const startRestrictedAreas = JSON.parse(JSON.stringify(restrictedAreas.value))

  // Don't add an area without height or width,
  // also show the user an error message
  if (
    space.width === null ||
    space.width < 1 ||
    space.height === null ||
    space.height < 1
  ) {
    notificationMessage.value = "Breite und Länge müssen mindestens 1 m groß sein!";
    toggleNotification();
    return;
  };

  try {
    switch (currentModalType) {
      case (modalTypes.newArea):
        await (addArea(space));
        break;
      case (modalTypes.editArea):
        await (editArea(space, editedNodeIndex));
        break;
      case (modalTypes.newRestrictedArea):
        await (addRestrictedArea(space, modalAreaIndex.value[0].index - 1));
        break;
      case (modalTypes.editRestrictedArea):
        await (editRestrictedArea(space, editedNodeGroupIndex, editedNodeIndex));
        break;
    };
    toggleModal();
  } catch (error) {
    areas.value = startAreas;
    restrictedAreas.value = startRestrictedAreas;

    await (updateCanvas()).then(async () => {
      await (scaleCanvas());
    });

    if (
      error instanceof OutOfBoundsError ||
      error instanceof IntersectionError
    ) {
      notificationMessage.value = error.message;
      toggleNotification();
    } else {
      console.log(error);
    };
  };
};

// Put all rectangles in a group for dragging them all at once, or
// move them back to the rectangle layer of the canvas for dragging them
// individually, depending on the current dragging mode
const constructGroups = async () => {
  const dragNode = draggingGroup.value.getNode();

  if (canvasStore.dragAll) {
    for (const group of groupRefs.value) {
      const node = group.getNode();
      node.draggable(false);
      dragNode.position({ x: 0, y: 0 });
      dragNode.add(node);
    };
  } else {
    for (const group of groupRefs.value) {
      const node = group.getNode();
      const pos = node.getAbsolutePosition();

      node.moveTo(rectLayer.value.getNode());
      node.position(pos);
      node.draggable(true);
    };
    dragNode.removeChildren();
  };
};

// Toggle whether all areas or only one is being dragged at a time
const toggleDraggingMode = async () => {
  await (new Promise((resolve, reject) => {
    canvasStore.toggleDraggingMode()
    resolve();
  }));
  updateCanvas();
};

// Set the canvas scale and renders rectangles
const updateCanvas = async (scale) => {
  areaRects.value = [];
  restrictedAreaRects.value = [];

  if (scale !== undefined && scale >= 0 && scale < canvasStore.CANVAS_SCALES.length) {
    canvasStore.currentScale = scale;
  };

  await (loadRectangles()).then(() => {
    constructGroups();
  });
};

// Update tooltip when mouse hovers over an area
const updateTooltip = async (e) => {
  const mousePos = stage.value.getNode().getPointerPosition();
  const node = e.target;
  let text = "";

  tooltipPos.value = {
    x: mousePos.x + 20,
    y: mousePos.y
  };

  const nodeIndex = isNodeInRefArray(node, areaTextRefs);
  if (nodeIndex !== null) {
    text = text.concat("Freifläche ", nodeIndex + 1, ": \n\n", "Breite (x): ", areas.value[nodeIndex].width, " m\n",
      "Länge (y): ", areas.value[nodeIndex].height, " m");
  };

  tooltipText.value = text;
  tooltipVisible.value = true;
};

const hideTooltip = () => {
  tooltipVisible.value = false;
};

onMounted(() => {
  areas.value = areaStore.areas;
  restrictedAreas.value = areaStore.restrictedAreas;
  updateCanvas();
});

onUnmounted(() => {
  areaStore.areas = areas.value;
  areaStore.restrictedAreas = restrictedAreas.value;
});
</script>

<template>
  <div class="content">
    <div class="canvas-container">
      <v-stage :config="configKonva" ref="stage">
        <v-layer @dragmove="updateLineGuides" @dragend="canvasStore.lineGuides = []" ref="rectLayer">
          <!--Group for dragging everything at once-->
          <v-group ref="draggingGroup" :config="{ draggable: true, x: 0, y: 0, name: 'draggingGroup' }"
            @dragstart="handleDragstart" @dragmove="handleDragmove"></v-group>

          <!--Visual representations of areas-->
          <v-group v-for="(item, index) in areaRects" :key="item.id" :config="item.groupConfig" ref="groupRefs"
            @dragstart="handleDragstart" @dragmove="handleDragmove" @dragend="handleDragend">
            <v-rect :config="item.rectConfig" ref="areaRectRefs"></v-rect>
            <v-text :config="item.textConfig" ref="areaTextRefs" @mousemove="updateTooltip" @mouseout="hideTooltip"
              @dblclick="areaDoubleClick"></v-text>
            <v-rect v-for="restrictedArea in restrictedAreaRects[index]" :config="restrictedArea.config"
              @dblclick="restrictedAreaDoubleClick"></v-rect>
          </v-group>
          <v-line v-for="item in canvasStore.lineGuides" :config="item"></v-line>
        </v-layer>
        <PlanningTooltip :text="tooltipText" :visible="tooltipVisible" :position="tooltipPos"></PlanningTooltip>
      </v-stage>
    </div>
    <div class="button-container">
      <button class="planning-button" @click="toggleModal(modalTypes.newArea)">
        Freifläche hinzufügen
      </button>
      <button class="planning-button" @click="toggleModal(modalTypes.newRestrictedArea)">
        Sperrfläche hinzufügen
      </button>
      <button class="planning-button" @click="toggleDraggingMode">
        {{ canvasStore.draggingButtonText }}
      </button>
    </div>
    <Modal @close="toggleModal" :modalActive="modalActive">
      <div class="modal-content">
        <h2 class="headline">{{ modalHeaderText }}</h2>
        <div class="row" v-if="currentModalType === modalTypes.newRestrictedArea">
          <PlanningInputColumn title="Freifläche" type="select" :selectList="areaIndexList" :list="modalAreaIndex"
            value="index" unit=""></PlanningInputColumn>
        </div>
        <div class="row">
          <PlanningInputColumn v-for="item in inputColumns" :key="item.id" :title="item.title" :type="item.type"
            :list="modalSpace" :value="item.value" :placeholder="item.placeholder" :unit="item.unit" :min="item.min"
            :max="item.max">
          </PlanningInputColumn>
        </div>
        <div class="modal-footer">
          <button v-if="currentModalType === modalTypes.editArea" @click="deleteArea"
            class="planning-button modal-button">Freifläche entfernen</button>
          <button v-if="currentModalType === modalTypes.editRestrictedArea" @click="deleteRestrictedArea"
            class="planning-button modal-button">Sperrfläche entfernen</button>
          <button @click="handleModalConfirm" class="planning-button modal-button">{{ modalConfirmText }}</button>
        </div>
      </div>
    </Modal>
    <Notification @close="toggleNotification" :notificationActive="notificationActive" :message="notificationMessage">
    </Notification>
  </div>
</template>

<style lang="scss" scoped>
.content .canvas-container {
  width: max-content;
  height: max-content;
}

.button-container {
  width: max-content;
  align-items: center;
  display: flex;
  flex-direction: column;
  margin-left: 50px;
  margin-right: 50px;

  .planning-button {
    width: 300px;
    margin-bottom: 20px;
  }
}

.modal-button {
  margin-right: 5px;
  margin-left: 5px;
}
</style>