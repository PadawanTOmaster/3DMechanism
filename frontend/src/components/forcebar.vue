<template>
<div>
<el-row >
    <div style="top:15px;left:15px;z-index:1000;position:absolute;opacity:0.8;">
        <el-button type="success" round @click="Topage('/threed')">返回</el-button>
        &nbsp;&nbsp;&nbsp;
        <el-button type='warning' round @click='changegraph()'>切换2D图</el-button>
        <el-button type="warning" round @click="show3Dgraph()">{{buttontype}}</el-button>
    </div>
</el-row>
 <div style="z-index:1000;position:absolute;left:20px;top:100px;">
        <el-container>
            <el-main>
                <el-collapse-transition>
                    <div v-show='show1'>
                        <div id="myecharts" style="width:400px;height:300px;"></div>
                        <div id="myecharts1" style="width:400px;height:300px;"></div>
                    </div>
                </el-collapse-transition>
                <el-collapse-transition>
                    <div v-show='show2'>
                        <div id="myecharts2" style="width:400px;height:300px;"></div>
                        <div id="myecharts3" style="width:400px;height:300px;"></div>
                    </div>
                </el-collapse-transition>
            </el-main>
        </el-container>
        </div>
    <div id="webGL_container" style="position:absolute;z-index:0">
    </div>
    <el-dialog
  title="输入杆所受力的数量"
  :visible.sync="dialogVisible"
  width="30%"
  :show-close=false
  :close-on-click-modal=false
  :close-on-press-escape=false
  >
   <el-form>
    <el-form-item label="力的数量" :label-width="formLabelWidth">
        <el-input v-model='numOfforce'></el-input>
    </el-form-item>
    <el-form-item label="力矩的数量" :label-width="formLabelWidth">
        <el-input v-model='numOfmoment'></el-input>
    </el-form-item>
    <el-form-item label="均布载荷的数量" :label-width="formLabelWidth">
        <el-input v-model='numOfuniform'></el-input>
    </el-form-item>
  </el-form>
  <span slot="footer" class="dialog-footer">
    <el-button type="primary" @click="sureToPost()">确 定</el-button>
  </span>
</el-dialog>

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
var controls={};
var forceValueList=[];
var forceDistanceList=[];
var forceTypeList=[];
var BarLength=400;
var arrowlist={};
var arrowmomentlist={};
var arrowunilist={};
var colorlist=[];
var lastPositionlist=[0];
var lastSizelist=[0];
var lastangleyzYlist=[0];
var lastanglexyYlist=[0];

var lastPositionMomlist=[0];
var lastSizeMomlist=[0];
var lastangleyzYMomlist=[0];
var lastanglexyYMomlist=[0];

var lastSizeUnilist=[0];
var lastangleyzYUnilist=[0];
var lastanglexyYUnilist=[0];
var laststartposition=[0];
var lastendposition=[0];

var lastcoefficients=1;
var lastMomcoefficients=1;
var lastUnicoefficients=1;
var Barmeshed;
var maxforcesize;

var EmultifyI = 0.206*Math.PI*160000/64;//拉伸模量乘惯性矩
var EmultifyA = 206*Math.PI*100000;//拉伸模量乘横截面积

var Endpoint=[0];
var Startpoint=[0];
var arrowstep=10;

var arrowlengthFs3D=[];
var arrowlengthMe3D=[];

var arrowFs3D=[];
var arrowMe3D=[];

var countbutton=0;
var arrowsegment=40;

var guiflag=0;
export default {

    data(){
        return{
            dialogVisible:true,
            formLabelWidth: '120px',
            numOfforce:'1',
            numOfmoment:'1',
            numOfuniform:'1',
            scene:null,
            camera:null,
            renderer:null,
            axis:null,
            setpath:'../../static/images/',
            format:'.jpg',
            SixSidesOfBox:['px','nx','py','ny','pz','nz'],
            skybox:null,
            skyboxTexture:[],
            skyboxmeshed:null,
            myChart:null,
            myChart1:null,
            buttontype:'查看3D剪力图',
            show1:true,
            show2:false,
            }
    },
    methods:{

        RemoveRedundantCss()
        {
            this.removeTags('dg main a');
        },
        
        removeTags(classname)
        {
            var targetElement=document.getElementsByClassName(classname);
            if(this.WhetherRedunctantCssExist()){
                var firstReluctantElement=targetElement[0]
                firstReluctantElement.parentNode.removeChild(firstReluctantElement);
            }
            
        },

        WhetherRedunctantCssExist()
        {
            if(targetElem.length>=2)return 1;
            else return 0;
        },

        InsertEchartsToHtml()
        {
            this.myChart=this.$echarts.init(document.getElementById('myecharts'));
            this.myChart1=this.$echarts.init(document.getElementById('myecharts1'));
            this.myChart2=this.$echarts.init(document.getElementById('myecharts2'));
        },

        sureToPost()
        {
            this.dialogVisible=false;
            this.numOfmoment=parseInt(this.numOfmoment)
            this.numOfforce=parseInt(this.numOfforce)
            this.numOfuniform=parseInt(this.numOfuniform)
            if(this.numOfforce>0)this.AddGui();
            if(this.numOfmoment>0)this.AddMomentGui();
            if(this.numOfuniform>0)this.AddUniformGui();
            this.ToThreeD();
        },

        ToThreeD()
        {
            this.AddScene();
            this.AddCamera();
            this.AddRender();
            this.AddOrbitControls();
            this.AddAxis();
            this.AddSkyBox();
            this.AddPlaneGeometry();
            this.AddLight();
            this.AddBarShadow();
            this.AddBar();
            requestAnimationFrame(this.animate);               
        },

        AddGui()
        {
            var gui=new dat.GUI();
            
            controls['coefficients']=1;
            gui.add(controls,'coefficients',0,25).name("力的形变系数");
            for(var i=1;i<=this.numOfforce;i++)
            {
                var strdistance='force'+i+"distance";
                var strsize='force'+i+"size";
                var angleyzY='force'+i+'angleyz';//力在yz面的投影与Y轴正方向的夹角
                var anglexyY='force'+i+'anglexy';//力在xy面的投影与Y轴正方向的夹角
                var maxforcesize=300/this.numOfforce;
                controls[angleyzY]=0;//
                controls[anglexyY]=0;//
                
                controls[strdistance]=0;
                controls[strsize]=0;
                gui.add(controls,strdistance,0,BarLength).name("力"+i+"与墙的间距");
                gui.add(controls,strsize,-maxforcesize,maxforcesize).name("力"+i+"的大小");
                gui.add(controls,angleyzY,-Math.PI/2+0.01,Math.PI/2-0.01).name("力与纵截面的夹角");
                gui.add(controls,anglexyY,-Math.PI/2+0.01,Math.PI/2-0.01).name("力与横截面的夹角");
                lastPositionlist.push(0);
                lastSizelist.push(0);
                lastangleyzYlist.push(0);
                lastanglexyYlist.push(0);
            }
        },

        AddMomentGui()
        {
            var gui = new dat.GUI();
            controls['Momcoefficients']=1;
            gui.add(controls,'Momcoefficients',0,25).name("力矩形变系数");
            var maxforcesize=40/this.numOfmoment;
            for(var i=1;i<=this.numOfmoment;i++)
            {
                var strdistance='moment'+i+"distance";
                var strsize='moment'+i+"size";
                var angleyzY='moment'+i+'angleyz';//力在yz面的投影与Y轴正方向的夹角
                var anglexyY='moment'+i+'anglexy';//力在xy面的投影与Y轴正方向的夹角
                
                controls[angleyzY]=0;//
                controls[anglexyY]=0;//
                
                controls[strdistance]=0;
                controls[strsize]=0;
                gui.add(controls,strdistance,0,BarLength).name("力矩"+i+"与墙的间距");
                gui.add(controls,strsize,-maxforcesize,maxforcesize).name("力矩"+i+"的大小");
                gui.add(controls,angleyzY,-Math.PI/2+0.01,Math.PI/2-0.01).name("力矩与纵截面的夹角");
                gui.add(controls,anglexyY,-Math.PI/2+0.01,Math.PI/2-0.01).name("力矩与横截面的夹角");
                lastPositionMomlist.push(0);
                lastSizeMomlist.push(0);
                lastangleyzYMomlist.push(0);
                lastanglexyYMomlist.push(0);
            }
        },

        AddUniformGui()
        {
            var gui=new dat.GUI();
            
            controls['Unicoefficients']=1;
            gui.add(controls,'Unicoefficients',0,25).name("力的形变系数");
            for(var i=1;i<=this.numOfuniform;i++)
            {
                var strsize='uniform'+i+"size";
                var angleyzY='uniform'+i+'angleyz';//力在yz面的投影与Y轴正方向的夹角
                var anglexyY='uniform'+i+'anglexy';//力在xy面的投影与Y轴正方向的夹角
                var startposition='startPosition'+i;
                var endposition='endPosition'+i;
                var maxforcesize=2500/this.numOfuniform;
                controls[angleyzY]=0;//
                controls[anglexyY]=0;//
                
                controls[startposition]=0;
                controls[endposition]=0;

                controls[strsize]=0;
                gui.add(controls,startposition,0,BarLength).name("均布载荷"+i+"的起始位置");
                gui.add(controls,endposition,0,BarLength).name("均布载荷"+i+"的终止位置");
                gui.add(controls,strsize,-maxforcesize,maxforcesize).name("均布载荷"+i+"的大小");
                gui.add(controls,angleyzY,-Math.PI/2+0.01,Math.PI/2-0.01).name("均布载荷与纵截面的夹角");
                gui.add(controls,anglexyY,-Math.PI/2+0.01,Math.PI/2-0.01).name("均布载荷与横截面的夹角");
                lastSizeUnilist.push(0);
                lastangleyzYUnilist.push(0);
                lastanglexyYUnilist.push(0);
                laststartposition.push(0);
                lastendposition.push(0);
                Startpoint.push(0);
                Endpoint.push(0);
            }
        },

        AddScene()
        {
            this.scene=new THREE.Scene();
        },

        AddCamera()
        {
            this.camera=new THREE.PerspectiveCamera( 50, window.innerWidth/window.innerHeight,0.1,10000);
            this.camera.position.x=-560;
            this.camera.position.y=240;
            this.camera.position.z=300;//40 40 40 //0 150 400
            this.camera.lookAt(0,0,0);
        },

        AddRender()
        {
            this.renderer=new THREE.WebGLRenderer({antialias : true});
            this.renderer.setClearColor(0xc7c7bf);
            this.renderer.setSize(window.innerWidth,window.innerHeight);
            document.getElementById("webGL_container").appendChild(this.renderer.domElement)
        },

        AddOrbitControls()
        {
            var OrbitControls = require('three-orbit-controls')(THREE);
            var controls = new OrbitControls(this.camera,this.renderer.domElement);
        },

        AddAxis()
        {
            this.axis=new THREE.AxesHelper(200);
            this.scene.add(this.axis);
        },
       
        AddPlaneGeometry()
        {
            var planeGeometry = new THREE.PlaneGeometry(200,200,10,10);
            var planeMeterial = new THREE.MeshLambertMaterial({map:new THREE.TextureLoader().load('../../static/images/hardwood.jpg'),side:THREE.DoubleSide});
            var plane = new THREE.Mesh(planeGeometry,planeMeterial);
            this.scene.add(plane);
        },

        AddLight()
        {
            var pointLight = new THREE.PointLight( 0xFFFFFF, 1);
            pointLight.position.set( 0, 0, -100  );
            this.scene.add( pointLight );

            var pointLight = new THREE.PointLight( 0xffffff, 1);
            pointLight.position.set( 0, 0, 100 );
            this.scene.add( pointLight );
            var light = new THREE.DirectionalLight(0xffffff);
            this.scene.add(light); //将光添加到场景中
         },

        AddBar()
        {
            var points=[];
            var FspointsY=[];
            var MepointsY=[];
            var FspointsX=[];
            var MepointsX=[];

            var Fnpoints=[];
            var Tpoints=[];
            arrowlengthFs3D=[];
            arrowlengthMe3D=[];
            for(var i=0;i<BarLength;i++)
            {
                var x=0;
                var y=0;
                var z=0;

                var FsY=0;
                var MeY=0;
                var FsX=0;
                var MeX=0;
                
                var Fn=0;
                var T=0;

                var Fs3D=[];
                var Me3D=[];
                for(var j=1;j<=this.numOfforce;j++)
                {
                    var strdistance='force'+j+"distance";
                    var strsize='force'+j+"size";
                    var angleyzY='force'+j+'angleyz';//力在yz面的投影与Y轴正方向的夹角
                    var anglexyY='force'+j+'anglexy';//力在xy面的投影与Y轴正方向的夹角

                    var tan1=Math.tan(controls[anglexyY]);
                    var tan2=Math.tan(controls[angleyzY]);
                    var Fx=controls[strsize]*tan1/Math.sqrt(1+Math.pow(tan1,2)+Math.pow(tan2,2));
                    var Fy=controls[strsize]/Math.sqrt(1+Math.pow(tan1,2)+Math.pow(tan2,2));
                    var Fz=controls[strsize]*tan2/Math.sqrt(1+Math.pow(tan1,2)+Math.pow(tan2,2));

                    
                    FsX+=(i<=controls[strdistance])*Fx;
                    FsY+=(i<=controls[strdistance])*Fy;
                    MeX+=-(i<=controls[strdistance])*(controls[strdistance]-i)/1000*Fy;
                    MeY+=(i<=controls[strdistance])*(controls[strdistance]-i)/1000*Fx;

                    Fn+=(i<=controls[strdistance])*Fz;
                    
                    var k=1000000;
                    y+=((i<=controls[strdistance])*(Fy*Math.pow(i,2)*(3*controls[strdistance]-i))/(6*EmultifyI)
                       +(i>controls[strdistance])*(Fy*Math.pow(controls[strdistance],2)*(3*i-controls[strdistance]))/(6*EmultifyI))*controls['coefficients']/k;
                    x+=((i<=controls[strdistance])*(Fx*Math.pow(i,2)*(3*controls[strdistance]-i))/(6*EmultifyI)
                       +(i>controls[strdistance])*(Fx*Math.pow(controls[strdistance],2)*(3*i-controls[strdistance]))/(6*EmultifyI))*controls['coefficients']/k;

                }

                for(var j=1;j<=this.numOfmoment;j++)
                {
                    var strdistance='moment'+j+"distance";
                    var strsize='moment'+j+"size";
                    var angleyzY='moment'+j+'angleyz';//力在yz面的投影与Y轴正方向的夹角
                    var anglexyY='moment'+j+'anglexy';//力在xy面的投影与Y轴正方向的夹角

                    var tan1=Math.tan(controls[anglexyY]);
                    var tan2=Math.tan(controls[angleyzY]);
                    
                    var Mx=controls[strsize]*tan1/Math.sqrt(1+Math.pow(tan1,2)+Math.pow(tan2,2));
                    var My=controls[strsize]/Math.sqrt(1+Math.pow(tan1,2)+Math.pow(tan2,2));
                    var Mz=controls[strsize]*tan2/Math.sqrt(1+Math.pow(tan1,2)+Math.pow(tan2,2));

                    MeX+=(i<=controls[strdistance])*Mx;
                    MeY+=(i<=controls[strdistance])*My;

                    T+=(i<=controls[strdistance])*Mz;

                    var k=1000;
                    y-=((i<=controls[strdistance])*Mx*Math.pow(i,2)/2/EmultifyI
                        +(i>controls[strdistance])*Mx*(2*i-controls[strdistance])*controls[strdistance]/EmultifyI/2)*controls['Momcoefficients']/k;
                   
                    x+=((i<=controls[strdistance])*My*Math.pow(i,2)/2/EmultifyI
                        +(i>controls[strdistance])*My*(2*i-controls[strdistance])*controls[strdistance]/EmultifyI/2)*controls['Momcoefficients']/k;
                }

                for(var j=1;j<=this.numOfuniform;j++)
                {
                    var strsize='uniform'+j+"size";
                    var angleyzY='uniform'+j+'angleyz';//力在yz面的投影与Y轴正方向的夹角
                    var anglexyY='uniform'+j+'anglexy';//力在xy面的投影与Y轴正方向的夹角
                    var startposition='startPosition'+j;
                    var endposition='endPosition'+j;
                    var tan1=Math.tan(controls[anglexyY]);
                    var tan2=Math.tan(controls[angleyzY]);
                    var qx=controls[strsize]*tan1/Math.sqrt(1+Math.pow(tan1,2)+Math.pow(tan2,2));
                    var qy=controls[strsize]/Math.sqrt(1+Math.pow(tan1,2)+Math.pow(tan2,2));
                    var qz=controls[strsize]*tan2/Math.sqrt(1+Math.pow(tan1,2)+Math.pow(tan2,2));
                    var a=Math.min(controls[startposition],controls[endposition]);
                    var b=Math.max(controls[startposition],controls[endposition]);

                    FsX+=((i<=a)*qx*(b-a)+(i>a && i<=b)*qx*(b-i))/1000;
                    FsY+=((i<=a)*qy*(b-a)+(i>a && i<=b)*qy*(b-i))/1000;
                    MeX-=((i<=a)*qy*(b-a)*(a/2+b/2-i)+(i>a && i<=b)*qy*(b-i)*(b-i)/2)/1000000;
                    MeY+=((i<=a)*qx*(b-a)*(a/2+b/2-i)+(i>a && i<=b)*qx*(b-i)*(b-i)/2)/1000000;

                    Fn+=((i<=a)*qz*(b-a)+(i>a && i<=b)*qz*(b-i))/1000;

                    var k=1000000000;
                    y+=((i<=a)*qy*(b-a)*i*i*(1.5*a+1.5*b-i)/6/EmultifyI
                       +(i>a && i<=b)*qy*(Math.pow(i,4)-4*b*Math.pow(i,3)+6*b*b*i*i-4*Math.pow(a,3)*i+Math.pow(a,4))/24/EmultifyI
                       +(i>b)*qy*((Math.pow(b,3)-Math.pow(a,3))*(i-b)*4+3*Math.pow(b,4)-4*Math.pow(a,3)*b+Math.pow(a,4))/24/EmultifyI)*controls['Unicoefficients']/k;
                    x+=((i<=a)*qx*(b-a)*i*i*(1.5*a+1.5*b-i)/6/EmultifyI
                       +(i>a && i<=b)*qx*(Math.pow(i,4)-4*b*Math.pow(i,3)+6*b*b*i*i-4*Math.pow(a,3)*i+Math.pow(a,4))/24/EmultifyI
                       +(i>b)*qx*((Math.pow(b,3)-Math.pow(a,3))*(i-b)*4+3*Math.pow(b,4)-4*Math.pow(a,3)*b+Math.pow(a,4))/24/EmultifyI)*controls['Unicoefficients']/k;
                }
                var count=0;
                for(var p=-Math.PI;p<Math.PI;p+=2*Math.PI/arrowsegment)
                {
                    Fs3D[count]=FsX*Math.cos(p)+FsY*Math.sin(p);
                    Me3D[count]=MeX*Math.cos(p)+MeY*Math.sin(p);
                    count++;
                }

                arrowlengthFs3D.push(Fs3D);
                arrowlengthMe3D.push(Me3D);
                points.push(new THREE.Vector3(x,y,i));
                if(i%4==0)
                {
                    MepointsY.push(MeY);
                    MepointsX.push(MeX);
                    FspointsY.push(FsY);
                    FspointsX.push(FsX);
                    Fnpoints.push(Fn);
                    Tpoints.push(T);
                }
            }

            var tubeGeometry=new THREE.TubeGeometry(new THREE.CatmullRomCurve3(points),64,10*Math.pow(BarLength/BarLength,2),20);
            var meterial = new THREE.MeshPhongMaterial({color:0xc7c7c7,side:THREE.DoubleSide});
            Barmeshed=new THREE.Mesh(tubeGeometry,meterial);
            this.scene.add(Barmeshed);
            
            this.myChart.setOption(this.AddGraph1(FspointsY,FspointsX,'剪力图'));
            this.myChart1.setOption(this.AddGraph1(MepointsY,MepointsX,'弯矩图'));
            this.myChart2.setOption(this.AddGraph2(Fnpoints,'轴力图'));
            this.myChart3.setOption(this.AddGraph2(Tpoints,'扭矩图'));
            
            
        },


        AddGraph2(data,text)
        {
            var xAxisData = [];
            for(var i=0;i<400;i+=4)
            {
                xAxisData.push(i);
            }
            var option = {
                title: {
                    text: text
                },
                legend: {
                    data: ['Z方向'],
                    align: 'left'
                },
                toolbox: {
                    // y: 'bottom',
                    feature: {
                        magicType: {
                            type: ['stack', 'tiled']
                        },
                        dataView: {},
                        saveAsImage: {
                            pixelRatio: 2
                        }
                    }
                },
                tooltip: {},
                xAxis: {
                    data: xAxisData,
                    silent: false,
                    splitLine: {
                        show: false
                    }
                },
                yAxis: {
                },
                series: [{
                    name: 'Z方向',
                    type: 'bar',
                    data: data,
                    animationDelay: function (idx) {
                        return idx * 10;
                    }
                }],
                animationEasing: 'elasticOut',
                animationDelayUpdate: function (idx) {
                    return idx * 5;
                }
                };
            return option;
        },
        AddGraph1(data1,data2,text)
        {
            var xAxisData = [];
            for(var i=0;i<400;i+=4)
            {
                xAxisData.push(i);
            }
            var option = {
                title: {
                    text: text
                },
                legend: {
                    data: ['Y方向', 'X方向'],
                    align: 'left'
                },
                toolbox: {
                    // y: 'bottom',
                    feature: {
                        magicType: {
                            type: ['stack', 'tiled']
                        },
                        dataView: {},
                        saveAsImage: {
                            pixelRatio: 2
                        }
                    }
                },
                tooltip: {},
                xAxis: {
                    data: xAxisData,
                    silent: false,
                    splitLine: {
                        show: false
                    }
                },
                yAxis: {
                },
                series: [{
                    name: 'Y方向',
                    type: 'bar',
                    data: data1,
                    animationDelay: function (idx) {
                        return idx * 10;
                    }
                }, {
                    name: 'X方向',
                    type: 'bar',
                    data: data2,
                    animationDelay: function (idx) {
                        return idx * 10 + 100;
                    }
                }],
                animationEasing: 'elasticOut',
                animationDelayUpdate: function (idx) {
                    return idx * 5;
                }
                };
            return option;
        },
        
        AddBarShadow()
        {
            var tubeGeometryOriginal=new THREE.TubeGeometry(new THREE.CatmullRomCurve3([new THREE.Vector3(0,0,0),new THREE.Vector3(0,0,BarLength)]),64,10,20);
            var meterialOriginal= new THREE.MeshBasicMaterial({transparent:true,opacity:0.1,color:0x000000});
            var meshedOriginal=new THREE.Mesh(tubeGeometryOriginal,meterialOriginal);
            this.scene.add(meshedOriginal);
        },

        AddArrow(forcedistance,forcesize,i)
        {
            var strdistance='force'+i+"distance";
            var strsize='force'+i+"size";
            var angleyzY='force'+i+'angleyz';//力在yz面的投影与Y轴正方向的夹角
            var anglexyY='force'+i+'anglexy';//力在xy面的投影与Y轴正方向的夹角

            var tan1=Math.tan(controls[anglexyY]);
            var tan2=Math.tan(controls[angleyzY]);
            var Fx=controls[strsize]*tan1/Math.sqrt(1+Math.pow(tan1,2)+Math.pow(tan2,2));
            var Fy=controls[strsize]/Math.sqrt(1+Math.pow(tan1,2)+Math.pow(tan2,2));
            var Fz=controls[strsize]*tan2/Math.sqrt(1+Math.pow(tan1,2)+Math.pow(tan2,2));

            var dir=new THREE.Vector3(Fx,Fy,Fz);
            dir.normalize();
            var origin= new THREE.Vector3(0,0,forcedistance);
            var arrowLength=(this.numOfforce+this.numOfmoment)*Math.abs(forcesize)*80/300;
            var hex=0xff0000;
            var headLength =(this.numOfforce+this.numOfmoment)*Math.abs(forcesize) *20/300;
            var headWidth = (this.numOfforce+this.numOfmoment)*Math.abs(forcesize)*4/300;
            arrowlist[i] = new THREE.ArrowHelper(dir, origin, arrowLength, hex,headLength,headWidth);
            this.scene.add(arrowlist[i]);
        },

        AddMomentArrow(momentdistance,momentsize,i)
        {
            var strsize='moment'+i+"size";
            var angleyzY='moment'+i+'angleyz';//力在yz面的投影与Y轴正方向的夹角
            var anglexyY='moment'+i+'anglexy';//力在xy面的投影与Y轴正方向的夹角

            var tan1=Math.tan(controls[anglexyY]);
            var tan2=Math.tan(controls[angleyzY]);
            var Mx=controls[strsize]*tan1/Math.sqrt(1+Math.pow(tan1,2)+Math.pow(tan2,2));
            var My=controls[strsize]/Math.sqrt(1+Math.pow(tan1,2)+Math.pow(tan2,2));
            var Mz=controls[strsize]*tan2/Math.sqrt(1+Math.pow(tan1,2)+Math.pow(tan2,2));

            var dir=new THREE.Vector3(Mx,My,Mz);
            dir.normalize();
            var origin= new THREE.Vector3(0,0,momentdistance);
            var arrowLength=(this.numOfforce+this.numOfmoment)*Math.abs(momentsize)*80/30;
            var hex=0xFF9900;
            var headLength =(this.numOfforce+this.numOfmoment)*Math.abs(momentsize) *20/30;
            var headWidth = (this.numOfforce+this.numOfmoment)*Math.abs(momentsize)*4/30;
            arrowmomentlist[i] = new THREE.ArrowHelper(dir, origin, arrowLength, hex,headLength,headWidth);
            this.scene.add(arrowmomentlist[i]);
        },

        AddUniformArrow(startpoint,endpoint,uniformsize,i)
        {
            arrowunilist[i]={};
            var strsize='uniform'+i+"size";
            var angleyzY='uniform'+i+'angleyz';
            var anglexyY='uniform'+i+'anglexy';

            var tan1=Math.tan(controls[anglexyY]);
            var tan2=Math.tan(controls[angleyzY]);
            var qx=controls[strsize]*tan1/Math.sqrt(1+Math.pow(tan1,2)+Math.pow(tan2,2));
            var qy=controls[strsize]/Math.sqrt(1+Math.pow(tan1,2)+Math.pow(tan2,2));
            var qz=controls[strsize]*tan2/Math.sqrt(1+Math.pow(tan1,2)+Math.pow(tan2,2));
            var dir=new THREE.Vector3(qx,qy,qz);
            dir.normalize();
            
            var arrowLength=(this.numOfforce+this.numOfmoment+this.numOfuniform)*Math.abs(uniformsize)*80/5000;
            var hex=0x432d00;
            var headLength =arrowLength/4;
            var headWidth =arrowLength/20;
            for(var j=0;j<=endpoint-startpoint;j+=arrowstep)
            {
                var origin= new THREE.Vector3(0,0,startpoint+j);
                arrowunilist[i][j] = new THREE.ArrowHelper(dir,origin,arrowLength, hex,headLength,headWidth);
                if(j%4==0)this.scene.add(arrowunilist[i][j]);
            }
            Endpoint[i]=endpoint;
            Startpoint[i]=startpoint;
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

        changegraph()
        {
            if(this.show1)
            {
               this.show1=false; 
               this.show2=true;
            }
            else
            {
                this.show1=true;
                this.show2=false;
            }
        },

        show3Dgraph()
        {
            countbutton++;
            if(countbutton==3)
            {
                countbutton=0;
            }
            switch (countbutton) {
                case 0:
                    this.buttontype='查看3D剪力图';
                    break;
                case 1:
                    this.buttontype='查看3D弯矩图';
                    break;
                default:
                    this.buttontype='收起3D图';
                    break;
            }
           this.draw3Dgraph();            
        },

        draw3Dgraph()
        {
            var bufFs=[];
            var bufMe=[];
            for(var i=0;i<BarLength;i++)
            {
                var origin=new THREE.Vector3(0,0,i);
                var count=0;

                var Fslist=[];
                var Melist=[];
                for(var j=-Math.PI;j<Math.PI;j+=2*Math.PI/arrowsegment)
                {
                    
                    var dir1=new THREE.Vector3(Math.cos(j),Math.sin(j),0);
                    if(arrowlengthFs3D[i][count]<0)
                    {
                        dir1=new THREE.Vector3(-Math.cos(j),-Math.sin(j),0);
                    }

                    var dir2=new THREE.Vector3(Math.cos(j),Math.sin(j),0);
                    if(arrowlengthMe3D[i][count]<0)
                    {
                        dir2=new THREE.Vector3(-Math.cos(j),-Math.sin(j),0);
                    }

                    var Fslength=Math.abs(arrowlengthFs3D[i][count])/((this.numOfforce!=0)+(this.numOfmoment!=0)+(this.numOfuniform!=0)+3);
                    
                    var Fsheadlength=Fslength/4;
                    var Fsheadwidth=Fslength/20;
                    var Fscolor='#fff0f5';

                    var Melength=Math.abs(arrowlengthMe3D[i][count]);
                    var Meheadlength=Melength/4;
                    var Meheadwidth=Melength/20;
                    var Mecolor='#fffafa';
                    if(arrowFs3D[0]!=undefined)
                    {
                        if(i%20==0)
                        {
                            this.scene.remove(arrowFs3D[i][count]);
                            this.scene.remove(arrowMe3D[i][count]);
                        }
                        
                    }
                   
                    
                    Fslist.push(new THREE.ArrowHelper(dir1,origin,Fslength,Fscolor,Fsheadlength,Fsheadwidth));
                    Melist.push(new THREE.ArrowHelper(dir2,origin,Melength,Mecolor,Meheadlength,Meheadwidth));
                    count++;
                }
                bufFs.push(Fslist);
                bufMe.push(Melist);
            }
            arrowFs3D=bufFs;
            arrowMe3D=bufMe;
            if(countbutton)
            {
                for(var i=0;i<BarLength;i+=20)
                {
                    for(var j=0;j<arrowsegment;j++)
                    {
                        if(countbutton==1)
                        {
                            this.scene.add(arrowFs3D[i][j]);
                        }
                        else
                        {
                            this.scene.add(arrowMe3D[i][j]);
                        }
                    }
                }
                
            }
        },

        
        animate() 
        {   
            var sumflagforce=0;
            var sumflagmoment=0;
            var sumflaguniform=0;
            for(var i=1;i<=this.numOfforce;i++)
            {
                var strdistance='force'+i+"distance";
                var strsize='force'+i+"size";
                var angleyzY='force'+i+'angleyz';//力在yz面的投影与Y轴正方向的夹角
                var anglexyY='force'+i+'anglexy';//力在xy面的投影与Y轴正方向的夹角
                if(controls[strsize]!=lastSizelist[i] || controls[strdistance]!=lastPositionlist[i]
                || controls[angleyzY]!=lastangleyzYlist[i]|| controls[anglexyY]!=lastanglexyYlist[i]
                || controls['coefficients']!=lastcoefficients)
                {
                    guiflag=1;
                    lastSizelist[i]=controls[strsize];
                    lastPositionlist[i]=controls[strdistance];
                    lastangleyzYlist[i]=controls[angleyzY];
                    lastanglexyYlist[i]=controls[anglexyY];
                    lastcoefficients=controls['coefficients'];
                    break;
                }
                else sumflagforce+=1;
            }
            for(var i=1;i<=this.numOfmoment;i++)
            {
                var strdistance='moment'+i+"distance";
                var strsize='moment'+i+"size";
                var angleyzY='moment'+i+'angleyz';//力在yz面的投影与Y轴正方向的夹角
                var anglexyY='moment'+i+'anglexy';//力在xy面的投影与Y轴正方向的夹角
                if( controls[strsize]!=lastSizeMomlist[i] || controls[strdistance]!=lastPositionMomlist[i] 
                || controls[angleyzY]!=lastangleyzYMomlist[i]|| controls[anglexyY]!=lastanglexyYMomlist[i]
                || controls['Momcoefficients']!=lastMomcoefficients)
                {
                    guiflag=1;
                    lastSizeMomlist[i]=controls[strsize];
                    lastPositionMomlist[i]=controls[strdistance];
                    lastangleyzYMomlist[i]=controls[angleyzY];
                    lastanglexyYMomlist[i]=controls[anglexyY];
                    lastMomcoefficients=controls['Momcoefficients'];
                    break;
                }
                else sumflagmoment+=1;
            }
            for(var i=1;i<=this.numOfuniform;i++)
            {
                
                var startposition='startPosition'+i;
                var endposition='endPosition'+i;
                var strsize='uniform'+i+"size";
                var angleyzY='uniform'+i+'angleyz';
                var anglexyY='uniform'+i+'anglexy';
                var startpoint=Math.min(controls[startposition],controls[endposition]);
                var endpoint=Math.max(controls[startposition],controls[endposition]);
                if(Math.abs(controls[strsize]-lastSizeUnilist[i])>1/this.numOfuniform || Math.abs(controls[angleyzY]-lastangleyzYUnilist[i])>0.2 
                || Math.abs(controls[anglexyY]-lastanglexyYUnilist[i])>0.2 || Math.abs(controls['Unicoefficients']-lastUnicoefficients)>1
                || Math.abs(controls[startposition]-laststartposition[i])>5 || Math.abs(controls[endposition]-lastendposition[i])>5 )
                {
                    guiflag=1;
                    lastSizeUnilist[i]=controls[strsize];
                    lastangleyzYUnilist[i]=controls[angleyzY];
                    lastanglexyYUnilist[i]=controls[anglexyY];
                    laststartposition[i]=controls[startposition];
                    lastendposition[i]=controls[endposition];
                    lastUnicoefficients=controls['Unicoefficients'];
                    break;
                }
                else sumflaguniform+=1;

            }
            if(sumflagforce==this.numOfforce && sumflagmoment==this.numOfmoment && sumflaguniform==this.numOfuniform && guiflag==1)
            {
                guiflag=0;
                this.scene.remove(Barmeshed);
                this.AddBar();
                for(var i=1;i<=this.numOfforce;i++)
                {
                    var strdistance='force'+i+"distance";
                    var strsize='force'+i+"size";
                    var angleyzY='force'+i+'angleyz';//力在yz面的投影与Y轴正方向的夹角
                    var anglexyY='force'+i+'anglexy';//力在xy面的投影与Y轴正方向的夹角
                    this.scene.remove(arrowlist[i]);
                    this.AddArrow(controls[strdistance],controls[strsize],i);
                }
                for(var i=1;i<=this.numOfmoment;i++)
                {
                    var strdistance='moment'+i+"distance";
                    var strsize='moment'+i+"size";
                    var angleyzY='moment'+i+'angleyz';//力在yz面的投影与Y轴正方向的夹角
                    var anglexyY='moment'+i+'anglexy';//力在xy面的投影与Y轴正方向的夹角
                    this.scene.remove(arrowmomentlist[i]);
                    this.AddMomentArrow(controls[strdistance],controls[strsize],i);
                }
                for(var i=1;i<=this.numOfuniform;i++)
                {
                
                    var startposition='startPosition'+i;
                    var endposition='endPosition'+i;
                    var strsize='uniform'+i+"size";
                    var angleyzY='uniform'+i+'angleyz';
                    var anglexyY='uniform'+i+'anglexy';
                    var startpoint=Math.min(controls[startposition],controls[endposition]);
                    var endpoint=Math.max(controls[startposition],controls[endposition]);
                    if(arrowunilist[i]!=undefined)
                    {
                        for(var j=0;j<=Endpoint[i]-Startpoint[i];j+=arrowstep)
                        {
                            this.scene.remove(arrowunilist[i][j]);
                        }
                    }
                    this.AddUniformArrow(startpoint,endpoint,controls[strsize],i);
                }
                this.draw3Dgraph();
            }
            this.RotateSkybox();
            this.RenderSceneInLoop();
            requestAnimationFrame(this.animate);
        },

        RotateSkybox()
        {
            this.skyboxmeshed.rotation.y+=0.001;
        },

        RenderSceneInLoop()
        {
            this.renderer.render( this.scene, this.camera );
        },
        Topage(path)
        {
            this.$router.push(path);
        },
    },
        mounted()
        {
            this.myChart=this.$echarts.init(document.getElementById('myecharts'));
            this.myChart1=this.$echarts.init(document.getElementById('myecharts1'));
            this.myChart2 = this.$echarts.init(document.getElementById('myecharts2'));
            this.myChart3 = this.$echarts.init(document.getElementById('myecharts3'));
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