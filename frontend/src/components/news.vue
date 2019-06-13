<template>
<div style="background-color:#297fb8;min-height:100vh;">
<!--从这里开始复制导航栏-->
<Topbar activeindex='6'></Topbar>
 <!--复制导航栏结尾-->
<div style="height:50px;"></div>
<el-row type='flex' justify='center'>
  <el-col :span='20'>
    <el-container style='background:#ffffff'>
      <el-aside>
        <div style="height:150px;"></div>
        <el-menu
          class="el-menu-vertical-demo"
          style="min-height:650px;"
          :default-active="'1'"
          @select='handleselect'
          >
          <div v-for="(item,index) in filedata" :key="index">
          <el-menu-item :index="String(index+1)" class="titlecss">
              {{item['release_time']}}&emsp;
              {{item['title']}}
          </el-menu-item>
          </div>
        </el-menu>
        <el-pagination
          layout="prev, pager, next"
          :total="pagetotal"
          :page-size='10'
          @current-change='changepagipage'
          :current-page="currentPage"
          >
        </el-pagination>
      </el-aside>
      <el-main>
        <h1>
          {{title}}
        </h1>
        <h5>
          发布时间：{{time}}
          &nbsp;&nbsp;&nbsp;
          阅读数量：{{count}}
        </h5>
        <div style="padding-top:20px;padding-left:50px;padding-right:50px;line-height:40px;">
          {{content}}
        </div>
      </el-main>
    </el-container>
  </el-col>
</el-row>
</div>
</template>
<style scoped>
 .titlecss {
    width: 80;          
    overflow: hidden;      
    text-overflow: ellipsis;
    white-space: nowrap; 
 }
</style>
<script>
 export default{
   data(){
     return{
       filedata:[],
       pagetotal:0,
       title:'',
       content:'',
       time:'',
       count:0,
       currentPage:1,
     }
   },
   methods:{
     init(page)
     {
       this.axios.request({
         url:'/news/',
         method:'GET',
         headers: {'Authorization':localStorage.getItem('token')},
         params:{
           'page':page
         }
       }).then(data=>
       {
         data=data.data
         this.filedata=data['results'];
         this.pagetotal=data['count'];
         this.title=this.filedata[0]['title'];
         this.content=this.filedata[0]['news_content']
         this.time=this.filedata[0]['release_time'];
         this.count=this.filedata[0]['read_count'];
       }
       )
     },
     handleselect(key)
     {
        key =parseInt(key-1)
        this.title=this.filedata[key]['title']
        this.content=this.filedata[key]['news_content']
        this.time=this.filedata[key]['release_time'];
        this.count=this.filedata[key]['read_count'];
     },
     changepagipage(page)
     {
        this.init(page);
        this.currentPage=page;
     },
     ToTheOtherPage(page)
     {
       this.$router.push(page);
     },
   },
   mounted(){
     this.init('1')
   }
   }
</script>
