<template>
<div>
<el-row >
    <div style="top:15px;left:15px;z-index:1000;position:absolute;opacity:0.8;">
        <el-button type="success" round @click="Topage('/threed')">返回</el-button>
        <el-button @click="show1=!show1" type="success" round>看图</el-button>
        <el-button @click="show2=!show2" type="success" round>看讲解</el-button>
    </div>
</el-row>
<el-collapse-transition>
<div style="z-index:1000;position:absolute;top:50px;">
<el-container v-show="show1">
 <el-main>
    <div id="myecharts" style="width:350px;height:350px;user-select:none;"><img src="../../static/images/gongzhuan.png" /></div>
    <div id="myecharts1" style="width:350px;height:350px;user-select:none;"><img src="../../static/images/zizhuan.png" /></div>
 </el-main>
</el-container>
</div>
</el-collapse-transition>
<div id="webGL_container">
</div>
<el-collapse-transition>
<el-card class="box-card" style="z-index:1000;position:absolute;user-select:none;top:100px;right:15px;opacity:0.4" v-show="show2">
<b>&nbsp;&nbsp;简单的行星齿轮机构中，位于行星齿轮机构中心的是太阳轮，太阳轮和行星轮常啮合，两个外齿轮啮合旋转方向相反。正如太阳位于太阳系的中心一样，太阳轮也因其位置而得名。行星轮除了可以绕行星架支承轴旋转外，在有些工况下，还会在行星架的带动下，围绕太阳轮的中心轴线旋转，这就像地球的自转和绕着太阳的公转一样，当出现这种情况时，就称为行星齿轮机构作用的传动方式。在整个行星齿轮机构中，如行星轮的自转存在，而行星架则固定不动，这种方式类似平行轴式的传动称为定轴传动。齿圈是内齿轮，它和行星轮常啮合，是内齿和外齿轮啮合，两者间旋转方向相同。行星齿轮的个数取决于变速器的设计负荷，通常有三个或四个，个数愈多承担负荷愈大。
简单的行星齿轮机构通常称为三构件机构，三个构件分别指太阳轮、行星架和齿圈。这三构件如果要确定相互间的运动关系，一般情况下首先需要固定其中的一个构件，然后确定谁是主动件，并确定主动件的转速和旋转方向，结果被动件的转速、旋转方向就确定了。</b>
</el-card>
</el-collapse-transition>
</div>
</template>

<style scoped>
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
  .box-card {
    width: 480px;
  }
 
</style>

<script>
import * as THREE from 'three'
import dat from 'dat.gui'
import {MTLLoader, OBJLoader} from 'three-obj-mtl-loader'
import {ViveController} from "three/examples/jsm/vr/ViveController.js"
import { WEBVR } from 'three/examples/jsm/vr/WebVR.js';
export default {

    data(){
        return{
            scene:null,
            camera:null,
            renderer:null,
            axis:null,
            setpath:'../../static/images/',
            format:'.jpg',
            array1:['px','nx','py','ny','pz','nz'],
            skybox:null,
            texture:[],
            mesh:null,
            geometry:null,
            //设置立体图形变量
            out:null,//最外面
            middle:null,//其次
            inside:null,//内
            myChart:null,
            myChart1:null,
            show1:true,
            show2:true,
            controls:null,//GUI界面
            lastAngle:Math.PI/2,
            middleR:4.8,//4.65
            z1:30,//中心轮
            z2:17,//行星
            z3:64,//内齿轮
            alist:[],
            blist:[],
            xData:[],
            yData:[],
            max1:-100000,
            min1:100000,
            max2:-100000,
            min2:100000
            }
    },
    methods:{
        
        init()
        {
            //var OrbitControls = require('three-orbit-controls')(THREE);
            this.scene=new THREE.Scene();
            //camera set 
           
            this.camera=new THREE.PerspectiveCamera( 50, window.innerWidth/window.innerHeight,0.1,10000);
            var user = new THREE.Group();
            user.add( this.camera );
            user.position.set(20,-2,10);
            user.rotation.y = Math.PI*0.33;
            this.scene.add(user);
            window.addEventListener( 'resize', this.onWindowResize, false );
            //render set
            this.renderer=new THREE.WebGLRenderer({antialias : true});
            this.renderer.setClearColor(0xc7c7bf);
            this.renderer.setSize(window.innerWidth,window.innerHeight);
            document.getElementById("webGL_container").appendChild(this.renderer.domElement)
            //var obcontrols = new OrbitControls(this.camera,this.renderer.domElement);
            this.renderer.setPixelRatio( window.devicePixelRatio );
            document.body.appendChild( WEBVR.createButton(this.renderer ) );
            this.renderer.vr.enabled = true;
            this.Gui();
            this.initLight();
            //coordinate axis
            //this.axis=new THREE.AxesHelper(200);
            //this.scene.add(this.axis);
            //X red Z blue Y green
            var loadermodel = new OBJLoader()
            loadermodel.load('../../static/models/skem_inner.obj',(obj)=>{
                this.inside=obj
                this.inside.children[0].geometry.center()
                this.inside.children[1].geometry.center()
                this.scene.add(this.inside)
                    loadermodel.load('../../static/models/skem_outer.obj',(obj1)=>{
                    this.out=obj1
                    this.out.children[0].geometry.center()
                    this.out.children[1].geometry.center()
                    this.scene.add(this.out)
                    this.out.rotateX(2*Math.PI/64*0.5)
                        loadermodel.load('../../static/models/skem_middle.obj',(obj2)=>{
                        this.middle=obj2
                        this.middle.children[0].geometry.center()
                        this.middle.children[1].geometry.center()
                        this.middle.rotateX(2*Math.PI/17*0.8)
                        this.middle.position.set(0,this.middleR,0)
                        this.scene.add(this.middle)
                        this.addSkybox()
                        this.renderer.setAnimationLoop(this.animate)
                    })
                })
            })
            
            
        },
        onWindowResize() {
            this.camera.aspect = window.innerWidth / window.innerHeight;
            this.camera.updateProjectionMatrix();
            this.renderer.setSize( window.innerWidth, window.innerHeight );
        },
        initLight()
        {
          var pointLight = new THREE.PointLight( 0x2a4895, 1);
          pointLight.position.set( 100, 100, 100 );
          this.scene.add( pointLight );

          var pointLight = new THREE.PointLight( 0xffaaaa, 1);
          pointLight.position.set( -100, 100, 100 );
          this.scene.add( pointLight );
         },
        animate() 
        {   
            var k=-64/30;
            var k1=-17/30;
            var omegaH=(k*this.controls.speedFar-this.controls.speedMiddle)/(k-1);//公转转速
            var presentAngle=this.lastAngle-omegaH;
            this.middle.position.z=this.middleR*Math.cos(presentAngle);
            this.middle.position.y=this.middleR*Math.sin(presentAngle);
            this.lastAngle=presentAngle;
            if(this.lastAngle>2*Math.PI)
            {
                this.lastAngle-=2*Math.PI;
            }
            else if(this.lastAngle<0)
            {
                this.lastAngle+=2*Math.PI;
            }
            var omega2=(this.controls.speedMiddle-omegaH+k1*omegaH)/k1;//自转速度
            this.middle.rotation.x+=omega2;
            this.out.rotation.x+=this.controls.speedFar;
            this.inside.rotation.x+=this.controls.speedMiddle;
            //天空盒
            this.mesh.rotation.y+=0.0003;
            //渲染
            this.renderer.render( this.scene, this.camera );
        },
        Gui()
        {
            this.controls=
            {
                speedFar:0,
                speedMiddle:0
            }
            var gui=new dat.GUI();
            //LongestPole为长度
            gui.add(this.controls,'speedFar',-0.1,0.1).name("内啮合齿轮速度");
            gui.add(this.controls,'speedMiddle',-0.1,0.1).name("中心轮速度");
        },
        //speedFar 最大的圆自转速度 speedMiddle 最小圆转速 omegaH 公转速度 omega2 自转速度
        //Mycharts为实时画图接口
        MyCharts(z1,z2,z3)
        {
            var k1=-z3/z1;
            var k2=-z2/z1;
            for(var i=0;i<=100;i++)
            {
                for(var j=0;j<=100;j++)
                {
                    var w1=i-50//中心轮转速
                    var w3=j-50//内齿轮转速
                    var wh=(k1*w3-w1)/(k1-1)
                    var w2=(w1-wh+k2*wh)/k2
                    if(wh>this.max1)this.max1=wh
                    if(wh<this.min1)this.min1=wh
                    if(w2>this.max2)this.max2=w2
                    if(w2<this.min2)this.min2=w2
                    this.alist.push([i,j,wh])
                    this.blist.push([i,j,w2])
                }
                this.xData.push(i-50)
                this.yData.push(i-50)
            }
            this.myChart.setOption(this.echartOption(this.xData,this.yData,this.alist,this.min1,this.max1,'行星轮公转速度'));
            this.myChart1.setOption(this.echartOption(this.xData,this.yData,this.blist,this.min2,this.max2,'行星轮自转速度'));
        },
        addSkybox(){
            for(var i=0;i<=5;i++){
                this.array1[i]=this.setpath+this.array1[i]+this.format;
            }
            //set the size of skybox
            this.skybox=new THREE.BoxBufferGeometry(5000,5000,5000);//5000 5000 5000
            for(i=0;i<=5;i++){
                this.texture[i]=new THREE.MeshBasicMaterial({map:new THREE.TextureLoader().load(this.array1[i]),side:THREE.BackSide});
            }
            this.mesh=new THREE.Mesh(this.skybox,this.texture);
            this.mesh.position.x=0;
            this.mesh.position.y=0;
            this.mesh.position.z=0;
            this.scene.add(this.mesh);
        },
        echartOption(xData,yData,List,min,max,text)
        {
            var option = {
                title:{
                    text: text
                },
                toolbox: {
                    // y: 'bottom',
                    feature: {
                        saveAsImage: {backgroundColor: 'rgba(255,255,255,0)'}
                    }
                },
                tooltip: {},
                xAxis: {
                    type: 'category',
                    data: xData
                },
                yAxis: {
                    type: 'category',
                    data: yData
                },
                visualMap: {
                    min: min,
                    max: max,
                    calculable: true,
                    realtime: true,
                    inRange: {
                        color: ['#313695', '#4575b4', '#74add1', '#abd9e9', '#e0f3f8', '#ffffbf', '#fee090', '#fdae61', '#f46d43', '#d73027', '#a50026']
                    }
                },
                series: [{
                    name: 'speed',
                    type: 'heatmap',
                    data: List,
                    itemStyle: {
                        emphasis: {
                            borderColor: '#333',
                            borderWidth: 1
                        }
                    },
                    progressive: 1000,
                    animation: false
                }]
            };
            return option;
        },
        Topage(path)
        {
            this.$router.push(path);
        },
        removeTags(classname)
        {
            var targetElem=document.getElementsByClassName(classname);
            if(targetElem.length>=2){
                targetElem[0].parentNode.removeChild(targetElem[0]);
            }
            
        }
        },
        mounted(){
            this.init();
            // this.myChart=this.$echarts.init(document.getElementById('myecharts'));
            // this.myChart1=this.$echarts.init(document.getElementById('myecharts1'));
            // this.MyCharts(this.z1,this.z2,this.z3)
        },
        destroyed()
        {
            var classname='dg main a'
            var targetElem=document.getElementsByClassName(classname);
            while(targetElem.length>0)
            {
                document.getElementsByClassName('dg ac')[0].removeChild(targetElem[0]);
            }
        }
    
}

</script>
