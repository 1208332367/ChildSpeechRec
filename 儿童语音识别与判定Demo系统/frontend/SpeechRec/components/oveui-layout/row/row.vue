<template>
	<view :class="['row', Justify, Align, Cols]" :style="{
		marginLeft:-gutter + 'rpx',marginRight:-gutter + 'rpx'
	}"><slot></slot>
	</view>
</template>

<script>
	export default {
		name: "row",
		props:{
		//给col添加左右间距，左右边距各占一半
			gutter: {
				type:[String, Number],
				default:0
			},
		//水平排列方式，可选值为`start`、`end`、`center`、`around`、`between`
			justify: {
				type:String,
				default:'start'
			},
		//垂直对齐方式，可选值为top、center、bottom、空值
			align: {
				type:String,
				default:'top' //如果默认留空，整组col会变成其中最大值的等高效果
			},
			bgClass: {
				type:String,
				default:''
			},
			bgStyle:{
				type:String,
				default:''
			},
			radius: {
				type:[Number, String],
				default:''
			},
			cols: {
				type:[Number, String],
				default:''
			}
		},
		provide() {
			return {
				gutter:this.gutter,
				bgclass:this.bgClass,
				bgstyle:this.bgStyle,
				radius:this.radius,
				cols:this.cols
			}
		},
		computed: {
			Justify() {
				let justify = 'start';
				switch (this.justify) {
					case 'start':
						justify = 'justify-start'
						break;
					case 'center':
						justify = 'justify-center'
						break;
					case 'end':
						justify = 'justify-end'
						break;
					case 'between':
						justify = 'justify-between'
						break;
					case 'around':
						justify = 'justify-around'
						break;
				}
				return justify
			},
			Align() {
				let align = 'center';
				switch (this.align) {
					case 'top':
						align = 'align-start'
						break;
					case 'center':
						align = 'align-center'
						break;
					case 'bottom':
						align = 'align-end'
						break;
					case '':
						align = ''
						break;
				}
				return align
			},
			Cols(){
				if(this.cols>1 || this.cols<=5) return 'cols-'+this.cols;
				else return ''
			}
		}
	}
</script>

<style lang="scss">
/*
	.row{
		/* #ifndef MP 
		flex-direction:row;
		display:flex;
		/* #endif 
		box-sizing:border-box;
		flex-wrap:wrap;
		/* #ifdef MP 
		&::before,&::after{display:table;content:"";}
		&::after{clear:both;}
		/* #endif 
	}
*/

.row{
		
		flex-direction:row;
		display:flex;
		
		box-sizing:border-box;
		flex-wrap:wrap;

	}
	
	.justify-start{justify-content:flex-start;}
	.justify-center{justify-content:center;}
	.justify-end{justify-content:flex-end;}
	.justify-between{justify-content:space-between;}
	.justify-around{justify-content:space-around;}
	.align-start{align-items:flex-start}
	.align-center{align-items:center}
	.align-end{align-items:flex-end}
	
</style>
