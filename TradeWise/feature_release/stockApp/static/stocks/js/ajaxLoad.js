console.log('working')
const postBox = document.getElementById('post-box')
const loadBtn = document.getElementById('load-btn')
const loadBox = document.getElementById('loading-box')

let visible = 3

const handleGetData = ()=>{
	$.ajax({
		type: 'GET',
		url: `/article/${visible}`,
		success: function(response){
			max_size = response.max
			const data = response.data
			data.map(post=>{
				console.log(post.id)
				postBox.innerHTML += `
				<div class="col-md-6 col-sm-6 mb-4">
				<div class="card card-shadow">
				<img src='media/${post.articleImage}' class="card-img" alt="...">
				<div class="card-body">
				<h5 class="card-title">${post.title}</h5>
				<p>${post.content}</p>
				<p class="p-color">${post.created}</p>
				<p>${post.author}</p>
				<a href="#" class=""><strong>Read More &#8594;</strong></a>
				</div>
				</div>
				</div>`
			});

			if(max_size){
				loadBox.innerHTML = "<h4> No More Data</h4>"
			}
		},
		error: function(error){
			console.log(error)
		}
	});
}
handleGetData()
loadBtn.addEventListener('click', ()=>{
	visible += 3
	handleGetData()
});




