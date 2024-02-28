<script setup>
import { computed, onMounted, onUnmounted, ref } from "vue";
import { usePlanningStore } from "../../../../store/store";
import { useCanvasStore } from "../../../../store/canvas";
import PlanningInputColumn from "./PlanningInputColumn.vue";
import PlanningTooltip from "./PlanningTooltip.vue";
import Modal from "../Modal.vue";

const planningStore = usePlanningStore();
const canvasStore = useCanvasStore();

const area = ref(planningStore.floorSpace);
const restrictedAreas = ref(planningStore.restrictedAreas);
const areaRects = ref([]);
const restrictedAreaRects = ref([]);
const areaRectRefs = ref([]);
const areaTextRefs = ref([]);
const lineGuides = ref([]);
const groupRefs = ref([]);
const draggingGroup = ref();
const modalActive = ref(false);
const modalHeaderText = ref("");
const modalConfirmText = ref("");
const modalFloorIndex = ref([{ index: 1 }]);
const stage = ref();
const rectLayer = ref();
const tooltipText = ref("");
const tooltipVisible = ref(false);
const tooltipPos = ref({ x: 0, y: 0 });
const inputColumns = planningStore.floorSpaceInputColumns;
const GUIDELINE_OFFSET = 5;
const CANVAS_SIZE = canvasStore.CANVAS_SIZE;
let draggedNode;
let editedNode;
let editedNodeIndex;
let editedNodeGroupIndex;
let beforDragPos = { x: 0, y: 0 };
let startPos = { x: 0, y: 0 };
let allStartPos = [];
let currentModalType = {};

// List for selecting a floor space when creating a restricted area
const areaIndexList = computed(() => {
  const indexList = [];
  for (const [index] of area.value.entries()) {
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
      editedSpace = area.value[editedNodeIndex];
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

// Set y position of the new floor space so it appears under the lowest floor space
const newArea = (width, height) => {
  const index = area.value.length - 1;
  let yPos = 0;
  let xPos = 0;

  if (index > -1) {
    for (const space of area.value) {
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

// Create a numbered rectangle to represent a floor space on the canvas
const createAreaRect = async (space, index) => {
  const width = space.width * canvasStore.areaPixelsPerMeter;
  const height = space.height * canvasStore.areaPixelsPerMeter;

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
      text: index,
      fontFamily: 'Calibri',
      fontSize: 30,
      align: 'center',
      verticalAlign: 'middle',
    }
  };
};

// Load rectangles of floor spaces and restricted areas to render them on the canvas
const loadRectangles = async () => {
  for (const [areaIndex, space] of area.value.entries()) {
    areaRects.value.push(await (createAreaRect(space, areaIndex + 1)));

    restrictedAreaRects.value.push([]);

    for (const restrictedArea of restrictedAreas.value[areaIndex]) {
      restrictedAreaRects.value[areaIndex].push(await (canvasStore.createRestrictedAreaRect(restrictedArea, canvasStore.areaPixelsPerMeter, true)));
    };
  };
};

// Add new floor space to the canvas
const addArea = async (size) => {
  await (updateCanvas());
  const space = newArea(size.width, size.height);
  area.value.push(space);
  restrictedAreas.value.push([]);

  await (createAreaRect(space, areaRects.value.length + 1).then((value) => {
    areaRects.value.push(value);
  }));

  await (constructGroups());
  scaleCanvas();
};

// Update the size of a floor space
const editArea = async (size, index) => {
  await (updateCanvas());
  const space = area.value[index];
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

  // Push/Pull floor spaces right of or below the edited floor space and
  // resize the edited floor space
  await (new Promise((resolve, reject) => {
    for (const [groupIndex, group] of groupRefs.value.entries()) {
      const node = group.getNode();
      const absolutePos = node.getAbsolutePosition();

      const groupSpace = area.value[groupIndex];
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

  scaleCanvas();
};

// Delete the edited floor space
const deleteArea = async () => {
  area.value.splice(editedNodeIndex, 1);
  restrictedAreas.value.splice(editedNodeIndex, 1);

  toggleModal();
  await (updateCanvas()).then(() => {
    scaleCanvas();
  });
};

// Add new restriced area to a floor space
const addRestrictedArea = async (size, groupIndex) => {
  const space = { x: 0, y: 0, width: size.width, height: size.height };
  restrictedAreas.value[groupIndex].push(space);

  await (updateCanvas());
};

// Update the size of a restricted area
const editRestrictedArea = async (size, groupIndex, index) => {
  await (updateCanvas());
  const area = restrictedAreas.value[groupIndex][index];
  area.width = size.width;
  area.height = size.height;

  await (updateCanvas());
};

// Delete the edited restriced area
const deleteRestrictedArea = async () => {
  restrictedAreas.value[editedNodeGroupIndex].splice(editedNodeIndex, 1);

  toggleModal();
  await (updateCanvas());
};

// Line guide positions for every node other than the one being dragged
const getLineGuideStops = (skipNode) => {
  let vertical = [];
  let horizontal = [];
  let nodeArr = [];

  for (const group of groupRefs.value) {
    const groupNode = group.getNode();
    const restrictedNodes = groupNode.find(".restrictedArea");
    nodeArr.push(groupNode);

    if (skipNode.hasName("restrictedArea")) {
      for (const restrictedNode of restrictedNodes) {
        nodeArr.push(restrictedNode);
      };
    };
  };

  for (const guideNode of nodeArr) {
    if (guideNode !== skipNode) {
      const node = nodeWithAbsolutePosition(guideNode);
      vertical.push([node.x, node.x + node.width, node.x + node.width / 2]);
      horizontal.push([node.y, node.y + node.height, node.y + node.height / 2]);
    };
  };
  return {
    vertical: vertical.flat(),
    horizontal: horizontal.flat(),
  };
};

// Snapping positions for the edges and center of the rectangle
const getRectangleSnappingEdges = (node) => {
  const box = nodeWithAbsolutePosition(node);
  const absPos = node.absolutePosition();

  return {
    vertical: [
      {
        guide: Math.round(box.x),
        offset: Math.round(absPos.x - box.x),
        snap: 'start',
      },
      {
        guide: Math.round(box.x + box.width / 2),
        offset: Math.round(absPos.x - box.x - box.width / 2),
        snap: 'center',
      },
      {
        guide: Math.round(box.x + box.width),
        offset: Math.round(absPos.x - box.x - box.width),
        snap: 'end',
      },
    ],
    horizontal: [
      {
        guide: Math.round(box.y),
        offset: Math.round(absPos.y - box.y),
        snap: 'start',
      },
      {
        guide: Math.round(box.y + box.height / 2),
        offset: Math.round(absPos.y - box.y - box.height / 2),
        snap: 'center',
      },
      {
        guide: Math.round(box.y + box.height),
        offset: Math.round(absPos.y - box.y - box.height),
        snap: 'end',
      },
    ],
  };
};

// Find all snapping possibilities
function getGuides(lineGuideStops, itemBounds) {
  let resultV = [];
  let resultH = [];

  lineGuideStops.vertical.forEach((lineGuide) => {
    itemBounds.vertical.forEach((itemBound) => {
      const diff = Math.abs(lineGuide - itemBound.guide);
      // Snap rectangle if position is close to the guideline
      if (diff < GUIDELINE_OFFSET) {
        resultV.push({
          lineGuide: lineGuide,
          diff: diff,
          snap: itemBound.snap,
          offset: itemBound.offset,
        });
      };
    });
  });

  lineGuideStops.horizontal.forEach((lineGuide) => {
    itemBounds.horizontal.forEach((itemBound) => {
      const diff = Math.abs(lineGuide - itemBound.guide);
      if (diff < GUIDELINE_OFFSET) {
        resultH.push({
          lineGuide: lineGuide,
          diff: diff,
          snap: itemBound.snap,
          offset: itemBound.offset,
        });
      };
    });
  });

  let guides = [];

  // Find closest snap
  let minV = resultV.sort((a, b) => a.diff - b.diff)[0];
  let minH = resultH.sort((a, b) => a.diff - b.diff)[0];
  if (minV) {
    guides.push({
      lineGuide: minV.lineGuide,
      offset: minV.offset,
      orientation: 'V',
      snap: minV.snap,
    });
  };
  if (minH) {
    guides.push({
      lineGuide: minH.lineGuide,
      offset: minH.offset,
      orientation: 'H',
      snap: minH.snap,
    });
  };
  return guides;
};

// Add line guides to the canvas
const drawGuides = (guides) => {
  guides.forEach((lg) => {
    if (lg.orientation === 'H') {
      const line = {
        x: 0,
        y: lg.lineGuide,
        points: [-6000, 0, 6000, 0],
        stroke: 'blue',
        strokeWidth: 1,
        dash: [4, 6],
      };
      lineGuides.value.push(line);
    } else if (lg.orientation === 'V') {
      const line = {
        x: lg.lineGuide,
        y: 0,
        points: [0, -6000, 0, 6000],
        stroke: 'blue',
        strokeWidth: 1,
        dash: [4, 6],
      };
      lineGuides.value.push(line);
    };
  });
};

const updateLineGuides = (e) => {
  // Do nothing if all floor spaces are being dragged
  if (canvasStore.dragAll && e.target.name() !== "restrictedArea") {
    return;
  };

  // Clear all previous lines on the screen
  lineGuides.value = [];

  // Find possible snapping lines
  const lineGuideStops = getLineGuideStops(e.target);

  // Find snapping points of current rectangle
  const itemBounds = getRectangleSnappingEdges(e.target);

  // Find the snapping possibilities for the current rectangle
  const guides = getGuides(lineGuideStops, itemBounds);

  // Do nothing if there is no snapping
  if (!guides.length) {
    return;
  }

  drawGuides(guides);

  const absPos = e.target.absolutePosition();
  // Force rectangle position
  guides.forEach((lg) => {
    switch (lg.snap) {
      case 'start': {
        switch (lg.orientation) {
          case 'V': {
            absPos.x = lg.lineGuide + lg.offset;
            break;
          }
          case 'H': {
            absPos.y = lg.lineGuide + lg.offset;
            break;
          }
        }
        break;
      }
      case 'center': {
        switch (lg.orientation) {
          case 'V': {
            absPos.x = lg.lineGuide + lg.offset;
            break;
          }
          case 'H': {
            absPos.y = lg.lineGuide + lg.offset;
            break;
          }
        }
        break;
      }
      case 'end': {
        switch (lg.orientation) {
          case 'V': {
            absPos.x = lg.lineGuide + lg.offset;
            break;
          }
          case 'H': {
            absPos.y = lg.lineGuide + lg.offset;
            break;
          }
        }
        break;
      }
    }
  });
  e.target.absolutePosition(absPos);
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

// Return an object with the absolute position, width and height of a konva node
const nodeWithAbsolutePosition = (node) => {
  const absolutePos = node.absolutePosition();
  return {
    x: absolutePos.x,
    y: absolutePos.y,
    width: node.width(),
    height: node.height()
  };
};

// Determine the appropriate scaling and adjust the actual scaling
// of the canvas accordingly, based on the size and position of the canvas nodes
const scaleCanvas = async () => {
  // Check if the scale is too small
  while (!allInCanvas()) {
    if (canvasStore.currentScale >= canvasStore.CANVAS_SCALES.length - 1) {
      break;
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

// Check if the rectangle is fully inside the bounding rectangle
const isInBounds = (rect, boundingRect) => {
  return !(
    rect.x < boundingRect.x ||
    rect.y < boundingRect.y ||
    rect.x + rect.width > boundingRect.x + boundingRect.width ||
    rect.y + rect.height > boundingRect.y + boundingRect.height
  );
};

// Check if all group nodes are fully inside the canvas
const allInCanvas = () => {
  for (const group of groupRefs.value) {
    const absoluteNode = nodeWithAbsolutePosition(group.getNode());
    if (!isInBounds(absoluteNode, CANVAS_SIZE)) {
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
    const absoluteNode = nodeWithAbsolutePosition(group.getNode());
    const scaledNode = scaleNode(absoluteNode, canvasStore.currentScale - 1);

    if (!isInBounds(scaledNode, CANVAS_SIZE)) {
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

const updateAllStartPos = () => {
  allStartPos = [];
  for (const group of groupRefs.value) {
    allStartPos.push(group.getNode().absolutePosition());
  };
};

// Show a modal for editing a floor space when doubleclicking on one
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
  beforDragPos = startPos;

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

  // For dragging all floor spaces
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
          await (canvasStore.setPosition(group, oldStartPos, allowedDirection, groupArr, area.value, canvasStore.areaPixelsPerMeter, true));
        };

      } else {
        node.x(oldStartPos.x);
        node.y(oldStartPos.y);
      };

      updateAllStartPos();
    });
    // For dragging a single floor space
  } else if (!node.hasName("restrictedArea")) {
    await (canvasStore.checkPosition(node, oldStartPos, groupArr, CANVAS_SIZE)).then(async (allowedDirection) => {
      newStartPos = await (canvasStore.setPosition(node, oldStartPos, allowedDirection, groupArr, area.value, canvasStore.areaPixelsPerMeter));
    });
    // For dragging a restricted area
  } else {
    const groupNode = node.findAncestor('.group');
    const boundingRect = nodeWithAbsolutePosition(groupNode);
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

// After dragging a single floor space around snap floor spaces together if possible
const handleDragend = async (e) => {
  // Don't do anything if there is only one floor space of if a restricted area is being dragged
  if (
    area.value.length <= 1 ||
    groupRefs.value.length === 0 ||
    e.target.hasName("restrictedArea")
  ) {
    return;
  };

  const node = e.target;
  const absoluteNode = nodeWithAbsolutePosition(node);
  let closestPosition = null;

  // Look for floor spaces directly above, below, to the right and to the left
  // of the dragged rectangle
  await (new Promise((resolve, reject) => {
    groupRefs.value.forEach((group) => {
      const groupNode = group.getNode();
      // Don't check position with itself
      if (node === groupNode) {
        return;
      };

      const position = { distance: null, isHorizontal: false };
      const absoluteGroup = nodeWithAbsolutePosition(groupNode);

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
    // Snap positions of the dragged floor space if possible, otherwise reset 
    // position of the floor space to the position prior to dragging it
    const groupIndex = isNodeInRefArray(node, groupRefs);
    const space = area.value[groupIndex];

    if (closestPosition === null) {
      node.position(beforDragPos);
    } else if (closestPosition.isHorizontal) {
      node.x(node.x() + closestPosition.distance);
    } else {
      node.y(node.y() + closestPosition.distance);
    };

    space.x = node.x() / canvasStore.areaPixelsPerMeter;
    space.y = node.y() / canvasStore.areaPixelsPerMeter;
  });
};

// Test Method for inverting y axis
const invertY = (rectArr) => {
  let invertedSpaces = [];
  const canvasHeightInMeters = CANVAS_SIZE.height / canvasStore.areaPixelsPerMeter;
  for (const rect of rectArr) {
    let newY = (rect.y - canvasHeightInMeters + rect.height).toFixed(3);
    if (newY !== 0) {
      newY = -newY;
    };
    invertedSpaces.push({ x: rect.x, y: newY, width: rect.width, height: rect.height });
  };
  return invertedSpaces;
};

const handleModalConfirm = () => {
  const space = modalSpace.value[0];

  switch (currentModalType) {
    case (modalTypes.newArea):
      addArea(space);
      break;
    case (modalTypes.editArea):
      editArea(space, editedNodeIndex);
      break;
    case (modalTypes.newRestrictedArea):
      addRestrictedArea(space, modalFloorIndex.value[0].index - 1);
      break;
    case (modalTypes.editRestrictedArea):
      editRestrictedArea(space, editedNodeGroupIndex, editedNodeIndex);
      break;
  };

  toggleModal();
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

// Toggle whether all floor spaces or only one is being dragged at a time
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

// Update tooltip when mouse hovers over a floor space
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
    text = text.concat("Freifläche ", nodeIndex + 1, ": \n\n", "Breite (x): ", area.value[nodeIndex].width, " m\n",
      "Länge (y): ", area.value[nodeIndex].height, " m");
  };

  tooltipText.value = text;
  tooltipVisible.value = true;
};

const hideTooltip = () => {
  tooltipVisible.value = false;
};

onMounted(() => {
  area.value = planningStore.floorSpace;
  restrictedAreas.value = planningStore.restrictedAreas;
  updateCanvas();
});

onUnmounted(() => {
  planningStore.floorSpace = area.value;
  planningStore.restrictedAreas = restrictedAreas.value;
});
</script>

<template>
  <div class="content">
    <div class="canvas-container">
      <v-stage :config="configKonva" ref="stage">
        <v-layer ref="rectLayer" @dragmove="updateLineGuides" @dragend="lineGuides = []">
          <!--Group for dragging everything at once-->
          <v-group ref="draggingGroup" :config="{ draggable: true, x: 0, y: 0, name: 'draggingGroup' }"
            @dragstart="handleDragstart" @dragmove="handleDragmove"></v-group>

          <!--Visual representations of floor spaces-->
          <v-group v-for="(item, index) in areaRects" :key="item.id" :config="item.groupConfig" ref="groupRefs"
            @dragstart="handleDragstart" @dragmove="handleDragmove" @dragend="handleDragend">
            <v-rect :config="item.rectConfig" ref="areaRectRefs"></v-rect>
            <v-text :config="item.textConfig" ref="areaTextRefs" @mousemove="updateTooltip" @mouseout="hideTooltip"
              @dblclick="areaDoubleClick"></v-text>
            <v-rect v-for="restrictedArea in restrictedAreaRects[index]" :config="restrictedArea.config"
              @dblclick="restrictedAreaDoubleClick"></v-rect>
          </v-group>
          <v-line v-for="item in lineGuides" :config="item"></v-line>
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
          <PlanningInputColumn title="Freifläche" type="select" :selectList="areaIndexList" :list="modalFloorIndex"
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
  </div>
</template>

<style lang="scss" scoped>
.content .canvas-container {
  width: max-content;
  height: max-content;
}

.button-container {
  width: 30%;
  align-items: center;
  display: flex;
  flex-direction: column;

  .planning-button {
    width: 60%;
    margin-bottom: 20px;
  }
}

.modal-button {
  margin-right: 5px;
  margin-left: 5px;
}
</style>