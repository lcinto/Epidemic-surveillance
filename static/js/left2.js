function getNightingaleRose(countryName,countryConfirm,countryDead){  //南丁格尔玫瑰图
    var myChart = echarts.init(document.getElementById('left2'),'white');
    var legenddata = [
        {name:countryName[0],Confirmed:countryConfirm[0],Dead:countryDead[0]},
        {name:countryName[1],Confirmed:countryConfirm[1],Dead:countryDead[1]},
        {name:countryName[2],Confirmed:countryConfirm[2],Dead:countryDead[2]},
        {name:countryName[3],Confirmed:countryConfirm[3],Dead:countryDead[3]},
        {name:countryName[4],Confirmed:countryConfirm[4],Dead:countryDead[4]},
        {name:countryName[5],Confirmed:countryConfirm[5],Dead:countryDead[5]},
        {name:countryName[6],Confirmed:countryConfirm[6],Dead:countryDead[6]},
        {name:countryName[7],Confirmed:countryConfirm[7],Dead:countryDead[7]},
        {name:countryName[8],Confirmed:countryConfirm[8],Dead:countryDead[8]},
        {name:countryName[9],Confirmed:countryConfirm[9],Dead:countryDead[9]},
        {name:countryName[10],Confirmed:countryConfirm[10],Dead:countryDead[10]},
        {name:countryName[11],Confirmed:countryConfirm[11],Dead:countryDead[11]},
        {name:countryName[12],Confirmed:countryConfirm[12],Dead:countryDead[12]},
        {name:countryName[13],Confirmed:countryConfirm[13],Dead:countryDead[13]},
        {name:countryName[14],Confirmed:countryConfirm[14],Dead:countryDead[14]},
        {name:countryName[15],Confirmed:countryConfirm[15],Dead:countryDead[15]},
        {name:countryName[16],Confirmed:countryConfirm[16],Dead:countryDead[16]},
        {name:countryName[17],Confirmed:countryConfirm[17],Dead:countryDead[17]},
        {name:countryName[18],Confirmed:countryConfirm[18],Dead:countryDead[18]},
        {name:countryName[19],Confirmed:countryConfirm[19],Dead:countryDead[19]},
    ],

        option = {
         dataset: {
            source: [

                ['Country','Confirmed','SQRT','Dead'],
                [countryName[0],countryConfirm[0],Math.sqrt(countryConfirm[0]),countryDead[0]],
                [countryName[1],countryConfirm[1],Math.sqrt(countryConfirm[1]),countryDead[1]],
                [countryName[2],countryConfirm[2],Math.sqrt(countryConfirm[2]),countryDead[2]],
                [countryName[3],countryConfirm[3],Math.sqrt(countryConfirm[3]),countryDead[3]],
                [countryName[4],countryConfirm[4],Math.sqrt(countryConfirm[4]),countryDead[4]],
                [countryName[5],countryConfirm[5],Math.sqrt(countryConfirm[5]),countryDead[5]],
                [countryName[6],countryConfirm[6],Math.sqrt(countryConfirm[6]),countryDead[6]],
                [countryName[7],countryConfirm[7],Math.sqrt(countryConfirm[7]),countryDead[7]],
                [countryName[8],countryConfirm[8],Math.sqrt(countryConfirm[8]),countryDead[8]],
                [countryName[9],countryConfirm[9],Math.sqrt(countryConfirm[9]),countryDead[9]],
                [countryName[10],countryConfirm[10],Math.sqrt(countryConfirm[10]),countryDead[10]],
                [countryName[11],countryConfirm[11],Math.sqrt(countryConfirm[11]),countryDead[11]],
                [countryName[12],countryConfirm[12],Math.sqrt(countryConfirm[12]),countryDead[12]],
                [countryName[13],countryConfirm[13],Math.sqrt(countryConfirm[13]),countryDead[13]],
                [countryName[14],countryConfirm[14],Math.sqrt(countryConfirm[14]),countryDead[14]],
                [countryName[15],countryConfirm[15],Math.sqrt(countryConfirm[15]),countryDead[15]],
                [countryName[16],countryConfirm[16],Math.sqrt(countryConfirm[16]),countryDead[16]],
                [countryName[17],countryConfirm[17],Math.sqrt(countryConfirm[17]),countryDead[17]],
                [countryName[18],countryConfirm[18],Math.sqrt(countryConfirm[18]),countryDead[18]],
                [countryName[19],countryConfirm[19],Math.sqrt(countryConfirm[19]),countryDead[19]],
            ]
         },
        toolbox: {
            show: true,
            feature: {
                mark: {show: true},
                dataView: {show: true, readOnly: false},
                magicType: {
                    show: true,
                    type: ['pie', 'funnel']
                },
                //restore: {show: true},
                saveAsImage: {show: true}
            }
        },
            title: {
                text: '海外疫情前二十玫瑰图',
                //subtext: '\n\t\t\t\t\t\t使用秀秀的数据\n\n——by Krystal1',
                x: '50%',
                y: '50',
                textStyle:{
                    fontSize:27,
                    fontWeight:'bold',
                    fontFamily:'Microsoft YaHei',
                    color:'#000'
                },
                subtextStyle:
                {
                    fontStyle:'italic',
                    fontSize:14
                }
            },
            legend: {
                x: 'right',//水平位置，【left\center\right\数字】
                y: '150',//垂直位置，【top\center\bottom\数字】
                align:'left',//字在图例的左边或右边【left/right】
                orient:'vertical',//图例方向【horizontal/vertical】
                icon: "circle",   //图例形状【circle\rect\roundRect\triangle\diamond\pin\arrow\none】
                textStyle://图例文字
                {
                    fontFamily:'微软雅黑',
                    color:'#000',

                },
                data: countryName,
                formatter: function(params)  {
                    //console.log('图例参数',params)
                    for (var i=0;i<legenddata.length;i++){
                          if (legenddata[i].name== params){
                              return params+"\t确诊:"+legenddata[i].Confirmed+"\t死亡:"+legenddata[i].Dead;
                             }
                    }
                }
            },

            calculable: true,
            series: [
                {
                    name: '半径模式',
                    type: 'pie',
                    clockWise: false ,
                    radius: [20, 400],
                    center: ['35%', '65%'],
                    roseType: 'area',          //指定南丁格尔玫瑰图
                    encode: {
                    itemName: 'Country',
                    value: 'SQRT'
                            },
                    itemStyle: {
                        normal: {
                        color: function(params) {
                               var colorList = [
                    "#a71a4f","#bc1540","#c71b1b","#d93824","#ce4018","#d15122","#e7741b","#e58b3d","#e59524","#dc9e31","#da9c2d",
                    "#d2b130","#bbd337","#8cc13f","#67b52d","#53b440","#48af54","#479c7f","#48a698","#57868c"
                                ];
                                return colorList[params.dataIndex]
                            },
                            label: {
                                position: 'inside',
                                textStyle:
                                {
                                    fontWeight:'bold',
                                    fontFamily:'Microsoft YaHei',
                                    color:'#FAFAFA',
                                    fontSize:10
                                },
                                formatter:'{b} \n{@Confirmed}例 \n死亡{@Dead}',//注意这里大小写敏感
                                formatter : function(params)
                                {  //console.log('参数列表',params)
                                    if(params.data[1]>3000000)
                                    {return params.data[0]+'\n'+params.data[1]+"例"+'\n'+"死亡"+params.data[3]+"例";}
                                    else{return "";}
                                },
                            },
                        },
            },
                },
                {
                    name:'透明圆圈',
                    type:'pie',
                    radius: [10,27],
                    center: ['35%', '65%'],
                    itemStyle: {
                            color: 'rgba(250, 250, 250, 0.3)',
                    },
                    data:[
                        {value:10,name:''}
                    ]
                },
                {
                    name:'透明圆圈',
                    type:'pie',
                    radius: [10,35],
                    center: ['35%', '65%'],
                    itemStyle: {
                            color: 'rgba(250, 250, 250, 0.3)',
                    },
                    data:[
                        {value:10,name:''}
                    ]
                }
                    ]
        };
       myChart.setOption(option);
}