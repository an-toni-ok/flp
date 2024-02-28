import { ref, computed } from 'vue';
import { defineStore } from 'pinia';

export const useCanvasStore = defineStore("canvas", () => {
    let CANVAS_SIZE = {
        x: 0,
        y: 0,
        width: 1200,
        height: 600
    };

    const setCanvasSize = (size) => {
        CANVAS_SIZE.width = size.width;
        CANVAS_SIZE.height = size.height;
    };

    const GUIDELINE_OFFSET = 5;

    const currentScale = ref(0);
    const CANVAS_SCALES = [40, 20, 10, 5, 2, 1];
    const areaPixelsPerMeter = computed(() => CANVAS_SCALES[currentScale.value]);

    const dragAll = ref(false);
    const toggleDraggingMode = () => (dragAll.value = !dragAll.value);
    const draggingButtonText = computed(() => dragAll.value ? "Flächen einzeln bewegen" : "Alle Flächen bewegen");

    const arrowVisibility = ref(false);
    const arrowButtonText = computed(() => arrowVisibility.value ? "Pfeile verstecken" : "Pfeile anzeigen");

    const lineGuides = ref([]);

    // Create a rectangle representing a restricted area for the depiction
    const createRestrictedAreaRect = async (area, pixelsPerMeter, draggable) => {
        return {
            config: {
                x: area.x * pixelsPerMeter,
                y: area.y * pixelsPerMeter,
                width: area.width * pixelsPerMeter,
                height: area.height * pixelsPerMeter,
                fill: 'white',
                stroke: 'black',
                strokeWidth: 1,
                draggable: draggable,
                name: 'restrictedArea'
            }
        };
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

    // Check if the rectangle is fully inside the bounding rectangle
    const isInBounds = (rect, boundingRect) => {
        return !(
            rect.x < boundingRect.x ||
            rect.y < boundingRect.y ||
            rect.x + rect.width > boundingRect.x + boundingRect.width ||
            rect.y + rect.height > boundingRect.y + boundingRect.height
        );
    };

    // Check if two rectangles overlap
    const haveIntersection = (r1, r2) => {
        return !(
            r2.x >= r1.x + r1.width ||
            r2.x + r2.width <= r1.x ||
            r2.y >= r1.y + r1.height ||
            r2.y + r2.height <= r1.y
        );
    };

    // Check if new position of a dragged node is allowed and return allowed direction
    const checkPosition = async (node, startPos, nodeArr, boundingRect) => {
        let absoluteNode = node.getClientRect({ skipStroke: true });

        const endPos = { x: absoluteNode.x, y: absoluteNode.y };
        const DIRECTIONS = ["both", "horizontal", "vertical"];
        let allowed = null;

        // Check if moving vertically or horizontally or both would be allowed
        DIRECTIONS.forEach(async (direction) => {
            await (new Promise((resolve, reject) => {
                // Don't continue if allowed direction is found
                if (allowed !== null) {
                    return;
                };

                switch (direction) {
                    case "horizontal":
                        absoluteNode.x = endPos.x;
                        absoluteNode.y = startPos.y;
                        break;
                    case "vertical":
                        absoluteNode.x = startPos.x;
                        absoluteNode.y = endPos.y;
                        break;
                    default:
                        break;
                };

                if (!isInBounds(absoluteNode, boundingRect)) {
                    return;
                } else if (!dragAll.value || node.hasName("restrictedArea") || node.hasName("machine")) {
                    for (const checkedNode of nodeArr) {
                        const absoluteChecked = checkedNode.getClientRect({ skipStroke: true });
                        if (checkedNode !== node) {
                            if (haveIntersection(absoluteChecked, absoluteNode)) {
                                return;
                            };
                        };
                    };
                };
                allowed = direction;
                resolve();
            }));
        });

        return allowed;
    };

    // Set position of a node so it moves only in the allowed direction
    const setPosition = async (node, startPos, allowed, nodeArr, rectArr, pixelsPerMeter, draggingAll = false) => {
        const absPos = node.absolutePosition();
        let pos;

        if (node.hasName("restrictedArea")) {
            pos = node.position();
        } else {
            pos = absPos;
        };

        const nodeIndex = nodeArr.indexOf(node);
        const rect = rectArr[nodeIndex];

        switch (allowed) {
            case "both":
                rect.x = pos.x / pixelsPerMeter;
                rect.y = pos.y / pixelsPerMeter;

                if (!draggingAll) {
                    startPos.x = absPos.x;
                    startPos.y = absPos.y;
                };
                break;
            case "horizontal":
                rect.x = pos.x / pixelsPerMeter;

                if (!draggingAll) {
                    node.absolutePosition({ x: absPos.x, y: startPos.y });
                    startPos.x = absPos.x;
                };
                break;
            case "vertical":
                rect.y = pos.y / pixelsPerMeter;

                if (!draggingAll) {
                    node.absolutePosition({ x: startPos.x, y: absPos.y });
                    startPos.y = absPos.y
                };
                break;
            // Don't change the position if no direction is allowed
            default:
                if (!draggingAll) {
                    node.absolutePosition({ x: startPos.x, y: startPos.y });
                };
                break;
        };

        return startPos;
    };

    // Line guide positions for every node other than the one being dragged
    const getLineGuideStops = (skipNode, nodeArr) => {
        let vertical = [];
        let horizontal = [];

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
    const getGuides = (lineGuideStops, itemBounds) => {
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

    const updateLineGuides = async (node, nodeArr) => {
        // Clear all previous lines on the screen
        lineGuides.value = [];

        // Find possible snapping lines
        const lineGuideStops = getLineGuideStops(node, nodeArr);

        // Find snapping points of current rectangle
        const itemBounds = getRectangleSnappingEdges(node);

        // Find the snapping possibilities for the current rectangle
        const guides = getGuides(lineGuideStops, itemBounds);

        // Do nothing if there is no snapping
        if (!guides.length) {
            return;
        }

        drawGuides(guides);

        const absPos = node.absolutePosition();
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
        node.absolutePosition(absPos);
    };

    return {
        CANVAS_SIZE,
        currentScale,
        CANVAS_SCALES,
        areaPixelsPerMeter,
        dragAll,
        draggingButtonText,
        arrowVisibility,
        arrowButtonText,
        lineGuides,
        setCanvasSize,
        updateLineGuides,
        isInBounds,
        nodeWithAbsolutePosition,
        toggleDraggingMode,
        createRestrictedAreaRect,
        checkPosition,
        setPosition,
    };
});