var ec_left1 = echarts.init(document.getElementById('l1'), "dark");
var ec_left1_Option = {
	tooltip: {
		trigger: 'axis',
		//指示器
		axisPointer: {
			type: 'line',
			lineStyle: {
				color: '#7171C6'
			}
		},
	},
	legend: {
		data: ['新增确诊', '新增疑似'],
		left: "right"
	},
	//标题样式
	title: {
		text: "本土新增趋势",
		textStyle: {
			color: 'white',
		},
		left: 'left'
	},
	//图形位置
	grid: {
		left: '4%',
		right: '6%',
		bottom: '4%',
		top: 50,
		containLabel: true
	},
	xAxis: [{
		type: 'category',
		//x轴坐标点开始与结束点位置都不在最边缘
		// boundaryGap : true,

		data: []
	}],
	yAxis: [{
		type: 'value',
		//y轴字体设置

		//y轴线设置显示
		axisLine: {
			show: true
		},
		axisLabel: {
			show: true,
			color: 'white',
			fontSize: 12,
			formatter: function(value) {
				if (value >= 1000) {
					value = value / 1000 + 'k';
				}
				return value;
			}
		},
		//与x轴平行的线样式
		splitLine: {
			show: true,
			lineStyle: {
				// color: '#FFF',
				width: 1,
				// type: 'solid',
			}
		}
	}],
	series: [{
		name: "新增确诊",
		type: 'line',
		smooth: true,
		data: []
	}/*, {
		name: "新增疑似",
		type: 'line',
		smooth: true,
		data: []
	}*/]
};

ec_left1.setOption(ec_left1_Option)
