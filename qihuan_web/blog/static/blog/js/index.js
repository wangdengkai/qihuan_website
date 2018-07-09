$(function(){
			//获取所有标题的a标签
			 var $TitleA=$(".index_get_post a")
			 console.log($TitleA)
			//获取文章主题对象
			var $PostBody =$("#post_body")
			//获取显示文章标题对象
			var $PostTitle = $("#post_title")
			//为所有a标签绑定点击事件
			// console.log($TitleA[0])
			

			$TitleA.click(function(){
				//发送异步请求,
				// alert($(this))
				//回调函数
				var $Durl = $(this).attr("href")
				var $Title =$(this).text()
				var $PostId = $(this).attr("data-id")
				// console.log($Title)
				// console.log($(this).attr('href'))
				$.get(
					$Durl,
					null,
					function(data){
						// console.log(data)
						$PostTitle.text($Title)
						var $show_data=data.split(";")[1]
						// console.log(show_data)
						// alert($show_data)
						var $SeaRes = $("#hide_sea")
						$SeaRes.hide()
						var $show_data=
						$PostBody.html($show_data)

						// get_common_list($PostId)

						var $PostId=$first.attr("data-id")
						get_common_list($PostId)
						get_common_form()

					}
					)
				console.log(false)
				return false
			})
		})




function get_common_list(post_id){
			//获取标签
			var $GetCommon =$("#get_common")
			var $Url ="/common/getcommon/"+post_id
			// $GetCommon.html("<h5>hhh</h5>")
			//发送异步请求
			$.get(
				$Url,
				null,
				function(data){
					// console.log("--------")
					console.log(data)
					// var show_data=data.split()[1]
					$GetCommon.html(data)
				}

				)

		}




//获取评论的表单
		function get_common_form(){
			//获取请求评论的对象
			var  $reqCommon = $("#req_common")
			console.log("get common form")
			//获取表单框
			var $SubCommon =$("#sub_common")
			//绑定请求事件
			$reqCommon.click(function(){
				var $Myurl = "common/common/"+$(this).attr("data-id")+"/1/"
				console.log($Myurl)
				console.log("评论------")
				$.get(
					$Myurl,
					null,
					function(data){
						
						// console.log("收到了回应")
						// alert(data)
						$SubCommon.html(data)
						$("form").submit(function(){
						var formData={
								"name":$("#id_name"),
								"email":$("#id_email"),
								"text":$("#id_text")
							}
						$.post(
								$(this).prop("action"),
								formData,
								function(data){
									alert(data)
									if(data=="true"){
										// 更新评论列表
										alert("----------")
										// get_common_list($(this).prop("data-post-id"))
									}else{
										alert("评论提交失败,请核对规则后查询")
									}
									
								})
								
							return false
						})
						// sendForm()
						// $("form").ajaxForm(function(data){
						// 	alert(data)
						// })
						// 获取提交按钮
						// var $SubButton = $("#subbutton")
						// //提交按钮绑定点击事件
						// $SubButton.submit(function(){
						// 	return false
						// 	alert("hahaha")
						// 	$(this).ajaxSubmit({
						// 			success:function(data){
						// 				alert("hahaha")
						// 			}
						// 	})

						// 	return false
						// })
					}
					)
				console.log("发送了请求")

				return false

			})
		}

// 这是发送评论表单请求的函数
		// function sendForm(){
		// 	var $oSub ={
		// 		"restForm":true,
		// 		"clearForm":true,
		// 		"timeout":6000,
		// 		"success":function(data){
		// 			alert(data)
		// 			if(data=="true"){
		// 				get_common_list($(this).prop("data-post-id"))


		// 			}else{
		// 				alert("请核对规则后查询")
		// 			}

		// 		}
		// 	};
		// 	$("#id_form").ajaxForm($oSub);
		// }
		// 	$("#id_form").ajaxForm(function(data){
		// 		alert("post succcess."+data)
		// 	})
		// 	return false
			// var $sendUrl =$(this).parent().prop("action")
			// console.log($sendUrl)
			// // var form =new FormData()
			// // form.append("name",$("#id_name"))
			// // form.append("email",$("#id_email"))
			// // form.append("text",$("#id_text"))
			// var formData={"name":$("#id_name"),
			// 			"email":$("#id_email"),
			// 			"text":$("#id_text"),}
			// $.post(
			// 	$sendUrl,
			// 	formData
			// 	function(data){
			// 		alert(data)
			// 		if(data=="true"){
			// 			// 更新评论列表
			// 			// get_common_list($(this).prop("data-post-id"))
			// 		}else{
			// 			alert("评论提交失败,请核对规则后查询")
			// 		}
			// 		return false
			// 	}
			// 	)
			// return false
		// }
		// 
		// 
		// 
		// 
$(function(){
				var $PostTitle = $("#post_title")
				var $PostBody =$("#post_body")
				var $first=$("#index_left a:eq(0)")
			console.log($first.attr('href'))
			$.get(
					$first.attr('href'),
					null,					
					function(data){
						// console.log(data)
						$PostTitle.text($first.text())
						var $SeaRes = $("#hide_sea")
						$SeaRes.hide()
						// var $show_data=data.split(";")[1]
						// // console.log(show_data)
						$PostBody.html(data)
						
						// console.log(data)
						var $PostId=$first.attr("data-id")
						get_common_list($PostId)
						get_common_form()
					

					}
				)
			})