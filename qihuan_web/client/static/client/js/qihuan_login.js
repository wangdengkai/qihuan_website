var vm = new Vue({
			el:'#login',
			data:{
				username:'',
				password:'',
				usermsg:'',
				passmsg:'',
				checkpassword:'',
				checkpass:'',
				uFlag:false	,
				pFlag:false ,
				cFlag:false 		

			},
			methods:{

				auditingUser:function(){
					if(this.username ==''){
						this.usermsg="用户名不能为空"
						this.uFlag = false
						return;
					}
					var re = /^[^.\\\/\n%@!*&#]{3,20}$/;
					var result = re.test(this.username)
					if(result != true){
						this.usermsg="用户名必须是3到20为的中文英文数字字符"
						this.uFlag = false
						return;
					}
					this.uFlag = true;


				},
				auditingPassword:function(){
					if(this.password == ''){
						this.passmsg='用户密码不能为空'
						this.pFlag = false
						return;

					}
					var  re=/^[a-zA-Z0-9_]{8,}$/;
					var result = re.test(this.password)
					if(result !=true){
						this.passmsg ="用户密码必须是大于8位的英文字母和数字"
						this.pFlag = false
						return;
					}
					this.pFlag = true;

				},
				auditingCheckpass:function(){
					if(this.checkpassword==''){
						this.checkpass="确认密码不能为空"
						this.cFlag = false
						return;
					}
					var  re=/^[a-zA-Z0-9_]{8,}$/;
					var result = re.test(this.checkpassword)
					if(result !=true){
						this.checkpass ="用户密码必须是大于8位的英文字母和数字"
						this.cFlag = false
						return;
					}
					if (this.checkpassword != this.password){
						this.checkpass="确认密码必须与密码相同"
						this.cFlag=false;
						return ;
					}
					this.cFlag = true;
				},
				close_usemsg:function(){
					this.usermsg ='';
					this.uFlag = true;
				},
				close_passmsg:function(){
					this.passmsg = '';
					this.pFlag = true;
				},
				close_check:function(){
					this.checkpass='';
					this.cFlag = true;
				}
				
			}

		})
