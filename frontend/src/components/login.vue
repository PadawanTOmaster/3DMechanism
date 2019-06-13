<template>
<div style="background-color:#297fb8;height:100vh;"  @keyup.enter="login()">
  <el-row class="longlogo">
    <img src="../../static/images/longlogo.png" style="width:40%"/>
  </el-row>
  <!-- <div style="padding:250px 100px;"> -->
  <el-row>
    <el-col :span="2">&nbsp;</el-col>
    <el-col :span="10">
        <el-carousel :interval="4000"  type="card" height="200px">

          <el-carousel-item 
          style="
          background:url('../../static/images/fourbar.png')no-repeat; 
          background-size:100% 100%;
          ">
            <h3>四杆机构</h3>
          </el-carousel-item>

          <el-carousel-item 
          style="
          background:url('../../static/images/gear.png')no-repeat; 
          background-size:100% 100%;
          ">
            <h3>差动轮系</h3>
          </el-carousel-item>

          <el-carousel-item 
          style="
          background:url('../../static/images/barforce.png')no-repeat; 
          background-size:100% 100%;
          ">
            <h3>杆件受力</h3>
          </el-carousel-item>

        </el-carousel>
    </el-col>
    <el-col :span="1">&nbsp;</el-col>
    <el-col :span="8">
        <el-form>
          <el-form-item>
            <el-input autocomplete="off" placeholder="用户名" v-model="username" @focus="usernameRule=''"></el-input>
            <div style="height:8px;text-align:left;" v-html="usernameRule"></div>
          </el-form-item>
          
          <el-form-item>
            <el-input type="password" autocomplete="off" placeholder="密码" v-model="password" @focus='passwordRule=""'></el-input>
            <div style="height:8px;text-align:left;" v-html='passwordRule'></div>
          </el-form-item>
          <div style="height:10px;"></div>
          <el-form-item style='text-align:left'>
            <el-button type="warning" @click="changepage('/signup')">注册</el-button>
            <el-button type="success" @click='login()'>&nbsp;登录&nbsp;</el-button>
          </el-form-item>
        </el-form>
    </el-col>
    
  </el-row>  
</div>



</template>

<style>

/*轮播*/
 .el-carousel__item h3 {
    color: #475669;
    font-size: 14px;
    opacity: 0.75;
    line-height: 300px;
    margin: 0;
  }
  .longlogo {
    text-align: left;
    padding-left:10%;
    padding-top:5%;
    padding-bottom: 5%
  }
  
</style>
<script>
export default {
    
    data(){
        return{
          username:'',
          password:'',
          usernameRule:'',
          passwordRule:'',
        }
    },
    methods:{
      login()
      {
        var Rex=/\s/;
        var flag=1;
        if(this.username=='')
        {
          flag=0;
          this.usernameRule='用户名<span style="color:#c43420">不能为空</span>';
        }
        else if(Rex.test(this.username)==true)
        {
          flag=0;
          this.usernameRule='用户名中含有<span style="color:#c43420">非法字符</span>，请重新输入';
          this.username='';
        }
        if(this.password=='')
        {
          flag=0;
          this.passwordRule='密码<span style="color:#c43420">不能为空</span>';
          this.password='';
        }
        if(flag==1)
        {
          this.axios.request(
            {
              url:'/login/',
              method:'POST',
              data:{
                username:this.username,
                password:this.password
              }
            }
          ).then(response=>{
            var response=response.data
            localStorage.setItem("token",response.token);
            localStorage.setItem('username',response.username);
            localStorage.setItem('nickname',response.nickname);
            localStorage.setItem('flag',response.flag);
            this.$message({message:'登陆成功',type:'success'});
            this.$router.push('/homepage');
          })
          .catch(error=>
          {
            if(error.message=='Request failed with status code 400')
            {
              this.$message({message:'密码或用户名错误',type:'error'});
            }
            else if(error.message=='Network Error')
            {
              this.$message({message:'服务器繁忙，请稍后再试',type:'error'});
            }
          })
        }
      },

      changepage(page)
      {
        this.$router.push(page);
      },
      

        

        
        
        removeTags(classname,type)
        {
          if(type=='class')
          {
            var targetElem=document.getElementsByClassName(classname);
            if(targetElem[0]!=null)
            targetElem[0].parentNode.removeChild(targetElem[0]);
          }
          if(type=='tag')
          {
            var targetElem=document.getElementsByTagName(classname);
            if(targetElem[0]!=null)
            targetElem[0].parentNode.removeChild(targetElem[0]);
          }
           
        }
    },
     mounted(){
          this.removeTags('dg main a','class');
          this.removeTags('footer','tag');
          if(localStorage.getItem('token')!=undefined)
          {
            this.$router.push('/homepage');
          }
        },
    
}

</script>
