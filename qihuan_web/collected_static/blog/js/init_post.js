/*
由于要用send_post中的代码,所以我们需要动态引入send_post文件
 */
//创建新的标签script
new_element = document.createElement("script");
//添加type属性
new_element.setAttribute("type","text/javascript");
//引入send_post.js
new_element.setAttribute("src","{% static 'blog/js/send_post.js' %}");
document.body.appendChild(new_element);






function post_init_detail(){
	/*
	这个函数是当每一页文章显示出来的时候,先把第一个文章显示在旁边
	 */
	console.log("你已经进入了post_init_detail")
	 //获取显示文章标题标签对象
	var $PostTitle = $("#post_title")
	//获取显示文章正文标签对象
	var $PostBody =$("#post_body")
	//获取页面左侧文章列表第一个文章链接
	var $first=$("#index_left a:eq(0)")
		
	//发送get请求,获取第一个左侧第一个文章的内容		
	$.get(
			$first.attr('href'),
			null,					
			function(data){
				/*
				回调函数,将文章内容渲染到页面中
				 */
				//渲染文章标题
				$PostTitle.text($first.text())
				//将文中显示搜索文章的div隐藏起来
				var $SeaRes = $("#hide_sea")
				$SeaRes.hide()
				//显示文章正文
				$PostBody.html(data)
				
				// 获取文章的评论和表单.
				var $PostId=$first.attr("data-id")
				get_common_list($PostId)
				get_common_form();
			

			}
		)

}


