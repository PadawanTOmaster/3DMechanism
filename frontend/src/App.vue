<template>
  <div id="app">
    <router-view></router-view>
    <el-container>
      <el-footer >
        <el-row>
          <el-col :span="12">
            <el-tag type='success' :hit="true" style="color:#fff">Copyright© 2018-2019 华东理工大学</el-tag>
            <el-tag type='success' :hit="true" style="color:#fff">京ICP备19009455号</el-tag>
          </el-col>
          <el-col :span="12">
            <el-tag type='success' :hit="true" style="color:#fff">谭仲夏</el-tag>
            <el-tag type='success' :hit="true" style="color:#fff">李侃</el-tag>
            <el-button  size='mini' type="success" plain>关于我们</el-button>
          </el-col>
        </el-row>
      </el-footer>
  </el-container>
  </div>
  
</template>

<script>
export default {
  name: 'App',
  methods:{
    linkto(){
      window.open("")
    }
  }
}
</script>

<style>
#app {
  font-family: "Helvetica Neue",Helvetica,"PingFang SC","Hiragino Sans GB","Microsoft YaHei","微软雅黑",Arial,sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
.el-footer{
		background-color: #409EFF;
    color: #333;
    text-align: center;
    line-height: 60px;
    z-index: -1;
	}
</style>
