<template>
<div style="background-color:#297fb8;min-height:100vh;">
<Topbar activeindex='5'></Topbar>

<div style="height:50px;"></div>
<el-row type='flex' justify='center'>
  <el-col :span='20'>
    <el-container style='background:#ffffff'>
      <el-aside>
        <el-menu
          class="el-menu-vertical-demo"
          style="min-height:1000px;"
          @select="ChooseMenu"
          >
          <el-submenu index="1">
            <template slot="title">
              <i class="el-icon-location"></i>
              <span>工程制图二学分</span>
            </template>
            <el-menu-item-group>
              <el-menu-item index='1-3'>期末考试题型</el-menu-item>
              <el-menu-item index="1-1">填空题</el-menu-item>
              <el-submenu index="1-2">
              <template slot="title">作图题</template>
                <button type="button" class="el-tag el-tag--primary el-tag--medium" @click='getDrawingProblem(1)'><span>尺寸标注</span></button>
                <button type="button" class="el-tag el-tag--success el-tag--medium" @click='getDrawingProblem(2)'><span>补画第三视图</span></button>
                <button type="button" class="el-tag el-tag--warning el-tag--medium" @click='getDrawingProblem(5)'><span>补画图线</span></button>
                <button type="button" class="el-tag el-tag--danger el-tag--medium" @click='getDrawingProblem(3)'><span>剖面图和断面图</span></button>
                <button type="button" class="el-tag el-tag--info el-tag--medium" @click='getDrawingProblem(4)'><span>零件图</span></button>
                <button type="button" class="el-tag el-tag--warning el-tag--medium" @click='getDrawingProblem()'><span>装配图</span></button>
                <button type="button" class="el-tag el-tag--danger el-tag--medium" @click='getDrawingProblem()'><span>标准件与常用件</span></button>
                <button type="button" class="el-tag el-tag--primary el-tag--medium" @click='getDrawingProblem()'><span>投影法</span></button>
                <button type="button" class="el-tag el-tag--success el-tag--medium" @click='getDrawingProblem()'><span>计算机绘图</span></button>
                <button type="button" class="el-tag el-tag--info el-tag--medium" @click='getDrawingProblem("")'><span>全部题型</span></button>
            </el-submenu>
            </el-menu-item-group>
          </el-submenu>
          <el-submenu index="2">
            <template slot="title">
              <i class="el-icon-location"></i>
              <span>机械原理</span>
            </template>
          </el-submenu>  
        </el-menu>
      </el-aside>
      <el-main>
        <div style='height:50px;'></div>

        <div v-if="chosen=='1-1'">
        <div v-for='item in maindata' :key="item['number']">
          <el-row>
            <el-col :span='2'>&nbsp;</el-col>
            <el-col :span='21'>
              <div style="height:100px;padding-top:20px;padding-left:20px;" class="grid-content bg-purple-light">
                <el-row :gutter="20">
                  <el-col :span='20'>
                    <label >{{item['number']}}</label>.
                    <label :id="'answere'+item['number']" v-html="item['problem']"></label>
                  </el-col>
                  <el-col :span='4'>
                    <el-button type="danger" :id="'button'+item['number']" @click="lookanswere(item)">查看答案</el-button>
                  </el-col>
                </el-row>
              </div>
            </el-col>
            <el-col :span='3'>&nbsp;</el-col>
          </el-row>
          <div style='height:20px;'></div>
        </div>
        </div>

        <!-- 画图题 -->
        <div v-if="chosen=='1-2'">
          <div style="padding-left:50px;">
            <div v-for="item in maindata" :key="item['number']">
              <el-row>
                <el-col :span='18'>
                   <label >{{item['number']}}</label>.
                   <label :id="'answere'+item['number']" v-html="item['problemtext']"></label>
                   <div style="height:50px;"></div>
                   <div v-if="item['problemimg'].split(',').length>=2">
                     <div v-for="i in item['problemimg'].split(',')" :key="i">
                      <img :src="serverurl+'/files/images/drawing_practice/'+i" alt="此图片暂时无法显示" style='max-width:100%;'/>
                     </div>
                   </div>
                   <div v-else>
                     <img :src="serverurl+'/files/images/drawing_practice/'+item['problemimg']" alt="此图片暂时无法显示" style='max-width:500px;'/>
                   </div>
                </el-col>
                <el-col :span="6">
                  <el-button type='primary' plain @click="showDrawinganswere(item)">查看答案</el-button>
                  <el-button v-if='item["hasthreed"]==1' type="primary" @click='show3D(item["number"])' >查看3D图</el-button>
                </el-col>
              </el-row>
           
            <div style="height:50px;"></div>
            </div>
          </div>
        </div>

        <div v-if="chosen=='1-3'">
            <div class=WordSection1 style='layout-grid:15.6pt;padding-left:50px;'>
            <p class=MsoNormal><b>考试题型：<span lang=EN-US></span></b></p>
            <p class=MsoNormal><b>填空（<span lang=EN-US>10</span>分）<span lang=EN-US
            style='color:red'>(工程制图<span lang=EN-US>100</span>点和作业复习<span
            lang=EN-US>)</span></span></b><span lang=EN-US></span></p>
            <p class=MsoNormal><b>尺寸标注（<span lang=EN-US>10</span>分）</b><span lang=EN-US></span></p>
            <p class=MsoNormal><b>由两个视图补画第三个视图（两道题<span lang=EN-US>) </span>（<span
            lang=EN-US>25</span>分）</b><span lang=EN-US></span></p>
            <p class=MsoNormal><b>剖视图（<span lang=EN-US>15</span>分）</b><span lang=EN-US></span></p>
            <p class=MsoNormal><b>零件图（<span lang=EN-US>20</span>分）</b><span lang=EN-US></span></p>
            <p class=MsoNormal><b>装配图（<span lang=EN-US>20</span>分）</b><span lang=EN-US></span></p>
            <p class=MsoNormal><span lang=EN-US>&nbsp;</span></p>
            <p class=MsoNormal><b>考试范围：<span lang=EN-US></span></b></p>
            <p class=MsoNormal style='tab-stops:list 36.0pt'><b>上课没讲过的章节不考<span lang=EN-US></span></b></p>
            <p class=MsoNormal style='tab-stops:list 36.0pt'><b>轴测图、轴承，弹簧，齿轮没有大题<span
            lang=EN-US></span></b></p>
            <p class=MsoNormal><span lang=EN-US>&nbsp;</span></p>
            <p class=MsoNormal><b>考试需要<span class=GramE>带如下</span>绘图工具：</b><span
            lang=EN-US></span></p>
            <p class=MsoNormal><b><span lang=EN-US>1.</span>铅笔，橡皮</b><span lang=EN-US></span></p>
            <p class=MsoNormal><b><span lang=EN-US>2.</span>圆规</b><span lang=EN-US></span></p>
            <p class=MsoNormal><b><span lang=EN-US>3.</span>黑色水笔</b><span lang=EN-US></span></p>
            <p class=MsoNormal><span lang=EN-US>&nbsp;</span></p>
            </div>
        </div>

        <el-dialog
          :visible.sync="DialogVisible"
          width="50%"
          :lock-scroll="false"
          @close='dialogclose'
          center>
          <label>{{drawingproblemnum}}</label>.
          <label v-html="drawingproblemtext"></label>
          <div style="height:20px;"></div>
          <div style="text-align:center">
            <img :src='serverurl+"/files/images/drawing_practice/"+Dialogimgpath' alt="该图片暂时无法显示" style="width:500px;"/>
          </div>
        </el-dialog>

        <el-dialog
          :visible.sync="DialogVisible2"
          width="50%"
          :lock-scroll="false"
          center>
          <div id="webGL_container">
          </div>
        </el-dialog>

        <el-pagination v-if="openbar==1"
          @current-change='changepagination'
          :current-page="currentpage" 
          background
          layout="prev, pager, next"
          :total="pagetotal"
          :page-size='5'
          >
        </el-pagination>
      </el-main>
    </el-container>
  </el-col>
</el-row>
</div>

</template>
<style scoped>
  /* .el-tag {
    margin:2px;
  } */
  .el-menu-vertical-demo:not(.el-menu--collapse) {
    width: 300px;
  }
  .text {
    font-size: 14px;
  }

  .item {
    margin-bottom: 18px;
  }

  .clearfix:before,
  .clearfix:after {
    display: table;
    content: "";
  }
  .clearfix:after {
    clear: both
  }

  .el-main {
    background-color: #ffffff;
    color: #000;
    text-align: left;
  }
  .bg-purple-light {
    background: #fdfbf3;
  }
  .grid-content {
    border-radius: 4px;
    min-height: 36px;
  }

</style>
<script>
import * as THREE from 'three'
import {MTLLoader, OBJLoader} from 'three-obj-mtl-loader'
 export default{
   data(){
     return{
       activeIndex:'6',
       maindata:[],
       pagetotal:0,
       openbar:0,
       currentpage:1,
       chosen:'1',
       serverurl:'http://3d1.top',
       DialogVisible:false,
       DialogVisible2:false,

       Dialogimgpath:'',
       drawingproblemnum:null,
       drawingproblemtext:'',
       drawingtype:'',
       scene:null,
       camera:null,
       renderer:null,
       setpath:'../../static/images/',
       format:'.jpg',
       array1:['px','nx','py','ny','pz','nz'],
       skybox:null,
       texture:[],
       mesh:null,
     }
   },
   methods:{
     ToTheOtherPage(page)
     {
       this.$router.push(page);
     },

     ChooseMenu(key)
     {
       this.openbar=1;
       this.chosen=key;
       this.currentpage=1;
       if(key=='1-1')
       {
         this.ConnectnotypeServer('/fillblanks/')
       }
     },
     
     changepagination(page)
     {
       this.currentpage=page;
       if(this.chosen=='1-1')
       {
         this.ConnectnotypeServer('/fillblanks/');
       }
       if(this.chosen=='1-2')
       {
         this.ConnecthastypeServer('/drawing/',this.drawingtype);
       }
     },

     ConnectnotypeServer(path)
      {
        this.axios.request(
           {
             url:path,
             method:'GET',
             headers: {'Authorization':localStorage.getItem('token')},
             params:{
               'page':this.currentpage
             }
           }
         ).then(
           response=>
           {
             this.pagetotal=response.data['count']
             this.maindata=response.data['results']
           }
         )
      },

      ConnecthastypeServer(path,type)
      {
        this.axios.request(
           {
             url:path,
             method:'GET',
             headers: {'Authorization':localStorage.getItem('token')},
             params:{
               'page':this.currentpage,
               'type':type,
             }
           }
         ).then(
           response=>
           {
             this.pagetotal=response.data['count']
             this.maindata=response.data['results']
           }
         )
      }
    ,
    lookanswere(item)
    {
      var buttonid = 'button'+item['number'];
      var buttontext = document.getElementById(buttonid).innerHTML
      if(buttontext.indexOf('查看答案')!=-1)
      {
        var jieba=item['problem'].split('______')
        var length=jieba.length
        var i=0;
        var answere='';
        for(i;i<length-1;i++)
        {
          answere+=jieba[i];
          var str='answere'+(i+1);
          answere+='<span style="color:#c43420"><u>&nbsp;&nbsp;'+item[str]+'&nbsp;&nbsp;</u></span>';
        }
        answere+=jieba[i];
        var id='answere'+item['number']
        document.getElementById(id).innerHTML=answere;
        document.getElementById(buttonid).innerHTML='查看题目';
      }
      if(buttontext.indexOf('查看题目')!=-1)
      {
        var problem=item['problem']
        var id='answere'+item['number']
        document.getElementById(id).innerHTML=problem;
        document.getElementById(buttonid).innerHTML='查看答案';
      }
    },
    

    getDrawingProblem(type)
    {
      this.openbar=1;
      this.chosen='1-2';
      this.drawingtype=type;
      this.currentpage=1;
      this.axios.request(
        {
          url:'/drawing/',
          method:'GET',
          params:{
            'type':type,
          }
        }
      ).then(
        response=>
        {
          this.maindata=response.data['results']
          //response.data['results'][0]['problemtext']
          this.pagetotal=response.data['count']
        }
      )
    },
    showDrawinganswere(item)
    {
      this.Dialogimgpath=item['answereimg'];
      this.drawingproblemnum=item['number'];
      this.drawingproblemtext=item['problemtext']
      this.DialogVisible=true;
    },

    dialogclose()
    {
      this.Dialogimgpath='';
      this.drawingproblemtext='';
      this.drawingproblemnum=null;
    },

    show3D(itemnumber)
    {
      this.DialogVisible2=true;
      var str='../../static/models/drawing'+itemnumber+'.obj';
      var loadermodel = new OBJLoader();
      loadermodel.load(str,(obj)=>
      {
        if(document.getElementById('webGL_container').firstChild!=null)
        {
          document.getElementById('webGL_container').removeChild(document.getElementById('webGL_container').firstChild);
        }
        this.AddScene();
        this.AddCamera();  
        this.AddRender();
        this.AddOrbitControls();
        this.initLight();
        for(var i=0;i<obj.children.length;i++)
        {
          obj.children[i].geometry.center();
        }
        this.scene.add(obj);
        this.animate()
      })
    },
    
    AddScene()
    {
        this.scene=new THREE.Scene();
    },

    AddCamera()
    {
        this.camera = new THREE.PerspectiveCamera( 50, window.innerWidth/window.innerHeight, 0.1, 1000 );
        this.camera.position.x = 5;
        this.camera.position.y = 0;
        this.camera.position.z = 5;
    },

    AddRender()
    {
        this.renderer=new THREE.WebGLRenderer({antialias : true});
        this.renderer.setClearColor(0xa0adb5);
        this.renderer.setSize(0.4*window.innerWidth,0.4*window.innerHeight);
        document.getElementById("webGL_container").appendChild(this.renderer.domElement)
    },

    AddOrbitControls()
    {
        var OrbitControls = require('three-orbit-controls')(THREE);
        var controls = new OrbitControls(this.camera,this.renderer.domElement);
    },

    initLight()
    {
      var pointLightfront = new THREE.PointLight( 0x4b0082, 1);
      pointLightfront.position.set( 0,0,100 );
      this.scene.add( pointLightfront );
      var pointLightback = new THREE.PointLight( 0x4b0082, 1);
      pointLightback.position.set( 0,0,-100 );
      this.scene.add( pointLightback );
      var pointLightleft = new THREE.PointLight( 0x5786d8, 1);
      pointLightleft.position.set( 100,0,0 );
      this.scene.add( pointLightleft );
      var pointLightright = new THREE.PointLight( 0x5786d8, 1);
      pointLightright.position.set( -100,0,100 );
      this.scene.add( pointLightright );
      var pointLightdown = new THREE.PointLight( 0x5786d8, 1);
      pointLightdown.position.set( 0,-100,0 );
      this.scene.add( pointLightdown );
      },
    animate()
    {
      this.renderer.render( this.scene, this.camera );
      requestAnimationFrame(this.animate);
      
    }
   }
 }
</script>
