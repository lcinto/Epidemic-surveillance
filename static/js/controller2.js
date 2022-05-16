 //获取时间
 function showTime(){
	var time = new Date();
	var year = time.getFullYear();
	var month = (time.getMonth()+1+'').padStart(2,'0');
	var day = (time.getDate()+'').padStart(2,'0');
	var hour = (time.getHours()+'').padStart(2,'0');
	var minute = (time.getMinutes()+'').padStart(2,'0');
	var second = (time.getSeconds()+'').padStart(2,'0');
	var content = `${year}年${month}月${day}日${hour}:${minute}:${second}`;
	$('#title .time').text(content);
}

showTime();
setInterval(showTime,1000);

//世界疫情地图
function get_world_data(){
    $.ajax({
        url:"/left1",
        success: function(data) {
			option.series[0].data=data.data
            myChart.setOption(option);
		},
		error: function(xhr, type, errorThrown) {
		}
    })
}
get_world_data();                      //执行数据获取

//确诊玫瑰图
function get_rose_data(){
    $.ajax({
		url:'/left2',
		success:function(data){
			var data = data.data;
            var countries = data;
            var count=0;          //计数，取前20个国家
             //存储前20个国家的数据（name，confirm，dead）
            var countryName = [];
            var countryConfirm = [];
            var countryDead = [];
            for(var country of countries){
                //console.log(country);
                if(count==20){
                    break;
                }else{
                countryName[count]=country.name
                countryConfirm[count]=country.confirm
                countryDead[count]=country.dead
                count++
            }
            }
             getNightingaleRose(countryName,countryConfirm,countryDead);
		}
	});
}
get_rose_data()


function refreshPage(){
    window.location.reload()
}




