<template>
<div>
    <el-row >
        <div style="top:15px;left:15px;z-index:1000;position:absolute;opacity:0.8;">
            <el-button type="success" round @click="Topage('/threed')">返回</el-button>
            <el-button @click="show1=!show1" type="success" round>看图</el-button>
            <el-button @click="show2=!show2" type="success" round>看讲解</el-button>
            <el-button @click="buttonpress=-buttonpress" type="warning" round>画线</el-button>
            <el-button @click="deleteline()" type="warning" round>删除已画线</el-button>
        </div>
    </el-row>
    <div id="webGL_container" style="position:absolute;z-index:0">
    </div>
    
     <el-collapse-transition>
         <div style="z-index:1000;position:absolute;left:20px;top:100px;">
        <el-container v-show="show1">
            <el-main>
                <div id="myecharts" style="width:400px;height:200px;"></div>
                <div id="myecharts1" style="width:400px;height:200px;"></div>
                <div id="myecharts2" style="width:400px;height:200px;"></div>
            </el-main>
        </el-container>
        </div>
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
export default {

    data(){
        return{
            scene:null,
            camera:null,
            renderer:null,
            axis:null,
            
            myChart:null,
            myChart1:null,
            myChart2:null,
            show:true,
            show1:true,
            show2:true,
           
            controls:null,//GUI界面
            transformcontrol:null,
            obcontrol:null,
            mesh:null
            }
    },
    methods:{
        
        init()
        {
            
            this.AddScene();
            this.AddCamera();
            this.AddRender();
            this.Addfloor();
            this.Addlight();
            this.AddAxis(-10*this.barwide,0,0,50*this.barwide,0,0);
            this.AddOrbitControls();
            this.AddTransformControls();
            
            //X red Z blue Y green	
            
            
            this.Addpoints();
            
            this.animate();
        },
         
        AddScene()
        {
            this.scene=new THREE.Scene();
        },

        AddCamera()
        {
            this.camera = new THREE.PerspectiveCamera( 50, window.innerWidth / window.innerHeight, 0.1, 1000 );
            this.camera.position.x = 40;
            this.camera.position.y = 20;
            this.camera.position.z = 40;
        },

        AddRender()
        {
            this.renderer=new THREE.WebGLRenderer({antialias : true});
            this.renderer.setClearColor(0x010101);
            this.renderer.setSize(window.innerWidth,window.innerHeight);
            document.getElementById("webGL_container").appendChild(this.renderer.domElement)
        },

        AddOrbitControls()
        {
            var OrbitControls = require('three-orbit-controls')(THREE);
            this.obcontrol = new OrbitControls(this.camera, this.renderer.domElement);
            
		    this.obcontrol.addEventListener( 'change', this.animate );
        },
        AddTransformControls(){
            var TransFormControls = require('threejs-transformcontrols')
            this.transformcontrol = new TransFormControls( this.camera,this.renderer.domElement)
            this.transformcontrol.setSize( this.transformcontrol.size - 0.6 );
			this.transformcontrol.addEventListener( 'change', this.animate );
			this.transformcontrol.addEventListener( 'dragging-changed', function ( event ) {
					this.obcontrol = ! event.value;
              } );
            
            
        },
        AddAxis()
        {
            this.axis=new THREE.AxesHelper(200);
            this.scene.add(this.axis);
        },

        Addfloor()
        {
            var floorMat = new THREE.MeshStandardMaterial( {
                roughness: 0.8,
                color: 0xffffff,
                metalness: 0.2,
                bumpScale: 0.0005
            } );
            var textureLoader = new THREE.TextureLoader();
            textureLoader.load( "../../static/images/hardwood2_diffuse.jpg", function ( map ) {
                map.wrapS = THREE.RepeatWrapping;
                map.wrapT = THREE.RepeatWrapping;
                map.anisotropy = 4;
                map.repeat.set( 10, 24 );
                floorMat.map = map;
                floorMat.needsUpdate = true;
            } );
            var floorGeometry = new THREE.PlaneBufferGeometry( 200, 200 );
            var floorMesh = new THREE.Mesh( floorGeometry, floorMat );
            floorMesh.receiveShadow = true;
            // floorMesh.rotation.x = - Math.PI / 2.0;
            floorMesh.position.set(0,0,-40)
            this.scene.add( floorMesh );
        },
        Addlight()
        {
            var bulbLight = new THREE.PointLight( 0xffee88, 3, 100, 2 );
            bulbLight.position.set(0,0, 20*this.barwide);
            bulbLight.castShadow = true;
            this.scene.add( bulbLight );
        },

       

        Addpoints()
        {   
            var material = new THREE.MeshNormalMaterial(
                {
                    map:new THREE.TextureLoader().load('../../static/images/crate.gif'),side:THREE.DoubleSide
                })    
            var geometry = new THREE.BoxGeometry(5,5,5);
            this.mesh = new THREE.Mesh(geometry,material);
            this.scene.add(this.mesh);
            this.transformcontrol.attach( this.mesh );
            this.scene.add(this.transformcontrol)
        },
        animate() 
        {   
            this.renderer.render( this.scene, this.camera );
            //requestAnimationFrame(this.animate);
        },
       
        Gui()
        {
            this.controls=
            {
                speed:0,
                a:10*this.barwide,
                d:20*this.barwide,
            }
            var gui=new dat.GUI();
            //LongestPole为长度
            gui.add(this.controls,'a',0,15*this.barwide).name("原动件长度");
            gui.add(this.controls,'d',20*this.barwide,30*this.barwide).name("机架间距");
            gui.add(this.controls,'speed',-0.1,0.1).name("原动件角速度");
        },
        //speedFar 最大的圆自转速度 speedMiddle 最小圆转速 omegaH 公转速度 omega2 自转速度
        Topage(path)
        {
            this.$router.push(path);
        },

        AddSkyBox()
        {
            this.skybox=new THREE.BoxBufferGeometry(5000,5000,5000);
            for(var i=0;i<=5;i++)
            {
                this.SixSidesOfBox[i]=this.setpath+this.SixSidesOfBox[i]+this.format;
            }
            for(i=0;i<=5;i++)
            {
                this.skyboxTexture[i]=new THREE.MeshBasicMaterial
                ({map:new THREE.TextureLoader().load(this.SixSidesOfBox[i]),side:THREE.BackSide});
            }
            this.skyboxmeshed=new THREE.Mesh(this.skybox,this.skyboxTexture);
            this.skyboxmeshed.position.x=0;
            this.skyboxmeshed.position.y=0;
            this.skyboxmeshed.position.z=0;
            this.scene.add(this.skyboxmeshed);
        },
        setEcharts(buffList,linecolor,text)
        {
            var option = {
                title: {
                    text: text,
                    textStyle: {
	        	        color: '#faf0e6'
	      	        }
                },
                xAxis: {
                    type: 'category',
                    data: []
                },
                yAxis: {
                    type: 'value'
                },
                color:[linecolor],
                series: [
                    {
                        data: buffList,
                        type: 'line',
                        smooth: false,
                    },
                    ]
            };
            return option;
        },
        },
        mounted(){
            this.init();
            //this.myChart=this.$echarts.init(document.getElementById('myecharts'));
            //this.myChart1=this.$echarts.init(document.getElementById('myecharts1'));
            //this.myChart2=this.$echarts.init(document.getElementById('myecharts2'));
            
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