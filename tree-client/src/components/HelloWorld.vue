<template>
  <div class="hello">
    <sortable-tree v-if="treeData" :data="treeData" mixinParentKey="$parent" @changePosition="changePosition" :dragEnable="true" closeStateKey="$foldClose">
      <template slot-scope="{item}">
        <div class="custom-tree-content" :class="{'exitChild': item.children && item.children.length}">
          <span v-if="item['$foldClose'] && item.children && item.children.length" @click="changeState(item)">▶</span>
          <span v-else-if="!item['$foldClose'] && item.children && item.children.length" @click="changeState(item)">▼</span>
          <span>{{item.name}}</span>
          <span v-if="item.id" class="caret" @click="deleteNode(item.id)">&#x2717;</span>
        </div>
      </template>
    </sortable-tree>
    <button  @click="sendData">Save editions</button>
    <button  @click="createTree">Create Tree</button>
  </div>
</template>

<script>
import SortableTree from './SortableTree'
import axios from 'axios'
import {
  CREATE_TREE_ENDPOINT,
  GET_TREE_ENDPOINT,
  UPDATE_TREE_ENDPOINT,
  DELETE_TREE_ENDPOINT
} from '@/services/endPointCollections'

export default {
  name: 'HelloWorld',
  components: {
    [SortableTree.name]: SortableTree
  },
  data () {
    return {
      msg: 'tree structure',
      treeData: {name: 'tree is empty'}
    }
  },
  created () {
    this.acceptTreeData()
  },
  methods: {
    createTree () {
      axios.get(CREATE_TREE_ENDPOINT).then(r => this.acceptTreeData())
    },
    acceptTreeData () {
      let tree = {}
      axios.get(GET_TREE_ENDPOINT).then(r => {
        console.log('asdasd')
        if (r.data[0]) {
          tree.name = r.data[0].data.name
          tree.id = r.data[0].id
          tree.children = []
          if (r.data[0].children) {
            r.data[0].children.forEach((i, index) => {
              i.data.id = i.id
              tree.children.push(i.data)
              this.addChildren(tree, i, index, false)
            })
          }
          this.treeData = Object.assign({}, this.treeData, tree)
          return true
        } else {
          this.treeData = {name: 'tree is empty'}
          return true
        }
      }).catch(e => console.log(e))
    },
    deleteNode (id) {
      axios.delete(DELETE_TREE_ENDPOINT(id), { id: id }).then(r => this.acceptTreeData()).catch(e => console.log(e))
    },
    prepareData () {
      let o = {}
      o.o = o
      let cache = []
      let newDataTree = JSON.stringify(this.treeData, (key, value) => {
        if (typeof value === 'object' && value !== null) {
          if (cache.indexOf(value) !== -1) {
            try {
              return JSON.parse(JSON.stringify(value))
            } catch (error) {
              return
            }
          }
          cache.push(value)
        }
        return value
      })
      cache = null
      return newDataTree
    },
    sendData () {
      let prepareData = this.prepareData()
      axios.put(UPDATE_TREE_ENDPOINT, prepareData).then(r => console.log(r)).catch(e => console.log(e))
    },
    addChildren (tree, i, index, isEndedDepth) {
      if (isEndedDepth) {
        if (Object.keys(i).includes('children')) {

          tree.children[index].children[0].children = []
          i.children.forEach((i) => {
            i.data.id = i.id
            tree.children[index].children[0].children.push(i.data)
          })
        }

        this.treeData = Object.assign({}, this.treeData, tree)
        return true
      } else {
        if (Object.keys(i).includes('children')) {
          tree.children[index].children = []
          i.children.forEach(i => {
            i.data.id = i.id
            tree.children[index].children.push(i.data)
            this.addChildren(tree, i, index, true)
          })
        }
        this.treeData = Object.assign({}, this.treeData, tree)
        return true
      }
    },
    consoleData () {
      console.log(this.treeData)
    },
    changeState (item) {
      this.$set(item, '$foldClose', !item['$foldClose'])
    },
    changePosition (option) {
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>
  .custom-tree-content {
    position: relative;
    top: 2px;
    z-index: 1;
    &.exitChild {
      margin-left: -7px;
    }
  }
  .caret {
    margin-left: 10px;
    cursor: pointer;
  }
</style>
