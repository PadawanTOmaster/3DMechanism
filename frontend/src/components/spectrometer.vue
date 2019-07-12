<template>
<div>
    <el-row >
        <div style="top:15px;left:15px;z-index:1000;position:absolute;opacity:0.8;">
            <el-button type="success" round @click="Topage('/threed')">返回</el-button>
            <!-- <el-button @click="show1=!show1" type="success" round>看图</el-button>
            <el-button @click="show2=!show2" type="success" round>看讲解</el-button> -->
        </div>
    </el-row>
    <div id="webGL_container" style="position:absolute;z-index:0">
    </div>
    
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
  .container {
        position:absolute;
        z-index: 1000;
        left:25px;
        top:100px;
        width:30%;
        
    }
    .container2{
        position:absolute;
        z-index: 1000;
        right:25px;
        top:100px;
        width:30%;
    }
    .block {
        text-align:left;
    }
    .bottom {
      clear: both;
      text-align: center;
    }

    .item {
      margin: 4px;
      
    }
 
</style>

<script>
import * as THREE from 'three'
import dat from 'dat.gui'
import {MTLLoader, OBJLoader} from 'three-obj-mtl-loader'


export default {

    data(){
        return{
            scene:null,
            camera:null,
            renderer:null,
            axis:null,
            }
    },
    methods:{
        
        init()
        {
            
            this.AddScene();
            this.AddCamera();
            this.AddRender();
            this.AddOrbitControls();
            this.Addfloor();
            this.Addlight()
    
            this.animate();
            
        },
         
        AddScene()
        {
            this.scene=new THREE.Scene();
        },

        AddCamera()
        {
            this.camera=new THREE.PerspectiveCamera( 50, window.innerWidth/window.innerHeight,0.1,10000);
            this.camera.position.x=400;
            this.camera.position.y=800;
            this.camera.position.z=400;//40 40 40 //0 150 400
            this.camera.lookAt(0,0,0);
        },

        AddRender()
        {
            this.renderer=new THREE.WebGLRenderer({antialias : true});
            this.renderer.setClearColor(0x000000);
            this.renderer.setSize(window.innerWidth,window.innerHeight);
            document.getElementById("webGL_container").appendChild(this.renderer.domElement)
        },

        AddOrbitControls()
        {
            var OrbitControls = require('three-orbit-controls')(THREE);
            var obcontrol = new OrbitControls(this.camera,this.renderer.domElement);
        },

        AddAxis()
        {
            this.axis=new THREE.AxesHelper(200);
            this.scene.add(this.axis);
        },
        
        Addfloor()
        {
            var boxTexture=[]
            boxTexture[3]=this.LoadTexture("../../static/images/hardwood2_diffuse.jpg",8,8)
            for(var i=0;i<=5;i++){
                if(i==3) continue;
                boxTexture[i]=this.LoadTexture("../../static/images/woodtexture.jpg",2,2)
            }
            var boxH = 5000
            var box=new THREE.BoxBufferGeometry(boxH,boxH,boxH)
            this.floor=new THREE.Mesh(box,boxTexture);
            this.floor.position.x=0;
            this.floor.position.y=1/2*boxH-300;
            this.floor.position.z=0;
            this.scene.add(this.floor);
        },
        LoadTexture(src,repeatx,repeaty){
            var floorMat = new THREE.MeshBasicMaterial( {
                color: 0xffffff,
                side:THREE.BackSide
            })
            var textureLoader = new THREE.TextureLoader()
            textureLoader.load(src, function ( map ) {
                map.wrapS = THREE.RepeatWrapping;
                map.wrapT = THREE.RepeatWrapping;
                map.anisotropy = 4;
                map.repeat.set(repeatx,repeaty);
                floorMat.map = map;
                floorMat.needsUpdate = true;
            })
            return floorMat
        },
        
        
        Addlight()
        {
            var bulblight=[];
            for(var i=0;i<=5;i++)
            {
                bulblight[i]=new THREE.PointLight( 0xffffff, 3, 100, 1 );
            }
            bulblight[0].position.set(50,-50,80)
            bulblight[1].position.set(50,50,80)
            bulblight[2].position.set(-50,-50,80)
            bulblight[3].position.set(-50,50,80)
            bulblight[4] = new THREE.PointLight( 0xffffff, 3, 300, 1 )
            bulblight[4].position.set(200,0,50)
            bulblight[5] = new THREE.PointLight( 0xffffff, 3, 300, 1 )
            bulblight[5].position.set(300,-90,0)
            this.scene.add(bulblight[0])
            this.scene.add(bulblight[1])
            this.scene.add(bulblight[2])
            this.scene.add(bulblight[3])
            this.scene.add(bulblight[4])
            this.scene.add(bulblight[5])
        },
         
        animate() 
        {   
            this.renderer.render( this.scene, this.camera );
            requestAnimationFrame(this.animate);
        },
        
        AddGui()
        {
           
        },
        //speedFar 最大的圆自转速度 speedMiddle 最小圆转速 omegaH 公转速度 omega2 自转速度
        Topage(path)
        {
            this.$router.push(path);
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
            // this.myChart=this.$echarts.init(document.getElementById('myecharts'));
            // this.myChart1=this.$echarts.init(document.getElementById('myecharts1'));
            // this.myChart2=this.$echarts.init(document.getElementById('myecharts2'));
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