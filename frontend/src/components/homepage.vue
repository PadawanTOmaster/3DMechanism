<template>
<div style="height:100vh;">
<!--从这里开始复制导航栏-->

<Topbar activeindex='1'></Topbar>
<div style="height:30px;"></div>
<el-row type="flex" justify="center">
	<el-col :span="5">
		<div style="height:50px;"></div>
		<div><img :src="avatar" class="avatar" alt="暂时无法显示"/></div>
		<div style="height:50px;"></div>
		<el-tag><span class="nickname">{{nickname}}</span></el-tag>
		<div style="height:50px;"></div>
		<el-card >
				{{information}}
		</el-card>
	</el-col>
	<el-col :span="1">
		&nbsp;
	</el-col>
	<el-col :span="10">
		
		<el-card class ="box-card">
			<div slot="header" class="clearfix">
				<span>最新新闻</span>
			</div>
			<div v-for="i in fivedata" :key="i['title']">
				<template>
					<el-alert
						:title="i['release_time']+' '+i['title']"
						:type="newstype"
						:closable="false"
						:description="i['news_content'].substr(0,50)+'...'">
					</el-alert>
				</template>
				<br>
			</div>
			
	    </el-card>
	</el-col>
</el-row>

</div>
</template>
<script>
export default {
    
    data(){
        return{
			nickname:'',
			avatar:'',
			information:'',
			defaulturl:"http://3d1.top/files/",
			newstype:'',
			filedata:[],
			fivedata:[],
			filedatapoint:0,
			alerttype:['success','warning','info','error'],
			alerttypepoint:0,
			timer:null,
        }
    },
    methods:{
      newsRoll(){
		
		if(this.alerttypepoint == 4)this.alerttypepoint = 0
		if(this.alerttypepoint%2==0){
			this.fivedata=this.filedata.slice(0,5)
		}else{
			this.fivedata=this.filedata.slice(5,10)
		}
		this.newstype = this.alerttype[this.alerttypepoint]
		this.alerttypepoint ++
		
	  }
        
    },
     mounted(){
           this.axios.request({
			url:'/getinfor/',
			method:'POST',
			headers: {'Authorization':localStorage.getItem('token')},
			data:{
				username:localStorage.getItem('username'),
			}}).then(data=>
			{
				data=data.data;
				this.information=data.information;
				if(data.information ==''){
					this.information = "这个人有点懒，什么也没留下~"
				}
				this.avatar=this.defaulturl+data.avatar;
				this.nickname = data.nickname;
			}
			)
		this.axios.request({
         url:'/news/',
         method:'GET',
         headers: {'Authorization':localStorage.getItem('token')},
         params:{
           'page':1
          }}).then(data=>
       {
         data=data.data
		 this.filedata=data['results']
		 this.timer = setInterval(this.newsRoll,2000) 
       }
       )
		},
	destroyed(){
		 clearInterval(this.timer);  
	}
    
}

</script>

<style scoped>
	.avatar{
		height:150px;
		width:150px;
		border-radius:10px;
		box-shadow: 0 2px 4px rgba(0, 0, 0, .12), 0 0 6px rgba(0, 0, 0, .04);
	}
  .text {
    font-size: 14px;
  }

  .item {
    padding: 18px 0;
  }

  .box-card {
		padding:20px;
		min-height:100%;
		text-align: left; 
	}
	.nickname{
		font-size: 18px;
	}
	
</style>
