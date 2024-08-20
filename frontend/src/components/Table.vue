<script setup>
import { ref, onMounted, reactive, h, onBeforeMount } from 'vue'
import apiClient from '@/services/axios';

const people = reactive(getPeople())
const rows = people.length + 1
const cols = 7
const cellHeight = 40
const cellWidth = 60

const weekDays = [
	'mon',
	'tue',
	'wed',
	'thu',
	'fri',
	'sat',
	'sun',
]

const gridContanerStyle = reactive({
  gridTemplateRows: `repeat(${rows}, ${cellHeight}px)`,
  gridTemplateColumns: `repeat(${cols}, ${cellWidth}px)`,
  margin: 0,
})

function getPeople() {
	return [
        'Leonardo',
        'Donatello',
        'Michelangelo',
        'Raphael',
    ]
}

const grid = ref(null);
let blocks = ref([]);
let isCreating = ref(false);
let isDragging = ref(false);
let isResizing = ref(false);
let startCell, currentBlock, resizeHandle, startX, blockStartLeft;


function startCreatingBlock(e) {
    if (e.target.classList.contains('grid-cell')) {
        const existingBlock = blocks.value.find(
          block => block.props['data-row'] == e.target.dataset.row
        )

        if (!existingBlock) {
            isCreating.value = true;

            blocks.value.push(h('div', {
              'data-row': e.target.dataset.row,
              'class': 'block',
              'onMouseup': finishAction,
              'onMousedown': startBlockAction,
              'style': {
                top: `${e.target.offsetTop}px`,
                left: `${e.target.offsetLeft}px`,
                width: `${cellWidth}px`,
                height: `${cellHeight}px`,
              },
            },
            [
              h('div', {'class': 'resize-handle resize-handle-left'}),
              h('div', {'class': 'resize-handle resize-handle-right'}),
              h('div', {'class': 'drag-handle'}),
            ]
          ))

            startCell = e.target;
        }
    }
}

function startBlockAction(e) {
  e.stopPropagation();
  currentBlock = e.currentTarget;
  startX = e.clientX;
  blockStartLeft = parseInt(currentBlock.style.left);

  if (e.target.classList.contains('resize-handle')) {
      isResizing.value = true;
      resizeHandle = e.target;
  } else if (e.target.classList.contains('drag-handle')) {
      isDragging.value = true;
  }
}


function getSizeByGrid(curCoord, rectLeft) {
  curCoord = curCoord - rectLeft
  let fullCellWidth = cellWidth + .55
  let remainder = curCoord % fullCellWidth
  if (remainder >= (fullCellWidth / 2)) {
      return (curCoord - remainder + fullCellWidth) + rectLeft
  } else {
      return (curCoord - remainder) + rectLeft
  }
}

function handleMouseMove(e) {
    if (!isCreating.value && !isDragging.value && !isResizing.value) return;

    if (e.target.classList.contains('block')) {
      currentBlock = e.target
    } else if (e.target.classList.contains('drag-handle')) {
      currentBlock = e.currentTarget.parentElement
    }


    const gridRect = grid.value.getBoundingClientRect();
    const blockRect = currentBlock.getBoundingClientRect();


    if (isResizing.value) {
      const isLeftHandle = resizeHandle.classList.contains('resize-handle-left');
      let newLeft, newWidth;

      if (isLeftHandle) {
          newLeft = Math.max(gridRect.left, Math.min(e.clientX, blockRect.right - cellWidth));
          newWidth = blockRect.right - newLeft;
      } else {
          newLeft = blockRect.left;
          newWidth = Math.max(cellWidth, Math.min(e.clientX - newLeft, gridRect.right - newLeft));
      }

      currentBlock.style.left = `${getSizeByGrid(newLeft, gridRect.left)}px`;
      currentBlock.style.width = `${getSizeByGrid(newWidth, gridRect.left)}px`;
    } else if (isDragging.value) {
      const deltaX = e.clientX - startX;
      const newLeft = Math.max(gridRect.left, Math.min(blockStartLeft + deltaX, gridRect.right - blockRect.width));
      currentBlock.style.left = `${getSizeByGrid(newLeft, gridRect.left)}px`;
    } else if (isCreating.value) {
      const targetCell = document.elementFromPoint(e.clientX, e.clientY);
      if (!targetCell || !targetCell.classList.contains('grid-cell')) return;

      const startIndex = parseInt(startCell.dataset.ind);
      const targetIndex = parseInt(targetCell.dataset.ind);
      const rowStart = Math.floor(startIndex / 10) * 10;
      const rowEnd = rowStart + 9;

      if (targetIndex < rowStart || targetIndex > rowEnd) return;

      const left = Math.min(startCell.offsetLeft, targetCell.offsetLeft);
      const width = Math.abs(targetCell.offsetLeft - startCell.offsetLeft) + cellWidth;

      currentBlock.style.left = left + 'px';
      currentBlock.style.width = width + 'px';
    }
  }


  function finishAction(e) {
      isCreating.value = false;
      isDragging.value = false;
      isResizing.value = false;
  }

</script>

<template>
    <div class="container">
      <h1 class="text-center mt-4">Interactive Scheduler</h1>
      <div class="container calendar border">
        <div class="people-container border">
          <div>&nbsp;</div>
          <div v-for="person in people" class="">{{ person }}</div>
        </div>
          <div
          ref="grid"
          class="grid-container"
          :style="gridContanerStyle"
          @mousedown="startCreatingBlock"
          @mousemove="handleMouseMove"
          @mouseup="finishAction"
          >
            <template v-for="row in rows">
              <template v-for="col in cols">
                <div v-if="row == 1"
                class="weekdays"
                >{{ weekDays[col - 1] }}</div>

                <div v-else
                :data-row="row - 2"
                :data-col="col - 1"
                :data-ind="`${row - 2}${col - 1}`"
                class="grid-cell"></div>
              </template>
            </template>

            <template v-for="block of blocks">
              <component :is="block"/>
            </template>


          </div>
        </div>
    </div>
</template>

<style>
.calendar {
  display: flex;
  justify-content: center;
  padding-block: 15px;
  width: 600px;
  border-radius: 20px;
  box-shadow: #000000 10px 10px 25px;
}
.people-container {
  padding-inline: 20px;
  display: flex;
  flex-direction: column;
  justify-content: space-around;

}
.grid-container {
	display: grid;
	gap: 1px;
	background-color: #ddd;
	padding: 1px;
	width: fit-content;
	margin: 20px auto;
}
.grid-cell {
	background-color: #fff;
	border: 1px solid #ccc;
}
.grid-cell:hover {
	background-color: #e6e6e6;
}
.weekdays {
  display: flex;
	background-color: #ccc;
  justify-content: center;
  align-items: center;
}
.block {
	position: absolute;
	background-color: #007bff;
	opacity: 0.7;
	display: flex;
	align-items: top;
	justify-content: center;
	color: white;
	font-weight: bold;
	user-select: none;
}
.resize-handle {
	position: absolute;
	width: 10px;
	height: 100%;
	top: 0;
	background-color: rgba(255, 255, 255, 0.5);
	cursor: ew-resize;
}
.resize-handle-left {
	left: 0;
}
.resize-handle-right {
	right: 0;
}
.drag-handle {
	position: absolute;
	width: 40px;
	height: 15px;
	top: 80%;
	left: 50%;
	transform: translate(-50%, -50%);
	border-radius: 50% 50% 0% 0%;
	cursor: move;
	
	background-image: radial-gradient(rgb(117, 117, 117) 29.6%, transparent 29.6%);
	background-position: 3px 3px;
	background-size: 6px 6px;
	background-color: rgba(255, 255, 255, 0.5);
}

</style>
