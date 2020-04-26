<template>
<div>
    <el-row >
        <div style="top:15px;left:15px;z-index:1000;position:absolute;opacity:0.8;">
            <el-button type="success" round @click="Topage('/threed')">返回</el-button>
            <!-- <el-button @click="show1=!show1" type="success" round>看图</el-button>
            <el-button @click="show2=!show2" type="success" round>看讲解</el-button> -->
        </div>
    </el-row>

    <div style="z-index:1000;position:absolute;left:50px;top:80px;color:white;font-weight:bold;
    text-align:left;width:300px">
        <span class="demonstration">目镜旋转角度(°) 从-150°到150°</span>
        <el-slider v-model="rotationAngle" :max=maxAngle :min=minAngle></el-slider>
    </div>

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
import {STLLoader} from 'three/examples/jsm/loaders/STLLoader.js'

export default {

    data(){
        return{
            scene:null,
            camera:null,
            renderer:null,
            axis:null,
            rotationAngle:0,
            maxAngle:150,
            minAngle:-150,
            eyepieceSet:null,
            eyepiece:null,
            set:null,
            collimator:null,
            eyepiecePotGroup:null,
            rotationInit:0
            }
        },
    methods:{
        
        init()
        {
            this.AddScene();
            this.AddCamera();
            this.AddRender();
            this.AddListener();
            this.AddOrbitControls();
            this.AddAxis();
            this.AddModel();
            this.Addfloor();
            this.Addlight();
            //this.AddLocatingSpot();
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

        AddListener(){
            
            window.addEventListener( 'resize', ()=>{
                this.camera.aspect = window.innerWidth / window.innerHeight;
                this.camera.updateProjectionMatrix();
                this.renderer.setSize( window.innerWidth, window.innerHeight ); 
            }, false );
        },

        AddOrbitControls(){
            var OrbitControls = require('three-orbit-controls')(THREE);
            var obcontrol = new OrbitControls(this.camera,this.renderer.domElement);
        },
        AddLocatingSpot(){
            //本函数用来添加定位点
            var geometry1=new THREE.SphereGeometry(5,5,5);
            var material1 = new THREE.MeshBasicMaterial({color:0xB3DD,opacity:0,transparent:true});
            var mesh1 = new THREE.Mesh(geometry1,material1);
            this.scene.add(mesh1);
            mesh1.position.copy(this.set.position);
            mesh1.position.x -= 238;
            mesh1.position.y -=105;
            mesh1.name = 'spot1';

            var geometry3=new THREE.SphereGeometry(5,5,5);
            var material3 = new THREE.MeshBasicMaterial({color:0xB3DD,opacity:0,transparent:true});
            var mesh3 = new THREE.Mesh(geometry3,material3);
            this.scene.add(mesh3);
            mesh3.position.copy(mesh1.position);
            mesh3.position.x += 800;
            mesh3.name = 'spot3';

            var material = new THREE.LineDashedMaterial({color:0xb91913});
            var geometry = new THREE.Geometry();
            geometry.vertices.push(mesh1.position);
            geometry.vertices.push(mesh3.position);
            var line = new THREE.Line(geometry, material);
            this.scene.add(line);

        },
        AddModel(){
            var x = 150;
            var z = -100;
            //4个模型都向左挪150,向后挪-100
            var loader = new STLLoader();
            //目镜架
            loader.load('../../static/models/eyepiece_holder.stl',(geometry)=>{
                var material = new THREE.MeshPhongMaterial( { color: 0xbebdc5,opacity:0.5,transparent:true} );
                this.eyepieceSet = new THREE.Mesh( geometry, material );
                this.eyepieceSet.position.set(x-240,-238,z);
                this.eyepieceSet.rotation.x = -Math.PI/2
                this.eyepieceSet.rotation.z = Math.PI/2;
                this.eyepieceSet.scale.set(5,5,5);
                this.eyepieceSet.name = 'eyepieceSet';
                this.scene.add(this.eyepieceSet);
            })
            /****************************************/
            var loader = new STLLoader();
            //目镜
            loader.load('../../static/models/eyepiece.stl',(geometry)=>{
                var material = new THREE.MeshPhongMaterial( { color: 0xbebdc5,opacity:0.5,transparent:true} );
                this.eyepiece = new THREE.Mesh( geometry, material );
                this.eyepiece.scale.set(5,5,5);
                this.eyepiece.name = 'eyepiece';  

                var geometry2=new THREE.SphereGeometry(5,5,5);
                var material2 = new THREE.MeshBasicMaterial({color:0xB3DD,opacity:0,transparent:true});
                var mesh2 = new THREE.Mesh(geometry2,material2);
                mesh2.position.y += 500;
                mesh2.position.z +=135;
                mesh2.name = 'spot2';
                
                this.eyepiecePotGroup = new THREE.Group();
                this.eyepiecePotGroup.add(mesh2);
                this.eyepiecePotGroup.add(this.eyepiece);
                this.eyepiecePotGroup.rotation.set(-Math.PI/2,0,Math.PI/2);
                this.eyepiecePotGroup.position.set(x-240,-238,z);
                
                this.scene.add(this.eyepiecePotGroup);
                
            })
            /****************************************/
            var loader = new STLLoader();
            loader.load('../../static/models/set.stl',(geometry)=>{
                var material = new THREE.MeshPhongMaterial( { color: 0xbebdc5,opacity:0.5,transparent:true} );
                this.set = new THREE.Mesh( geometry, material );
                this.set.position.set(x,0,z);
                this.set.rotation.x = -Math.PI/2;
                this.set.rotation.z = Math.PI/2;
                this.set.scale.set(5,5,5);
                this.scene.add(this.set);
                this.AddLocatingSpot();
            })
            /****************************************/
            var loader = new STLLoader();
            //平行光管
            loader.load('../../static/models/collimator.stl',(geometry)=>{
                var material = new THREE.MeshPhongMaterial( { color: 0xbebdc5,opacity:0.5,transparent:true} );
                this.collimator = new THREE.Mesh( geometry, material );
                this.collimator.position.set(x,0,z);
                this.collimator.rotation.x = -Math.PI/2;
                this.collimator.rotation.z = Math.PI/2;
                this.collimator.scale.set(5,5,5);
                this.scene.add(this.collimator);
            })
            
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
            var bulblight=new THREE.PointLight( 0xffffff);
            bulblight.position.set(-200,-200,200);
            this.scene.add(bulblight);

        },
         
        AddAxis()
        {
            //x红 z蓝 y绿
            this.axis=new THREE.AxesHelper(200);
            this.scene.add(this.axis);
        },

        animate() 
        {   
            if(this.scene.getObjectByName('eyepieceSet')!=undefined && this.scene.getObjectByName('spot1')!=undefined && this.eyepiecePotGroup!=null){
                this.eyepieceSet.rotation.z=Math.PI/2+this.rotationAngle*Math.PI/180;
                this.eyepiecePotGroup.rotation.z=Math.PI/2+this.rotationAngle*Math.PI/180; 
                if(this.eyepiecePotGroup.rotation.z!=this.rotationInit){
                    var material = new THREE.LineDashedMaterial({color:0xb91913});
                    var geometry = new THREE.Geometry();
                    geometry.vertices.push(this.scene.getObjectByName('spot2').matrixWorld.getPosition());
                    geometry.vertices.push(this.scene.getObjectByName('spot1').position);
                    var line = new THREE.Line(geometry, material);
                    line.name = 'line1';
                    this.scene.remove(this.scene.getObjectByName('line1'));
                    this.scene.add(line);
                    this.rotationInit = this.eyepiecePotGroup.rotation.z;
                }
                
            }
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