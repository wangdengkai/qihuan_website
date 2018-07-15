$(function(){
	//设置全局变量来控制是增加还是减少点赞数量
	like_flag = 'true'
	// 获取所有评论
	get_common_list()
	//获取所有文章列表
	// get_post_detail();	
	

			
})




function get_post_detail(){
	/*
	这个函数是用来为每一文章的标题绑定一个点击事件,事件结果是返回文章的详情,并且将文章的评论列表和评论表单都自动渲染完成
	采用的方式是异步方式
	 */
	//获取所有标题的a标签
			 var $TitleA=$(".index_get_post a")
			 console.log($TitleA)
			//获取文章主题对象
			var $PostBody =$("#post_body")
			//获取显示文章标题对象
			var $PostTitle = $("#post_title")
			//为所有a标签绑定点击事件
			// console.log($TitleA[0])
			
			//为每一个文章绑定点击事件
			$TitleA.click(function(){
				//发送异步请求,
				// alert($(this))
				//回调函数
				var $Durl = $(this).attr("href")
				console.log($(this))
				var $Title =$(this).data("posttitle")
				console.log("post_title")
				console.log($Title)
				var $PostId = $(this).data("postid")
				console.log($PostId)
				
				// 点击后发送异步请求,获取文章详情
				$.get(
					$Durl,
					null,
					function(data){
						//收到服务器返回的文章内容后,渲染文章内容到页面中
						
						
						$PostTitle.html($Title)
						var $show_data=data				
						var $SeaRes = $("#hide_sea")
						$SeaRes.hide()						
						$PostBody.html($show_data)

						
						
						// //渲染好文章后,绑定点赞标记
						
						$('#cpostlike').click(get_like_number);
						//渲染好文章后,立马请求评论,要求渲染评论
						get_common_list($PostId)
						//请求文章下面的评论表单
						get_common_form()

					}
					)
				console.log(false)
				return false
			})
}


function get_common_list(){
		/*
		这是为了获取每一个文章下面的评论列表.
		在这里发送异步get请求,获取列表
		接受一个文章的id
		 */
			//获取标签,将评论渲染在其中
			var $GetCommon =$("#comment")
			var post_id = $("#postcom").data('postid')
			console.log("-------")
			console.log(post_id)
			//请求url
			var $Url ="/common/getcommon/"+post_id+"/"
			
			//发送异步请求
			$.get(
				$Url,
				null,
				function(data){
					/*
					收到评论数据后,进行渲染到页面中
					 */
					console.log(data)					
					$GetCommon.html(data);
					get_common_form();
					
			})

		

}




//获取评论的表单
function get_common_form()
{
	/*
	这个函数用来获取每个文章下面的评论表单,将其渲染到页面中.
	 */
			//获取评论按钮的对象
			var  $reqCommon = $(".req_common")
			
			//获取表单要渲染到的标签div中
			// var $SubCommon = $(".req_common").next()
			//评论按钮绑定请求事件
			$reqCommon.click
			(function()
			{
				/*
				评论按钮点击后,自动发送get请求到服务器,获取评论表单

				 */
				var $comid = $(this).data("commonid")				

				//请求的url
				var $Myurl = "localhost:8000/common/common/"+$(this).data("postid")+"/"+$comid+"/";
				var $SubCommon =$(this).next()
				//发送get请求
				$.get
				(
					$Myurl,
					null,
					function(data)
					{
						/*
						请求表单获取的回调函数
						 */
						//将请求到的表单渲染到页面中,			
						
						$SubCommon.html(data)

						//把刚刚请求到的表单设置成异步submit
						sendForm($SubCommon);
								
					}
				)
				return false;

			}
			)

}

function sendForm($SubCommon){
	/*
	将表单提交设置为异步方式,并且提交后,自动清空表单,更新评论列表

	 */
	//设置请求对象------------
	var $subObj = {
			"success":function(data){
				//提交成功后的回调函数
				//返回的json字符串可以当做json对象直接使用
				// console.log(data.postId)
				// 调用请求评论列表刷新评论
				// var oRes = eval('('+data+')')
				// console.log(oRes.postId)
				get_common_list(data.postId)
			},
			"error":function(data){
				//提交失败后的回调函数
				console.log("数据提交失败")
				alert("数据提交失败请重新提交")
			},

			
			"clearForm":true,
			"restForm":true,
			"timeout":6000



	}
	//绑定异步请求------------
	$SubCommon.children(".id_form").ajaxForm($subObj);
}

function get_like_number(){
		/*
		这个函数用来增加和减少文章的点赞数量
		 */
		
		
	
		//获取标签标记
		var $cNumer = $('#cpostlike')
		
		//判断是增加还是减少点赞数量
		console.log("---------------")
		console.log(like_flag)

		//获取标签本身的url,并构造出请求url
			var $gUrl = $cNumer.prop('href');
		
		if(like_flag == 'false'){
			var reL = new RegExp('/1/');
			console.log(reL)
			
			$gUrl=$gUrl.replace(reL,'/2/');
			console.log($gUrl)
			like_flag = 'true';
		}else{
			//更改flag,实现点击后再次点击可以取消点赞的效果
			like_flag = 'false';

		}	
		
		

		//发送get请求
		$.get(
			$gUrl,
			null,
			function(data){
				$('#likenumber').text(data.like_number)
			}
		)
	
	//进制冒泡和默认行为
	return false;	

}
	
