// a javascript file to display the product details and change the various variants of the product
const el = document.querySelector("#view");
el.addEventListener('click', () => {
    const productId = el.dataset.slug;
    fetchProductDetails(productId);
},
    false);
// a function to fetch product details from the server
function fetchProductDetails(productId) {
    // get the product id from the url

    const csrf = getCookie('csrftoken');
    const urlParams = '/get-item/';
    // const productId = urlParams.get('id');

    // fetch the product details from the server
    fetch(urlParams, {
        method: 'POST',
        credentials: 'include',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf,
        },
        body: JSON.stringify({
            'productId': productId,
        })
    })
        .then(response => response.json())
        .then(product => {
            // display the product details
            console.log(product);
            displayProductDetails(product);
        });
}

// a function to display the product details
function displayProductDetails(product) {
    const data = product;
    const prodtitle = document.querySelector('#prod-title');
    const prodprice = document.querySelector('#prod-price');
    const proddiscount = document.querySelector('#prod-discount');
    const prodid = document.querySelector('#quick-prod-id');
    const prodimage = document.querySelector('#prod-img');
    const proddesc = document.querySelector('#prod-desc');
    const sizeele = document.querySelector('#prod-img');
    const colorele = document.querySelector('#prod-desc');

    // populate product details
    prodtitle.innerHTML = data.product_title;
    prodimage.src = data.product_image;
    prodprice.innerHTML = data.product_price;
    proddesc.innerHTML = data.product_desc;
    prodid.innerHTML = `<input type=hidden name="prodid" value="${data.product_slug}">`;
    let color = JSON.parse(data.product_variant);
    console.log(color); 
    // populating color fields
    for (let i = 0; i < data.product_variant.length; i++) {
        // POPULATE SELECT ELEMENT WITH JSON.
        colorele.innerHTML = colorele.innerHTML +
            `
        <div data-value="${color[i].fields.name}" class="swatch-element color ${color[i].fields.name} available">
            <input class="swatchInput" id="swatch-0-${color[i].fields.name.toLowerCase()}" type="radio" name="color" value="${color[i].pk}" required>
            <label class="swatchLbl color medium rectangle" for="swatch-0-${color[i].fields.name.toLowerCase()}" style="background-color:${color[i].fields.color};" title="${color[i].fields.name}"></label>
        </div>
        `};
}