<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<title>簡宏宥的簡介</title>
	<style type="text/css">
		* { font-family:"標楷體"; margin-left:auto; margin-right:auto;}

h1 {color:blue; font-size:60px;}

h2 {color:#33ff33; font-size:40px;}

</style>

<script>
     function change1() {
           document.getElementById("pic").src = "istockphoto-470604022-612x612.jpg";
           document.getElementById("h2text").innerText = "靜宜資管";
     }

     function change2() {
           document.getElementById("pic").src = "premium_photo-1688645554172-d3aef5f837ce.jpg";
           document.getElementById("h2text").innerText = "Hong-Yu Chien";
     }
     </script>
<head>
	<?php echo date("Y-m-d") ?>
	<body>

	<table width="70%">
		<tr>
			<td>
	           <img src="istockphoto-470604022-612x612.jpg"width="100%"id="pic"
onmouseover="change1()" onmouseout="change2()"></img>
	        	
		    <td>
	 			<h1>簡宏宥</h1>
	            <h2 id="h2text">Hong-Yu Chien</h2>
	        </td>
		</tr>
	</table>
	<table width="70%" border="1">
		<tr>
			<td>
	            個人網頁：<a href="https://www1.pu.edu.tw/~tcyang">https://www1.pu.edu.tw/~tcyang</a><br>
	            FB：<a href="https://www.facebook.com/tcyang1971"
	            target="_blank">https://www.facebook.com/tcyang1971</a><br>
	            Tel: <a href="tel:04-26328001#18110">04-26328001#18110</a><br>
	            E-Mail: <a href="mailto:hankfgh1230@gmail.com">hankfgh1230@gmail.com</a><br>
	        </td>

	        <td>
	            大象席地而坐電影配樂<br>
	            <audio controls>
		        <source src="elephant.mp3" type="audio/mP3">
	            </audio><br>
	       </td>

	       <td>
	           不要去臺灣<br>
	           <iframe src="https://www.youtube.com/embed/pW88QFpHXa8" allowfullscreen></iframe>
	       </td>
		</tr>
	</table>
</body>
</html>