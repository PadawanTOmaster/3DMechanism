<template>
<div>
<!--从这里开始复制导航栏-->
<Topbar activeindex='3'></Topbar>
 <!--复制导航栏结尾-->
<div style="height:100px;"></div>
<el-row>
  <el-col :span="2">&nbsp;</el-col>
  <el-col :span="20">
      <el-col :span="5" v-for="file  in filedata" :key="file['id']" :offset="1">
        <el-tooltip placement="bottom-start">
        <div slot="content">{{file['description']}}</div>
        <el-card :body-style="{ padding: '0px' }" style="min-height:250px;">
          <div style="padding: 14px;">
            <img  :src="defaulturl+file['imgpath']" class="image"/>
            <span style="font-weight:bold"><br>{{file['filename']}}</span>
          </div>
        </el-card>
        </el-tooltip>
        <div style="height:10px;"></div>
        <el-button type="info" plain @click="downloadFile(defaulturl+file['filepath'])" class="button">下载</el-button>
        <div style="height:50px;"></div>
      </el-col>
  </el-col>
  <el-col :span="2">&nbsp;</el-col>
</el-row>


</div>
</template>
<style scoped>
  .time {
    font-size: 13px;
    color: #999;
  }
  
  .bottom {
    margin-top: 13px;
    line-height: 12px;
  }

  .button {
    padding: 5px;
    float: right;
  }

  .image {
    width: 100%;
    height: 200px;;
  }

  .clearfix:before,
  .clearfix:after {
      display: table;
      content: "";
  }

  .clearfix:after {
      clear: both
  }
</style>
<script>
 export default{
   data(){
     return{
       filedata:[],
       defaulturl:"http://3d1.top",
     }
   },
   methods:{
     init()
     {
       this.axios.request({
         url:'/filedownload/',
         method:'GET',
         headers: {'Authorization':localStorage.getItem('token')},
       }).then(data=>
       {
         data=data.data;
         this.filedata=data;
         console.log(data);
       }
       )
     },
     downloadFile(path)
     {
       window.open(path);
     },
     ToTheOtherPage(page)
     {
       this.$router.push(page);
     },
   },
   mounted()
   {
     this.init();
   },
   }
</script>
