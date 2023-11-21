//////--------/////////////////////////////////------------------///////////////////
//////////////////---------------Quick View----------------------//////////////////
/////--------/////////////////////////////////------------------///////////////////
// var view = document.getElementsByClassName('view')
// for (i = 0; i < view.length; i++) {
//     view[i].addEventListener('click', function () {
//         var productId = this.dataset.slug
//         console.log("productId:", productId)
//         console.log('User:', user)
//         if (user === 'anonymumous.user') {
//             console.log('not logged in')
//         } else {
//             getItem(productId)
//         }
//     })
// }


// function getItem(productId) {
//     var csrf = getCookie('csrftoken');
//     var url = '/get-item/'
//     fetch(url, {
//         method: 'POST',
//         credentials: 'include',
//         headers: {
//             'Content-Type': 'application/json',
//             'X-CSRFToken': csrf,
//         },
//         body: JSON.stringify({
//             'productId': productId
//         })
//     })

//         .then((response) => {
//             console.log('first then ran successfully');
//             return response.json();
//         })

//         .then((data) => {
//             console.log('data:', data);
//             //var data = JSON.parse(data); 
//             var prodtitle = document.getElementById('prod-title');
//             var prodprice = document.getElementById('prod-price');
//             var proddiscount = document.getElementById('prod-discount');
//             var prodid = document.getElementById('quick-prod-id');
//             var prodimage = document.getElementById('prod-img');
//             var proddesc = document.getElementById('prod-desc');

//             //var prodidele = document.getElementById('prod-id');

//             console.log(data['slug'])
//             prodtitle.innerHTML = data['title'];
//             prodimage.src = data['image'];
//             prodprice.innerHTML = data['price'];
//             //proddiscount.innerHTML=data['discount'];
//             proddesc.innerHTML = data['desc'];
//             prodid.innerHTML = "";
//             prodid.innerHTML = `<input type=hidden name="prodid" value="${data['slug']}">`;
//             //for (let i = 0; i < data.size.fields['size'].length; i++){}
//             var color = JSON.parse(data.color);
//             var size = JSON.parse(data.size);
//             console.log(size[0].fields.size);
//             console.log(size[0].pk);
//             console.log(color[0].pk);
//             console.log(color[0].fields.color);
//             var sizeele = document.getElementById('sizei');
//             var colorele = document.getElementById('colori');
//             sizeele.innerHTML = "";
//             colorele.innerHTML = "";
//             //console.log(data.size[0].fields.color);
//             //console.log(data['color']);
//             for (let i = 0; i < size.length; i++) {

//                 // POPULATE SELECT ELEMENT WITH JSON.
//                 sizeele.innerHTML = sizeele.innerHTML +
//                     `
//                 <div data-value="${size[i].fields.size}" class="swatch-element ${size[i].fields.size.toLowerCase()} available">
//                 <input class="swatchInput" id="swatch-1-${size[i].fields.size.toLowerCase()}" type="radio" name="size" value="${size[i].pk}" required>
//                     <label class="swatchLbl medium rectangle" for="swatch-1-${size[i].fields.size.toLowerCase()}" title="${size[i].fields.size}">${size[i].fields.size}</label>
//                 </div>
//                 `;

//             }
//             for (let i = 0; i < color.length; i++) {
//                 // POPULATE SELECT ELEMENT WITH JSON.
//                 colorele.innerHTML = colorele.innerHTML +
//                     `
//                 <div data-value="${color[i].fields.name}" class="swatch-element color ${color[i].fields.name} available">
//                     <input class="swatchInput" id="swatch-0-${color[i].fields.name.toLowerCase()}" type="radio" name="color" value="${color[i].pk}" required>
//                     <label class="swatchLbl color medium rectangle" for="swatch-0-${color[i].fields.name.toLowerCase()}" style="background-color:${color[i].fields.color};" title="${color[i].fields.name}"></label>
//                 </div>
//                 `

//             }


//         })
// }
//////--------/////////////////////////////////------------------///////////////////
//////////////////---------------Add to Cart----------------------//////////////////
/////--------/////////////////////////////////------------------///////////////////
// document.getElementById('addToCart').addEventListener('click', function (e) {
//     e.preventDefault();
//     const addForm = document.getElementById('addtocartform');
//     const formData = new FormData(addForm);
//     console.log(formData);
//     var data = [];
//     for (const [key, value] of formData) {
//         console.log(key, value)
//         data.push(key, value);
//     }

//     console.log(data);
//     if (user === 'anonymumous.user') {
//         console.log('not logged in')
//     } else {
//         updateUserCart(formData)
//     }
// })

// function updateUserCart(formData) {
//     var csrf = getCookie('csrftoken');
//     var url = '/update_item/'
//     fetch(url, {
//         method: 'POST',
//         credentials: 'include',
//         headers: {
//             'Content-Type': 'application/json',
//             'X-CSRFToken': csrf,
//         },
//         body: JSON.stringify({
//             'form': formData
//         })
//     })
//         .then((response) => {
//             console.log('first then ran successfully');
//             return response.json();
//         })
//         .then((data) => {
//             console.log('data:', data);
//             location.reload();
//         })
//         .catch(() => {
//             console.log('undefined')
//         })
// }

// function addToCart() {
//     var firstname = document.forms["myForm"]["firstname"].value;
//     var lastname = document.forms["myForm"]["lastname"].value;
// }

//////--------/////////////////////////////////------------------///////////////////
//////////////////---------------Add to Cart----------------------//////////////////
/////--------/////////////////////////////////------------------///////////////////
var updateBtns = document.getElementsByClassName('update-cart')
for (i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function () {
        var productId = this.dataset.slug
        var action = this.getAttribute('data-action')
        console.log("productId:", productId, "Action:", action)
        console.log('User:', user)
        if (user === 'anonymumous.user') {
            console.log('not logged in')
        } else {
            updateUserOrder(productId, action)
        }
    })
}


function updateUserOrder(productId, action) {
    var csrf = getCookie('csrftoken');
    var url = '/update_item/'
    fetch(url, {
        method: 'POST',
        credentials: 'include',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf,
        },
        body: JSON.stringify({
            'productId': productId, 'action': action
        })
    })

        .then((response) => {
            console.log('first then ran successfully');
            return response.json();
        })

        .then((data) => {
            console.log('data:', data);
            location.reload();
        })
}