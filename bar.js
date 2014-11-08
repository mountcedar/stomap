d3.json('./data.json', function(pointdata){
	main(pointdata);
    });

function main(pointdata) {
    console.log(pointdata);
	d3.select(".overlay").remove();
	var  style_array_from_above_here = [{"featureType":"water","elementType":"all","stylers":[{"hue":"#e9ebed"},{"saturation":-78},{"lightness":67},{"visibility":"simplified"}]},{"featureType":"landscape","elementType":"all","stylers":[{"hue":"#ffffff"},{"saturation":-100},{"lightness":100},{"visibility":"simplified"}]},{"featureType":"road","elementType":"geometry","stylers":[{"hue":"#bbc0c4"},{"saturation":-93},{"lightness":31},{"visibility":"simplified"}]},{"featureType":"poi","elementType":"all","stylers":[{"hue":"#ffffff"},{"saturation":-100},{"lightness":100},{"visibility":"off"}]},{"featureType":"road.local","elementType":"geometry","stylers":[{"hue":"#e9ebed"},{"saturation":-90},{"lightness":-8},{"visibility":"simplified"}]},{"featureType":"transit","elementType":"all","stylers":[{"hue":"#e9ebed"},{"saturation":10},{"lightness":69},{"visibility":"on"}]},{"featureType":"administrative.locality","elementType":"all","stylers":[{"hue":"#2c2e33"},{"saturation":7},{"lightness":19},{"visibility":"on"}]},{"featureType":"road","elementType":"labels","stylers":[{"hue":"#bbc0c4"},{"saturation":-93},{"lightness":31},{"visibility":"on"}]},{"featureType":"road.arterial","elementType":"labels","stylers":[{"hue":"#bbc0c4"},{"saturation":-93},{"lightness":-2},{"visibility":"simplified"}]}];
	
	//Google Map 初期化
	var map = new google.maps.Map(document.getElementById('map'), {
			zoom: 12,
			mapTypeId: google.maps.MapTypeId.ROADMAP,
			center: new google.maps.LatLng(35.596943,139.685257),
			styles: style_array_from_above_here,
			disableDefaultUI: false
		});

		
	var overlay = new google.maps.OverlayView(); //OverLayオブジェクトの作成
	overlay.onAdd = function () {
		//オーバーレイ設定

		var layer = d3.select(this.getPanes().floatShadow).append("div").attr("class", "SvgOverlay");
		var svg = layer.append("svg");
		var gunmalayer = svg.append("g").attr("class", "AdminDivisions");
		var markerOverlay = this;
		var overlayProjection = markerOverlay.getProjection();
		
		//Google Projection作成
		var googleMapProjection = function (coordinates) {
			var googleCoordinates = new google.maps.LatLng(coordinates[1], coordinates[0]);
			var pixelCoordinates = overlayProjection.fromLatLngToDivPixel(googleCoordinates);
			return [pixelCoordinates.x, pixelCoordinates.y];
		}
		    
		overlay.draw = function () {
		    console.log("Zoom: " + map.getZoom());
		    //ピクセルポジション情報
		    pointdata.forEach(function(d) {
				var point = googleMapProjection([d['lng'] ,d['lat']]);//位置情報→ピクセル
				d['xpoint'] = point[0];
				d['ypoint'] = point[1];
			});

			var max = 10000;

			//棒グラフの高さスケールを設定
			var barH = 300;
			var barW = 8;
			var yScale = d3.scale.linear().domain([0, max]).range([0, barH]);
			
			//前のグラフをすべて削除する
			d3.selectAll(".bar").remove()
			
			//データの数だけ棒グラフを書く
			pointdata.forEach(function(point){
				//console.log(point);

				//棒グラフ作成用のデータセットを作る
				var data = [
					    {key:"value", value:point["value"], name:point["name"], address:point["address"]}
				];
					
				//棒グラフグループ
				var barGroup = gunmalayer //Gmap上のsvgレイヤ
					.append("g")
					.attr("class", "bar")
					.attr("transform", "translate(" + point.xpoint+ "," + point.ypoint + ")")　//円グラフを表示する座標を指定
				
				//棒グラフ描画
				var bar = barGroup.selectAll("rect")
					.data(data)
					.enter()
					.append("rect")
					.attr({
						x:function(d,i){ return barW - (barW/2); },
						y:function(d,i){ return -1 * yScale(d.value) },
						width:barW,
						height:function(d){ return yScale(d.value) },
						stroke:"black",
						fill:function(d, i){ 
						    return "red";
						},
						opacity:"0.75"
					});
				
				//マウスオーバーした際に詳細を表示		
				bar.append("title")
					.text(function(d){ return "会社名：" + d.name + "\n住所：" + d.address + "\n株価：" + d.value + "円"})
			});
		};
		
		d3.select("#age").on("change", function(){
			overlay.draw();
		});
	};

	//作成したSVGを地図にオーバーレイする
	overlay.setMap(map);
};

